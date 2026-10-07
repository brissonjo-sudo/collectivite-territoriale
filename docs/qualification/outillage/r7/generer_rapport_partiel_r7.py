"""Établit la portée limitée r7 : six réponses, une interruption et neuf cas non exécutés."""
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
from generer_rapport_r7 import check_packet_export
from preuves_campagne_r7 import CANDIDATE, ROOT, RUN, execution_scope

EVIDENCE = CANDIDATE / 'tests/evidence/coactivation-corrigee'
RECEIPT = EVIDENCE / 'interruption-controlee-r7.json'
MEASURED_NUMBERS = (1, 2, 3, 4, 11, 12)
INTERRUPTED_NUMBER = 5
EXPECTED_AGENTS = {f'/root/juge_corrige_r7_{number:02d}' for number in MEASURED_NUMBERS}


def verify_frozen(frozen: dict[str, Any], candidate: Path = CANDIDATE) -> None:
    """Les 211 octets gelés sont contrôlés avant tout résultat dérivé."""
    if len(frozen['files']) != 211 or frozen['runtime_files'] != 166:
        raise ValueError('Inventaire gelé partiel r7 inattendu')
    for relative, expected in frozen['files'].items():
        path = candidate / relative
        if (Path(relative).is_absolute() or '..' in Path(relative).parts
                or not path.resolve().is_relative_to(candidate.resolve())
                or archive.digest(path) != expected):
            raise ValueError('Octets gelés divergents : ' + relative)


def verify_receipt(receipt: dict[str, Any], frozen: dict[str, Any], cases: list[dict[str, Any]]) -> None:
    """La distinction non exécuté/interrompu vient du reçu de l’orchestrateur, pas de l’absence seule."""
    measured = [cases[number - 1]['id'] for number in MEASURED_NUMBERS]
    not_executed = [case['id'] for number, case in enumerate(cases, 1)
        if number not in MEASURED_NUMBERS and number != INTERRUPTED_NUMBER]
    if (receipt.get('run') != 'r7' or receipt.get('candidate_commit') != frozen['candidate_commit']
            or receipt.get('interrupted_case_id') != cases[INTERRUPTED_NUMBER - 1]['id']
            or receipt.get('response_captured') is not False
            or receipt.get('launcher_interrupted') is not True
            or not isinstance(receipt.get('reason'), str) or not receipt['reason'].strip()
            or receipt.get('completed_case_ids') != measured
            or receipt.get('not_executed_case_ids') != not_executed):
        raise ValueError('Reçu d’interruption contrôlée absent ou divergent')


def require_bound_response(trace: Path, directory: Path) -> tuple[Path, Path]:
    """Une réponse achevée sans liaison native ne figure jamais dans les résultats jugés."""
    judgment = directory / (trace.stem + '.jugement.json')
    copied = trace.with_suffix('.jugement.json')
    proof = directory / 'liaison/execution-juge.json'
    if not all(path.is_file() for path in (trace, judgment, copied, proof)):
        raise ValueError('Réponse achevée non liée à un juge frais : ' + trace.stem)
    if judgment.read_bytes() != copied.read_bytes():
        raise ValueError('Copie de jugement divergente : ' + trace.stem)
    return judgment, proof


def reject_unproved_nominal(case: dict[str, Any], checked: dict[str, Any], events: list[dict[str, Any]]) -> None:
    """Un nominal sans contenu primaire ne peut devenir une réussite dégradée."""
    assessments = [event for event in events if event.get('type') == 'technical_assessment']
    if len(assessments) != 1:
        raise ValueError('Bilan technique absent ou ambigu')
    if (case['mcp_mode'] == 'required' and checked.get('verdict') == 'reussite'
            and assessments[0].get('observables', {}).get('primary_content_available') is not True):
        raise ValueError('Réussite nominale sans primaire refusée : ' + case['id'])


