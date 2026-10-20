"""Avis Jo liés aux runs originaux ; jamais de résolution d'une violation ou panne."""
from __future__ import annotations

from datetime import datetime
import gzip
import io
import json
from pathlib import Path
import re
import subprocess
from typing import Any

import run_codex_campaign as campaign
from measurement_common import bound, canonical, checked, digest, fingerprint
from review_codex_campaign import validate_report
from cli_toolchains import compatibility_files, measurement_contract


def dated(value: str) -> datetime:
    """Exige une date avec fuseau explicite, sans deviner une date absente."""
    try:
        result = datetime.fromisoformat(value)
        if result.tzinfo is None:
            raise ValueError('Fuseau absent')
        return result
    except (ValueError, TypeError) as exc:
        raise ValueError('Avis humain non daté') from exc


def resolve_case(case_id: str, report: dict, technical_failures: list[str], opinion: dict,
                 binding: dict, expected: dict) -> dict:
    """Résolution pure et testable ; aucune mutation du rapport automatique."""
    if technical_failures:
        raise ValueError('Échec technique non résoluble')
    items = report['invariants']
    if any(i['statut'] == 'violation' for i in items):
        raise ValueError('Violation non résoluble')
    if opinion.get('decideur') != 'Jo':
        raise ValueError('Décideur humain différent de Jo')
    dated(opinion.get('date_utc'))
    if (opinion.get('plugin_commit') != expected['measurement_commit']
            or opinion.get('campagne') != expected['campaign_attempt_id']
            or opinion.get('resume_campagne_sha256') != expected['summary_sha256']
            or binding.get('summary_sha256') != expected['summary_sha256']
            or binding['response_session']['sha256'] != expected['response_session_sha256']
            or binding['review_session']['sha256'] != expected['review_session_sha256']):
        raise ValueError('Avis lié à un autre run, commit ou campagne')
    verdicts = opinion.get('cas_valides') or opinion.get('verdicts') or {}
    verdict = verdicts.get(case_id)
    if verdict not in {'conforme', 'reserve'}:
        raise ValueError('Cas non approuvé par Jo')
    reservation = (opinion.get('reserves') or {}).get(case_id)
    if verdict == 'reserve' and (not isinstance(reservation, str) or not reservation.strip()):
        raise ValueError('Réserve humaine perdue')
    effective, resolutions = {}, []
    for item in items:
        status = item['statut']
        if status == 'non_verifiable':
            if verdict != 'conforme':
                raise ValueError('Non vérifiable sans avis conforme lié')
            resolutions.append({'invariant': item['invariant'], 'automatic_status': status,
                'effective_status': 'respecte_par_avis_humain',
                'opinion': binding['human_opinion'], 'response_session': binding['response_session'],
                'summary_sha256': expected['summary_sha256'], 'decideur': 'Jo', 'date_utc': opinion['date_utc']})
        elif status != 'respecte':
            raise ValueError('Statut automatique non résoluble')
        effective[item['invariant']] = True
    return {'invariants': effective, 'resolutions': resolutions,
            'human_verdict': verdict, 'reservation': reservation,
            'opinion': binding['human_opinion'], 'date_utc': opinion['date_utc']}


def compatible(root: Path, measured: dict, target: dict) -> None:
    """Identité du runtime et protocole, jamais identité supposée d'une nouvelle tête."""
    for key in ('runtime_sha256', 'plugin_configuration_sha256', 'case_file_sha256', 'upstream_sha256'):
        if measured.get(key) != target.get(key):
            raise ValueError('Runtime, configuration ou cas différents de la mesure : ' + key)
    permitted = {'scripts/assemble_release_evidence.py', 'scripts/human_resolution.py'}
    permitted |= compatibility_files(root, measured, target)
    old, current = measured['toolchain_sha256'], target['toolchain_sha256']
    if any(old.get(n) != current.get(n) for n in set(old) | set(current) if n not in permitted):
        raise ValueError('Protocole ou outillage mesuré différent')
    source, destination = measured['plugin_commit'], target['plugin_commit']
    if source != destination:
        argv = ['git', '-c', 'safe.directory=' + str(root)]
        ancestor = subprocess.run(argv + ['merge-base', '--is-ancestor', source, destination], cwd=root,
                                  capture_output=True, check=False)
        if ancestor.returncode:
            raise ValueError('Commit cible non descendant du commit mesuré')
        names = subprocess.check_output(argv + ['diff', '--name-only', source, destination], cwd=root).decode().splitlines()
        if any(n not in permitted and not n.startswith(('docs/adr/', 'tests/')) for n in names):
            raise ValueError('Diff cible hors assemblage documentaire')


