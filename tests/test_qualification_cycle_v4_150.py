"""Mesure 1.5.0 sous contrat v4 : contrats fermés et preuves synthétiques, sans processus modèle."""
from pathlib import Path
import contextlib
import copy
import io
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import assemble_release_evidence as assembly
import campaign_contract as cases
import cli_toolchains as cli
import human_resolution as human
import measurement_common as common
import qualify_distribution as qualifier
import run_codex_campaign as runner
import test_qualification_cycle_v2 as v2
from support_distribution_contract import complete_synthetic_contract, refresh_smoke_snapshot

V4 = 'scripts/cas-plugin-cycle-v4.json'
# Identité explicitement factice, autorisée uniquement par patch dans ces tests.
SYNTHETIC_COMMIT = '5' * 40


class CycleV4Version150Tests(unittest.TestCase):
    def setUp(self):
        self.fixture = v2.QualificationCycleTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.root, self.evidence = self.fixture.root, self.fixture.evidence
        self.v4 = json.loads((ROOT / V4).read_bytes())

    def set_version(self, version):
        self.evidence['plugin_version'] = version
        manifest = qualifier.load(self.root, '.codex-plugin/plugin.json')
        manifest['version'] = version
        (self.root / '.codex-plugin/plugin.json').write_text(json.dumps(manifest), encoding='utf-8')

    def bind_150(self):
        self.set_version('1.5.0')
        for name in (V4, cases.CYCLE_CASES_FILE):
            (self.root / name).write_bytes((ROOT / name).read_bytes())
        upstream = qualifier.load(self.root, 'upstream.json')
        upstream['skills']['dsi-fpt'] = qualifier.load(ROOT, 'upstream.json')['skills']['dsi-fpt']
        shutil.copytree(ROOT / 'skills/dsi-fpt', self.root / 'skills/dsi-fpt')
        (self.root / 'upstream.json').write_text(json.dumps(upstream), encoding='utf-8')
        self.evidence['upstream_commits'] = {name: item['commit'] for name, item in upstream['skills'].items()}
        native = qualifier.load(self.root, self.evidence['native_campaign']['evidence_path'])
        response_path = self.root / native['runs'][0]['evidence_path']
        response = json.loads(response_path.read_bytes())
        response['runtime_sha256'] = common.snapshot(self.root)['runtime_sha256']
        response_path.write_text(json.dumps(response), encoding='utf-8')
        self.fixture.project(self.v4)
        config = qualifier.load(self.root, 'scripts/measurement-cli.json')
        config['prepared_cycles']['1.5.0-v4']['measurement_commit'] = SYNTHETIC_COMMIT
        config['campaign_measurements'][SYNTHETIC_COMMIT] = {
            'campaign_cli': copy.deepcopy(cli.CAMPAIGN_150_CLI), 'case_contract_sha256': cli.CYCLE_V4[1]}
        self.config = config
        (self.root / 'scripts/measurement-cli.json').write_text(json.dumps(config), encoding='utf-8')
        self.fixture.index['measurement_commit'] = SYNTHETIC_COMMIT
        self.fixture.contract_path.write_bytes((ROOT / V4).read_bytes())
        self.fixture.index['case_contract'] = common.binding(self.fixture.contract_path, self.fixture.index_path.parent)
        self.fixture.link_index()
        smoke = qualifier.load(self.root, self.evidence['codex_smoke']['evidence_path'])
        snapshot = common.snapshot(self.root)
        smoke['plugin_configuration_sha256'] = snapshot['plugin_configuration_sha256']
        smoke['runtime_sha256'] = snapshot['runtime_sha256']
        smoke['visible_skills'] = sorted(upstream['skills'])
        self.fixture.fixture.write_proof('codex_smoke', smoke)
        refresh_smoke_snapshot(self.fixture.fixture)
        binding = patch.object(cli, 'MEASUREMENT_150_V4', SYNTHETIC_COMMIT)
        self.addCleanup(binding.stop)
        binding.start()
        # Reçus factices portant les pins de la 1.5.0 (campagne et smoke), depuis une source de verrous locale.
        directory = tempfile.TemporaryDirectory(prefix='source-verrous-150-')
        self.addCleanup(directory.cleanup)
        source = Path(directory.name)
        (source / 'scripts').mkdir()
        (source / 'scripts/measurement-cli.json').write_text(json.dumps(config), encoding='utf-8')
        shutil.copyfile(ROOT / 'scripts/smoke-cli.json', source / 'scripts/smoke-cli.json')
        complete_synthetic_contract(self.fixture.fixture, source, SYNTHETIC_COMMIT)

    def errors(self):
        return qualifier.distribution_errors(self.root, self.evidence)

    def test_preuve_150_liee_passe_en_vue_CI_et_lecteur_assembleur(self):
        self.bind_150()
        self.assertEqual(self.errors(), [])
        expected = {c['id']: c for c in self.v4}
        self.assertEqual(qualifier.qualification_cases(self.root, self.evidence), expected)
        self.assertEqual(assembly.measurement_cases(self.root, SYNTHETIC_COMMIT), expected)
        self.assertEqual(human.bundle_cases(self.root, self.fixture.index_path.parent, self.fixture.index), expected)

    def test_pins_150_pour_campagne_et_smoke_seulement_pour_le_commit_lie(self):
        self.bind_150()
        pins = cli.toolchains(self.root, SYNTHETIC_COMMIT)
        self.assertEqual(pins['campaign_cli'], cli._pin(cli.CAMPAIGN_150_CLI, True))
        self.assertEqual(pins['smoke_cli'], cli._pin(cli.CAMPAIGN_150_CLI, True))
        # Sans commit lié ou pour la 1.4.0, le smoke garde scripts/smoke-cli.json (0.163).
        historical = cli.phase_pin('smoke_cli')
        self.assertEqual(historical['version'], cli.CAMPAIGN_140_CLI['version'])
        self.assertEqual(cli.phase_pin('smoke_cli', cli.MEASUREMENT_140_V4), historical)
        self.assertEqual(cli.phase_pin('campaign_cli', cli.MEASUREMENT_140_V4), cli._pin(cli.CAMPAIGN_140_CLI, True))

    def test_150_avec_le_commit_lie_de_la_140_refusee(self):
        self.bind_150()
        self.fixture.index['measurement_commit'] = cli.MEASUREMENT_140_V4
        self.fixture.link_index()
        self.assertTrue(any('v4 réservé' in e for e in self.errors()))
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            assembly.measurement_cases(self.root, cli.MEASUREMENT_140_V4)

    def test_140_avec_le_commit_lie_de_la_150_refusee(self):
        self.bind_150()
        self.set_version('1.4.0')
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            qualifier.qualification_cases(self.root, self.evidence)
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            assembly.measurement_cases(self.root, SYNTHETIC_COMMIT)

    def test_commit_inconnu_et_champ_de_preuve_ne_selectionnent_pas_v4(self):
        self.bind_150()
        self.fixture.index['measurement_commit'] = '2' * 40
        self.evidence['measurement_commit'] = SYNTHETIC_COMMIT
        self.fixture.link_index()
        self.assertTrue(any('1.5.0 sans commit lié' in e for e in self.errors()))

    def test_ajout_au_registre_seul_n_autorise_pas_commit(self):
        self.bind_150()
        with patch.object(cli, 'MEASUREMENT_150_V4', None):
            self.assertIsNone(cli.measurement_contract(self.root, SYNTHETIC_COMMIT))
            with self.assertRaisesRegex(ValueError, '1.5.0 sans commit lié'):
                assembly.measurement_cases(self.root, SYNTHETIC_COMMIT)

    def test_150_sans_projection_refusee(self):
        self.bind_150()
        del self.evidence['public_projection']
        self.assertEqual(self.errors(), ['Projection publique refusée : Projection publique absente'])

    def test_projection_exigee_meme_sans_lien_pour_150_et_suivantes(self):
        self.bind_150()
        del self.evidence['public_projection']
        del self.evidence['review']['linked_sources']
        for version in ('1.5.0', '1.5.1', '1.6.0', '2.0.0'):
            with self.subTest(version=version):
                self.evidence['plugin_version'] = version
                self.assertEqual(self.errors(), ['Projection publique refusée : Projection publique absente'])

    def test_160_non_liee_refusee(self):
        self.bind_150()
        self.evidence['plugin_version'] = '1.6.0'
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            qualifier.qualification_cases(self.root, self.evidence)
        self.fixture.index['measurement_commit'] = '2' * 40
        self.fixture.link_index()
        with self.assertRaisesRegex(ValueError, '1.6.0 sans commit lié'):
            qualifier.qualification_cases(self.root, self.evidence)
        del self.evidence['review']['linked_sources']
        with self.assertRaisesRegex(ValueError, '1.6.0 sans commit lié'):
            qualifier.qualification_cases(self.root, self.evidence)

    def test_repli_v1_ferme_hors_liste_historique(self):
        for version in ('1.5.0', '1.5.1', '1.6.0', '0.9.0', None):
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, 'sans commit lié'):
                cli.require_cycle_version(None, version)
        for version in sorted(cli.UNBOUND_HISTORICAL_VERSIONS - {'1.4.0'}):
            with self.subTest(version=version):
                cli.require_cycle_version(None, version)

    def test_v4_sans_commit_ou_avec_autre_commit_refuse(self):
        contract = {'campaign_cli': cli._pin(cli.CAMPAIGN_150_CLI, True), 'case_contract_sha256': cli.CYCLE_V4[1]}
        with patch.object(cli, 'MEASUREMENT_150_V4', SYNTHETIC_COMMIT):
            cli.require_cycle_version(contract, '1.5.0', SYNTHETIC_COMMIT)
            for version, commit in (('1.5.0', None), ('1.5.0', '2' * 40), ('1.5.0', cli.MEASUREMENT_140_V4),
                                    ('1.4.0', SYNTHETIC_COMMIT), ('1.3.0', SYNTHETIC_COMMIT), ('1.6.0', SYNTHETIC_COMMIT)):
                with self.subTest(version=version, commit=commit), self.assertRaisesRegex(ValueError, 'v4 réservé'):
                    cli.require_cycle_version(contract, version, commit)
        # H1 : aucune version n'est liée, donc v4 est réservé à la seule 1.4.0 liée.
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            cli.require_cycle_version(contract, '1.5.0', None)

    def test_message_140_sans_commit_lie_inchange(self):
        with self.assertRaisesRegex(ValueError, 'Mesure 1.4.0 sans commit lié au contrat de cycle v3'):
            cli.require_cycle_version(None, '1.4.0')

    def test_campagne_150_sans_v4_refusee_sans_processus(self):
        with patch.object(cases, 'manifest_version', return_value='1.5.0'), \
                patch.object(common.subprocess, 'run') as process, patch.object(runner, 'run_cli') as model:
            with self.assertRaisesRegex(ValueError, 'sans commit lié'):
                cases.campaign_cycle(ROOT, '0' * 40, preparation=True)
            with self.assertRaisesRegex(ValueError, 'sans commit lié'):
                cases.campaign_cycle(ROOT, '0' * 40)
        process.assert_not_called()
        model.assert_not_called()

    def test_campagne_150_v4_prepa_ne_depend_que_du_cycle_prepare(self):
        with patch.object(cases, 'manifest_version', return_value='1.5.0'):
            relative, loaded = cases.campaign_cycle(ROOT, '0' * 40, preparation=True, cycle_v4=True)
        self.assertEqual(relative, V4)
        self.assertEqual(loaded, self.v4)
        for version in ('1.6.0', '1.3.0'):
            with self.subTest(version=version), patch.object(cases, 'manifest_version', return_value=version), \
                    self.assertRaisesRegex(ValueError, 'Contrat de cycle v4 absent ou divergent'):
                cases.campaign_cycle(ROOT, '0' * 40, preparation=True, cycle_v4=True)

    def test_dry_run_cycle_v4_avec_entree_150_alteree_refuse(self):
        altered = [
            lambda entry: entry.update(measurement_commit='1' * 40),
            lambda entry: entry.update(case_contract_sha256='0' * 64),
            lambda entry: entry.update(case_contract_file='scripts/cas-plugin-cycle-v3.json'),
            lambda entry: entry.pop('measurement_commit'),
        ]
        for mutate in altered:
            directory = tempfile.TemporaryDirectory(prefix='racine-dry-run-150-')
            self.addCleanup(directory.cleanup)
            root = Path(directory.name)
            for name in ('.codex-plugin/plugin.json', 'tests/cas-plugin.json', 'upstream.json',
                         'scripts/measurement-cli.json', V4):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_bytes((ROOT / name).read_bytes())
            config = json.loads((root / 'scripts/measurement-cli.json').read_bytes())
            mutate(config['prepared_cycles']['1.5.0-v4'])
            (root / 'scripts/measurement-cli.json').write_text(json.dumps(config), encoding='utf-8')
            argv = ['campagne', '--cycle-v4', '--plugin-commit', '0' * 40, '--output-dir', 'jamais-cree-150', '--dry-run']
            with self.subTest(entree=config['prepared_cycles']['1.5.0-v4']), \
                    patch.object(sys, 'argv', argv), patch.object(runner, 'ROOT', root), \
                    patch.object(runner, 'run_cli') as model, patch.object(runner.subprocess, 'run') as process, \
                    self.assertRaisesRegex(ValueError, 'Contrat de cycle v4 absent ou divergent'):
                runner.main()
            model.assert_not_called()
            process.assert_not_called()

    def test_dry_run_cycle_v4_depot_reel_sans_processus(self):
        stream = io.StringIO()
        argv = ['campagne', '--cycle-v4', '--plugin-commit', '0' * 40, '--output-dir', 'jamais-cree-150', '--dry-run']
        with patch.object(sys, 'argv', argv), patch.object(runner, 'run_cli') as model, \
                patch.object(runner.subprocess, 'run') as process, contextlib.redirect_stdout(stream):
            self.assertEqual(runner.main(), 0)
        model.assert_not_called()
        process.assert_not_called()
        result = json.loads(stream.getvalue())
        self.assertEqual((result['case_contract'], result['case_contract_sha256'], result['sessions']),
                         (V4, cli.CYCLE_V4[1], 18))

    def test_cli_063_presentee_pour_une_mesure_150_refusee(self):
        self.bind_150()
        old = copy.deepcopy(self.config)
        old['campaign_measurements'][SYNTHETIC_COMMIT]['campaign_cli'] = copy.deepcopy(cli.CAMPAIGN_140_CLI)
        (self.root / 'scripts/measurement-cli.json').write_text(json.dumps(old), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Mesure v4 sans contrat CLI/cas épinglé'):
            cli.measurement_contract(self.root, SYNTHETIC_COMMIT)
        self.assertTrue(any('Mesure v4 sans contrat CLI/cas' in e or 'Verrous CLI' in e or 'Toolchains' in e
                            for e in self.errors()))

    def test_recus_et_verrous_063_refuses_pour_une_mesure_150(self):
        self.bind_150()
        pins = cli.toolchains(self.root, SYNTHETIC_COMMIT)
        old = cli._pin(cli.CAMPAIGN_140_CLI, True)
        for phase in ('campaign_cli', 'smoke_cli'):
            origin = {'cli_version': old['version'], 'cli_sha256': old['sha256'],
                      'cli_phase': phase, 'cli_toolchain': old}
            with self.subTest(phase=phase):
                self.assertFalse(cli.receipt_matches(origin, phase, pins[phase]))
        for key in ('campaign_cli', 'smoke_cli'):
            with self.subTest(verrou=key):
                self.evidence[key] = old
                self.assertTrue(any('Verrous CLI différents' in e for e in self.errors()))
                self.evidence[key] = pins[key]


if __name__ == '__main__':
    unittest.main()
