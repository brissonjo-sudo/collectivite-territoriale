"""Structure des cas DSI ; aucun répondant, juge ou contrôle comportemental."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CoactivationDsiStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads((ROOT / "tests/cas-coactivation-dsi.json").read_bytes())
        self.cases = self.data["cases"]
        self.skills = json.loads((ROOT / "upstream.json").read_bytes())["skills"]

    def test_cas_locaux_non_mesures_et_identifiants_uniques(self) -> None:
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual(self.data["status"], "structure_only")
        self.assertIs(self.data["measured"], False)
        self.assertEqual(self.data["historical_cases"], "tests/cas-plugin.json")
        ids = [case["id"] for case in self.cases]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(self.skills), {"dpm-fpt", "drh-fpt", "dirfi-fpt", "dpo-ct",
                                           "dcp-fpt", "dsi-fpt", "recherche-juridique"})
        for case in self.cases:
            self.assertNotIn("judgment", case)
            self.assertNotIn("score", case)
            self.assertNotIn("verdict", case)

    def test_roles_routes_et_modes_coherents(self) -> None:
        covered = set()
        for case in self.cases:
            with self.subTest(case=case["id"]):
                skills = case["expected_skills"]
                covered.update(skills)
                self.assertIn("dsi-fpt", skills)
                self.assertEqual(len(skills), len(set(skills)))
                self.assertTrue(set(skills).issubset(self.skills))
                self.assertTrue(set(case["routes"].values()).issubset(skills))
                self.assertIs(type(case["stop_first"]), bool)
                self.assertGreaterEqual(len(case["invariants"]), 4)
                self.assertIn(case["source_mode"], ("required", "disabled", "not_applicable"))
                if case["source_mode"] in ("required", "disabled"):
                    self.assertIn("recherche-juridique", skills)
        self.assertEqual(covered, set(self.skills))

    def test_forcee_et_spontanee_distinguees_sans_biais_dans_le_prompt(self) -> None:
        modes = {case["activation_mode"] for case in self.cases}
        self.assertEqual(modes, {"forced", "spontaneous"})
        for case in self.cases:
            with self.subTest(case=case["id"]):
                if case["activation_mode"] == "forced":
                    self.assertEqual(case["activation_sequence"], case["expected_skills"])
                else:
                    self.assertEqual(case["activation_sequence"], [])
                    for skill in self.skills:
                        self.assertNotIn(skill, case["prompt"])
        self.assertTrue(any(case["source_mode"] == "disabled" for case in self.cases))
        self.assertTrue(any(case["stop_first"] for case in self.cases))

    def test_cas_dcp_historiques_et_nouveau_croisement_conserves(self) -> None:
        historical = json.loads((ROOT / "tests/cas-plugin.json").read_bytes())
        dcp_ids = {case["id"] for case in historical if case["id"].startswith("plugin-dcp-")}
        self.assertEqual(dcp_ids, {"plugin-dcp-egalite", "plugin-dcp-acte-irreversible",
                                  "plugin-dcp-frontieres-finance-donnees", "plugin-dcp-frontiere-dsi-externe",
                                  "plugin-dcp-mcp-indisponible"})
        old = next(case for case in historical if case["id"] == "plugin-dcp-frontiere-dsi-externe")
        self.assertNotIn("dsi-fpt", old["activation_sequence"])
        mixed = next(case for case in self.cases if case["id"] == "dsi-achat-contrat-mixte")
        self.assertEqual(mixed["routes"]["fond_juridique_du_marche"], "dcp-fpt")
        self.assertEqual(mixed["routes"]["specifications_et_reversibilite"], "dsi-fpt")

    def test_bascule_dsi_installee_avant_attribution_pas_regroupee_en_fin(self) -> None:
        rule = ("Chaque BASCULE est émise au moment où le volet est confié, avant toute phrase "
                "qui attribue ou traite ce volet ; une BASCULE regroupée en fin de réponse "
                "ne compte pas.")
        for relative in ("overlays/dsi-fpt.md", "skills/dsi-fpt/SKILL.md"):
            with self.subTest(fichier=relative):
                text = " ".join((ROOT / relative).read_text(encoding="utf-8").split())
                self.assertEqual(text.count(rule), 1)
                self.assertIn("Avant un fond délégué, afficher BASCULE en nommant le skill destinataire", text)


if __name__ == "__main__":
    unittest.main()