def verify_parent(parent_path: Path) -> str:
    """Les six spawns frais sont les seuls événements d’outils du parent publié."""
    events = binder._events(parent_path)
    archive.unique_metadata(events)
    calls = [event for event in events if event.get('payload', {}).get('type') == 'function_call'
        and event['payload'].get('name') == 'spawn_agent']
    returned = [event for event in events if event.get('payload', {}).get('type') == 'function_call_output']
    agents = set()
    if len(events) != 13 or len(calls) != 6 or len(returned) != 6:
        raise ValueError('Parent filtré des six juges absent ou divergent')
    for event in calls:
        arguments = binder._json(event['payload']['arguments'])
        agent = '/root/' + arguments.get('task_name', '')
        if (arguments.get('fork_turns') != 'none' or 'message' in arguments
                or event['payload'].get('initial_message_verified') is not False
                or agent not in EXPECTED_AGENTS or agent in agents):
            raise ValueError('Spawn frais ou retrait du message opaque non établi')
        agents.add(agent)
        outputs = [value for value in returned if value['payload'].get('call_id') == event['payload']['call_id']]
        if len(outputs) != 1 or binder._json(outputs[0]['payload']['output']).get('task_name') != agent:
            raise ValueError('Retour du spawn non lié')
    if agents != EXPECTED_AGENTS:
        raise ValueError('Les six noms de juges attendus ne sont pas établis')
    return events[0]['payload']['id']


