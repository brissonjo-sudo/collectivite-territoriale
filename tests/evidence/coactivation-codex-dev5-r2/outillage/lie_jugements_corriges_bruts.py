"""Lecture brute fermée : aucune trace projetée n'est exportée comme native."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import lie_jugements_corriges as binder

READ_PRAGMA = '// @exec: {"max_output_tokens": 55000}\n'
PROJECTION = 'raw_output_three_parts_v1'
BASE_NATIVE_PROOF = binder.native_proof


def read_command(path: Path) -> str:
    return "Get-Content -LiteralPath '" + path.resolve().as_posix().replace("'", "''") + "' -Raw"


def read_script(arguments: dict) -> str:
    return (READ_PRAGMA + 'const result = await tools.exec_command(' +
        json.dumps(arguments, ensure_ascii=False) +
        '); text({exit_code:result.exit_code}); text(result.output);')


def raw_arguments(script: str) -> dict:
    """Une unique commande littérale, suivie des deux projections exactes."""
    match = re.fullmatch(re.escape(READ_PRAGMA) +
        r'const result = await tools\.exec_command\((.*)\); text\(\{exit_code:result\.exit_code\}\); text\(result\.output\);\s*',
        script, re.S)
    if not match:
        raise binder.BindingError('Lecture brute hors grammaire fermée')
    arguments = binder._json(match[1])
    if (not isinstance(arguments, dict) or set(arguments) != {'cmd', 'max_output_tokens'}
            or type(arguments['max_output_tokens']) is not int or arguments['max_output_tokens'] != 55000):
        raise binder.BindingError('Arguments de lecture brute invalides')
    return arguments


def native_proof(native, parent, agent, parent_id, packet_path, judgment_path, exported_at):
    """Contrôle la sortie brute, puis réutilise le lieur sur une projection en mémoire."""
    projected = copy.deepcopy(native)
    raw_by_call = {}
    packet = binder._json(packet_path.read_text(encoding='utf-8'))
    for index, event in enumerate(native):
        payload = event.get('payload', {})
        if payload.get('type') not in ('custom_tool_call', 'function_call'):
            continue
        script = payload.get('input', payload.get('arguments'))
        if not isinstance(script, str) or 'tools.apply_patch(' in script:
            continue
        arguments = raw_arguments(script)
        if arguments['cmd'] != binder._read_command(packet_path):
            raise binder.BindingError('Lecture brute hors paquet')
        identifier = payload.get('call_id')
        outputs = [(i, item) for i, item in enumerate(native)
            if item.get('payload', {}).get('call_id') == identifier
            and item['payload'].get('type') in ('custom_tool_call_output', 'function_call_output')]
        if len(outputs) != 1:
            raise binder.BindingError('Sortie brute absente ou ambiguë')
        output_index, output_event = outputs[0]
        parts = binder._output(output_event['payload'])
        if len(parts) != 3 or not parts[0].startswith('Script completed\n'):
            raise binder.BindingError('Trois parties natives brutes requises')
        exit_value = binder._json(parts[1])
        if (not isinstance(exit_value, dict) or set(exit_value) != {'exit_code'}
                or type(exit_value['exit_code']) is not int or exit_value['exit_code'] != 0):
            raise binder.BindingError('Lecture brute échouée')
        if binder._canonical(binder._json(parts[2])) != binder._canonical(packet):
            raise binder.BindingError('Lecture brute tronquée ou divergente')
        projected[index]['payload']['input' if 'input' in payload else 'arguments'] = (
            'text(await tools.exec_command(' + json.dumps(arguments, ensure_ascii=False) + '));')
        projected[output_index]['payload']['output'] = [
            {'type': 'text', 'text': parts[0]}, {'type': 'text', 'text': json.dumps(
                {'exit_code': 0, 'output': parts[2]}, ensure_ascii=False)}]
        raw_by_call[identifier] = (payload, output_event['payload'])
    proof, kept = BASE_NATIVE_PROOF(projected, parent, agent, parent_id,
        packet_path, judgment_path, exported_at)
    if len(raw_by_call) != 1:
        raise binder.BindingError('Lecture brute unique requise')
    # Les appels et sorties retenus reprennent les valeurs réelles, jamais la projection.
    for event in kept:
        payload = event.get('payload', {})
        originals = raw_by_call.get(payload.get('call_id'))
        if originals:
            original = originals[1 if payload.get('type') in
                ('custom_tool_call_output', 'function_call_output') else 0]
            for field in ('input', 'arguments', 'output'):
                if field in original:
                    payload[field] = copy.deepcopy(original[field])
    proof.update(exact_read_path_format='absolute_posix', raw_projection=PROJECTION,
        raw_adapter_sha256=binder._sha(Path(__file__)), initial_message_verified=False)
    return proof, kept


def export_packet(candidate, response, destination):
    old_read = binder._read_command
    try:
        binder._read_command = read_command
        result = binder.export_packet(candidate, response, destination)
    finally:
        binder._read_command = old_read
    packet, prompt, manifest = (Path(result[key]) for key in ('packet', 'prompt', 'export'))
    packet.write_text(json.dumps(binder._json(packet.read_text(encoding='utf-8')),
        ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
    text = prompt.read_text(encoding='utf-8')
    replacement = '```javascript\n' + read_script({'cmd': read_command(packet), 'max_output_tokens': 55000}) + '\n```'
    text, count = re.subn(r'```javascript\n.*?\n```', lambda _: replacement, text, flags=re.S)
    if count != 1:
        raise binder.BindingError('Appel de lecture unique absent du prompt')
    prompt.write_text(text, encoding='utf-8', newline='\n')
    value = binder._json(manifest.read_text(encoding='utf-8'))
    value.update(packet_sha256=binder._sha(packet), prompt_sha256=binder._sha(prompt),
        raw_adapter_sha256=binder._sha(Path(__file__)), raw_projection=PROJECTION,
        external_read_output_tokens=55000, compact_packet=True)
    manifest.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return result


def bind_judgment(*args, **kwargs):
    old_read, old_native = binder._read_command, binder.native_proof
    try:
        binder._read_command, binder.native_proof = read_command, native_proof
        return binder.bind_judgment(*args, **kwargs)
    finally:
        binder._read_command, binder.native_proof = old_read, old_native
