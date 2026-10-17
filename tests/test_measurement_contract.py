"""Traces synthétiques uniquement : contrat des dix-huit cas et chronologie."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_codex_campaign as campaign
from campaign_contract import validate_cases
from codex_event_contract import activated_skills


def synthetic_trace(case: dict, order: list[str] | None = None) -> list[dict]:
    """Fabrique seulement une entrée d'essai, jamais une preuve de mesure."""
    events = [{"type": "item.completed", "item": {"id": "stop", "type": "agent_message", "text": "STOP — contrôle synthétique"}}]
    for name in order if order is not None else case["skills"]:
        for chunk in campaign.entry_chunks(f".agents/skills/{name}/SKILL.md"):
            identity = str(len(events))
            command = f"Get-Content -LiteralPath '{chunk['path']}' -Encoding utf8 | Select-Object -Skip {chunk['start']} -First {chunk['count']}"
            events.append({"type": "item.started", "item": {"id": identity, "type": "command_execution"}})
            events.append({"type": "item.completed", "item": {"id": identity, "type": "command_execution",
                "command": command, "aggregated_output": chunk["content"], "status": "completed", "exit_code": 0}})
    if case["mcp_mode"] == "required":
        events.append({"type": "item.started", "item": {"id": "mcp", "type": "mcp_tool_call"}})
        events.append({"type": "item.completed", "item": {"id": "mcp", "type": "mcp_tool_call",
            "server": "droit-francais", "tool": "get_article", "status": "completed",
            "result": {"content": [{"type": "text", "text": "fixture_sans_droit"}]}}})
    events.extend([{"type": "item.completed", "item": {"id": "final", "type": "agent_message", "text": "Réponse synthétique, aucun avis."}},
                   {"type": "turn.completed"}])
    return events


class MeasurementContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = campaign.load_cases()
        self.case = next(c for c in self.cases if c["id"] == "l8-dsi-donnees-sans-source")

    def errors(self, events: list[dict]) -> list[str]:
        return campaign.failures(campaign.sanitize(events, chronology=True), self.case, 0, campaign.PROFILE)

    def test_18_cas_et_neuf_historiques_sans_changement(self) -> None:
        raw = subprocess.check_output(["git", "show", "58495cebd7f49e68d6d4d048208f1172d3e14dbd:tests/cas-plugin.json"], cwd=ROOT)
        self.assertEqual(self.cases[:9], json.loads(raw))
        self.assertEqual(len(self.cases), 18)
        self.assertEqual({s for c in self.cases for s in c["skills"]}, set(json.loads((ROOT / "upstream.json").read_bytes())["skills"]))
        for case in self.cases[9:]:
            self.assertEqual(case["invariants"], case["invariants_observables"])
            self.assertEqual(case["skills"], case["expected_skills"])
            self.assertNotIn("max_budget_usd", case)

    def test_schema_refuse_mode_sequence_et_perte_invariant(self) -> None:
        for field, value in (("activation_mode", "automatic"), ("activation_sequence", []),
                             ("stop_first", "true"), ("invariants_observables", [])):
            case = copy.deepcopy(self.case); case[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_cases([case], set(self.case["skills"]))

    def test_identifiant_non_slug_et_budget_non_fini_refuses(self) -> None:
        for field, value in (("id", "../sortie"), ("skills", [["dsi-fpt"]]), ("max_budget_usd", float("nan"))):
            case = copy.deepcopy(self.case); case[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_cases([case], set(self.case["skills"]))

    def test_conforme_STOP_et_activations_completees(self) -> None:
        events = synthetic_trace(self.case)
        self.assertEqual(self.errors(events), [])
        clean = campaign.sanitize(events, chronology=True)
        self.assertEqual(activated_skills(clean, campaign.entry_chunks), (self.case["skills"], []))

    def test_STOP_apres_debut_outil_meme_non_termine_refuse(self) -> None:
        events = synthetic_trace(self.case)
        events.insert(0, {"type": "item.started", "item": {"id": "aborted", "type": "mcp_tool_call"}})
        self.assertIn("stop_after_tool", self.errors(events))
        self.assertIn("trace_error", self.errors(events))

    def test_STOP_absent_ou_dans_raisonnement_seul_refuse(self) -> None:
        events = synthetic_trace(self.case)
        events[0]["item"]["type"] = "reasoning"
        self.assertIn("stop_first_absent", self.errors(events))
        self.assertNotIn("contrôle synthétique", json.dumps(campaign.sanitize(events, chronology=True), ensure_ascii=False))

    def test_annonce_avant_STOP_refuse(self) -> None:
        events = synthetic_trace(self.case)
        events.insert(0, {"type": "item.completed", "item": {"id": "intro", "type": "agent_message", "text": "Je vais vérifier."}})
        self.assertIn("stop_first_absent", self.errors(events))

    def test_debut_outil_manquant_ne_permet_pas_de_prouver_STOP_avant_outil(self) -> None:
        events = synthetic_trace(self.case)
        del events[1]
        self.assertIn("trace_error", self.errors(events))

    def test_activation_manquante_ne_vaut_pas_mention(self) -> None:
        events = synthetic_trace(self.case, self.case["skills"][1:])
        events[-2]["item"]["text"] = "dsi-fpt activé (simple mention synthétique)"
        self.assertIn("activation_missing_or_unexpected", self.errors(events))

    def test_ordre_inverse_refuse_meme_avec_lectures_valides(self) -> None:
        self.assertIn("activation_sequence_mismatch", self.errors(synthetic_trace(self.case, list(reversed(self.case["skills"])))))

    def test_segment_tronque_ou_duplique_refuse(self) -> None:
        events = synthetic_trace(self.case)
        events[2]["item"]["aggregated_output"] = "tronqué"
        self.assertIn("activation_entry_unverified", self.errors(events))
        events = synthetic_trace(self.case)
        events.insert(3, copy.deepcopy(events[2]))
        self.assertIn("activation_entry_order_mismatch", self.errors(events))

    def test_STOP_streaming_doit_etre_complet_avant_outil(self) -> None:
        events = synthetic_trace(self.case)
        events[0]["type"] = "item.updated"; events[0]["item"]["text"] = "S"
        events.insert(1, {"type": "item.updated", "item": {"id": "stop", "type": "agent_message", "text": "STOP"}})
        self.assertEqual(self.errors(events), [])
        events[1], events[2] = events[2], events[1]
        self.assertIn("stop_after_tool", self.errors(events))

    def test_spontanee_couverture_sans_ordre_force_et_prompt_sans_oracle(self) -> None:
        self.case = next(c for c in self.cases if c["id"] == "l8-dsi-incident-ancien-spontane")
        self.assertEqual(self.case["activation_sequence"], [])
        self.assertEqual(self.errors(synthetic_trace(self.case, list(reversed(self.case["skills"])))), [])
        prompt = campaign.prompt(self.case)
        self.assertNotIn("Active exactement ces entrées", prompt)
        self.assertIn("catalogue complet n'est pas une liste", prompt)
        self.assertNotIn(self.case["invariants"][0], prompt)


if __name__ == "__main__":
    unittest.main()
