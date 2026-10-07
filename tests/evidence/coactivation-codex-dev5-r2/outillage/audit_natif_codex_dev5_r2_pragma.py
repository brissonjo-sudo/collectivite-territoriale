"""Audit distinct des scripts sources avec directive native explicite."""
from pathlib import Path
import argparse
import json
import audit_natif_codex_dev5_r2_mcp_tronque as previous
import controler_codex_dev5_r2_pragma as pragma

original = previous.original
base = original.base
BASE_RESPONDENT = previous.audit_respondent

def respondent(number, case, manifest, parent):
    proof = base.binder._json((original.campaign.RUN / case['id'] / 'liaison/execution-repondant.json').read_text(encoding='utf-8'))
    if proof.get('source_pragma_wrapper_sha256'):
        original.require(proof['source_pragma_wrapper_sha256'] == base.binder._sha(Path(pragma.__file__)), 'Enveloppe directive altérée')
        native = base.binder._events(original.campaign.BASE_DISCOVER(f'/root/repondant_codex_dev5_r2_{number:02d}')[0])
        actual = pragma.collect(native)
        original.require(actual and actual == proof['native_source_pragmas'], 'Directives non liées aux scripts natifs')
    return BASE_RESPONDENT(number, case, manifest, parent)

def audit(complete=False):
    pragma.activate_parser()
    previous.audit_respondent = respondent
    result = previous.audit(complete)
    result.update(mcp_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=base.binder._sha(Path(__file__)),
                  source_pragma_wrapper_sha256=base.binder._sha(Path(pragma.__file__)))
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
