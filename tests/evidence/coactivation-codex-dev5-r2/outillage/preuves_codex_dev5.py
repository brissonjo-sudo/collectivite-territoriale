"""Adaptateur distinct Codex natif : lecture runtime par fichier, pas outil Skill.

Ne modifie ni runtime ni barème. Les sources sont liées au résultat natif réel.
La seule différence de calcul technique est le modèle Claude remplacé par le
modèle attesté du contexte natif Codex. Aucun appel Claude Code n'est exécuté.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import lie_jugements_corriges as binder
import lie_jugements_corriges_bruts as raw
from preuves_campagne_r7 import native_inventory, agent_path

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / 'Collectivite-corrections-pr5'
RUN = ROOT / 'qualification-coactivation-dev5-codex-r1'
PARENT_ID = '01a1103e-0b49-70c1-8f4e-66a36b54916f'
SELF_AGENT = '/root/outillage_codex_dev5'
DIRECTORIES = tuple(Path('C:/Users/Krn/.codex/sessions/2026/10') / day for day in ('06', '07', '08'))
NATIVE_TOOLS = frozenset(('search', 'fetch', 'search_articles', 'get_article', 'search_case_law', 'get_decision', 'get_section', 'get_text'))

def modules():
    assessment = binder._module(CANDIDATE)
    import run_coactivation_v2 as transport
    import source_evidence as sources
    return assessment, transport, sources

def write(path, value):
    binder._write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def case_and_number(identifier):
    cases = binder._json((CANDIDATE / 'tests/cas-coactivation-v2.json').read_text(encoding='utf-8'))
    found = [(number, case) for number, case in enumerate(cases, 1) if case['id'] == identifier]
    if len(found) != 1:
        raise binder.BindingError('Cas absent ou ambigu')
    return found[0]

def discover(agent):
    inventory = native_inventory(DIRECTORIES)
    found = [(path, meta) for path, meta in inventory.values() if agent_path(meta) == agent]
    if len(found) != 1:
        raise binder.BindingError('Session native absente ou ambiguë : ' + agent)
    if PARENT_ID not in inventory:
        raise binder.BindingError('Parent natif absent')
    return found[0][0], inventory[PARENT_ID][0]

def identity(native, parent, agent, created_at):
    meta = native[0].get('payload', {})
    spawn = meta.get('source', {}).get('subagent', {}).get('thread_spawn', {})
    if (native[0].get('type') != 'session_meta' or spawn.get('agent_path') != agent
            or spawn.get('parent_thread_id') != PARENT_ID or meta.get('id') == PARENT_ID
            or sum(e.get('type') == 'session_meta' for e in native) != 1):
        raise binder.BindingError('Identité native répondant divergente')
    if parent[0].get('payload', {}).get('id') != PARENT_ID:
        raise binder.BindingError('Identité parent divergente')
    calls = [e for e in parent if e.get('payload', {}).get('type') == 'function_call'
             and e['payload'].get('name') == 'spawn_agent'
             and binder._json(e['payload']['arguments']).get('task_name') == agent.rsplit('/', 1)[-1]]
    if len(calls) != 1:
        raise binder.BindingError('Spawn répondant absent ou ambigu')
    call = calls[0]
    args = binder._json(call['payload']['arguments'])
    if args.get('fork_turns') != 'none' or 'model' in args or 'reasoning_effort' in args:
        raise binder.BindingError('Création sans historique et sans override requise')
    returns = [e for e in parent if e.get('payload', {}).get('type') == 'function_call_output'
               and e['payload'].get('call_id') == call['payload']['call_id']]
    if len(returns) != 1 or binder._json(returns[0]['payload']['output']).get('task_name') != agent:
        raise binder.BindingError('Retour spawn non lié')
    if not (binder._time(created_at) <= binder._time(call['timestamp']) <= binder._time(meta['timestamp']) <= binder._time(returns[0]['timestamp'])):
        raise binder.BindingError('Export antérieur au spawn non établi')
    starts = [e for e in native if e.get('payload', {}).get('type') == 'task_started']
    ends = [e for e in native if e.get('payload', {}).get('type') == 'task_complete']
    contexts = [e for e in native if e.get('type') == 'turn_context']
    if len(starts) != 1 or len(ends) != 1 or not contexts:
        raise binder.BindingError('Exécution fraîche unique et achevée requise')
    turn = starts[0]['payload'].get('turn_id')
    if not turn or ends[0]['payload'].get('turn_id') != turn or any(e['payload'].get('turn_id') != turn for e in contexts):
        raise binder.BindingError('Session réutilisée ou tour divergent')
    if native.index(starts[0]) >= native.index(ends[0]):
        raise binder.BindingError('Ordre début/fin divergent')
    models = {e['payload'].get('model') for e in contexts}
    if len(models) != 1 or not isinstance(next(iter(models)), str):
        raise binder.BindingError('Modèle natif absent ou ambigu')
    result = {'agent': agent, 'thread_id': meta['id'], 'parent_thread_id': PARENT_ID,
              'model': next(iter(models)), 'turn_id': turn, 'created_at': meta['timestamp'],
              'started_at': starts[0]['timestamp'], 'completed_at': ends[0]['timestamp'],
              'fork_turns': 'none', 'initial_message_verified': False,
              'initial_message_sha256': hashlib.sha256(binder._canonical(args.get('message')).encode()).hexdigest()}
    retained_spawn = {'timestamp': call['timestamp'], 'call_id': call['payload']['call_id'],
                      'arguments': {k: v for k, v in args.items() if k != 'message'},
                      'initial_message_sha256': result['initial_message_sha256'],
                      'result_timestamp': returns[0]['timestamp'], 'result': binder._json(returns[0]['payload']['output'])}
    return result, retained_spawn

def outputs(native, call):
    found = [e for e in native if e.get('payload', {}).get('type') in ('custom_tool_call_output', 'function_call_output')
             and e['payload'].get('call_id') == call['payload'].get('call_id')]
    if len(found) != 1 or native.index(found[0]) <= native.index(call):
        raise binder.BindingError('Résultat natif absent, ambigu ou antérieur')
    return found[0], binder._output(found[0]['payload'])

def single_result(parts):
    if len(parts) != 2 or not parts[0].startswith('Script completed\n'):
        raise binder.BindingError('Résultat exec simple et achevé requis')
    return binder._json(parts[1])

def read_call(script, parts):
    try:
        args = raw.raw_arguments(script)
        if len(parts) != 3 or not parts[0].startswith('Script completed\n'):
            raise binder.BindingError('Lecture brute incomplète')
        result = {'exit_code': binder._json(parts[1]).get('exit_code'), 'output': parts[2]}
    except binder.BindingError:
        args = binder._arguments(script, 'exec_command')
        result = single_result(parts)
    if set(args) != {'cmd', 'max_output_tokens'} or type(args['max_output_tokens']) is not int:
        raise binder.BindingError('Arguments lecture hors protocole')
    match = re.fullmatch(r"Get-Content -LiteralPath '([^']+)' -Raw", args['cmd'])
    if not match or result.get('exit_code') != 0:
        raise binder.BindingError('Lecture littérale échouée ou hors grammaire')
    path = Path(match[1]).resolve()
    if result.get('output', '').rstrip('\r\n') != path.read_text(encoding='utf-8').rstrip('\r\n'):
        raise binder.BindingError('Lecture tronquée ou différente du fichier')
    return path

def literal_patch(script, target, parts):
    patch = binder._arguments(script, 'apply_patch')
    if not isinstance(patch, str):
        raise binder.BindingError('Patch littéral requis')
    lines = patch.splitlines()
    if (len(lines) < 4 or lines[0] != '*** Begin Patch' or lines[-1] != '*** End Patch'
            or lines[1].replace('\\', '/').casefold() != ('*** Add File: ' + target.resolve().as_posix()).casefold()
            or any(not line.startswith('+') for line in lines[2:-1])):
        raise binder.BindingError('Patch hors destination unique')
    content = '\n'.join(line[1:] for line in lines[2:-1]) + '\n'
    if content != target.read_text(encoding='utf-8') or single_result(parts) != {}:
        raise binder.BindingError('Patch non réussi ou réponse transformée')
    return content

def codex_failures(events, case):
    """Différence de host explicite ; aucun champ modèle historique falsifié."""
    _, transport, _ = modules()
    failures = transport.technical_failures(events, case)
    init = next((e for e in events if e['type'] == 'init'), None)
    if init and init.get('host') == 'Codex' and init.get('model_native_verified') is True:
        failures = [f for f in failures if f != 'model_mismatch']
    else:
        failures.append('codex_model_unverified')
    return failures

def validate_codex(case, events, judgment, digest):
    assessment, _, _ = modules()
    old = assessment.technical_failures
    try:
        assessment.technical_failures = codex_failures
        return assessment.validate_judgment(case, events, judgment, digest)
    finally:
        assessment.technical_failures = old

def filter_native(events):
    """Conserve outil/retour littéraux utiles, sans raisonnement ni message opaque."""
    retained = []
    for event in events:
        payload = event.get('payload', {})
        if event.get('type') == 'session_meta':
            value = {k: payload[k] for k in ('id', 'timestamp', 'cli_version') if k in payload}
            value['source'] = {'subagent': {'thread_spawn': payload.get('source', {}).get('subagent', {}).get('thread_spawn', {})}}
        elif event.get('type') == 'turn_context':
            value = {k: payload[k] for k in ('turn_id', 'model') if k in payload}
        elif payload.get('type') in ('task_started', 'task_complete'):
            value = {k: v for k, v in payload.items() if k in ('type', 'turn_id', 'started_at', 'completed_at')}
        elif payload.get('type') in ('function_call', 'function_call_output', 'custom_tool_call', 'custom_tool_call_output'):
            value = {k: v for k, v in payload.items() if k in ('type', 'name', 'call_id', 'arguments', 'input', 'output')}
        elif payload.get('type') == 'message' and payload.get('role') == 'assistant':
            value = {k: v for k, v in payload.items() if k in ('type', 'role', 'phase', 'content')}
        else:
            continue
        retained.append({'timestamp': event['timestamp'], 'type': event['type'], 'payload': value})
    return retained

def export_judge(identifier):
    """Exporte les 124 atomes inchangés ; limite Codex ajoutée au prompt, pas au barème."""
    response = RUN / (identifier + '.jsonl')
    destination = RUN / 'juges' / identifier
    result = raw.export_packet(CANDIDATE, response, destination)
    prompt = Path(result['prompt'])
    text = prompt.read_text(encoding='utf-8')
    note = ('Portée distincte : host Codex natif. Les événements skill_activation avec '
            'activation_kind=file_read attestent uniquement la lecture intégrale de fichiers '
            'runtime du candidat. Ils ne prouvent ni un appel Skill Claude ni le chargement '
            'natif d’un plugin Codex. Le modèle réel du contexte Codex est conservé ; aucun '
            'score ou smoke Claude n’est transféré. Un invariant exigeant littéralement '
            'une activation « via Skill » ne peut pas être true sur cette lecture : '
            'la preuve manquante vaut null. Les autres invariants de méthode et de rôle '
            'restent évaluables sur la réponse. Les événements documentaire/source_evidence proviennent '
            'des résultats réellement capturés, jamais d’une réponse reconstruite.\n\n')
    prompt.write_text(note + text, encoding='utf-8', newline='\n')
    manifest_path = Path(result['export'])
    manifest = binder._json(manifest_path.read_text(encoding='utf-8'))
    manifest.update(prompt_sha256=binder._sha(prompt), native_adapter_sha256=binder._sha(Path(__file__)),
                    host='Codex', activation_kind='file_read', historical_scores_reused=False)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return result

def bind_judge(identifier):
    number, case = case_and_number(identifier)
    directory = RUN / 'juges' / identifier
    response = RUN / (identifier + '.jsonl')
    packet = directory / (identifier + '.packet.json')
    judgment = directory / (identifier + '.jugement.json')
    manifest = binder._json((directory / (identifier + '.export.json')).read_text(encoding='utf-8'))
    for path, key in ((packet, 'packet_sha256'), (response, 'response_sha256'), (directory / (identifier + '.prompt.md'), 'prompt_sha256')):
        if binder._sha(path) != manifest[key]:
            raise binder.BindingError('Pièce modifiée depuis export : ' + path.name)
    if manifest['native_adapter_sha256'] != binder._sha(Path(__file__)):
        raise binder.BindingError('Adaptateur modifié après export')
    assessment, _, _ = modules()
    expected = assessment.build_judge_packet(case, response, CANDIDATE / 'docs/protocole-coactivation-v2.md')
    if binder._canonical(expected) != binder._canonical(binder._json(packet.read_text(encoding='utf-8'))):
        raise binder.BindingError('Paquet différent de la reconstruction')
    agent = f'/root/juge_codex_dev5_{number:02d}'
    native_path, parent_path = discover(agent)
    old = binder._read_command
    try:
        binder._read_command = raw.read_command
        proof, retained = raw.native_proof(binder._events(native_path), binder._events(parent_path), agent, PARENT_ID, packet, judgment, manifest['exported_at'])
    finally:
        binder._read_command = old
    document = binder._json(judgment.read_text(encoding='utf-8'))
    if set(document) != {'case_id', 'trace_sha256', 'verdict', 'invariants'}:
        raise binder.BindingError('Champs racine jugement invalides')
    validated = validate_codex(case, binder._events(response), document, binder._sha(response))
    proof.update(case_id=identifier, assessment=validated, host='Codex', activation_kind='file_read',
                 native_adapter_sha256=binder._sha(Path(__file__)), response_sha256=binder._sha(response),
                 packet_sha256=binder._sha(packet), judgment_sha256=binder._sha(judgment),
                 native_session_file=native_path.name, parent_session_file=parent_path.name)
    destination = directory / 'liaison'
    trace = destination / 'trace-juge.jsonl'
    binder._write(trace, ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in retained))
    proof['trace_sha256'] = binder._sha(trace)
    write(destination / 'execution-juge.json', proof)
    with (RUN / (identifier + '.jugement.json')).open('xb') as stream:
        stream.write(judgment.read_bytes())
    return validated

def source_call(script):
    match = re.fullmatch(r'\s*text\(await tools\.([A-Za-z0-9_]+)\((.*)\)\);\s*', script, re.S)
    if not match:
        match = re.fullmatch(r'\s*const result\s*=\s*await tools\.([A-Za-z0-9_]+)\((.*)\);\s*text\(result\);\s*', script, re.S)
    if not match:
        raise binder.BindingError('Appel source hors grammaire littérale')
    literal = match[2]
    # JSON plus clefs de propriétés JS non citées, sans expression ni évaluation.
    parts = re.split(r'("(?:\\.|[^"\\])*")', literal)
    for index in range(0, len(parts), 2):
        parts[index] = re.sub(r'(?<=[{,])(\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*):',
                             lambda item: item[1] + json.dumps(item[2]) + item[3] + ':', parts[index])
    args = binder._json(''.join(parts))
    if not isinstance(args, dict):
        raise binder.BindingError('Arguments source non objet')
    return match[1], args

def safe_source_native(native, source_ids):
    """Corps source exclus du journal natif publié ; extraits assainis dans v2."""
    retained = filter_native(native)
    for event in retained:
        payload = event['payload']
        if payload.get('call_id') in source_ids:
            if payload.get('type') in ('custom_tool_call_output', 'function_call_output'):
                payload.pop('output', None)
                payload['source_output_retained_as'] = 'sanitized_source_evidence_v2'
            else:
                payload.pop('input', None)
                payload.pop('arguments', None)
                payload['source_call_retained_as'] = 'native_tool_name_and_call_id_in_v2'
    return retained

def bind_respondent(identifier):
    """Vérifie les outils natifs, puis crée une nouvelle trace v2 bornée."""
    number, case = case_and_number(identifier)
    directory = RUN / identifier
    input_path = directory / 'input.json'
    packet = binder._json(input_path.read_text(encoding='utf-8'))
    export_path = directory / 'responder.export.json'
    export_pre_spawn = export_path.is_file()
    if export_pre_spawn:
        exported = binder._json(export_path.read_text(encoding='utf-8'))
    elif number in (1, 2):
        exported = {'created_at': datetime.fromtimestamp(input_path.stat().st_mtime, timezone.utc).isoformat(),
                    'input_sha256': binder._sha(input_path), 'manifest_sha256': binder._sha(RUN / 'manifest.json'),
                    'timestamp_basis': 'input_current_filesystem_mtime; not an export attestation'}
    else:
        raise binder.BindingError('Export répondant avant spawn absent')
    manifest = binder._json((RUN / 'manifest.json').read_text(encoding='utf-8'))
    if binder._sha(input_path) != exported['input_sha256'] or binder._sha(RUN / 'manifest.json') != exported['manifest_sha256']:
        raise binder.BindingError('Entrée ou manifest modifié après export répondant')
    if packet['case_id'] != identifier or packet['question'] != case['prompt'] or packet['case_number'] != number:
        raise binder.BindingError('Question différente de la suite figée')
    if binder._sha(CANDIDATE / 'tests/cas-coactivation-v2.json') != manifest['suite_sha256']:
        raise binder.BindingError('Suite du candidat modifiée')
    if binder._sha(CANDIDATE / 'docs/protocole-coactivation-v2.md') != manifest['protocol_sha256']:
        raise binder.BindingError('Barème du candidat modifié')
    for relative, digest in manifest['files'].items():
        if binder._sha(CANDIDATE / relative) != digest:
            raise binder.BindingError('Candidat changé pendant mesure : ' + relative)
    allowed = {Path(path).resolve(): digest for path, digest in packet['allowed_runtime_files'].items()}
    if len(allowed) != 166 or any(binder._sha(path) != digest for path, digest in allowed.items()):
        raise binder.BindingError('Inventaire runtime différent du gel')
    response_path = Path(packet['response_path']).resolve()
    if response_path != (directory / 'response.md').resolve():
        raise binder.BindingError('Destination réponse extérieure au cas')
    agent = f'/root/repondant_codex_dev5_{number:02d}'
    native_path, parent_path = discover(agent)
    native, parent = binder._events(native_path), binder._events(parent_path)
    proof, spawn = identity(native, parent, agent, exported['created_at'])
    assessment, transport, sources = modules()
    catalog = sorted('collectivite-territoriale:' + name for name in binder._json((CANDIDATE / 'upstream.json').read_text(encoding='utf-8'))['skills'])
    events = [{'type': 'init', 'host': 'Codex', 'session_id': proof['thread_id'], 'model': proof['model'],
               'model_native_verified': True, 'activation_kind': 'file_read',
               'actual_plugin_activation_verified': False, 'standalone_recherche_juridique_loaded': False,
               'foreign_available_skills': [], 'available_skills': catalog, 'mcp_servers': [],
               'catalogue_scope': 'candidate_runtime_only; no claim about globally available tools'}]
    question_read = None
    writes = 0
    loads = []
    read_files = []
    source_ids = set()
    catalogue_read_count = 0
    start = next(i for i, e in enumerate(native) if e.get('payload', {}).get('type') == 'task_started')
    end = next(i for i, e in enumerate(native) if e.get('payload', {}).get('type') == 'task_complete')
    for index, event in enumerate(native):
        payload = event.get('payload', {})
        if payload.get('type') == 'message' and payload.get('role') == 'assistant':
            text = ''.join(piece.get('text', '') for piece in payload.get('content', [])
                           if piece.get('type') in ('output_text', 'text'))
            if text.strip():
                clean = sources.scrub_visible_text(text)
                events.append({'type': 'assistant_text', 'text': clean['text'], 'text_redacted': clean['redacted'],
                               'text_truncated': clean['truncated'], 'phase': payload.get('phase'),
                               'timestamp': event['timestamp'], 'native_message_index': index})
            continue
        if payload.get('type') not in ('custom_tool_call', 'function_call'):
            continue
        if not start < index < end or payload.get('name') != 'exec':
            raise binder.BindingError('Outil répondant hors exécution fraîche ou protocole exec')
        output_event, parts = outputs(native, event)
        script = payload.get('input', payload.get('arguments'))
        if not isinstance(script, str):
            raise binder.BindingError('Script natif absent')
        call_id = payload['call_id']
        if 'tools.apply_patch(' in script:
            if question_read is None or writes:
                raise binder.BindingError('Écriture unique après entrée requise')
            literal_patch(script, response_path, parts)
            writes += 1
            events.append({'type': 'response_write', 'call_id': call_id, 'path': response_path.as_posix(),
                           'response_sha256': binder._sha(response_path), 'succeeded': True,
                           'timestamp': output_event['timestamp']})
            continue
        if writes:
            raise binder.BindingError('Outil après écriture finale interdit')
        if 'tools.exec_command(' in script:
            path = read_call(script, parts)
            if path == input_path.resolve():
                if question_read is not None or read_files or loads:
                    raise binder.BindingError('Entrée intégrale requise une fois en premier')
                question_read = call_id
                events.append({'type': 'question_read', 'call_id': call_id, 'path': path.as_posix(),
                               'question_sha256': binder._sha(path), 'succeeded': True, 'timestamp': output_event['timestamp']})
                continue
            if question_read is None or path not in allowed or binder._sha(path) != allowed[path]:
                raise binder.BindingError('Lecture hors runtime autorisé ou modifié')
            relative = path.relative_to(CANDIDATE / 'skills').as_posix()
            read_files.append(relative)
            if path.name == 'SKILL.md':
                name = relative.split('/')[0]
                loads.append(name)
                events.append({'type': 'skill_activation', 'skill': 'collectivite-territoriale:' + name,
                               'activation_kind': 'file_read', 'host': 'Codex', 'actual_plugin_activation_verified': False,
                               'path': path.as_posix(), 'runtime_sha256': allowed[path], 'succeeded': True,
                               'call_id': call_id, 'timestamp': output_event['timestamp']})
            else:
                events.append({'type': 'plugin_file_read', 'path': relative, 'runtime_sha256': allowed[path],
                               'activation_kind': 'file_read', 'succeeded': True, 'call_id': call_id,
                               'timestamp': output_event['timestamp']})
            continue
        if 'ALL_TOOLS' in script and 'tools.' not in script:
            if question_read is None or catalogue_read_count:
                raise binder.BindingError('Métadonnées outils une seule fois après entrée')
            catalogue_read_count += 1
            events.append({'type': 'tool_metadata_read', 'call_id': call_id, 'timestamp': output_event['timestamp'],
                           'scope': 'runtime_tool_metadata; no source retrieval'})
            continue
        if question_read is None:
            raise binder.BindingError('Source avant question complète')
        tool, args = source_call(script)
        result = single_result(parts)
        source_ids.add(call_id)
        if tool.startswith('mcp__droit_francais__') and tool[len('mcp__droit_francais__'):] in NATIVE_TOOLS:
            method = tool[len('mcp__droit_francais__'):]
            normalized_tool = 'mcp__droit-francais__' + method
            evidence = sources.extract_source_evidence(result, tool=normalized_tool, call_id=call_id, retrieved_at=output_event['timestamp'])
            succeeded = evidence.get('reason') not in ('tool_error', 'empty_transport') and not (isinstance(result, dict) and (result.get('isError') is True or result.get('is_error') is True or 'error' in result))
            events.append({'type': 'plugin_mcp_call', 'tool': normalized_tool, 'native_tool': tool, 'host': 'Codex',
                           'connector_origin': 'current_session_droit_francais', 'call_id': call_id,
                           'succeeded': succeeded, 'timestamp': event['timestamp'], 'result_timestamp': output_event['timestamp']})
            evidence.update(native_tool=tool, timestamp=output_event['timestamp'])
            events.append(evidence)
        elif tool == 'web__run':
            approved = set(case.get('official_source_hosts', []))
            urls = [item.get('ref_id') for item in args.get('open', []) if isinstance(item, dict)]
            if case['web_mode'] != 'official_source' or not urls or any(not isinstance(url, str) or urlsplit(url).hostname not in approved for url in urls):
                events.append({'type': 'unexpected_tool_call', 'tool': tool, 'call_id': call_id, 'reason': 'web_not_allowed'})
            else:
                events.append({'type': 'official_source_call', 'tool': 'web__run', 'native_tool': tool, 'call_id': call_id,
                               'host': urlsplit(urls[0]).hostname, 'succeeded': True, 'timestamp': event['timestamp']})
                events.append({'type': 'source_evidence', 'tool': 'web__run', 'native_tool': tool, 'call_id': call_id,
                               'status': 'missing', 'documents': [], 'reason': 'native_web_transport_not_primary_attested',
                               'content_trust': 'untrusted_source_data', 'retrieved_at': output_event['timestamp']})
        else:
            raise binder.BindingError('Outil source extérieur au protocole autorisé')
    if question_read is None or writes != 1:
        raise binder.BindingError('Entrée complète et écriture unique non démontrées')
    visible = [e for e in events if e['type'] == 'assistant_text']
    if not visible or visible[-1]['text'].rstrip('\r\n') != response_path.read_text(encoding='utf-8').rstrip('\r\n'):
        raise binder.BindingError('Réponse finale visible différente du fichier écrit')
    connections = [e for e in events if e['type'] == 'plugin_mcp_call']
    if connections:
        events[0]['mcp_servers'] = [{'name': 'droit-francais', 'status': 'connected' if any(e['succeeded'] for e in connections) else 'failed',
                                   'status_basis': 'actual_tool_result; not configuration'}]
    events.append({'type': 'result', 'host': 'Codex', 'subtype': 'success', 'is_error': False,
                   'result': visible[-1]['text'], 'timestamp': proof['completed_at']})
    for index, event in enumerate(events):
        event['event_id'] = f'e{index + 1}'
    failures = codex_failures(events, case)
    if len(loads) != len(set(loads)):
        failures.append('runtime_skill_load_duplicate')
    events.append({'type': 'technical_assessment', 'host': 'Codex', 'case_id': identifier, 'process_exit': 0,
                   'status': 'failed' if failures else 'passed', 'failures': failures,
                   'actual_plugin_activation_verified': False, 'activation_kind': 'file_read',
                   'observables': transport.observable_checks(events, case), 'event_id': f'e{len(events) + 1}'})
    assessment.validate_source_links(events)
    trace = RUN / (identifier + '.jsonl')
    binder._write(trace, ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events))
    retained = safe_source_native(native, source_ids)
    native_target = directory / 'liaison/trace-repondant.jsonl'
    binder._write(native_target, ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in retained))
    proof.update(case_id=identifier, host='Codex', activation_kind='file_read', actual_plugin_activation_verified=False,
                 export_pre_spawn=export_pre_spawn,
                 export_timestamp_basis='responder.export.json' if export_pre_spawn else exported['timestamp_basis'],
                 question_file_read_verified=True, question_call_id=question_read, input_sha256=binder._sha(input_path),
                 native_adapter_sha256=binder._sha(Path(__file__)), response_sha256=binder._sha(response_path),
                 trace_sha256=binder._sha(trace), native_filtered_sha256=binder._sha(native_target),
                 native_session_file=native_path.name, parent_session_file=parent_path.name,
                 loaded_skills=loads, runtime_files_read=read_files, source_call_ids=sorted(source_ids),
                 technical_failures=failures, source_output_retention='sanitized v2 only; raw body omitted')
    write(directory / 'liaison/execution-repondant.json', proof)
    write(directory / 'liaison/spawn-repondant.json', spawn)
    return {'case_id': identifier, 'native_thread_id': proof['thread_id'], 'loaded_skills': loads,
            'source_calls': len(source_ids), 'technical_failures': failures, 'trace': str(trace)}

def report():
    cases = binder._json((RUN / 'suite.json').read_text(encoding='utf-8'))
    results = []
    for case in cases:
        name = case['id']
        proof_path = RUN / 'juges' / name / 'liaison/execution-juge.json'
        if not proof_path.is_file():
            continue
        proof = binder._json(proof_path.read_text(encoding='utf-8'))
        response = RUN / (name + '.jsonl')
        judgment = RUN / (name + '.jugement.json')
        if binder._sha(response) != proof['response_sha256'] or binder._sha(judgment) != proof['judgment_sha256']:
            raise binder.BindingError('Preuve liée modifiée : ' + name)
        validated = validate_codex(case, binder._events(response), binder._json(judgment.read_text(encoding='utf-8')), binder._sha(response))
        if validated != proof['assessment']:
            raise binder.BindingError('Rejeu différent du jugement lié')
        results.append(validated)
    summary = {'run': 'codex-dev5-native-r1', 'host': 'Codex', 'case_count': len(cases), 'judged_count': len(results),
               'counts': {v: sum(r['verdict'] == v for r in results) for v in ('reussite', 'echec', 'bloque')},
               'actual_plugin_activation_verified': False, 'activation_kind': 'file_read', 'codex_plugin_smoke': 'not_established',
               'historical_scores_reused': False, 'release_ready': False, 'results': results}
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('respondent', 'export', 'bind', 'report'))
    parser.add_argument('--case')
    args = parser.parse_args()
    if args.command == 'export':
        result = export_judge(args.case)
    elif args.command == 'bind':
        result = bind_judge(args.case)
    elif args.command == 'respondent':
        result = bind_respondent(args.case)
    else:
        result = report()
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
