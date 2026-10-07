"""Audit final distinct des directives et de la tentative refusée."""
from pathlib import Path
import argparse
import json
import audit_natif_codex_dev5_r2_ecriture_refusee as previous
import controler_codex_dev5_r2_patch_pragma as patch

original = previous.original
base = original.base
BASE_RESPONDENT = previous.respondent

def respondent(number, case, manifest, parent):
    proof = base.binder._json((original.campaign.RUN / case['id'] / 'liaison/execution-repondant.json').read_text(encoding='utf-8'))
    if proof.get('patch_pragma_wrapper_sha256'):
        original.require(number == 13, 'Directive patch hors cas enregistré')
        original.require(proof['patch_pragma_wrapper_sha256'] == base.binder._sha(Path(patch.__file__)), 'Enveloppe patch modifiée')
        patch.activate()
        original.require(proof['native_patch_pragmas'] == patch.RECEIPTS, 'Directive patch non native')
    return BASE_RESPONDENT(number, case, manifest, parent)

def audit(complete=False):
    previous.respondent = respondent
    result = previous.audit(complete)
    result.update(rejected_patch_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=base.binder._sha(Path(__file__)),
                  patch_pragma_wrapper_sha256=base.binder._sha(Path(patch.__file__)))
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
