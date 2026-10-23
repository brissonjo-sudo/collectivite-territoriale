"""B1 : contrats synthétiques de distribution ; aucun modèle ni preuve de release."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cli_toolchains as cli
import measurement_common as common
import public_projection as public
import qualify_distribution as qualifier
import test_distribution_qualification as historical
from support_distribution_contract import closed_transition_root, refresh_smoke_snapshot


class DistributionSmokeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = historical.DistributionQualificationTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.root, self.evidence = self.fixture.root, self.fixture.evidence
        self.native = qualifier.load(self.root, self.evidence['native_campaign']['evidence_path'])
        self.reviews = qualifier.load(self.root, self.evidence['distribution']['proofs']['assistant_review']['evidence_path'])
        self.smoke = qualifier.load(self.root, self.evidence['codex_smoke']['evidence_path'])

    def errors(self) -> list[str]:
        self.fixture.write_proof('codex_smoke', self.smoke)
        return qualifier.distribution_errors(self.root, self.evidence)

    def test_contrat_conforme_accepte(self) -> None:
        self.assertEqual(self.errors(), [])
        self.assertIs(self.evidence['release_evidence'], False)

    def test_case_file_sha256_divergent_refuse(self) -> None:
        self.smoke['case_file_sha256'] = '0' * 64
        self.assertIn('Empreinte différente du smoke : case_file_sha256', self.errors())

    def test_upstream_sha256_divergent_refuse(self) -> None:
        self.smoke['upstream_sha256'] = '0' * 64
        self.assertIn('Empreinte différente du smoke : upstream_sha256', self.errors())

    def test_toolchain_sha256_divergent_refuse(self) -> None:
        self.smoke['toolchain_sha256']['scripts/run_codex_campaign.py'] = '0' * 64
        self.assertIn('Protocole ou outillage du smoke différent', self.errors())

    def test_inventaire_ajoute_ou_incomplet_refuse(self) -> None:
        original = copy.deepcopy(self.smoke['toolchain_sha256'])
        for mutation in ('ajout', 'retrait'):
            self.smoke['toolchain_sha256'] = copy.deepcopy(original)
            if mutation == 'ajout':
                self.smoke['toolchain_sha256']['scripts/factice.py'] = '0' * 64
            else:
                del self.smoke['toolchain_sha256']['scripts/run_codex_campaign.py']
            with self.subTest(mutation=mutation):
                self.assertIn('Protocole ou outillage du smoke différent', self.errors())

    def test_nouveaux_champs_absents_refuses(self) -> None:
        original = copy.deepcopy(self.smoke)
        for key in ('case_file_sha256', 'upstream_sha256', 'toolchain_sha256', 'smoke_cli'):
            self.smoke = copy.deepcopy(original)
            del self.smoke[key]
            with self.subTest(key=key):
                self.assertTrue(self.errors())

    def test_verrou_smoke_cli_divergent_refuse(self) -> None:
        self.smoke['smoke_cli']['sha256'] = '0' * 64
        self.assertTrue(any('Toolchains de distribution refusées' in error for error in self.errors()))

    def test_verrou_smoke_cli_compagnon_divergent_refuse(self) -> None:
        self.smoke['smoke_cli']['companions_sha256']['codex-command-runner.exe'] = '0' * 64
        self.assertTrue(any('Toolchains de distribution refusées' in error for error in self.errors()))

    def test_declaration_CLI_release_divergente_refusee(self) -> None:
        self.evidence['smoke_cli']['sha256'] = '0' * 64
        self.assertTrue(any('Toolchains de distribution refusées' in error for error in self.errors()))

    def test_recu_smoke_autre_phase_refuse_meme_lien_recalcule(self) -> None:
        directory = (self.root / self.evidence['codex_smoke']['evidence_path']).parent
        run = self.smoke['runs'][0]
        path = directory / run['proof']['evidence_path']
        value = json.loads(path.read_bytes())
        value['origin']['cli_phase'] = 'campaign_cli'
        path.write_text(json.dumps(value), encoding='utf-8')
        run['proof'] = common.binding(path, directory)
        self.assertTrue(any('Reçu CLI différent de sa phase : smoke_cli' in error for error in self.errors()))

    def test_recu_smoke_altere_refuse(self) -> None:
        directory = (self.root / self.evidence['codex_smoke']['evidence_path']).parent
        path = directory / self.smoke['runs'][0]['proof']['evidence_path']
        path.write_bytes(path.read_bytes() + b'\n')
        self.assertTrue(any('Preuve liée altérée' in error for error in self.errors()))

    def test_vue_CI_expose_scripts_et_resout_empreinte_source(self) -> None:
        directory = (self.root / self.evidence['codex_smoke']['evidence_path']).parent
        path = directory / self.smoke['runs'][0]['proof']['evidence_path']
        original = path.read_bytes()
        path.write_bytes(original + b'\n')  # Projection factice, distincte de l'original lié.
        name = path.relative_to(self.root).as_posix()
        view = public.ProjectionView(self.root, {name: {
            'projection_sha256': common.fingerprint(path), 'original_sha256': common.digest(original)}})
        self.assertEqual(view.fingerprint(self.root / 'scripts/smoke-cli.json'),
                         common.fingerprint(self.root / 'scripts/smoke-cli.json'))
        self.assertEqual(qualifier._distribution_errors(self.root, self.evidence, view), [])

    def test_transition_fermee_existante_acceptee_et_derive_refusee(self) -> None:
        closed = closed_transition_root(self, ROOT)
        shutil.copytree(closed / 'scripts', self.root / 'scripts', dirs_exist_ok=True)
        for name in ('CHANGELOG.md', '.gitattributes', '.git'):
            shutil.copyfile(closed / name, self.root / name)
        refresh_smoke_snapshot(self.fixture)
        self.smoke = qualifier.load(self.root, self.evidence['codex_smoke']['evidence_path'])
        transition = json.loads((closed / cli.TRANSITION_D).read_bytes())
        self.smoke['plugin_commit'] = cli.MEASUREMENT_D
        self.smoke['toolchain_sha256'].update(transition['source_files_sha256'])
        self.smoke['toolchain_sha256'].pop(cli.TRANSITION_D)
        self.assertEqual(qualifier.smoke_contract_errors(
            self.root, self.evidence, self.native, self.reviews, self.smoke), [])
        self.smoke['toolchain_sha256']['scripts/qualify_distribution.py'] = '0' * 64
        self.assertTrue(any('transition d refusée' in error for error in qualifier.smoke_contract_errors(
            self.root, self.evidence, self.native, self.reviews, self.smoke)))

    def test_ecart_qualificateur_sans_transition_refuse(self) -> None:
        self.smoke['toolchain_sha256']['scripts/qualify_distribution.py'] = '0' * 64
        self.assertIn('Protocole ou outillage du smoke différent', self.errors())


if __name__ == '__main__':
    unittest.main()