def events(directory: Path, session: dict) -> tuple[list[dict], list[dict]]:
    """Vérifie la trace publique liée et ses métadonnées sans relire un état privé."""
    path = bound(directory, session['trace'])
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not rows:
        raise ValueError('Trace publique absente')
    for key in ('plugin_commit', 'case_id', 'role', 'origin', 'campaign_attempt_id'):
        if rows[0].get(key) != session.get(key):
            raise ValueError('Métadonnées de trace divergentes')
    return rows, [event for row in rows for event in row.get('events', [])]


def original_bytes(directory: Path, binding: dict) -> bytes:
    """Pièce originale, éventuellement gzip sans perte ; double empreinte, taille bornée."""
    raw = bound(directory, binding).read_bytes()
    if 'compression' not in binding:
        return raw
    limit = binding.get('original_octets')
    if (binding['compression'] != 'gzip' or not isinstance(limit, int)
            or not 0 <= limit <= 1_000_000):
        raise ValueError('Conservation sans perte non prise en charge')
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        decoded = stream.read(limit + 1)
    if len(decoded) != limit or digest(decoded) != binding.get('original_sha256'):
        raise ValueError('Pièce originale décompressée altérée')
    return decoded


def bundle_cases(root: Path, directory: Path, index: dict) -> dict[str, dict]:
    """Le commit lié de d exige son contrat v2 exact ; aucun repli sur v1."""
    contract = measurement_contract(root, index['measurement_commit'])
    if contract is None:
        cases = json.loads((root / 'tests/cas-plugin.json').read_bytes())
    else:
        binding = index.get('case_contract') or {}
        if (binding.get('sha256') != contract['case_contract_sha256']
                or fingerprint(root / campaign.CYCLE_CASES_FILE) != contract['case_contract_sha256']):
            raise ValueError('Contrat de cycle v2 absent ou divergent')
        bound(directory, binding)
        cases = campaign.load_cycle_cases(root)
    return {case['id']: case for case in cases}


def verify_case_hash(source: dict, case: dict) -> None:
    """Empreinte du cas complet, sans équivalence entre contrats v1 et v2."""
    if source['case_sha256'] != digest(canonical(case)):
        raise ValueError('Scénario mesuré différent')


