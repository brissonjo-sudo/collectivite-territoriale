"""Smoke L22 : processus et installation simulés, contrôle STOP réel."""
from pathlib import Path
from contextlib import ExitStack
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_codex_smoke as smoke


class SmokeCycleStopTests(unittest.TestCase):
    def run_fixture(self, case_id: str, variant: str) -> dict:
        """Exécute le chemin run sur événements synthétiques et sorties temporaires."""
        with tempfile.TemporaryDirectory(prefix="t43-L22-smoke-synthetique-") as tmp:
            directory = Path(tmp)
            prepared_root = directory / "preparation"
            environment = prepared_root / "environment"
            installed = environment / "plugin"
            output = directory / "mesure"
            commit = "0" * 40
            baseline = {"plugin_commit": commit}
            prepared = {**baseline, "cli_sha256": "fixture-cli",
                        "environment_path": "environment", "installed_path": "environment/plugin"}
            endpoint = json.loads((ROOT / ".mcp.json").read_bytes())["mcpServers"]["droit-francais"]["url"]
            events = [
                {"type": "item.started", "item": {"id": "mcp", "type": "mcp_tool_call"}},
                {"type": "item.completed", "item": {"id": "mcp", "type": "mcp_tool_call",
                 "server": "legal", "tool": "get_article", "status": "completed",
                 "result": {"content": [{"type": "text", "text": "fixture sans droit"}]}}},
                {"type": "item.completed", "item": {"id": "final", "type": "agent_message", "text": "Réponse synthétique"}},
                {"type": "turn.completed"},
            ]
            stop = {"type": "item.completed", "item": {"id": "stop", "type": "agent_message", "text": "STOP — fixture synthétique"}}
            if variant == "correct":
                events.insert(0, stop)
            elif variant == "announcement":
                events.insert(0, stop)
                events.insert(0, {"type": "item.completed", "item": {
                    "id": "annonce", "type": "agent_message", "text": "Annonce synthétique"}})
            elif variant == "after_tool":
                events.insert(2, stop)
            elif variant != "absent":
                raise AssertionError(variant)
            receipt = {"kind": "real_cli", "synthetic": True, "dry_run": True, "test_only": True}
            reads = [{"path": f"skills/{name}/SKILL.md", "start": 0, "count": 1,
                      "line_count": 1, "content_verified": True} for name in ("dcp-fpt", "recherche-juridique")]
            mocks = {
                "candidate": baseline, "verify_codex_cli": {"fixture": True}, "checked": prepared,
                "fingerprint": "fixture-cli", "verify_plugin_read": None, "main_config_hash": "fixture-config",
                "installed_snapshot": {}, "visible_skills": {}, "verify_visible": [],
                "metadata": [{"name": "legal", "enabled": True, "transport": {"url": endpoint}}],
                "run_cli": (events, 0, receipt), "read_events": reads,
            }
            with ExitStack() as stack:
                for name, value in mocks.items():
                    stack.enter_context(patch.object(smoke, name, return_value=value))
                stack.enter_context(patch.object(smoke, "CASES", (case_id,)))
                process = stack.enter_context(patch.object(smoke.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)))
                if variant == "correct":
                    smoke.run(ROOT, commit, "fixture-non-executable", output, prepared_root, "fixture", 1)
                else:
                    with self.assertRaisesRegex(ValueError, "Smoke en échec"):
                        smoke.run(ROOT, commit, "fixture-non-executable", output, prepared_root, "fixture", 1)
                    self.assertFalse((output / "installation-codex.json").exists())
                self.assertEqual(process.call_count, 1)  # login status simulé, aucun processus réel.
            proof = json.loads((output / (case_id + ".json")).read_bytes())
            self.assertTrue(proof["origin"]["synthetic"])
            self.assertTrue(proof["candidate_entry_read"])
            self.assertTrue(proof["installed_mcp_success"])
            self.assertIs(proof["stop_required"], True)
            return proof

    def test_deux_cas_sources_exigent_STOP(self) -> None:
        for case_id in ("activation-implicite", "mcp-installe"):
            with self.subTest(case=case_id):
                self.assertIs(smoke.source_case(ROOT, case_id)["stop_first"], True)

    def test_deux_smoke_refusent_STOP_absent_tardif_ou_apres_annonce(self) -> None:
        for case_id in ("activation-implicite", "mcp-installe"):
            for variant in ("absent", "announcement", "after_tool"):
                with self.subTest(case=case_id, variant=variant):
                    self.assertEqual(self.run_fixture(case_id, variant)["technical_status"], "failed")

    def test_deux_smoke_acceptent_STOP_premier_toutes_conditions_simulees(self) -> None:
        for case_id in ("activation-implicite", "mcp-installe"):
            with self.subTest(case=case_id):
                self.assertEqual(self.run_fixture(case_id, "correct")["technical_status"], "passed")


if __name__ == "__main__":
    unittest.main()
