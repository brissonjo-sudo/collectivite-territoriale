"""Transition fermée 1.5.0 sous contrat v4 sur un vrai SHA de fixture locale, jamais une mesure."""
from pathlib import Path
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cli_toolchains as cli
import human_resolution as human

LINE = r'^MEASUREMENT_150_V4: str \| None = .*$'
UNBOUND = 'MEASUREMENT_150_V4: str | None = None'


class Transition150V4Tests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='transition-150-diagnostic-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'scripts').mkdir()
        self.names = cli.MIGRATION_150_V4 - {cli.TRANSITION_150_V4}
        self.cli_path = self.root / 'scripts/cli_toolchains.py'
        # Valable en H1 (None) comme en H2 et H3 (SHA lié) : la fixture repart toujours de H1.
        raw = (ROOT / 'scripts/cli_toolchains.py').read_text(encoding='utf-8')
        raw = re.sub(LINE, UNBOUND, raw, count=1, flags=re.M)
        self.cli_path.write_text(raw, encoding='utf-8', newline='\n')
        self.config_path = self.root / 'scripts/measurement-cli.json'
        config = json.loads((ROOT / 'scripts/measurement-cli.json').read_bytes())
        kept = {cli.MEASUREMENT_D, cli.MEASUREMENT_140_V4}
        config['campaign_measurements'] = {k: v for k, v in config['campaign_measurements'].items() if k in kept}
        config['prepared_cycles']['1.5.0-v4']['measurement_commit'] = None
        self.write(self.config_path, config)
        self.manifest_path = self.root / cli.TRANSITION_150_V4
        self.open_manifest = {'adr': cli.ADR_150_V4, 'measurement_commit': None,
            'case_contract_sha256': cli.CYCLE_V4[1], 'campaign_cli': cli.CAMPAIGN_150_CLI,
            'source_files_sha256': {n: None for n in self.names}, 'target_files_sha256': {n: None for n in self.names}}
        self.write(self.manifest_path, self.open_manifest)
        for name, _ in (*cli.CYCLE_CONTRACTS.values(), cli.CYCLE_V4):
            (self.root / name).write_bytes((ROOT / name).read_bytes())
        self.write(self.root / 'fixture-diagnostic.json', {'release_evidence': False, 'diagnostic_only': True})
        self.git('init')
        self.git('-c', 'core.autocrlf=false', 'add', '.')
        self.commit('fixture H1 non probante')
        self.h1 = self.git('rev-parse', 'HEAD').decode().strip()
        self.measured = {'plugin_commit': self.h1, 'toolchain_sha256': self.inventory()}
        self.cli_path.write_text(raw.replace(UNBOUND + '\n', "MEASUREMENT_150_V4: str | None = '" + self.h1 + "'\n", 1),
                                 encoding='utf-8', newline='\n')
        config['prepared_cycles']['1.5.0-v4']['measurement_commit'] = self.h1
        config['campaign_measurements'][self.h1] = {'campaign_cli': cli.CAMPAIGN_150_CLI,
                                                  'case_contract_sha256': cli.CYCLE_V4[1]}
        self.write(self.config_path, config)
        self.transition = {**copy.deepcopy(self.open_manifest), 'measurement_commit': self.h1,
            'source_files_sha256': {n: self.measured['toolchain_sha256'][n] for n in self.names},
            'target_files_sha256': {n: cli.sha(self.root / n) for n in self.names}}
        self.refresh()
        self.git('add', '.')
        self.commit('fixture H2 non probante')
        self.target['plugin_commit'] = self.git('rev-parse', 'HEAD').decode().strip()
        binding = patch.object(cli, 'MEASUREMENT_150_V4', self.h1)
        binding.start()
        self.addCleanup(binding.stop)

    def git(self, *args):
        return subprocess.check_output(['git', '-c', 'safe.directory=' + str(self.root), *args],
            cwd=self.root, stderr=subprocess.PIPE)

    def commit(self, message):
        self.git('-c', 'user.name=Fixture diagnostique', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', message)

    def write(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

    def inventory(self):
        return {p.relative_to(self.root).as_posix(): cli.sha(p) for p in (self.root / 'scripts').iterdir()}

    def refresh(self):
        self.write(self.manifest_path, self.transition)
        self.target = {'toolchain_sha256': self.inventory()}

    def refused(self, cause=None):
        with self.assertRaisesRegex(ValueError, 'transition 1.5.0 refusée') as caught:
            cli.compatibility_files(self.root, self.measured, self.target)
        if cause is not None:
            self.assertIn(cause, str(caught.exception.__cause__))

    def retarget(self, name):
        self.transition['target_files_sha256'][name] = cli.sha(self.root / name)
        self.refresh()

    def test_manifeste_ferme_conforme_et_compatible(self):
        self.assertEqual(cli.compatibility_files(self.root, self.measured, self.target), cli.MIGRATION_150_V4)
        human.compatible(self.root, self.measured, self.target)

    def test_manifeste_non_ferme_refuse(self):
        self.transition = copy.deepcopy(self.open_manifest)
        self.refresh()
        self.refused()
        for value in (None, list(self.names)):
            with self.subTest(inventaire=value):
                self.transition['source_files_sha256'] = value
                self.refresh()
                self.refused()

    def test_aucune_autorisation_si_H1_encore_inconnu(self):
        with patch.object(cli, 'MEASUREMENT_150_V4', None):
            with self.assertRaisesRegex(ValueError, 'transition 1.5.0 refusée'):
                cli.transition_v4_files(self.root, self.measured, self.target, '1.5.0')
            self.assertIsNone(cli.measurement_contract(self.root, self.h1))

    def test_fichier_outillage_supplementaire_refuse(self):
        (self.root / 'scripts/supplement.py').write_text('# diagnostic\n', encoding='utf-8')
        self.refresh()
        self.refused()

    def test_fichier_declare_supplementaire_refuse(self):
        self.transition['target_files_sha256']['CHANGELOG.md'] = '0' * 64
        self.refresh()
        self.refused()

    def test_document_supplementaire_dans_commit_H2_refuse(self):
        (self.root / 'note.md').write_text('Diagnostic non probant\n', encoding='utf-8')
        self.git('add', 'note.md')
        self.commit('fichier supplementaire non autorise')
        self.target['plugin_commit'] = self.git('rev-parse', 'HEAD').decode().strip()
        self.refused('Fichier Git supplémentaire')

    def test_empreinte_source_divergente_refusee(self):
        self.transition['source_files_sha256']['scripts/cli_toolchains.py'] = '0' * 64
        self.refresh()
        self.refused()

    def test_empreinte_cible_divergente_refusee(self):
        self.transition['target_files_sha256']['scripts/cli_toolchains.py'] = '0' * 64
        self.refresh()
        self.refused()

    def test_source_redeclaree_ne_remplace_pas_objet_Git_H1(self):
        self.measured['toolchain_sha256']['scripts/cli_toolchains.py'] = '0' * 64
        self.transition['source_files_sha256']['scripts/cli_toolchains.py'] = '0' * 64
        self.refresh()
        self.refused()

    def test_cible_sur_disque_divergente_refusee(self):
        self.cli_path.write_bytes(self.cli_path.read_bytes() + b'\n')
        self.refused()

    def test_SHA_H1_different_dans_manifeste_refuse(self):
        self.transition['measurement_commit'] = '0' * 40
        self.refresh()
        self.refused()

    def test_SHA_H1_different_dans_mesure_refuse(self):
        self.measured['plugin_commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'transition 1.5.0 refusée'):
            cli.transition_v4_files(self.root, self.measured, self.target, '1.5.0')

    def test_H1_egal_au_commit_lie_140_refuse(self):
        for other in (cli.MEASUREMENT_140_V4, cli.MEASUREMENT_D):
            with self.subTest(commit=other), patch.object(cli, 'MEASUREMENT_150_V4', other):
                self.measured['plugin_commit'] = other
                with self.assertRaisesRegex(ValueError, 'transition 1.5.0 refusée') as caught:
                    cli.transition_v4_files(self.root, self.measured, self.target, '1.5.0')
                self.assertIn('SHA H1 non autorisé', str(caught.exception.__cause__))

    def test_commit_lie_a_deux_versions_refuse(self):
        with patch.object(cli, 'MEASUREMENT_150_V4', cli.MEASUREMENT_140_V4):
            with self.assertRaisesRegex(ValueError, 'deux versions'):
                cli.measurement_contract(self.root, cli.MEASUREMENT_140_V4)

    def test_v2_altere_refuse(self):
        path = self.root / cli.CYCLE_CONTRACTS['1.3.0'][0]
        path.write_bytes(path.read_bytes() + b'\n')
        self.refresh()
        self.refused()

    def test_v3_altere_refuse(self):
        path = self.root / cli.CYCLE_CONTRACTS['1.4.0'][0]
        path.write_bytes(path.read_bytes() + b'\n')
        self.refresh()
        self.refused()

    def test_v4_altere_refuse(self):
        path = self.root / cli.CYCLE_V4[0]
        path.write_bytes(path.read_bytes() + b'\n')
        self.refresh()
        self.refused()

    def test_v2_declare_a_la_place_de_v4_refuse(self):
        self.transition['case_contract_sha256'] = cli.CYCLE_CONTRACTS['1.3.0'][1]
        self.refresh()
        self.refused()

    def test_cli_ou_compagnon_non_exact_refuse(self):
        for mutate in ('version', 'companion', 'sha256'):
            with self.subTest(champ=mutate):
                pin = copy.deepcopy(cli.CAMPAIGN_150_CLI)
                if mutate == 'version':
                    pin['version'] = 'codex-cli 0.162.0-alpha.17.2'
                elif mutate == 'sha256':
                    pin['sha256'] = '0' * 64
                else:
                    pin['companions_sha256']['codex-command-runner.exe'] = '0' * 64
                self.transition['campaign_cli'] = pin
                self.refresh()
                self.refused()

    def test_cli_d_une_autre_version_refusee(self):
        self.transition['campaign_cli'] = copy.deepcopy(cli.CAMPAIGN_140_CLI)
        self.refresh()
        self.refused('Manifeste 1.5.0 non fermé')

    def test_cli_d_une_autre_version_dans_le_verrou_refusee(self):
        config = json.loads(self.config_path.read_bytes())
        config['campaign_measurements'][self.h1]['campaign_cli'] = copy.deepcopy(cli.CAMPAIGN_140_CLI)
        self.write(self.config_path, config)
        self.retarget('scripts/measurement-cli.json')
        self.refused('Modification du verrou autre que la liaison H1')
        with self.assertRaisesRegex(ValueError, 'Mesure v4 sans contrat CLI/cas épinglé'):
            cli.measurement_contract(self.root, self.h1)

    def test_lecteur_modifie_meme_avec_hash_cible_recalcule_refuse(self):
        self.cli_path.write_bytes(self.cli_path.read_bytes() + b'# hors liaison\n')
        self.retarget('scripts/cli_toolchains.py')
        self.refused('Modification du lecteur autre que la liaison H1')

    def test_ligne_MEASUREMENT_140_V4_modifiee_refusee(self):
        raw = self.cli_path.read_text(encoding='utf-8')
        changed = re.sub(r'^MEASUREMENT_140_V4: str \| None = .*$', 'MEASUREMENT_140_V4: str | None = None',
                         raw, count=1, flags=re.M)
        self.assertNotEqual(raw, changed)
        self.cli_path.write_text(changed, encoding='utf-8', newline='\n')
        self.retarget('scripts/cli_toolchains.py')
        self.refused('Modification du lecteur autre que la liaison H1')

    def test_verrou_historique_modifie_meme_avec_hash_recalcule_refuse(self):
        config = json.loads(self.config_path.read_bytes())
        config['codex']['sha256'] = '0' * 64
        self.write(self.config_path, config)
        self.retarget('scripts/measurement-cli.json')
        self.refused('Modification du verrou autre que la liaison H1')

    def test_entree_140_v4_modifiee_meme_avec_hash_recalcule_refusee(self):
        config = json.loads(self.config_path.read_bytes())
        config['prepared_cycles']['1.4.0-v4']['measurement_commit'] = '0' * 40
        self.write(self.config_path, config)
        self.retarget('scripts/measurement-cli.json')
        self.refused('Modification du verrou autre que la liaison H1')

    def test_mesure_140_modifiee_meme_avec_hash_recalcule_refusee(self):
        config = json.loads(self.config_path.read_bytes())
        config['campaign_measurements'][cli.MEASUREMENT_140_V4]['campaign_cli']['sha256'] = '0' * 64
        self.write(self.config_path, config)
        self.retarget('scripts/measurement-cli.json')
        self.refused('Modification du verrou autre que la liaison H1')

    def test_mesure_140_supprimee_meme_avec_hash_recalcule_refusee(self):
        config = json.loads(self.config_path.read_bytes())
        del config['campaign_measurements'][cli.MEASUREMENT_140_V4]
        self.write(self.config_path, config)
        self.retarget('scripts/measurement-cli.json')
        self.refused('Modification du verrou autre que la liaison H1')

    def test_manifeste_empreinte_non_recalculee_refuse(self):
        self.manifest_path.write_bytes(self.manifest_path.read_bytes() + b'\n')
        self.refused()

    def test_transition_140_non_utilisable_pour_150(self):
        with self.assertRaisesRegex(ValueError, 'transition 1.4.0 refusée'):
            cli.transition_140_v4_files(self.root, self.measured, self.target)


class Repository150V4Tests(unittest.TestCase):
    """Cohérence du dépôt réel, valable en H1, H2 et H3 : jamais MEASUREMENT_150_V4 is None."""

    def setUp(self):
        self.config = json.loads((ROOT / 'scripts/measurement-cli.json').read_bytes())

    def test_liaison_du_cycle_prepare_egale_a_la_constante(self):
        entry = self.config['prepared_cycles']['1.5.0-v4']
        self.assertEqual(entry, {'case_contract_file': cli.CYCLE_V4[0], 'case_contract_sha256': cli.CYCLE_V4[1],
                                 'measurement_commit': cli.MEASUREMENT_150_V4})
        self.assertEqual(cli.prepared_cycle_v4(ROOT, '1.5.0'), cli.CYCLE_V4[0])

    def test_etat_h1_ou_lie(self):
        manifest = json.loads((ROOT / cli.TRANSITION_150_V4).read_bytes())
        commit, measurements = cli.MEASUREMENT_150_V4, self.config['campaign_measurements']
        self.assertEqual(manifest['adr'], cli.ADR_150_V4)
        self.assertEqual(manifest['campaign_cli'], cli.CAMPAIGN_150_CLI)
        self.assertEqual(manifest['case_contract_sha256'], cli.CYCLE_V4[1])
        if commit is None:
            self.assertIsNone(manifest['measurement_commit'])
            self.assertEqual(set(manifest['source_files_sha256'].values()) | set(manifest['target_files_sha256'].values()), {None})
            self.assertEqual(set(measurements), {cli.MEASUREMENT_D, cli.MEASUREMENT_140_V4})
            self.assertIsNone(cli.measurement_contract(ROOT, '0' * 40))
        else:
            self.assertEqual(measurements[commit], {'campaign_cli': cli.CAMPAIGN_150_CLI,
                                                    'case_contract_sha256': cli.CYCLE_V4[1]})

    def test_pins_fermes_et_distincts(self):
        self.assertEqual(cli.CAMPAIGN_150_CLI['version'], 'codex-cli 0.164.0-alpha.11.1')
        self.assertEqual(cli.CAMPAIGN_150_CLI['sha256'], '1103e9e09c71fa2cd0afd6d8f3b9a2d63174fe8efd7cb5bd09f1cb14ef58a098')
        self.assertEqual(set(cli.CAMPAIGN_150_CLI['companions_sha256']), cli.COMPANIONS)
        self.assertEqual(cli.CAMPAIGN_140_CLI['version'], 'codex-cli 0.163.0-alpha.10.2')
        self.assertNotEqual(cli.CAMPAIGN_150_CLI['sha256'], cli.CAMPAIGN_140_CLI['sha256'])
        self.assertEqual(self.config['campaign_measurements'][cli.MEASUREMENT_140_V4]['campaign_cli'],
                         cli.CAMPAIGN_140_CLI)

    def test_contrat_v4_inchange(self):
        self.assertEqual(cli.CYCLE_V4[1], 'be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24')
        self.assertEqual(cli.sha(ROOT / cli.CYCLE_V4[0]), cli.CYCLE_V4[1])

    def test_liste_historique_fermee_sans_140_ni_150(self):
        self.assertEqual(cli.UNBOUND_HISTORICAL_VERSIONS, {'1.1.0', '1.1.1', '1.2.0', '1.3.0'})


if __name__ == '__main__':
    unittest.main()