def build_report() -> tuple[dict[str, Any], str]:
    """Vérifie uniquement les six mesures disponibles, sans faire apparaître seize exécutions."""
    frozen_path = EVIDENCE / 'gel-r7.json'
    frozen = archive.load(frozen_path)
    verify_frozen(frozen)
    cases = archive.load(CANDIDATE / 'tests/cas-coactivation-v2.json')
    if len(cases) != 16:
        raise ValueError('La suite figée doit contenir seize cas')
    receipt = archive.load(RECEIPT)
    verify_receipt(receipt, frozen, cases)
    expected_ids = {cases[number - 1]['id'] for number in MEASURED_NUMBERS}
    traces = list(RUN.glob('*.jsonl'))
    if {trace.stem for trace in traces} != expected_ids or len(traces) != 6:
        raise ValueError('Les seules six traces disponibles ne sont pas établies')
    result = subprocess.run([sys.executable, str(CANDIDATE / 'scripts/verify_corrected_campaign.py'),
        '--manifest', str(frozen_path), '--traces', str(RUN)], cwd=CANDIDATE,
        capture_output=True, text=True, encoding='utf-8', check=True)
    verified = json.loads(result.stdout)
    if (verified.get('full_campaign') is not False or len(verified['cases']) != 6
            or {item['case_id'] for item in verified['cases']} != expected_ids
            or verified.get('evidence_integrity') != 'passed'):
        raise ValueError('Les six traces partielles ne sont pas vérifiées')
    checked_cases = {checked['case_id']: checked for checked in verified['cases']}
    parent_path = RUN / 'juges/trace-parent-filtre.jsonl'
    parent_id = verify_parent(parent_path)
    proof_paths = list((RUN / 'juges').glob('*/liaison/execution-juge.json'))
    if len(proof_paths) != 6 or {path.parent.parent.name for path in proof_paths} != expected_ids:
        raise ValueError('La campagne partielle doit conserver exactement six liaisons')
    records, identities, agents, needs_auth = [], set(), set(), []
    for number, case in enumerate(cases, 1):
        name = case['id']
        trace = RUN / (name + '.jsonl')
        directory = RUN / 'juges' / name
        record: dict[str, Any] = {'case_id': name, 'suite_number': number,
            'activation_mode': case.get('activation_mode', 'forced'), 'mcp_mode': case['mcp_mode'],
            'judge_identity_checked': False, 'verdict': None, 'release_ready': False}
        if number not in MEASURED_NUMBERS:
            if (trace.exists() or trace.with_suffix('.jugement.json').exists()
                    or (directory / (name + '.jugement.json')).exists()
                    or (directory / 'liaison/execution-juge.json').exists()):
                raise ValueError('Pièce de réponse ou de jugement sur un cas non capturé : ' + name)
            record.update(business_status='not_judged', technical_status='not_measured',
                execution_scope=('controlled_interruption_without_response' if number == INTERRUPTED_NUMBER
                    else 'not_executed'), receipt_sha256=archive.digest(RECEIPT))
            records.append(record)
            continue
        events = binder._events(trace)
        scope, _ = execution_scope(events)
        if scope != 'completed_response':
            raise ValueError('Une des six réponses n’est pas achevée : ' + name)
        checked = checked_cases[name]
        reject_unproved_nominal(case, checked, events)
        judgment_path, proof_path = require_bound_response(trace, directory)
        exported = check_packet_export(case, trace, directory)
        proof = archive.load(proof_path)
        expected_agent = f'/root/juge_corrige_r7_{number:02d}'
        if (proof.get('agent') != expected_agent or proof.get('parent_thread_id') != parent_id
                or proof.get('raw_adapter_sha256') != exported['raw_adapter_sha256']
                or proof.get('raw_projection') != exported['raw_projection']
                or proof.get('binder_sha256') != archive.digest(Path(binder.__file__))):
            raise ValueError('Identité ou adaptateur de liaison divergent : ' + name)
        session = archive.replay_judge(directory, directory / (name + '.packet.json'), judgment_path,
            parent_path, proof_path, ROOT.as_posix(), exported['exported_at'])
        if session in identities or expected_agent in agents:
            raise ValueError('Identité de juge réutilisée')
        identities.add(session)
        agents.add(expected_agent)
        judgment = archive.load(judgment_path)
        module = binder._module(CANDIDATE)
        assessment = module.validate_judgment(case, events, judgment, archive.digest(trace))
        reject_unproved_nominal(case, assessment, events)
        init = [event for event in events if event.get('type') == 'init']
        if len(init) != 1 or init[0].get('model') != frozen['model']:
            raise ValueError('Contexte répondant absent ou divergent')
        servers = [server for server in init[0].get('mcp_servers', [])
            if server.get('name') == 'droit-francais']
        auth = any(server.get('status') == 'needs-auth' for server in servers)
        if auth:
            needs_auth.append({'case_id': name, 'event_id': init[0]['event_id'],
                'server_name': 'droit-francais', 'status': 'needs-auth'})
        atoms = Counter('true' if atom['status'] is True else 'false' if atom['status'] is False
            else 'unknown' for atom in judgment['invariants'].values())
        record.update(checked, execution_scope='completed_response', trace_path=trace.relative_to(CANDIDATE).as_posix(),
            trace_sha256=archive.digest(trace), judge_identity_checked=True,
            judge_session_id=session, judge_agent=expected_agent, verdict=judgment['verdict'],
            judgment_path=judgment_path.relative_to(CANDIDATE).as_posix(),
            judgment_sha256=archive.digest(judgment_path), proof_path=proof_path.relative_to(CANDIDATE).as_posix(),
            atomic_status_counts=dict(atoms), needs_auth_observed=auth,
            mcp_observation_event_id=init[0]['event_id'])
        records.append(record)
    if len(identities) != 6 or agents != EXPECTED_AGENTS:
        raise ValueError('Les six juges frais ne sont pas établis')
    required_ids = {cases[number - 1]['id'] for number in (1, 2, 3)}
    if {item['case_id'] for item in needs_auth} != required_ids:
        raise ValueError('Les trois observations needs-auth attendues ne sont pas établies')
    verdicts = Counter(record['verdict'] for record in records if record['verdict'] is not None)
    atomic: Counter[str] = Counter()
    for record in records:
        atomic.update(record.get('atomic_status_counts', {}))
    summary = {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
        'run': 'r7', 'measurement_scope': 'partial_six_completed_responses',
        'candidate_commit': frozen['candidate_commit'], 'candidate_tree': frozen['candidate_tree'],
        'frozen_manifest_sha256': archive.digest(frozen_path), 'runtime_files': frozen['runtime_files'],
        'frozen_file_count': len(frozen['files']), 'case_count': 16, 'attempted_case_count': 7,
        'captured_trace_count': 6, 'completed_response_count': 6, 'fresh_judge_count': 6,
        'controlled_interruption_without_response_count': 1, 'not_executed_count': 9,
        'not_judged_count': 10, 'needs_auth_observed_count': len(needs_auth),
        'needs_auth_observations': needs_auth, 'quota_interrupted_count': 0,
        'execution_scope_counts': dict(Counter(record['execution_scope'] for record in records)),
        'technical_status_counts': dict(Counter(record['technical_status'] for record in records
            if record['execution_scope'] == 'completed_response')),
        'verdict_counts': dict(verdicts), 'atomic_status_counts': dict(atomic),
        'evidence_integrity': verified['evidence_integrity'], 'judge_identity_checked': True,
        'judge_identity_scope': 'six_completed_responses_only', 'parent_thread_id': parent_id,
        'behavioral_campaign_complete': False, 'historical_scores_reused': False,
        'interruption_receipt_sha256': archive.digest(RECEIPT),
        'interruption_receipt_scope': 'Déclaration assainie de l’orchestrateur ; aucune réponse absente n’est reconstituée.',
        'legal_human_review': False, 'practitioner_review': False,
        'codex_activation_smoke': 'not_established', 'release_ready': False, 'runs': records}
    rows = '\n'.join(f"| {record['case_id']} | {record['technical_status']} | "
        f"{record['execution_scope']} | {record['verdict'] or 'non jugé'} |" for record in records)
    report = f'''# Coactivation corrigée — mesure partielle r7 — 7 octobre 2026

**Six réponses capturées et six juges frais sur seize scénarios.**
Trois nominaux signalent `needs-auth` pour `droit-francais` dans leurs événements init.
Le lanceur nominal a été interrompu sur le cinquième cas : aucune réponse de ce cas
n’est capturée. Neuf autres cas ne sont pas exécutés, selon le reçu de l’orchestrateur.
La campagne comportementale est inachevée ; `release_ready=false`.

## Identité et portée vérifiées

- Commit plugin `{frozen['candidate_commit']}` ; arbre `{frozen['candidate_tree']}`.
- {frozen['runtime_files']} fichiers runtime ; {len(frozen['files'])} empreintes gelées vérifiées hors ligne.
- Réponses mesurées : ordres 1, 2, 3, 4, 11 et 12 de la suite inchangée.
- Six paquets intégraux reconstruits, six écritures de jugements et six sessions
  natives rejouées ; parent filtré limité aux six spawns sans historique.
- Les dix scénarios sans réponse capturée restent non jugés. Aucun score antérieur
  n’est transféré et aucun message initial opaque du fournisseur n’est déclaré lisible.

## Résultats dérivés

Contrôles techniques sur les six réponses : `{summary['technical_status_counts']}`.
Verdicts des six juges : `{dict(verdicts)}`.
Statuts atomiques retenus : `{dict(atomic)}`.
Observations `needs-auth` : `{[item['case_id'] for item in needs_auth]}`.

| Cas | Contrôle technique | Exécution | Verdict indépendant |
|---|---|---|---|
{rows}

## Limites et suite

Les trois réponses nominales sans primaire ne deviennent pas des réussites dégradées.
Les trois scénarios qui désactivent volontairement MCP conservent leur propre barème.
Le reçu `interruption-controlee-r7.json` distingue le cas interrompu des neuf cas non
exécutés ; il est une déclaration de l’orchestrateur, sans réponse reconstruite.
La disponibilité d’un texte primaire ne certifie pas indépendamment son applicabilité
ou sa vigueur. La revue juridique, la recette DSI/RSSI et le smoke d’activation Codex
restent ouverts. Les variantes locales des six skills ne sont pas qualifiées par
la mesure DSI autonome. Les anciennes traces et tentatives restent conservées.
'''
    return summary, report


def main() -> None:
    """À lancer seulement après accord de l’orchestrateur et liaison des six juges."""
    summary_path = EVIDENCE / 'synthese-partielle-r7.json'
    report_path = EVIDENCE / 'rapport-partiel-corrections-r7.md'
    if summary_path.exists() or report_path.exists():
        raise ValueError('Rapport partiel r7 déjà présent ; aucun écrasement autorisé')
    summary, report = build_report()
    binder._write(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    binder._write(report_path, report)
    print(json.dumps({key: summary[key] for key in ('run', 'candidate_commit', 'completed_response_count',
        'fresh_judge_count', 'needs_auth_observed_count', 'not_judged_count', 'verdict_counts',
        'atomic_status_counts', 'behavioral_campaign_complete')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
