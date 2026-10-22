"""B5 : transition fermée sur un vrai SHA de fixture locale, jamais une mesure."""
from pathlib import Path
import copy
import hashlib
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


class Transition140V4Tests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='transition-140-diagnostic-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'scripts').mkdir()
        self.names = cli.MIGRATION_140_V4 - {cli.TRANSITION_140_V4}
        self.cli_path = self.root / 'scripts/cli_toolchains.py'
        raw = (ROOT / 'scripts/cli_toolchains.py').read_text(encoding='utf-8')
        raw = re.sub(r'^MEASUREMENT_140_V4: str \| None = .*$', 'MEASUREMENT_140_V4: str | None = None', raw, count=1, flags=re.M)
        self.cli_path.write_text(raw, encoding='utf-8', newline='\n')
        self.config_path = self.root / 'scripts/measurement-cli.json'
        config = json.loads((ROOT / 'scripts/measurement-cli.json').read_bytes())
        config['campaign_measurements'] = {cli.MEASUREMENT_D: config['campaign_measurements'][cli.MEASUREMENT_D]}
        config['prepared_cycles']['1.4.0-v4']['measurement_commit'] = None
        self.write(self.config_path, config)
        self.manifest_path = self.root / cli.TRANSITION_140_V4
        self.open_manifest = {'adr': cli.ADR_140_V4, 'measurement_commit': None,
            'case_contract_sha256': cli.CYCLE_V4[1], 'campaign_cli': cli.CAMPAIGN_140_CLI,
            'source_files_sha256': {n: None for n in self.names}, 'target_files_sha256': {n: None for n in self.names}}
        self.write(self.manifest_path, self.open_manifest)
        for name, _ in (*cli.CYCLE_CONTRACTS.values(), cli.CYCLE_V4):
            (self.root / name).write_bytes((ROOT / name).read_bytes())
        self.write(self.root / 'fixture-diagnostic.json', {'release_evidence': False, 'diagnostic_only': True})
        self.git('init')
        self.git('-c', 'core.autocrlf=false', 'add', '.')
        self.git('-c', 'user.name=Fixture diagnostique', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', 'fixture H1 non probante')
        self.h1 = self.git('rev-parse', 'HEAD').decode().strip()
        self.measured = {'plugin_commit': self.h1, 'toolchain_sha256': self.inventory()}
        self.cli_path.write_text(raw.replace('MEASUREMENT_140_V4: str | None = None\n',
            "MEASUREMENT_140_V4: str | None = '" + self.h1 + "'\n", 1), encoding='utf-8', newline='\n')
        config['prepared_cycles']['1.4.0-v4']['measurement_commit'] = self.h1
        config['campaign_measurements'][self.h1] = {'campaign_cli': cli.CAMPAIGN_140_CLI,
                                                  'case_contract_sha256': cli.CYCLE_V4[1]}
        self.write(self.config_path, config)
        self.transition = {**copy.deepcopy(self.open_manifest), 'measurement_commit': self.h1,
            'source_files_sha256': {n: self.measured['toolchain_sha256'][n] for n in self.names},
            'target_files_sha256': {n: cli.sha(self.root / n) for n in self.names}}
        self.refresh()
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture diagnostique', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', 'fixture H2 non probante')
        self.target['plugin_commit'] = self.git('rev-parse', 'HEAD').decode().strip()
        binding = patch.object(cli, 'MEASUREMENT_140_V4', self.h1)
        binding.start()
        self.addCleanup(binding.stop)

    def git(self, *args):
        return subprocess.check_output(['git', '-c', 'safe.directory=' + str(self.root), *args],
            cwd=self.root, stderr=subprocess.PIPE)

    def write(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

    def inventory(self):
        return {p.relative_to(self.root).as_posix(): cli.sha(p) for p in (self.root / 'scripts').iterdir()}

    def refresh(self):
        self.write(self.manifest_path, self.transition)
        self.target = {'toolchain_sha256': self.inventory()}

    def refused(self):
        with self.assertRaisesRegex(ValueError, 'transition 1.4.0 refusée'):
            cli.compatibility_files(self.root, self.measured, self.target)

    def test_manifeste_ferme_conforme_et_compatible(self):
        self.assertEqual(cli.compatibility_files(self.root, self.measured, self.target), cli.MIGRATION_140_V4)
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
        with patch.object(cli, 'MEASUREMENT_140_V4', None):
            with self.assertRaisesRegex(ValueError, 'transition 1.4.0 refusée'):
                cli.transition_140_v4_files(self.root, self.measured, self.target)
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
        self.git('-c', 'user.name=Fixture diagnostique', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', 'fichier supplementaire non autorise')
        self.target['plugin_commit'] = self.git('rev-parse', 'HEAD').decode().strip()
        self.refused()

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
        with self.assertRaisesRegex(ValueError, 'transition 1.4.0 refusée'):
            cli.transition_140_v4_files(self.root, self.measured, self.target)

    def test_v2_altere_refuse(self):
        path = self.root / cli.CYCLE_CONTRACTS['1.3.0'][0]
        path.write_bytes(path.read_bytes() + b'\n')
        self.refresh()
        self.refused()

    def test_v3_altere_refuse(self):
        path = self.root / cli.CYCLE_V4[0]
        path.write_bytes(path.read_bytes() + b'\n')
        self.refresh()
        self.refused()

    def test_v2_declare_a_la_place_de_v3_refuse(self):
        self.transition['case_contract_sha256'] = cli.CYCLE_CONTRACTS['1.3.0'][1]
        self.refresh()
        self.refused()

    def test_cli_ou_compagnon_non_exact_refuse(self):
        for mutate in ('version', 'companion'):
            with self.subTest(champ=mutate):
                pin = copy.deepcopy(cli.CAMPAIGN_140_CLI)
                if mutate == 'version':
                    pin['version'] = 'codex-cli 0.162.0-alpha.17.2'
                else:
                    pin['companions_sha256']['codex-command-runner.exe'] = '0' * 64
                self.transition['campaign_cli'] = pin
                self.refresh()
                self.refused()

    def test_lecteur_modifie_meme_avec_hash_cible_recalcule_refuse(self):
        self.cli_path.write_bytes(self.cli_path.read_bytes() + b'# hors liaison\n')
        self.transition['target_files_sha256']['scripts/cli_toolchains.py'] = cli.sha(self.cli_path)
        self.refresh()
        self.refused()

    def test_verrou_historique_modifie_meme_avec_hash_recalcule_refuse(self):
        config = json.loads(self.config_path.read_bytes())
        config['codex']['sha256'] = '0' * 64
        self.write(self.config_path, config)
        self.transition['target_files_sha256']['scripts/measurement-cli.json'] = cli.sha(self.config_path)
        self.refresh()
        self.refused()

    def test_manifeste_empreinte_non_recalculee_refuse(self):
        self.manifest_path.write_bytes(self.manifest_path.read_bytes() + b'\n')
        self.refused()


if __name__ == '__main__':
    unittest.main()
