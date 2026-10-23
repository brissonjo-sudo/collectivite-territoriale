"""B3 : contrats fermés et preuves synthétiques, sans processus modèle."""
from pathlib import Path
import contextlib
import copy
import io
import json
import shutil
import sys
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
from support_distribution_contract import refresh_smoke_snapshot

V4 = 'scripts/cas-plugin-cycle-v4.json'
# Identité explicitement factice, autorisée uniquement par patch dans ces tests.
SYNTHETIC_COMMIT = '1' * 40


class CycleV4Tests(unittest.TestCase):
    def setUp(self):
        self.fixture = v2.QualificationCycleTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.root, self.evidence = self.fixture.root, self.fixture.evidence
        self.v4 = json.loads((ROOT / V4).read_bytes())

    def bind_v4(self):
        self.evidence['plugin_version'] = '1.4.0'
        manifest = qualifier.load(self.root, '.codex-plugin/plugin.json')
        manifest['version'] = '1.4.0'
        (self.root / '.codex-plugin/plugin.json').write_text(json.dumps(manifest), encoding='utf-8')
        for name in (V4, cases.CYCLE_CASES_FILE):
            (self.root / name).write_bytes((ROOT / name).read_bytes())
        # Le socle 1.2.0 précède DSI ; le contrat validé couvre les sept rôles.
        upstream = qualifier.load(self.root, 'upstream.json')
        upstream['skills']['dsi-fpt'] = qualifier.load(ROOT, 'upstream.json')['skills']['dsi-fpt']
        shutil.copytree(ROOT / 'skills/dsi-fpt', self.root / 'skills/dsi-fpt')
        (self.root / 'upstream.json').write_text(json.dumps(upstream), encoding='utf-8')
        self.evidence['upstream_commits'] = {name: item['commit'] for name, item in upstream['skills'].items()}
        # Le modèle de preuve synthétique porte le runtime complet des sept rôles.
        native = qualifier.load(self.root, self.evidence['native_campaign']['evidence_path'])
        response_path = self.root / native['runs'][0]['evidence_path']
        response = json.loads(response_path.read_bytes())
        response['runtime_sha256'] = common.snapshot(self.root)['runtime_sha256']
        response_path.write_text(json.dumps(response), encoding='utf-8')
        # Produit les reçus synthétiques avec le verrou complet de d.
        self.fixture.project(self.v4)
        config = qualifier.load(self.root, 'scripts/measurement-cli.json')
        config['prepared_cycles']['1.4.0-v4']['measurement_commit'] = SYNTHETIC_COMMIT
        config['campaign_measurements'][SYNTHETIC_COMMIT] = {
            'campaign_cli': config['campaign_measurements'][cli.MEASUREMENT_D]['campaign_cli'],
            'case_contract_sha256': cli.CYCLE_V4[1]}
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
        binding = patch.object(cli, 'MEASUREMENT_140_V4', SYNTHETIC_COMMIT)
        self.addCleanup(binding.stop)
        binding.start()

    def test_preuve_v3_liee_passe_en_vue_CI_et_lecteur_assembleur(self):
        self.bind_v4()
        self.assertEqual(qualifier.distribution_errors(self.root, self.evidence), [])
        expected = {c['id']: c for c in self.v4}
        self.assertEqual(assembly.measurement_cases(self.root, SYNTHETIC_COMMIT), expected)
        self.assertEqual(human.bundle_cases(self.root, self.fixture.index_path.parent, self.fixture.index), expected)

    def test_v3_altere_refuse_meme_lien_recalcule(self):
        self.bind_v4()
        self.fixture.contract_path.write_bytes(self.fixture.contract_path.read_bytes() + b'\n')
        self.fixture.index['case_contract'] = common.binding(self.fixture.contract_path, self.fixture.index_path.parent)
        self.fixture.link_index()
        self.assertTrue(any('Contrat de cycle v4 absent ou divergent' in e
                            for e in qualifier.distribution_errors(self.root, self.evidence)))
        with self.assertRaisesRegex(ValueError, 'Contrat de cycle v4'):
            human.bundle_cases(self.root, self.fixture.index_path.parent, self.fixture.index)

    def test_fichier_v3_local_altere_refuse(self):
        self.bind_v4()
        (self.root / V4).write_bytes((self.root / V4).read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'Contrat de cycle v4'):
            assembly.measurement_cases(self.root, SYNTHETIC_COMMIT)

    def test_v2_pour_mesure_140_refuse_sans_repli(self):
        self.bind_v4()
        self.fixture.contract_path.write_bytes((ROOT / cases.CYCLE_CASES_FILE).read_bytes())
        self.fixture.index['case_contract'] = common.binding(self.fixture.contract_path, self.fixture.index_path.parent)
        self.fixture.link_index()
        self.assertTrue(any('Contrat de cycle v4 absent ou divergent' in e
                            for e in qualifier.distribution_errors(self.root, self.evidence)))
        with self.assertRaisesRegex(ValueError, '1.4.0 sans commit lié'):
            assembly.measurement_cases(self.root, cli.MEASUREMENT_D)

    def test_commit_v2_lie_refuse_pour_140(self):
        self.bind_v4()
        self.fixture.index['measurement_commit'] = cli.MEASUREMENT_D
        self.fixture.link_index()
        self.assertTrue(any('1.4.0 sans commit lié' in e
                            for e in qualifier.distribution_errors(self.root, self.evidence)))

    def test_v3_refuse_pour_130(self):
        self.bind_v4()
        self.evidence['plugin_version'] = '1.3.0'
        with self.assertRaisesRegex(ValueError, 'v4 réservé'):
            qualifier.qualification_cases(self.root, self.evidence)

    def test_v2_reserve_a_130(self):
        self.evidence['plugin_version'] = '1.2.0'
        with self.assertRaisesRegex(ValueError, 'v2 réservé'):
            qualifier.qualification_cases(self.root, self.evidence)

    def test_commit_inconnu_et_champ_de_preuve_ne_selectionnent_pas_v3(self):
        self.bind_v4()
        self.fixture.index['measurement_commit'] = '2' * 40
        self.evidence['measurement_commit'] = SYNTHETIC_COMMIT
        self.fixture.link_index()
        self.assertTrue(any('1.4.0 sans commit lié' in e
                            for e in qualifier.distribution_errors(self.root, self.evidence)))

    def test_ajout_au_registre_seul_n_autorise_pas_commit(self):
        self.bind_v4()
        with patch.object(cli, 'MEASUREMENT_140_V4', None):
            self.assertIsNone(cli.measurement_contract(self.root, SYNTHETIC_COMMIT))
            with self.assertRaisesRegex(ValueError, '1.4.0 sans commit lié'):
                assembly.measurement_cases(self.root, SYNTHETIC_COMMIT)

    def test_campagne_130_conserve_v2_par_commit_d(self):
        relative, value = cases.campaign_cycle(ROOT, cli.MEASUREMENT_D, preparation=True)
        self.assertEqual(relative, cases.CYCLE_CASES_FILE)
        self.assertEqual(value, json.loads((ROOT / relative).read_bytes()))

    def test_projection_absente_refusee_pour_140(self):
        self.bind_v4()
        del self.evidence['public_projection']
        self.assertEqual(qualifier.distribution_errors(self.root, self.evidence),
                         ['Projection publique refusée : Projection publique absente'])
