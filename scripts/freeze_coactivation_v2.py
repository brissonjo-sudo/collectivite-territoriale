"""Crée un gel v2 depuis des octets committés et le runtime r3 inchangé."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from run_coactivation_v2 import ROOT
from run_plugin_campaign import frozen_failures

ADDED = (
    'scripts/run_coactivation_v2.py', 'scripts/source_evidence.py',
    'scripts/coactivation_assessment.py', 'scripts/freeze_coactivation_v2.py',
    'tests/cas-coactivation-v2.json', 'tests/test_coactivation_v2.py',
    'tests/test_source_evidence.py', 'docs/cas-coactivation-v2.md',
    'docs/protocole-coactivation-v2.md', '.gitattributes',
)


def main() -> int:
    """Refuse tout runtime divergent, fichier non committé ou gel déjà présent."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Gel existant conservé')
    prior = json.loads((ROOT / 'tests/evidence/qualification-dsi/gel-r3.json').read_text(encoding='utf-8'))
    if failures := frozen_failures(prior):
        parser.error(' | '.join(failures))
    git = ['git', '-c', 'safe.directory=' + ROOT.as_posix()]
    commit = subprocess.check_output([*git, 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    files = dict(prior['files'])
    for relative in (*files.keys(), *ADDED):
        data = (ROOT / relative).read_bytes()
        committed = subprocess.check_output([*git, 'show', commit + ':' + relative], cwd=ROOT)
        if data != committed:
            parser.error('Octets locaux différents du commit : ' + relative)
        files[relative] = hashlib.sha256(data).hexdigest()
    frozen = {'schema_version': 2, 'candidate_commit': commit,
        'baseline_runtime_commit': prior['candidate_commit'],
        'created_at': datetime.now(timezone.utc).isoformat(), 'model': prior['model'],
        'runtime_files': prior['runtime_files'], 'runtime_changed': False,
        'prior_manifest_sha256': hashlib.sha256((ROOT / 'tests/evidence/qualification-dsi/gel-r3.json').read_bytes()).hexdigest(),
        'files': dict(sorted(files.items()))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(frozen, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'candidate_commit': commit, 'frozen_files': len(files), 'runtime_files': prior['runtime_files']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
