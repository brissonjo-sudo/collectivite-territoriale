"""Pilote ciblé partiel : conserver cinq jugements et un rejet hors score."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import zipfile
import campagne_codex_dev6_r1 as campaign
import jugements_codex_dev6_r1 as judges
import audit_natif_codex_dev6_final as auditor

SELECTED = ('plugin-prime-depart-retraite', 'plugin-garde-fou-apja', 'plugin-violation-donnees', 'plugin-dsi-reouverture', 'plugin-spontane-budget', 'plugin-spontane-reversibilite')
REJECTED = 'plugin-garde-fou-apja'
EXPECTED_VALID = tuple(case for case in SELECTED if case != REJECTED)

def finalize() -> dict:
    campaign.configure()
    base = campaign.base
    result = judges.report()
    assert (result['completed_respondents'], result['judged_count'], result['retained_unique_role_count']) == (5, 5, 10), 'Attendre les cinq répondants liés et leurs cinq juges'
    assert tuple(row['case_id'] for row in result['results']) == EXPECTED_VALID
    manifest = base.binder._json((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
    cases = base.binder._json((campaign.RUN / 'suite.json').read_text(encoding='utf-8'))
    rejected_dir = campaign.RUN / 'rejets-protocole' / REJECTED
    rejection = base.binder._json((rejected_dir / 'rejet-protocole.json').read_text(encoding='utf-8'))
    assert rejection['status'] == 'rejected_protocol_not_scored' and rejection['business_trace_created'] is False
    for filename, field in (('trace-native-filtre-assainie.jsonl', 'native_filtered_sanitized_sha256'), ('argument-rejete.json', 'exact_argument_file_sha256')):
        assert base.binder._sha(rejected_dir / filename) == rejection[field]
    assert base.binder._sha(campaign.RUN / REJECTED / 'response.md') == rejection['response_sha256']
    assert base.binder._sha(campaign.ROOT / 'preserver_rejet_codex_dev6.py') == rejection['preserver_sha256']
    executed = []
    fresh_threads = {rejection['thread_id']}
    native_inventory = base.native_inventory(base.DIRECTORIES)
    for number, case in enumerate(cases, 1):
        agent = f'/root/repondant_codex_dev6_r1_{number:02d}'
        matches = [path for path, meta in native_inventory.values() if base.agent_path(meta) == agent]
        assert len(matches) <= 1, 'Identité native ambiguë, ne pas compter comme absence'
        if not matches:
            assert case['id'] not in SELECTED, 'Identité native attendue manquante'
            continue
        native_path, parent_path = campaign.BASE_DISCOVER(agent)
        assert case['id'] in SELECTED, 'Un autre cas a été créé : revoir le périmètre partiel'
        native = base.binder._events(native_path)
        parent = base.binder._events(parent_path)
        export = base.binder._json((campaign.RUN / case['id'] / 'responder.export.json').read_text(encoding='utf-8'))
        parent, _ = campaign.guarded.successful_parent(parent, agent)
        identity, _ = base.identity(native, parent, agent, export['created_at'])
        if case['id'] == REJECTED:
            assert identity['thread_id'] == rejection['thread_id']
        else:
            assert identity['thread_id'] not in fresh_threads
        fresh_threads.add(identity['thread_id'])
        executed.append(case['id'])
    assert tuple(executed) == SELECTED
    audit = auditor.audit(False)
    assert audit['status'] == 'passed' and audit['require_complete'] is False
    assert (audit['respondents_verified'], audit['judges_verified'], audit['unique_retained_roles']) == (5, 5, 10)
    assert [row['assessment'] for row in audit['judges']] == result['results']
    assert rejection['thread_id'] not in {row['thread_id'] for group in ('respondents', 'judges') for row in audit[group]}
    audit_path = campaign.RUN / 'audit-natif-PARTIEL-final.json'
    base.write(audit_path, audit)
    measured_atoms = sum(result['atomic_results'].values())
    expected_atoms = sum(len(case['invariant_objects']) for case in cases if case['id'] in EXPECTED_VALID)
    assert measured_atoms == expected_atoms
    partial = {**result, 'created_at': datetime.now(timezone.utc).isoformat(), 'scope': 'PARTIEL targeted native file-load pilot; no full-suite result',
               'prepared_cases': 16, 'original_suite_atomic_count': 124, 'executed_case_count': 6,
               'bound_respondent_count': 5, 'judged_case_count': 5, 'effectively_judged_atomic_count': measured_atoms,
               'rejected_protocol_case_count': 1, 'rejected_protocol_cases': [rejection],
               'not_executed_cases': [case['id'] for case in cases if case['id'] not in SELECTED],
               'native_audit_sha256': base.binder._sha(audit_path), 'full_suite_complete': False,
               'total_observed_unique_roles_including_rejected': 11, 'actual_plugin_activation_verified': False, 'release_ready': False}
    base.write(campaign.RUN / 'synthese-PARTIELLE.json', partial)
    lines = ['# Pilote natif Codex dev.6 — PARTIEL', '', f"Candidat `{result['candidate_commit']}` ; source runtime `{result['runtime_source_commit']}`.", '',
             f"16 cas et 124 atomes préparés ; six cas exécutés, cinq réponses liées, cinq jugements, {measured_atoms} atomes effectivement jugés. Un rôle rejeté conservé séparément ; dix cas non exécutés.", '',
             f"Comptes des cinq cas liés uniquement : {result['counts']}. Ces nombres ne sont pas un résultat de la suite complète.", '', '| Cas | Statut |', '| --- | --- |']
    lines += [f"| {row['case_id']} | {row['verdict']} |" for row in result['results']]
    lines += [f"| {REJECTED} | Rejet de protocole, hors score : six lectures regroupées dans un seul exec |", '',
              'Le rejet conserve identité native, export antérieur, argument exact en JSON et SHA, journal filtré/assaini et SHA de la réponse. Aucune trace métier, jugement inventé, acteur remplacé ni lecture réparée.', '',
              'L’audit natif reste explicitement partiel : cinq répondants liés et cinq juges frais. La commande --require-complete exige toujours 16 répondants, 16 juges et 32 identités ; elle n’est pas rendue verte.', '',
              'Lectures par fichiers et fragments bornés : aucune activation réelle du plugin attestée. Messages initiaux opaques et isolation absolue du système non vérifiés. Consignes forcées de STOP/chargement limitent les conclusions causales. Recherche, réception d’une source primaire pertinente et vérification de vigueur restent distinctes. Aucun score dev.5, historique ou DSI autonome transféré.', '',
              'Installation isolée et smoke sont des opérations distinctes, hors prompts de mesure. Aucun merge, release ou validation humaine/juridique dans ce pilote.', '',
              'Cas non exécutés : ' + ', '.join(partial['not_executed_cases']) + '.', '']
    for case in cases:
        if case['id'] not in EXPECTED_VALID:
            continue
        document = base.binder._json((campaign.RUN / (case['id'] + '.jugement.json')).read_text(encoding='utf-8'))
        missing = [(key, item) for key, item in document['invariants'].items() if item['status'] is not True]
        if missing:
            lines += ['## ' + case['id'], '']
            lines += [f"- `{key}` = `{item['status']}` : {item['rationale']}" for key, item in missing]
            lines.append('')
    base.binder._write(campaign.RUN / 'rapport-PARTIEL.md', '\n'.join(lines))
    files = {path.relative_to(campaign.RUN).as_posix(): path for path in campaign.RUN.rglob('*') if path.is_file()}
    for name, digest in manifest['outillage_sha256'].items():
        assert base.binder._sha(campaign.ROOT / name) == digest
        files['outillage/' + name] = campaign.ROOT / name
    for name in ('preserver_rejet_codex_dev6.py', 'finaliser_codex_dev6_PARTIEL.py', 'test_grammaire_codex_dev6.py', 'lie_jugements_corriges.py', 'lie_jugements_corriges_bruts.py', 'preuves_campagne_r7.py'):
        files['outillage/' + name] = campaign.ROOT / name
    inventory = {relative: base.binder._sha(path) for relative, path in sorted(files.items())}
    archive = campaign.ROOT / 'livrables/Preuves-coactivation-Codex-dev6-PARTIEL-2026-10-07.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as package:
        for relative, path in sorted(files.items()):
            package.writestr(relative, path.read_bytes())
        package.writestr('inventory.json', json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None
        for relative, digest in inventory.items():
            assert hashlib.sha256(package.read(relative)).hexdigest() == digest
    receipt = {'archive_path': archive.resolve().as_posix(), 'archive_sha256': base.binder._sha(archive), 'entry_count': len(inventory) + 1,
               'scope': 'PARTIEL', 'candidate_commit': result['candidate_commit'], 'runtime_source_commit': result['runtime_source_commit'],
               'prepared_cases': 16, 'executed_cases': 6, 'bound_cases': 5, 'judged_cases': 5, 'effectively_judged_atoms': measured_atoms,
               'rejected_protocol_cases': 1, 'not_executed_cases': 10, 'counts_bound_only': result['counts'],
               'native_audit_sha256': base.binder._sha(audit_path), 'release_ready': False, 'full_suite_complete': False}
    base.write(campaign.ROOT / 'livrables/Controle-archive-Codex-dev6-PARTIEL-2026-10-07.json', receipt)
    return receipt

if __name__ == '__main__':
    print(json.dumps(finalize(), ensure_ascii=False, indent=2))
