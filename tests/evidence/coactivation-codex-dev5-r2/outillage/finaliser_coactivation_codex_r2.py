"""Archive une campagne terminée sans modifier son runtime ni ses jugements."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile
import jugements_codex_dev5_r2 as judges
import campagne_codex_dev5_r2 as campaign

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

def main():
    summary = judges.report()
    assert summary['completed_respondents'] == summary['judged_count'] == 16
    assert summary['retained_unique_role_count'] == 32
    assert sum(summary['atomic_results'].values()) == 124
    assert summary['historical_scores_reused'] is False and summary['release_ready'] is False
    audit = json.loads((campaign.RUN / 'audit-natif-final.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'passed' and audit['require_complete'] is True
    assert audit['respondents_verified'] == audit['judges_verified'] == 16
    assert audit['unique_retained_roles'] == 32
    assert audit['audit_script_sha256'] == sha(ROOT / 'audit_natif_codex_dev5_r2_final.py')
    assert audit['base_audit_script_sha256'] == sha(ROOT / 'audit_natif_codex_dev5_r2.py')
    assert [entry['assessment'] for entry in audit['judges']] == summary['results']
    write(campaign.RUN / 'synthese.json', summary)
    manifest = json.loads((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
    assert all(sha(campaign.CANDIDATE / name) == digest for name, digest in manifest['files'].items())
    # Les journaux parent privés ne sont jamais publiés ; seuls les rôles de test filtrés sont copiés.
    destination = campaign.CANDIDATE / 'tests/evidence/coactivation-codex-dev5-r2'
    assert not destination.exists(), 'Archive existante : choisir un nouveau nom'
    shutil.copytree(campaign.RUN, destination)
    tools = destination / 'outillage'
    tools.mkdir()
    names = [
        'preuves_codex_dev5.py', 'controler_codex_dev5.py',
        'preuves_codex_dev5_fragments.py', 'controler_codex_dev5_fragments_crlf.py',
        'preuves_codex_dev5_web.py', 'campagne_codex_dev5_r2.py',
        'jugements_codex_dev5_r2.py', 'controler_codex_dev5_r2_site_literal.py',
        'rapport_codex_dev5.py', 'preparer_coactivation_codex_dev5.py',
        'lie_jugements_corriges.py', 'lie_jugements_corriges_bruts.py',
        'preuves_campagne_r7.py', 'finaliser_coactivation_codex_r2.py',
        'audit_natif_codex_dev5_r2.py', 'rediger_rapport_codex_r2.py',
        'audit_natif_codex_dev5_r2_final.py', 'test_audit_codex_dev5_final.py',
        'test_audit_natif_codex_dev5_r2.py',
        'audit_natif_codex_dev5_r2_mcp_tronque.py', 'controler_codex_dev5_r2_mcp_tronque.py',
        'controler_codex_dev5_r2_pragma.py', 'audit_natif_codex_dev5_r2_pragma.py',
        'controler_codex_dev5_r2_patch_pragma.py', 'audit_natif_codex_dev5_r2_patch_pragma.py',
        'controler_codex_dev5_r2_ecriture_refusee.py', 'audit_natif_codex_dev5_r2_ecriture_refusee.py',
        'test_codex_dev5_pragma.py', 'test_codex_dev5_patches.py',
        'test_preuves_codex_dev5.py', 'test_preuves_codex_dev5_fragments.py',
        'test_enveloppes_codex_dev5.py', 'test_campagne_codex_dev5_r2.py',
        'test_codex_dev5_site_literal.py',
        'test_codex_dev5_mcp_tronque.py',
    ]
    for name in names:
        shutil.copyfile(ROOT / name, tools / name)
    shutil.copyfile(ROOT / 'qualification-coactivation-dev5-codex-r1/STATUT-EXPLORATOIRE.md', destination / 'portee-r1-exploratoire.md')
    paths = {path.relative_to(destination).as_posix(): sha(path)
             for path in sorted(destination.rglob('*')) if path.is_file()}
    inventory = {'created_at': datetime.now(timezone.utc).isoformat(),
                 'candidate_commit': manifest['candidate_commit'],
                 'runtime_source_commit': manifest['runtime_source_commit'],
                 'files': paths, 'count': len(paths), 'private_parent_log_published': False,
                 'claim': 'Empreintes des pièces copiées ; audit natif local et qualification de release distincts.'}
    write(destination / 'inventaire.json', inventory)
    archive = ROOT / 'livrables/Preuves-coactivation-Codex-dev5-r2-2026-10-07.zip'
    assert not archive.exists(), 'Archive finale existante'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                package.write(path, path.relative_to(destination).as_posix())
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None
        assert set(package.namelist()) == set(paths) | {'inventaire.json'}
        for name, digest in paths.items():
            assert hashlib.sha256(package.read(name)).hexdigest() == digest
    write(ROOT / 'livrables/Controle-archive-Codex-dev5-r2-2026-10-07.json',
          {'archive': archive.name, 'sha256': sha(archive), 'verified_entries': len(paths) + 1,
           'entry_bytes_match': True, 'claim': 'Contrôle ZIP et octets ; aucun transfert de qualification.'})
    evidence_path = campaign.CANDIDATE / 'tests/evidence/release-1.2.0-dev.5.json'
    evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
    evidence.update(candidate_commit_status='committed_native_file_load_measured',
                    measurement_status='native_file_load_measured_without_plugin_smoke',
                    native_codex_measurement={'summary_path': 'tests/evidence/coactivation-codex-dev5-r2/synthese.json',
                        'candidate_commit': manifest['candidate_commit'],
                        'runtime_source_commit': manifest['runtime_source_commit'],
                        'case_count': 16, 'fresh_role_count': 32, 'counts': summary['counts'],
                        'atomic_results': summary['atomic_results'], 'actual_plugin_activation_verified': False,
                        'historical_scores_reused': False})
    evidence['release_blockers'] = [
        'Résultats de la campagne native à examiner ; chargement de fichiers distinct de l’activation du plugin',
        'Relecture DSI/RSSI et juridique humaine non recueillie',
        'Smoke du candidat dans Codex non établi',
    ]
    assert evidence['release_ready'] is False and evidence['runs'] == []
    write(evidence_path, evidence)
    print(json.dumps({'summary': summary, 'archive': str(archive), 'copied_files': len(paths)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
