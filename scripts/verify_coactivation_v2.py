"""Recalcule le gel et les preuves v2, sans réseau ni accès à Git."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from coactivation_assessment import validate_judgment
from run_coactivation_v2 import SUITE, build_prompt, frozen_failures_v2, load_cases, observable_checks, technical_failures


def digest(value: Any) -> str:
    """Calcule l'empreinte JSON canonique des seules preuves assainies."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                  separators=(',', ':')).encode()).hexdigest()


def main() -> int:
    """Refuse toute divergence ; distingue une trace valide d'un cas réussi."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--traces', required=True, type=Path)
    args = parser.parse_args()
    frozen = json.loads(args.manifest.read_text(encoding='utf-8'))
    if failures := frozen_failures_v2(frozen):
        parser.error(' | '.join(failures))
    cases = {case['id']: case for case in load_cases()}
    paths = sorted(args.traces.glob('*.jsonl'))
    if not paths:
        parser.error('Aucune trace mesurée')
    results = []
    sessions = set()
    for path in paths:
        case = cases[path.stem]
        events = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        provenance = events[0]
        expected = {
            'type': 'provenance', 'schema_version': 2,
            'candidate_commit': frozen['candidate_commit'],
            'suite_sha256': hashlib.sha256(SUITE.read_bytes()).hexdigest(),
            'case_sha256': hashlib.sha256(json.dumps(case, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
            'prompt_sha256': hashlib.sha256(build_prompt(case).encode()).hexdigest(),
            'frozen_manifest_sha256': hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        }
        if any(provenance.get(key) != value for key, value in expected.items()):
            parser.error('Provenance divergente : ' + path.name)
        init = [event for event in events if event['type'] == 'init']
        if len(init) != 1 or init[0]['session_id'] in sessions:
            parser.error('Session absente, ambiguë ou réutilisée : ' + path.name)
        sessions.add(init[0]['session_id'])
        for event in events:
            if event['type'] != 'source_evidence' or event.get('status') == 'missing':
                continue
            for document in event['documents']:
                if digest({key: value for key, value in document.items() if key != 'sha256'}) != document['sha256']:
                    parser.error('Document modifié : ' + path.name)
            if digest(event['documents']) != event['sha256']:
                parser.error('Ensemble documentaire modifié : ' + path.name)
        assessment = events[-1]
        measured = technical_failures(events, case)
        if assessment.get('process_exit') != 0:
            measured.append('process_exit_nonzero')
        if (assessment['type'] != 'technical_assessment' or assessment['case_id'] != case['id']
                or assessment['failures'] != measured
                or assessment['status'] != ('failed' if measured else 'passed')
                or assessment['observables'] != observable_checks(events, case)):
            parser.error('Bilan technique divergent : ' + path.name)
        judgment = path.with_suffix('.jugement.json')
        status = {'case_id': case['id'], 'technical_status': assessment['status'],
                  'business_status': 'not_judged', 'release_ready': False}
        if judgment.exists():
            status.update(validate_judgment(case, events,
                json.loads(judgment.read_text(encoding='utf-8')), hashlib.sha256(path.read_bytes()).hexdigest()))
            # La liaison à une session indépendante demeure un contrôle distinct.
            status['judge_identity_checked'] = False
        results.append(status)
    print(json.dumps({'evidence_integrity': 'passed', 'cases': results,
                      'full_campaign': len(paths) == len(cases), 'release_ready': False}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
