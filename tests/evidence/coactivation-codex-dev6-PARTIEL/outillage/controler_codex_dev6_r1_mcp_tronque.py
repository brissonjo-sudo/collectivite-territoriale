"""Enveloppe distincte : transport MCP achevé, charge native explicitement tronquée.

Aucun JSON incomplet n'est analysé ou reconstruit. Un objet interne typé porte
uniquement la réception native ; il ne simule pas une réponse du fournisseur.
Les fichiers figés, les sources distantes et les réponses ne sont pas modifiés.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import preuves_codex_dev6 as base
import campagne_codex_dev6_r1 as campaign

BASE_SINGLE = base.single_result
BASE_JSON = base.binder._json
BASE_WRITE = base.write
BASE_LINKS = None
BASE_EXTRACT = None
CAPTURES = {}
BY_TEXT = {}
MARKER = re.compile(r'^Warning: truncated output \(original token count: ([1-9][0-9]*)\)\n')

class TruncatedNativePayload:
    """Marqueur interne de transport, sans champ de réponse fournisseur."""
    def __init__(self, call_id):
        self.call_id = call_id

def marker(text):
    return MARKER.match(text) if isinstance(text, str) else None

def prepare(identifier):
    global BASE_EXTRACT, BASE_LINKS
    campaign.configure()
    number, case = base.case_and_number(identifier)
    native_path, _ = campaign.BASE_DISCOVER(f'/root/repondant_codex_dev6_r1_{number:02d}')
    native = base.binder._events(native_path)
    assessment, _, sources = base.modules()
    BASE_EXTRACT = sources.extract_source_evidence
    BASE_LINKS = assessment.validate_source_links
    CAPTURES.clear(); BY_TEXT.clear()
    for event in native:
        payload = event.get('payload', {})
        if payload.get('type') != 'custom_tool_call':
            continue
        script = payload.get('input', '')
        if 'tools.mcp__droit_francais__' not in script:
            continue
        tool, arguments = base.source_call(script)
        result, parts = base.outputs(native, event)
        if len(parts) != 2 or not parts[0].startswith('Script completed\n'):
            raise base.binder.BindingError('Transport MCP natif non achevé')
        match = marker(parts[1])
        if not match:
            continue
        if case['mcp_mode'] != 'required' or tool.removeprefix('mcp__droit_francais__') not in base.NATIVE_TOOLS:
            raise base.binder.BindingError('MCP tronqué hors outils/mode autorisés')
        if parts[1] in BY_TEXT:
            raise base.binder.BindingError('Charge tronquée native ambiguë')
        call_id = payload['call_id']
        CAPTURES[call_id] = {'call_id': call_id, 'native_tool': tool, 'actual_arguments': arguments,
            'timestamp': event['timestamp'], 'result_timestamp': result['timestamp'],
            'native_transport_succeeded': True, 'payload_integrity_verified': False,
            'payload_status': 'truncated', 'native_truncation_marker': match.group(0).rstrip('\n'),
            'original_token_count_reported': int(match[1]), 'received_characters': len(parts[1]),
            'source_provider_error_verified': False, **sources.scrub_visible_text(parts[1])}
        BY_TEXT[parts[1]] = TruncatedNativePayload(call_id)
    return case

def single_result(parts):
    if len(parts) == 2 and parts[0].startswith('Script completed\n') and parts[1] in BY_TEXT:
        return BY_TEXT[parts[1]]
    return BASE_SINGLE(parts)

def evidence(payload, *, tool, call_id, retrieved_at):
    if not isinstance(payload, TruncatedNativePayload):
        return BASE_EXTRACT(payload, tool=tool, call_id=call_id, retrieved_at=retrieved_at)
    capture = CAPTURES.get(call_id)
    if (payload.call_id != call_id or capture is None
            or tool != capture['native_tool'].replace('mcp__droit_francais__', 'mcp__droit-francais__', 1)
            or retrieved_at != capture['result_timestamp']):
        raise base.binder.BindingError('Réception tronquée non liée à son appel natif réel')
    return {'type': 'source_evidence', 'tool': tool, 'call_id': call_id, 'status': 'missing',
        'documents': [], 'reason': 'native_mcp_payload_truncated', 'retrieved_at': retrieved_at,
        'content_trust': 'untrusted_source_data', 'native_transport_succeeded': True,
        'payload_integrity_verified': False, 'payload_status': 'truncated',
        'native_truncation_marker': capture['native_truncation_marker'],
        'source_provider_error_verified': False, 'json_payload_parsed': False,
        'mcp_truncation_wrapper_sha256': base.binder._sha(Path(__file__))}

def validate_links(events):
    for event in events:
        if event.get('type') == 'plugin_mcp_call' and event.get('call_id') in CAPTURES:
            event.update(native_transport_succeeded=True, payload_integrity_verified=False,
                         payload_status='truncated', source_provider_error_verified=False)
    return BASE_LINKS(events)

def write(path, value):
    if path.name == 'execution-repondant.json':
        capture_path = path.parent / 'capture-mcp-tronque-assainie.jsonl'
        base.binder._write(capture_path, ''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in CAPTURES.values()))
        value = dict(value)
        value.update(mcp_truncation_wrapper_sha256=base.binder._sha(Path(__file__)),
                     native_mcp_truncation_capture_sha256=base.binder._sha(capture_path),
                     native_mcp_truncated_call_ids=list(CAPTURES), full_mcp_payload_context_verified=False,
                     native_mcp_truncation_scope='Successful native transport; incomplete payload retained as missing; no JSON reconstruction or provider error assertion.')
    return BASE_WRITE(path, value)

def activate(identifier):
    case = prepare(identifier)
    if not CAPTURES:
        raise base.binder.BindingError('Aucune troncature MCP native attestée pour cette enveloppe')
    base.single_result = single_result
    base.modules()[2].extract_source_evidence = evidence
    base.modules()[0].validate_source_links = validate_links
    base.write = write
    return case

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    args = parser.parse_args()
    activate(args.case)
    result = campaign.respondent(args.case)
    result.update(native_mcp_truncated_call_ids=list(CAPTURES), full_mcp_payload_context_verified=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))
