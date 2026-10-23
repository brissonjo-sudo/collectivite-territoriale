"""Contre-épreuves synthétiques L33 ; aucun appel modèle ni qualification réelle."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cli_toolchains as cli
import measurement_common as common
import qualify_distribution as qualifier
import public_projection as public
import test_distribution_qualification as historical
from support_distribution_contract import closed_transition_root, complete_synthetic_contract


class QualificationCycleTests(unittest.TestCase):
    def setUp(self) -> None:
        # Socle historique positif, étendu par des projections explicitement factices.
        self.fixture = historical.DistributionQualificationTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.root, self.evidence = self.fixture.root, self.fixture.evidence
        self.evidence['fixture'] = True
        # B3 réserve v2 à 1.3.0 ; la fixture conserve l'API publique complète.
        self.evidence['plugin_version'] = '1.3.0'
        manifest = qualifier.load(self.root, '.codex-plugin/plugin.json')
        manifest['version'] = '1.3.0'
        (self.root / '.codex-plugin/plugin.json').write_text(json.dumps(manifest), encoding='utf-8')
        self.cases = json.loads((ROOT / 'tests/cas-plugin.json').read_bytes())
        self.cycle = json.loads((ROOT / 'scripts/cas-plugin-cycle-v2.json').read_bytes())
        (self.root / 'tests/cas-plugin.json').write_bytes((ROOT / 'tests/cas-plugin.json').read_bytes())
        (self.root / 'scripts/measurement-cli.json').write_bytes((ROOT / 'scripts/measurement-cli.json').read_bytes())
        directory = self.root / 'tests/evidence/fixture-l33'
        directory.mkdir()
        self.index_path = directory / 'index.json'
        self.contract_path = directory / 'cycle.json'
        self.contract_path.write_bytes((ROOT / 'scripts/cas-plugin-cycle-v2.json').read_bytes())
        self.index = {'fixture': True, 'schema': 'ct-human-linked-v1',
                      'measurement_commit': cli.MEASUREMENT_D,
                      'case_contract': common.binding(self.contract_path, directory)}
        self.link_index()
        self.project(self.cycle)
        # Projection locale réelle d'une pièce synthétique, sans accès externe.
        pieces = self.root / public.PIECES
        pieces.mkdir(parents=True)
        (pieces / 'cycle-fixture.json').write_bytes(self.contract_path.read_bytes())
        relative = 'tests/evidence/release-fixture.json'
        public.write_json(self.root / relative, self.evidence)
        destination = self.root.parent / 'projection-synthetique-l33'
        release = public.publish(self.root, destination, relative)
        index_relative = self.index_path.relative_to(self.root)
        self.root = self.fixture.root = destination
        self.evidence = self.fixture.evidence = json.loads(release.read_bytes())
        self.index_path = destination / index_relative
        self.contract_path = self.index_path.parent / 'cycle.json'

    def link_index(self) -> None:
        self.index_path.write_text(json.dumps(self.index), encoding='utf-8')
        self.evidence['review']['linked_sources'] = common.binding(self.index_path, self.root)

    def project(self, cases: list[dict]) -> None:
        """Construit uniquement une fixture de la propriété de sélection des scénarios."""
        native = qualifier.load(self.root, self.evidence['distribution']['proofs']['native_campaign']['evidence_path'])
        reviews = qualifier.load(self.root, self.evidence['distribution']['proofs']['assistant_review']['evidence_path'])
        response = qualifier.load(self.root, native['runs'][0]['evidence_path'])
        review = qualifier.load(self.root, reviews['runs'][0]['evidence_path'])
        native_template, review_template = native['runs'][0], reviews['runs'][0]
        recorded_template = self.evidence['runs'][0]
        native['runs'], reviews['runs'], self.evidence['runs'] = [], [], []
        for case in cases:
            name = case['id']
            value = {**copy.deepcopy(response), 'fixture': True, 'case_id': name,
                     'case_sha256': common.digest(json.dumps(case, sort_keys=True, ensure_ascii=False).encode())}
            path = self.root / f'tests/evidence/fixture-l33/{name}.json'
            path.write_text(json.dumps(value), encoding='utf-8')
            relative = path.relative_to(self.root).as_posix()
            native['runs'].append({**native_template, 'case_id': name, 'evidence_path': relative,
                                   'evidence_sha256': common.fingerprint(path)})
            self.evidence['runs'].append({**recorded_template, 'case_id': name, 'evidence_path': relative})
            value = {**copy.deepcopy(review), 'fixture': True, 'evidence_sha256': common.fingerprint(path),
                     'report': {'invariants': [{'invariant': item, 'statut': 'respecte',
                                               'motif': 'Fixture synthétique L33.'} for item in case['invariants']]}}
            path = path.with_name(name + '-review.json')
            path.write_text(json.dumps(value), encoding='utf-8')
            reviews['runs'].append({**review_template, 'case_id': name,
                                    'evidence_path': path.relative_to(self.root).as_posix(),
                                    'evidence_sha256': common.fingerprint(path)})
        native['case_count'] = native['technical_passed_count'] = len(cases)
        self.fixture.write_proof('native_campaign', native)
        self.fixture.write_proof('assistant_review', reviews)
        commit = self.index.get('measurement_commit') if 'linked_sources' in self.evidence['review'] else None
        complete_synthetic_contract(self.fixture, ROOT, commit)
        # Le manifeste synthétique 1.3.0 est bien celui installé dans le smoke.
        smoke = qualifier.load(self.root, self.evidence['codex_smoke']['evidence_path'])
        smoke['plugin_configuration_sha256'] = common.snapshot(self.root)['plugin_configuration_sha256']
        self.fixture.write_proof('codex_smoke', smoke)

    def test_projection_d_liee_au_contrat_v2_exact_passe(self) -> None:
        self.assertEqual(qualifier.distribution_errors(self.root, self.evidence), [])

    def test_meme_projection_v2_contre_v1_refusee(self) -> None:
        del self.evidence['review']['linked_sources']
        # Un champ déclaré par la preuve ne remplace jamais le lien vers le commit.
        self.evidence['measurement_commit'] = cli.MEASUREMENT_D
        # Isole le choix des cas : reçus CLI factices conformes au contexte sans lien.
        complete_synthetic_contract(self.fixture, ROOT)
        errors = qualifier.distribution_errors(self.root, self.evidence)
        self.assertEqual(set(errors), {'Scénario modifié : ' + name for name in (
            'plugin-garde-fou-apja', 'plugin-dcp-egalite', 'plugin-dcp-acte-irreversible')})

    def test_v2_altere_refuse_meme_apres_recalcul_du_lien(self) -> None:
        self.contract_path.write_bytes(self.contract_path.read_bytes() + b'\n')
        self.index['case_contract'] = common.binding(self.contract_path, self.index_path.parent)
        self.link_index()
        errors = qualifier.distribution_errors(self.root, self.evidence)
        self.assertTrue(any('Contrat de cycle v2 absent ou divergent' in error for error in errors))

    def test_v2_altere_refuse_sans_recalcul_du_lien(self) -> None:
        self.contract_path.write_bytes(self.contract_path.read_bytes() + b'\n')
        errors = qualifier.distribution_errors(self.root, self.evidence)
        self.assertTrue(any('Preuve liée altérée' in error for error in errors))

    def test_index_altere_refuse_sans_repli_v1(self) -> None:
        self.index_path.write_bytes(self.index_path.read_bytes() + b'\n')
        errors = qualifier.distribution_errors(self.root, self.evidence)
        self.assertTrue(any('Preuve liée altérée' in error for error in errors))

    def test_contrat_manquant_pour_d_refuse_sans_repli(self) -> None:
        self.index.pop('case_contract')
        self.link_index()
        errors = qualifier.distribution_errors(self.root, self.evidence)
        self.assertTrue(any('Contrat de cycle v2 absent ou divergent' in error for error in errors))

    def test_preuve_non_liee_conserve_v1_meme_si_elle_declare_d(self) -> None:
        del self.evidence['review']['linked_sources']
        self.evidence['measurement_commit'] = cli.MEASUREMENT_D
        self.project(self.cases)
        self.assertEqual(qualifier.distribution_errors(self.root, self.evidence), [])

    def test_index_lie_a_un_autre_commit_conserve_v1(self) -> None:
        self.index['measurement_commit'] = self.evidence['plugin_commit']
        self.link_index()
        self.project(self.cases)
        self.assertEqual(qualifier.distribution_errors(self.root, self.evidence), [])


class QualificationTransitionTests(unittest.TestCase):
    def test_transition_qualificateur_exacte_et_derive_refusee(self) -> None:
        # La transition est fermée sur la tête 1.3.0 mesurée, jamais sur le code B1.
        root = closed_transition_root(self, ROOT)
        transition = json.loads((root / cli.TRANSITION_D).read_bytes())
        old = {'plugin_commit': cli.MEASUREMENT_D,
               'toolchain_sha256': dict(transition['source_files_sha256'])}
        current = {'toolchain_sha256': {p.relative_to(root).as_posix(): common.fingerprint(p)
                                      for p in (root / 'scripts').iterdir() if p.suffix in {'.py', '.json'}}}
        self.assertIn('scripts/qualify_distribution.py', cli.compatibility_files(root, old, current))
        current['toolchain_sha256']['scripts/qualify_distribution.py'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'transition d refusée'):
            cli.compatibility_files(root, old, current)


if __name__ == '__main__':
    unittest.main()
