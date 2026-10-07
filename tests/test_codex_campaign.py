"""Contre-épreuves de traçabilité Codex, sans appel modèle."""
import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_codex_campaign as campaign


class CodexCampaignTests(unittest.TestCase):
    def setUp(self):
        self.case = next(c for c in campaign.load_cases() if c["id"] == "plugin-dcp-egalite")

    def test_echec_mcp_ne_vaut_pas_resultat_reussi_et_raisonnement_exclu(self):
        events = [
            {"type": "item.completed", "item": {"type": "reasoning", "text": "CANARI"}},
            {"type": "item.completed", "item": {"type": "mcp_tool_call", "server": "droit-francais",
             "tool": "get_article", "status": "completed", "result": {"isError": True, "content": "CANARI"}}},
        ]
        clean = campaign.sanitize(events)
        self.assertNotIn("CANARI", json.dumps(clean))
        self.assertIn("plugin_mcp_call_missing", campaign.failures(clean, self.case, 0))

    def test_mention_et_lecture_bloquee_ne_prouvent_pas_activation_native(self):
        clean = campaign.sanitize([
            {"type": "item.completed", "item": {"type": "agent_message", "text": "dcp-fpt recherche-juridique"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "Get-Content .agents/skills/dcp-fpt/SKILL.md", "exit_code": 1, "status": "completed"}},
        ])
        self.assertIn("native_read_sequence_mismatch", campaign.failures(clean, self.case, 0))

    def test_mcp_absent_en_degrade_et_requis_en_nominal(self):
        degraded = next(c for c in campaign.load_cases() if c["id"] == "plugin-dcp-mcp-indisponible")
        with patch.object(campaign.sys, "platform", "win32"):
            nominal_cmd = campaign.command(self.case, "cli", "modèle")
            degraded_cmd = campaign.command(degraded, "cli", "modèle")
        self.assertIn("mcp_servers.droit-francais.required=true", nominal_cmd)
        self.assertFalse(any("mcp_servers." in s for s in degraded_cmd))
        self.assertIn("--ignore-user-config", degraded_cmd)
        self.assertIn('web_search="disabled"', degraded_cmd)
        self.assertIn('windows.sandbox="elevated"', degraded_cmd)
        self.assertIn("read-only", degraded_cmd)

    def test_timeout_ne_fabrique_pas_de_reponse(self):
        with patch.object(campaign.subprocess, "run", side_effect=subprocess.TimeoutExpired("cli", 1)):
            clean, code = campaign.execute(self.case, "cli", "modèle", 1)
        self.assertEqual(clean, [])
        self.assertEqual(code, 124)
        self.assertIn("result_error_or_absent", campaign.failures(clean, self.case, code))

    def test_preuves_exportees_rattachees_aux_cas_et_runtime(self):
        root = campaign.ROOT
        folder = root / "tests/evidence/2026-10-07-codex-natif"
        summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
        cases = {c["id"]: c for c in campaign.load_cases()}
        self.assertEqual({r["case_id"] for r in summary["runs"]}, set(cases))
        self.assertEqual(len(summary["runs"]), len(cases))
        runtime = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (root / "skills").rglob("*") if p.is_file()}
        for run in summary["runs"]:
            with self.subTest(cas=run["case_id"]):
                path = root / run["evidence_path"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), run["evidence_sha256"])
                evidence = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(evidence["runtime_sha256"], runtime)
                case = cases[run["case_id"]]
                digest = hashlib.sha256(json.dumps(case, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                self.assertEqual(evidence["case_sha256"], digest)
                errors = campaign.failures(evidence["events"], case, evidence["process_exit"])
                self.assertEqual(evidence["failures"], errors)
                self.assertEqual(run["technical_status"], "failed" if errors else "passed")
                self.assertFalse(run["human_invariants_reviewed"])
        self.assertFalse(summary["publication_ready"])

    def test_mesure_autonome_correspond_aux_octets_dcp_embarques(self):
        root = campaign.ROOT
        evidence = json.loads((root / "tests/evidence/2026-10-07-candidat/dcp-autonome.json").read_text(encoding="utf-8"))
        upstream = json.loads((root / "upstream.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["upstream_runtime_commit"], upstream["skills"]["dcp-fpt"]["commit"])
        for name, digest in evidence["summary"]["runtime_sha256"].items():
            self.assertEqual(hashlib.sha256((root / "skills/dcp-fpt" / name).read_bytes()).hexdigest(), digest)
        self.assertFalse(evidence["human_legal_validation"])


if __name__ == "__main__":
    unittest.main()
