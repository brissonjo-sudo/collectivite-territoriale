"""B12b : commande et prompt hors CLI ; chemin v4 et sources satisfaisables."""
from pathlib import Path
import copy
import json
import sys
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import campaign_contract as contract
import run_codex_campaign as campaign
from skill_citation import forbidden_skill_path


class CycleV4SourceTests(unittest.TestCase):
    def setUp(self):
        self.cases = contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json')

    def test_seuls_les_trois_cas_autorises_changent(self):
        old = json.loads((ROOT / 'scripts/cas-plugin-cycle-v3.json').read_bytes())
        changed = {a['id'] for a, b in zip(old, self.cases) if a != b}
        self.assertEqual(changed, {'plugin-prime-depart-retraite', *contract.V4_PATH_CASES})
        for a, b in zip(old, self.cases):
            self.assertEqual(b['invariants'][:len(a['invariants'])], a['invariants'])
            self.assertEqual(b['mcp_mode'], a['mcp_mode'])

    def test_commande_et_prompt_retraite_sans_cli(self):
        case = self.cases[0]
        with patch.object(campaign.subprocess, 'run', side_effect=AssertionError('Aucun processus')):
            argv = campaign.command(case, 'CLI-jamais-lancee', 'modele-jamais-appele')
            prompt = campaign.prompt(case)
        self.assertIn('web_search="live"', argv)
        self.assertIn(case['official_source_instruction'], prompt)
        self.assertIn('Seul www.senat.fr est autorisé', prompt)
        self.assertNotIn('articles 33 et 34 du RGPD', prompt)
        self.assertNotIn('eur-lex.europa.eu', prompt)

    def test_prompt_rgpd_et_liste_fermee_restent_exacts(self):
        case = next(c for c in self.cases if c['id'] == 'plugin-violation-donnees')
        self.assertEqual(case['official_source_hosts'], ['eur-lex.europa.eu', 'www.cnil.fr'])
        prompt = campaign.prompt(case)
        self.assertIn('Vérifie les articles 33 et 34 du RGPD en ouvrant EUR-Lex ou la CNIL ; ne présume aucun délai si la récupération échoue. Seuls eur-lex.europa.eu et www.cnil.fr sont autorisés pour le web.', prompt)
        self.assertNotIn('Seul www.senat.fr est autorisé', prompt)

    def test_chemins_refuses_et_citations_nom_section_permises(self):
        for text in ['[DCP](C:/local/dcp-fpt/SKILL.md)', '[réf](references/branche.md)', '.agents/skills/dsi-fpt/SKILL.md', 'dcp-fpt/references/sources.md', r'C:\local\dcp-fpt\SKILL.md']:
            with self.subTest(text=text): self.assertTrue(forbidden_skill_path(text))
        for text in ['dcp-fpt, §5.5', '[source](https://www.senat.fr/questions/base/2024/qSEQ241001222.html)', 'dsi-fpt, section Sécurité']:
            self.assertFalse(forbidden_skill_path(text))

    def test_controle_ajoute_aux_deux_cas_v4_seulement(self):
        for case in self.cases:
            clean = [{'type': 'reply', 'text': '[entrée](dcp-fpt/SKILL.md)'}, {'type': 'turn_completed'}]
            errors = campaign.failures(clean, case, 0)
            self.assertEqual('skill_path_in_response' in errors, case['id'] in contract.V4_PATH_CASES)

    def test_source_senat_impossible_sans_web_refusee(self):
        bad = copy.deepcopy(self.cases)
        bad[0]['web_mode'] = 'disabled'
        # La sélection à empreinte fermée refuse cet état avant toute campagne.
        self.assertNotEqual(bad, contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json'))


class SatisfiabilityV4Tests(unittest.TestCase):
    def test_tous_les_invariants_des_18_cas_examines(self):
        from cycle_satisfiability import assess
        cases = contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json')
        results = assess(ROOT, cases)
        self.assertEqual(len(results), 18)
        self.assertTrue(all(r['satisfaisable'] for r in results))
        self.assertEqual(sum(len(r['invariants']) for r in results), sum(len(c['invariants']) for c in cases))

    def test_mcp_seul_ne_satisfait_pas_la_RM_senat(self):
        from cycle_satisfiability import assess
        cases = contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json')
        cases[0]['web_mode'] = 'disabled'
        results = assess(ROOT, cases)
        self.assertFalse(results[0]['satisfaisable'])
        self.assertFalse(results[0]['invariants'][7]['satisfaisable'])

    def test_invariant_non_examine_refuse(self):
        from cycle_satisfiability import assess
        cases = contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json')
        cases[1]['invariants'].append('invariant non examiné')
        with self.assertRaisesRegex(ValueError, 'non examiné'):
            assess(ROOT, cases)


class EntryPointV4Tests(unittest.TestCase):
    def test_dry_run_v4_explicite_sans_cli(self):
        import contextlib
        import io
        import cli_toolchains as cli
        output = io.StringIO()
        argv = ['campagne', '--cycle-v4', '--plugin-commit', '0' * 40,
                '--output-dir', 'jamais-cree-v4', '--dry-run']
        with patch.object(sys, 'argv', argv), patch.object(campaign, 'run_cli') as model, \
                patch.object(campaign.subprocess, 'run') as process, contextlib.redirect_stdout(output):
            self.assertEqual(campaign.main(), 0)
        model.assert_not_called()
        process.assert_not_called()
        result = json.loads(output.getvalue())
        self.assertEqual(result['case_contract'], cli.CYCLE_V4[0])
        self.assertEqual(result['case_contract_sha256'], cli.CYCLE_V4[1])
        self.assertEqual(result['sessions'], 18)

    def test_v4_reel_non_lie_refuse_sans_cli(self):
        with patch.object(campaign.subprocess, 'run') as process:
            with self.assertRaisesRegex(ValueError, 'sans commit lié'):
                contract.campaign_cycle(ROOT, '0' * 40, cycle_v4=True)
        process.assert_not_called()
