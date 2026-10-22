"""Compatibilité structurelle des invariants et outils ; aucune mesure de droit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cli_toolchains import CYCLE_V4


def assess(root: Path, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Couverture fermée de chaque invariant ; source web exigée jamais simulée."""
    requirements = json.loads((root / 'scripts/cycle-v4-source-requirements.json').read_bytes())
    if (requirements.get('schema') != 'ct-cycle-satisfiability-v1'
            or requirements.get('case_contract_sha256') != CYCLE_V4[1]
            or [c['id'] for c in cases] != [c['id'] for c in requirements['cases']]):
        raise ValueError('Matrice de satisfiabilité absente ou divergente')
    results = []
    for case, expected in zip(cases, requirements['cases']):
        if case['invariants'] != [i['texte'] for i in expected['invariants']]:
            raise ValueError('Invariant non examiné : ' + case['id'])
        rows = []
        for item in expected['invariants']:
            kind = item['requirement']
            if kind == 'local_or_abstention':
                possible = True
            elif kind == 'official_primary':
                possible = (case['mcp_mode'] == 'required' or
                            (case['web_mode'] == 'official_source' and bool(case.get('official_source_hosts'))))
            elif kind == 'senat_web':
                possible = (case['web_mode'] == 'official_source' and
                            case.get('official_source_hosts') == ['www.senat.fr'] and
                            bool(case.get('official_source_instruction')))
            else:
                raise ValueError('Exigence de source inconnue')
            rows.append({**item, 'satisfaisable': possible})
        results.append({'id': case['id'], 'web_mode': case['web_mode'], 'mcp_mode': case['mcp_mode'],
                        'official_source_hosts': case.get('official_source_hosts', []),
                        'satisfaisable': all(i['satisfaisable'] for i in rows), 'invariants': rows})
    return results
