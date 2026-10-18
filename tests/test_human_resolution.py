"""Résolution humaine liée, sur fixtures explicites et pièces réelles inchangées ; aucun modèle."""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import assemble_release_evidence as assembly
import human_resolution as human
import measurement_common as common
import qualify_distribution as qualifier

BUNDLE = ROOT / 'tests/evidence/2026-10-18-candidat-1-3-0'
SOURCE = '08f92936dd0ae09775a2d2293bae315cdf20847d'


class HumanRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.report = {'invariants': [{'invariant': 'constat synthétique sans droit', 'statut': 'non_verifiable', 'motif': 'fixture'}]}
        self.opinion = {'fixture': True, 'decideur': 'Jo', 'date_utc': '2026-10-18T18:40:53+00:00',
                        'plugin_commit': SOURCE, 'campagne': 'campagne-l14-20261018-a',
                        'resume_campagne_sha256': '1' * 64, 'cas_valides': {'cas-factice': 'conforme'}}
        self.binding = {'summary_sha256': '1' * 64, 'response_session': {'sha256': '2' * 64},
                        'review_session': {'sha256': '3' * 64}, 'human_opinion': {'sha256': '4' * 64}}
        self.expected = {'measurement_commit': SOURCE, 'campaign_attempt_id': 'campagne-l14-20261018-a',
                         'summary_sha256': '1' * 64, 'response_session_sha256': '2' * 64,
                         'review_session_sha256': '3' * 64}

    def resolve(self, failures: list[str] | None = None) -> dict:
        return human.resolve_case('cas-factice', self.report, failures or [], self.opinion, self.binding, self.expected)

    def test_resolution_liee_valide_sans_mutation_automatique(self) -> None:
        original = copy.deepcopy(self.report)
        value = self.resolve()
        self.assertTrue(all(value['invariants'].values()))
        self.assertEqual(value['resolutions'][0]['effective_status'], 'respecte_par_avis_humain')
        self.assertEqual(self.report, original)

    def test_autre_decideur_refuse(self) -> None:
        self.opinion['decideur'] = 'autre'
        with self.assertRaisesRegex(ValueError, 'Décideur'):
            self.resolve()

    def test_autre_empreinte_run_refusee(self) -> None:
        self.binding['response_session']['sha256'] = '5' * 64
        with self.assertRaisesRegex(ValueError, 'autre run'):
            self.resolve()

    def test_autre_commit_refuse(self) -> None:
        self.opinion['plugin_commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'autre run, commit'):
            self.resolve()

    def test_autre_campagne_refusee(self) -> None:
        self.opinion['campagne'] = 'autre-campagne'
        with self.assertRaisesRegex(ValueError, 'campagne'):
            self.resolve()

    def test_autre_resume_refuse(self) -> None:
        self.opinion['resume_campagne_sha256'] = '6' * 64
        with self.assertRaisesRegex(ValueError, 'campagne'):
            self.resolve()

    def test_avis_non_date_ou_sans_fuseau_refuse(self) -> None:
        for value in (None, '2026-10-18'):
            self.opinion['date_utc'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'non daté'):
                self.resolve()

    def test_violation_avec_avis_conforme_toujours_refusee(self) -> None:
        self.report['invariants'][0]['statut'] = 'violation'
        with self.assertRaisesRegex(ValueError, 'Violation non résoluble'):
            self.resolve()

    def test_echec_technique_avec_avis_toujours_refuse(self) -> None:
        with self.assertRaisesRegex(ValueError, 'Échec technique'):
            self.resolve(['unexpected_command'])

    def test_reserve_ne_resout_pas_non_verifiable(self) -> None:
        self.opinion['cas_valides']['cas-factice'] = 'reserve'
        self.opinion['reserves'] = {'cas-factice': 'Réserve synthétique'}
        with self.assertRaisesRegex(ValueError, 'sans avis conforme'):
            self.resolve()

    def test_reserve_preservee_sur_un_constat_deja_respecte(self) -> None:
        self.report['invariants'][0]['statut'] = 'respecte'
        self.opinion['cas_valides']['cas-factice'] = 'reserve'
        self.opinion['reserves'] = {'cas-factice': 'Réserve synthétique à conserver'}
        value = self.resolve()
        case = {'id': 'cas-factice', 'activation_sequence': [], 'mcp_mode': 'disabled',
                'invariants': ['constat synthétique sans droit']}
        run = assembly.qualified_run(case, {'events': []}, SOURCE, 'fixture.json', value, SOURCE)
        self.assertEqual(run['human_reservation'], 'Réserve synthétique à conserver')
        self.assertEqual(run['human_verdict'], 'reserve')
        linked = {'human': {'human_legal_validation': True, 'reservations': {'cas-factice': value['reservation']}}}
        evidence = {'fixture': True, 'review': assembly.human_review_fields(linked, {'sha256': '7' * 64})}
        self.assertEqual(evidence['review']['reservations']['cas-factice'], value['reservation'])
        self.assertNotIn('linked_sources', linked['human'])
        self.assertTrue(qualifier.distribution_errors(ROOT, evidence))


class HumanBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = {'plugin_commit': SOURCE, **common.snapshot(ROOT)}

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix='L15-humain-fixtures-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_bundle_reel_quatre_resolutions_et_reserve_sans_release(self) -> None:
        value = human.load_bundle(ROOT, BUNDLE, self.baseline)
        self.assertEqual(len(value['runs']), 18)
        self.assertEqual(sum(len(r['resolutions']) for r in value['resolutions'].values()), 4)
        self.assertEqual(set(n for n, r in value['resolutions'].items() if r['resolutions']),
            {'plugin-violation-donnees', 'plugin-dcp-frontiere-dsi-externe', 'l8-dsi-donnees-sans-source'})
        self.assertEqual(set(value['human']['reservations']), {'plugin-prime-depart-retraite'})
        opinion = json.loads((BUNDLE / 'avis-humain-jo-20261018-quinze.json').read_bytes())
        self.assertEqual(value['human']['reservations'], opinion['reserves'])
        self.assertTrue(value['human']['human_legal_validation'])
        self.assertFalse((ROOT / 'tests/evidence/release-1.3.0.json').exists())

    def copied(self) -> Path:
        destination = self.root / 'bundle-public-fixture'
        shutil.copytree(BUNDLE, destination)
        return destination

    def test_avis_ou_trace_alteres_refuses(self) -> None:
        bundle = self.copied()
        (bundle / 'avis-humain-jo-20261018.json').write_bytes((bundle / 'avis-humain-jo-20261018.json').read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'Preuve liée altérée'):
            human.load_bundle(ROOT, bundle, self.baseline)

    def test_runtime_cible_different_refuse(self) -> None:
        target = copy.deepcopy(self.baseline)
        target['runtime_sha256']['skills/dsi-fpt/SKILL.md'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Runtime, configuration ou cas'):
            human.load_bundle(ROOT, BUNDLE, target)

    def test_protocole_cible_different_refuse(self) -> None:
        target = copy.deepcopy(self.baseline)
        target['toolchain_sha256']['scripts/run_codex_campaign.py'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Protocole ou outillage'):
            human.load_bundle(ROOT, BUNDLE, target)

    def test_aucune_ecriture_d_assemblage_sans_smoke(self) -> None:
        output = self.root / 'aucune-preuve'
        with patch.object(assembly, 'candidate', return_value=self.baseline):
            with self.assertRaises(FileNotFoundError):
                assembly.assemble(ROOT, SOURCE, BUNDLE / 'campagne', self.root / 'smoke-absent.json',
                    ROOT / 'tests/evidence/2026-10-08-candidat-013/dcp-autonome.json',
                    BUNDLE / 'campagne', output, BUNDLE)
        self.assertFalse(output.exists())
        self.assertEqual(qualifier.current_distribution_errors(ROOT), ['Preuve courante absente : release-1.3.0.json'])

    def test_fiche_humaine_ou_lien_run_absents_refuses(self) -> None:
        bundle = self.copied()
        (bundle / 'FICHE-RELECTURE-17.md').unlink()
        with self.assertRaises((OSError, ValueError)):
            human.load_bundle(ROOT, bundle, self.baseline)

    def replace_piece(self, bundle: Path, relative: str, value: dict) -> None:
        path = bundle / relative
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        index_path = bundle / 'liaisons-humaines.json'
        index = json.loads(index_path.read_bytes())
        index['files'][relative] = {'sha256': common.fingerprint(path), 'octets': path.stat().st_size}
        for binding in index['cases'].values():
            for item in binding.values():
                if isinstance(item, dict) and item.get('evidence_path') == relative:
                    item['sha256'] = common.fingerprint(path)
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

    def test_session_synthetique_refusee_meme_avec_avis_et_index_relies(self) -> None:
        bundle = self.copied()
        relative = 'campagne/plugin-prime-depart-retraite/reponse/session.json'
        value = json.loads((bundle / relative).read_bytes())
        value.pop('payload_sha256')
        value['origin']['synthetic'] = True
        self.replace_piece(bundle, relative, common.seal(value))
        with self.assertRaisesRegex(ValueError, 'Pièce synthétique'):
            human.load_bundle(ROOT, bundle, self.baseline)

    def test_decideur_substitue_refuse_meme_apres_recalcul_index(self) -> None:
        bundle = self.copied()
        relative = 'avis-humain-jo-20261018.json'
        value = json.loads((bundle / relative).read_bytes())
        value['decideur'] = 'autre'
        self.replace_piece(bundle, relative, value)
        with self.assertRaisesRegex(ValueError, 'Décideur humain différent'):
            human.load_bundle(ROOT, bundle, self.baseline)

    def test_validation_globale_ne_peut_pas_etre_inventee(self) -> None:
        bundle = self.copied()
        relative = 'avis-humain-jo-20261018-quinze.json'
        value = json.loads((bundle / relative).read_bytes())
        value['human_legal_validation_globale'] = False
        self.replace_piece(bundle, relative, value)
        with self.assertRaisesRegex(ValueError, 'Décision humaine globale absente'):
            human.load_bundle(ROOT, bundle, self.baseline)


if __name__ == '__main__':
    unittest.main()
