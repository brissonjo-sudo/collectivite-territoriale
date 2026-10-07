"""Audit final : active le parseur de patch après la configuration du harnais.

Les enveloppes et les pièces déjà liées restent inchangées. Aucun outil trouvé
dans les traces n'est exécuté et aucun jugement n'est remplacé.
"""
import argparse
import json
from pathlib import Path
import audit_natif_codex_dev5_r2_patch_pragma as previous

original = previous.original
base = original.base
BASE_PATCH = original.exact_patch

def exact_patch(native, call, target):
    script = call['payload'].get('input', call['payload'].get('arguments', ''))
    if script.startswith('// @exec:') and 'tools.apply_patch(' in script:
        original.require(target == original.campaign.RUN / 'plugin-spontane-incident-donnees/response.md', 'Directive patch hors réponse enregistrée')
        previous.patch.activate()
        original.require(script in previous.patch.REGISTERED, 'Patch avec directive non natif')
    return BASE_PATCH(native, call, target)

def audit(complete=False):
    original.exact_patch = exact_patch
    result = previous.audit(complete)
    result.update(patch_pragma_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=base.binder._sha(Path(__file__)))
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
