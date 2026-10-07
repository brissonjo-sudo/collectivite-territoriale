"""Audit complet dev.6 readonly, modules préfigés et 32 rôles natifs frais."""
import argparse
import json
from pathlib import Path
import audit_natif_codex_dev6_r1_mcp_tronque as audit_module
import campagne_codex_dev6_r1 as campaign

def audit(complete: bool = False) -> dict:
    campaign.configure()
    base = campaign.base
    manifest = base.binder._json((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
    for filename, digest in manifest['outillage_sha256'].items():
        audit_module.original.require(base.binder._sha(campaign.ROOT / filename) == digest, 'Outillage préfigé divergent : ' + filename)
    result = audit_module.audit(complete)
    result.update(inner_audit_script_sha256=result['audit_script_sha256'], audit_script_sha256=base.binder._sha(Path(__file__)),
                  grammar_predeclared=True, outillage_sha256=manifest['outillage_sha256'])
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.require_complete)
    if args.output:
        campaign.base.binder._write(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'passed' else 1)
