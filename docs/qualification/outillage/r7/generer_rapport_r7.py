"""Dérive le rapport r7 des seules tentatives et des preuves natives rejouées."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import lie_jugements_corriges as binder
import verifier_archive_corrigee as archive
from preuves_campagne_r7 import CANDIDATE, ROOT, RUN, execution_scope
from verifier_archive_r7 import check_current_raw_export

EVIDENCE = CANDIDATE / 'tests/evidence/coactivation-corrigee'


def check_packet_export(case: dict[str, Any], trace: Path, directory: Path) -> dict[str, Any]:
    """Reconstruit chaque paquet depuis la trace, la suite et le barème figés."""
    name = case['id']
    exported = archive.load(directory / (name + '.export.json'))
    check_current_raw_export(exported)
    expected_hashes = {'packet_sha256': directory / (name + '.packet.json'),
        'response_sha256': trace, 'prompt_sha256': directory / (name + '.prompt.md'),
        'suite_sha256': CANDIDATE / 'tests/cas-coactivation-v2.json',
        'protocol_sha256': CANDIDATE / 'docs/protocole-coactivation-v2.md'}
    if exported.get('case_id') != name or any(exported.get(field) != archive.digest(path)
            for field, path in expected_hashes.items()):
        raise ValueError('Paquet, réponse, barème ou suite modifié : ' + name)
    module = binder._module(CANDIDATE)
    rebuilt = module.build_judge_packet(case, trace, CANDIDATE / 'docs/protocole-coactivation-v2.md')
    packet = archive.load(directory / (name + '.packet.json'))
    if binder._canonical(rebuilt) != binder._canonical(packet):
        raise ValueError('Paquet différent de la mesure reconstruite : ' + name)
    return exported


def build_report() -> tuple[dict[str, Any], str]:
    """Refuse une campagne partielle ou une réponse achevée sans juge frais lié."""
    frozen_path = EVIDENCE / 'gel-r7.json'
    frozen = archive.load(frozen_path)
    result = subprocess.run([sys.executable, str(CANDIDATE / 'scripts/verify_corrected_campaign.py'),
        '--manifest', str(frozen_path), '--traces', str(RUN)], cwd=CANDIDATE,
        capture_output=True, text=True, encoding='utf-8', check=True)
    verified = json.loads(result.stdout)
    cases = {case['id']: case for case in archive.load(CANDIDATE / 'tests/cas-coactivation-v2.json')}
    if len(cases) != 16 or len(verified['cases']) != 16 or verified.get('full_campaign') is not True:
        raise ValueError('Les seize tentatives ne sont pas établies')
    if len(frozen['files']) != 211 or frozen['runtime_files'] != 166:
        raise ValueError('Inventaire gelé r7 inattendu')
    for relative, expected in frozen['files'].items():
        path = CANDIDATE / relative
        if Path(relative).is_absolute() or '..' in Path(relative).parts or archive.digest(path) != expected:
            raise ValueError('Octets gelés divergents : ' + relative)
    records, identities = [], set()
    for checked in verified['cases']:
        case_id = checked['case_id']
        case = cases[case_id]
        trace = RUN / (case_id + '.jsonl')
        events = binder._events(trace)
        scope, reason = execution_scope(events)
        directory = RUN / 'juges' / case_id
        judgment_path = directory / (case_id + '.jugement.json')
        copy_path = trace.with_suffix('.jugement.json')
        proof_path = directory / 'liaison/execution-juge.json'
        record = dict(checked, execution_scope=scope, trace_path=trace.relative_to(CANDIDATE).as_posix(),
            trace_sha256=archive.digest(trace), activation_mode=case.get('activation_mode', 'forced'),
            judge_identity_checked=False)
        if scope != 'completed_response':
            if judgment_path.exists() or copy_path.exists() or proof_path.exists():
                raise ValueError('Jugement métier déclaré sur exécution interrompue : ' + case_id)
            record.update(business_status='not_judged', verdict=None, blocking_reason=reason)
        else:
            exported = check_packet_export(case, trace, directory)
            if judgment_path.read_bytes() != copy_path.read_bytes():
                raise ValueError('Copie de jugement divergente : ' + case_id)
            proof = archive.load(proof_path)
            if (proof.get('raw_adapter_sha256') != exported['raw_adapter_sha256']
                    or proof.get('raw_projection') != exported['raw_projection']
                    or proof.get('binder_sha256') != archive.digest(Path(binder.__file__))):
                raise ValueError('Provenance de liaison divergente : ' + case_id)
            session = archive.replay_judge(directory, directory / (case_id + '.packet.json'),
                judgment_path, RUN / 'juges/trace-parent-filtre.jsonl', proof_path,
                ROOT.as_posix(), exported['exported_at'])
            if session in identities:
                raise ValueError('Identité de juge réutilisée')
            identities.add(session)
            judgment = archive.load(judgment_path)
            atoms = Counter('true' if atom['status'] is True else 'false' if atom['status'] is False
                else 'unknown' for atom in judgment['invariants'].values())
            record.update(judge_identity_checked=True, judge_session_id=session,
                judgment_path=judgment_path.relative_to(CANDIDATE).as_posix(),
                judgment_sha256=archive.digest(judgment_path), verdict=judgment['verdict'],
                atomic_status_counts=dict(atoms), proof_path=proof_path.relative_to(CANDIDATE).as_posix())
        records.append(record)
    scopes = Counter(record['execution_scope'] for record in records)
    completed = scopes['completed_response']
    if len(identities) != completed:
        raise ValueError('Portée des identités non établie')
    verdicts = Counter(record['verdict'] for record in records if record['verdict'] is not None)
    atomic: Counter[str] = Counter()
    for record in records:
        atomic.update(record.get('atomic_status_counts', {}))
    summary = {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
        'run': 'r7', 'candidate_commit': frozen['candidate_commit'], 'candidate_tree': frozen['candidate_tree'],
        'frozen_manifest_sha256': archive.digest(frozen_path), 'runtime_files': frozen['runtime_files'],
        'frozen_file_count': len(frozen['files']), 'case_count': 16,
        'completed_response_count': completed, 'quota_interrupted_count': scopes['quota_interrupted'],
        'execution_failed_count': scopes['execution_failed'], 'execution_scope_counts': dict(scopes),
        'fresh_judge_count': len(identities), 'judge_identity_checked': True,
        'judge_identity_scope': 'completed_only', 'behavioral_campaign_complete': completed == 16,
        'evidence_integrity': verified['evidence_integrity'], 'technical_status_counts': dict(Counter(
            record['technical_status'] for record in records)), 'verdict_counts': dict(verdicts),
        'atomic_status_counts': dict(atomic), 'historical_scores_reused': False,
        'legal_human_review': False, 'practitioner_review': False,
        'codex_activation_smoke': 'not_established', 'release_ready': False, 'runs': records}
    rows = '\n'.join(f"| {record['case_id']} | {record['technical_status']} | "
        f"{record['execution_scope']} | {record['verdict'] or 'non jugé'} |" for record in records)
    reasons = '\n'.join('- `' + record['case_id'] + '` : ' +
        record['blocking_reason'].replace('\n', ' ') for record in records if record.get('blocking_reason'))
    report = f'''# Coactivation corrigée — r7 — 7 octobre 2026

**{completed} réponses achevées et {len(identities)} juges frais sur seize tentatives.**
La campagne comportementale est {'complète' if completed == 16 else 'inachevée'}.
`release_ready=false`. Aucun verdict comportemental n’est déduit d’un refus de quota
ou d’une erreur d’exécution ; les motifs sont ceux des traces actuelles.

## Identité mesurée

- Commit plugin `{frozen['candidate_commit']}` ; arbre `{frozen['candidate_tree']}`.
- {frozen['runtime_files']} fichiers runtime ; {len(frozen['files'])} empreintes gelées vérifiées hors ligne.
- Modèle répondant `{frozen['model']}` ; modèles de chaque juge attestés par les traces natives.
- Suite inchangée : 16 scénarios, 124 invariants, 11 sélections forcées et 5 spontanées.
- Paquets intégraux reconstruits depuis les nouvelles traces ; lectures et écritures
  littérales, identités natives et spawns sans historique rejoués.
- Les messages initiaux opaques du fournisseur ne sont pas déclarés lisibles ou vérifiés.

## Résultats dérivés

Contrôles techniques : `{summary['technical_status_counts']}`.
Exécutions : `{dict(scopes)}`.
Verdicts sur réponses achevées : `{dict(verdicts)}`.
Statuts atomiques des jugements retenus : `{dict(atomic)}`.

| Cas | Contrôle technique | Exécution | Verdict indépendant |
|---|---|---|---|
{rows}

## Limites et suite

{reasons or 'Aucun refus de quota ni erreur d’exécution dans ces seize tentatives.'}

Cette mesure porte uniquement sur le commit et les traces r7 indiqués. Aucun score
antérieur n’est transféré. Les retours primaires conservés établissent leur disponibilité,
sans certifier indépendamment chaque règle, son applicabilité ou sa vigueur.
La revue juridique, la recette DSI/RSSI et le smoke d’activation Codex restent ouverts.
Les variantes locales des six skills ne sont pas qualifiées par la mesure DSI autonome.
Les anciennes traces, tentatives de juges rejetées et scores restent conservés.
'''
    return summary, report


def main() -> None:
    """À exécuter seulement après la fin de la campagne et la validation de ses juges."""
    summary_path = EVIDENCE / 'synthese-r7.json'
    report_path = EVIDENCE / 'rapport-corrections-r7.md'
    if summary_path.exists() or report_path.exists():
        raise ValueError('Un rapport r7 existe déjà ; aucun remplacement autorisé')
    summary, report = build_report()
    binder._write(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    binder._write(report_path, report)
    print(json.dumps({key: summary[key] for key in ('run', 'candidate_commit', 'completed_response_count',
        'quota_interrupted_count', 'execution_failed_count', 'verdict_counts', 'atomic_status_counts',
        'judge_identity_checked')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
