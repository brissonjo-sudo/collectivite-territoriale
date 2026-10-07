"""Audit des tentatives refusées, jamais promues en conformité."""
from pathlib import Path
import argparse
import json
import audit_natif_codex_dev5_r2_pragma as previous
import controler_codex_dev5_r2_ecriture_refusee as rejected

original = previous.original
base = original.base
BASE_RESPONDENT = previous.respondent

def respondent(number, case, manifest, parent):
    proof = base.binder._json((original.campaign.RUN / case['id'] / 'liaison/execution-repondant.json').read_text(encoding='utf-8'))
    if proof.get('rejected_patch_wrapper_sha256'):
        original.require(number == 14 and proof['protocol_compliance'] is False, 'Tentative masquée comme conformité')
        original.require(proof['rejected_patch_wrapper_sha256'] == base.binder._sha(Path(rejected.__file__)), 'Enveloppe refus modifiée')
        rejected.activate_projection()
        original.require(proof['rejected_native_patch_attempts'] == rejected.REJECTED, 'Tentative différente du natif')
        exported = base.binder._json((original.campaign.RUN / case['id'] / 'responder.export.json').read_text(encoding='utf-8'))
        original.identity(rejected.RAW, parent, '/root/repondant_codex_dev5_r2_14', exported['created_at'])
        values = rejected.ORIGINAL_EVENTS(original.campaign.RUN / (case['id'] + '.jsonl'))
        original.require(values[-1]['status'] == 'failed' and 'unexpected_tool_call' in values[-1]['failures'], 'Échec technique absent')
    result = BASE_RESPONDENT(number, case, manifest, parent)
    if number == 14:
        result['rejected_write_attempt_count'] = len(rejected.REJECTED)
        result['protocol_compliance'] = False
    return result

def audit(complete=False):
    previous.respondent = respondent
    result = previous.audit(complete)
    result.update(pragma_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=base.binder._sha(Path(__file__)),
                  rejected_patch_wrapper_sha256=base.binder._sha(Path(rejected.__file__)))
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