def load_bundle(root: Path, directory: Path, target: dict) -> dict[str, Any]:
    """Contrôle les 18 cas L14 et leurs avis ; ne crée aucune preuve de release."""
    index = json.loads((directory / 'liaisons-humaines.json').read_bytes())
    if index.get('schema') != 'ct-human-linked-v1':
        raise ValueError('Index humain non pris en charge')
    for name, info in index['files'].items():
        path = bound(directory, {'evidence_path': name, 'sha256': info['sha256']})
        if path.stat().st_size != info['octets']:
            raise ValueError('Taille de pièce divergente')
        original_bytes(directory, {'evidence_path': name, **info})
    summary_path = bound(directory, index['summary'])
    summary = json.loads(summary_path.read_bytes())
    attempt, commit = index['campaign_attempt_id'], index['measurement_commit']
    if (summary.get('attempt_id') != attempt or summary.get('suite_de') is not None
            or summary.get('synthetic_inputs_allowed') is not False
            or summary.get('technical_failed_case_ids')):
        raise ValueError('Campagne différente, composite ou en échec')
    cases = bundle_cases(root, directory, index)
    recorded = {c['case_id']: c for c in summary['cas']}
    if set(index['cases']) != set(cases) or set(recorded) != set(cases) or len(summary['cas']) != len(cases):
        raise ValueError('Campagne ou couverture humaine incomplète')
    runs, reviews, resolved, opinions, threads = {}, {}, {}, {}, set()
    for name, case in cases.items():
        link = index['cases'][name]
        response_path = bound(directory, link['response_session'])
        review_path = bound(directory, link['review_session'])
        source = checked(response_path, commit, {'real_cli'})
        review = checked(review_path, commit, {'real_cli'})
        for role, value in [('reponse', source), ('relecture', review)]:
            if (value.get('case_id') != name or value.get('role') != role
                    or value.get('campaign_attempt_id') != attempt or value.get('campaign_only') is not True
                    or value.get('diagnostic_only') is True or value.get('model_requested') != 'gpt-6.1-sol'
                    or value.get('effort_requested') != 'high' or value.get('process_exit') != 0
                    or value.get('execution_errors') or value.get('failures')
                    or value.get('technical_status') != 'passed' or value.get('response_technical_failures')):
                raise ValueError('Échec technique ou session étrangère non résoluble')
            compatible(root, value, target)
            identity = value['origin']['thread_id']
            if identity in threads:
                raise ValueError('Conversation réutilisée')
            threads.add(identity)
        verify_case_hash(source, case)
        response_rows, clean = events(response_path.parent, source)
        review_rows, review_events = events(review_path.parent, review)
        if (bound(directory, link['response_trace']) != bound(response_path.parent, source['trace'])
                or bound(directory, link['review_trace']) != bound(review_path.parent, review['trace'])
                or review['response_session_sha256'] != fingerprint(response_path)
                or review['response_trace_sha256'] != source['trace']['sha256']):
            raise ValueError('Relecture ou trace liée à une autre réponse')
        failures = campaign.failures(clean, case, source['process_exit'], campaign.PROFILE)
        if failures or source.get('invariant_violations') or review.get('invariant_violations'):
            raise ValueError('Échec automatique ou violation non résoluble')
        if any(e['type'] == 'mcp_call' and (not e['succeeded'] or e['server'] != 'droit-francais'
               or e['tool'] not in campaign.MCP_TOOLS) for e in clean):
            raise ValueError('Échec MCP non résoluble')
        for line, row in enumerate(response_rows, 1):
            for event in row.get('events', []):
                if event['type'] == 'native_read' and (event.get('exit_code') != 0 or event.get('status') != 'completed'):
                    optional = next((p for p in source.get('optional_reads_absent', []) if p['trace_line'] == line), None)
                    if (event.get('paths') != ['.agents/skills/recherche-juridique/profil.md'] or not optional
                            or optional['paths'] != event['paths'] or optional.get('runtime_absence_verified') is not True
                            or (root / 'skills/recherche-juridique/profil.md').exists()):
                        raise ValueError('Lecture native échouée non résoluble')
        replies = [e['text'] for e in clean if e['type'] == 'reply']
        review_texts = [e['text'] for e in review_events if e['type'] == 'reply']
        report = review['report']
        validate_report(report, case['invariants'])
        if not replies or not review_texts or json.loads(review_texts[-1]) != report:
            raise ValueError('Rapport ou réponse absents de la trace')
        if (not any(e['type'] == 'turn_completed' for e in clean)
                or not any(e['type'] == 'turn_completed' for e in review_events)
                or any(e['type'] in {'tool_boundary', 'trace_error', 'native_read', 'unexpected_command',
                                    'mcp_call', 'web_call'} for e in review_events)):
            raise ValueError('Outil de relecture interdit')
        item = recorded[name]
        if (item.get('plugin_commit') != commit or item.get('technical_status') != 'passed'
                or item.get('tentative_reponse') != attempt or item.get('tentative_relecture') != attempt
                or {i['invariant']: i['statut_relecteur'] for i in item['invariants']}
                    != {i['invariant']: i['statut'] for i in report['invariants']}):
            raise ValueError('Résumé différent des sessions et rapports')
        opinion = json.loads(original_bytes(directory, link['human_opinion']))
        sheet_bytes = original_bytes(directory, link['review_sheet'])
        if digest(sheet_bytes) != opinion['fiche_relecture_sha256']:
            raise ValueError('Fiche relue différente')
        text = sheet_bytes.decode('utf-8').replace('\r\n', '\n')
        sections = list(re.finditer(r'(?m)^## \d+\. `([^`]+)`', text))
        section = next((text[m.end():sections[i + 1].start() if i + 1 < len(sections) else len(text)]
                        for i, m in enumerate(sections) if m[1] == name), None)
        if section is None or replies[-1] not in section:
            raise ValueError('Réponse exacte absente de la fiche approuvée')
        if dated(opinion.get('date_utc')) < dated(review['completed_at']):
            raise ValueError('Avis humain antérieur à la relecture')
        resolution = resolve_case(name, report, failures, opinion, link,
            {'measurement_commit': commit, 'campaign_attempt_id': attempt,
             'summary_sha256': fingerprint(summary_path), 'response_session_sha256': fingerprint(response_path),
             'review_session_sha256': fingerprint(review_path)})
        resolved[name] = resolution
        opinions[link['human_opinion']['evidence_path']] = opinion
        original_verdicts = opinion.get('cas_valides') or opinion.get('verdicts')
        if name not in original_verdicts:
            raise ValueError('Avis humain sans ce cas')
        normalized = {**source, 'events': clean, 'events_sha256': digest(canonical(clean)),
            'runner_sha256': source['toolchain_sha256']['scripts/run_codex_campaign.py'], 'profile': campaign.PROFILE,
            'case_sha256': digest(json.dumps(case, sort_keys=True, ensure_ascii=False).encode()),
            'measurement_commit': commit, 'qualification_target_commit': target['plugin_commit'],
            'derivation': {'kind': 'projection_of_original_session', 'original': link['response_session'],
                           'summary': index['summary']}}
        normalized.pop('payload_sha256', None)
        runs[name] = (response_path, normalized)
        projected_review = {**review, 'source_response_session_sha256': fingerprint(response_path),
            'reply_sha256': digest(replies[-1].encode()), 'source_review': link['review_session'],
            'human_resolution': resolution}
        projected_review.pop('payload_sha256', None)
        reviews[name] = (review_path, projected_review)
    coverage = []
    for opinion in opinions.values():
        coverage.extend((opinion.get('cas_valides') or opinion.get('verdicts')).keys())
    if len(coverage) != len(cases) or set(coverage) != set(cases):
        raise ValueError('Avis humains incomplets ou cas en double')
    global_opinions = [p for p in opinions.values() if p.get('human_legal_validation_globale') is True]
    if len(global_opinions) != 1:
        raise ValueError('Décision humaine globale absente ou ambiguë')
    global_opinion = global_opinions[0]
    if dated(global_opinion['decision_globale']['date_utc']) < max(dated(p['date_utc']) for p in opinions.values()):
        raise ValueError('Décision globale antérieure aux avis')
    reservations = {n: r['reservation'] for n, r in resolved.items() if r['reservation']}
    if reservations and global_opinion['decision_globale'].get('reserve_maintenue') is not True:
        raise ValueError('Réserve humaine perdue dans la décision globale')
    common = {**target, 'measurement_commit': commit, 'source_campaign': index['summary'],
              'origin': {'kind': 'derived_qualification_projection', 'synthetic': False, 'dry_run': False}}
    return {'runs': runs, 'reviews': reviews, 'resolutions': resolved, 'cases': cases,
        'campaign': {**common, 'runner_sha256': fingerprint(root / 'scripts/run_codex_campaign.py'),
                     'case_count': len(cases), 'technical_passed_count': len(cases)},
        'review': dict(common), 'source_bundle': directory, 'source_commit': commit,
        'human': {'human_legal_validation': global_opinion['human_legal_validation_globale'], 'reservations': reservations,
                  'measurement_commit': commit, 'campaign_attempt_id': attempt,
                  'decision_globale': global_opinion['decision_globale'],
                  'opinions': [index['cases'][n]['human_opinion'] for n in cases]}}
