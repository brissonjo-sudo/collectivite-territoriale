"""Audit distinct en lecture seule, y compris réception MCP native tronquée.

Réutilise l'audit initial intact. L'interception limitée au texte exact lié au
retour natif transmet un marqueur interne ; aucun JSON incomplet n'est analysé.
Les reçus antérieurs et toutes les pièces existantes restent inchangés.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import audit_natif_codex_dev6_r1 as original
import controler_codex_dev6_r1_mcp_tronque as mcp

base = original.base
BASE_AUDIT_RESPONDENT = original.audit_respondent
BASE_JSON = base.binder._json
BASE_EXTRACT = base.modules()[2].extract_source_evidence

def native_json(value):
    if isinstance(value, str) and value in mcp.BY_TEXT:
        return mcp.BY_TEXT[value]
    return BASE_JSON(value)

def audit_respondent(number, case, manifest, parent):
    base.binder._json = BASE_JSON
    base.modules()[2].extract_source_evidence = BASE_EXTRACT
    proof_path = original.campaign.RUN / case['id'] / 'liaison/execution-repondant.json'
    proof = BASE_JSON(proof_path.read_text(encoding='utf-8'))
    if not proof.get('mcp_truncation_wrapper_sha256'):
        return BASE_AUDIT_RESPONDENT(number, case, manifest, parent)
    original.require(proof['mcp_truncation_wrapper_sha256'] == base.binder._sha(Path(mcp.__file__)), 'Enveloppe MCP tronqué altérée')
    mcp.prepare(case['id'])
    original.require(bool(mcp.CAPTURES), 'Troncature native MCP non retrouvée')
    base.binder._json = native_json
    base.modules()[2].extract_source_evidence = mcp.evidence
    try:
        result = BASE_AUDIT_RESPONDENT(number, case, manifest, parent)
        capture_path = proof_path.parent / 'capture-mcp-tronque-assainie.jsonl'
        original.require(proof['native_mcp_truncation_capture_sha256'] == base.binder._sha(capture_path), 'Capture MCP tronquée altérée')
        original.require(original.normalized(base.binder._events(capture_path)) == original.normalized(list(mcp.CAPTURES.values())), 'Capture MCP différente du retour assaini réel')
        original.require(proof['native_mcp_truncated_call_ids'] == list(mcp.CAPTURES), 'Appels MCP tronqués différents')
        original.require(proof['full_mcp_payload_context_verified'] is False, 'Intégrité MCP faussement attestée')
        events = base.binder._events(original.campaign.RUN / (case['id'] + '.jsonl'))
        for call_id in mcp.CAPTURES:
            calls = [e for e in events if e.get('call_id') == call_id and e.get('type') == 'plugin_mcp_call']
            original.require(len(calls) == 1 and calls[0]['succeeded'] is True and calls[0]['native_transport_succeeded'] is True
                             and calls[0]['payload_integrity_verified'] is False and calls[0]['payload_status'] == 'truncated'
                             and calls[0]['source_provider_error_verified'] is False, 'Transport MCP et intégrité confondus')
            result['warnings'].append({'call_id': call_id, 'kind': 'native_mcp_payload_truncated',
                                       'native_transport_succeeded': True, 'full_mcp_payload_context_verified': False})
        return result
    finally:
        base.binder._json = BASE_JSON
        base.modules()[2].extract_source_evidence = BASE_EXTRACT

def audit(require_complete=False):
    original.audit_respondent = audit_respondent
    result = original.audit(require_complete)
    result.update(base_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=base.binder._sha(Path(__file__)),
                  native_mcp_truncation_wrapper_sha256=base.binder._sha(Path(mcp.__file__)))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.require_complete)
    if args.output:
        base.binder._write(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'passed' else 1)
