"""Diagnostics L19 sur fixtures ; aucun modele, processus ou permission reelle."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_codex_smoke as smoke

COMMIT = "0" * 40


class SmokeReadDiagnosticTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="t43-l19-synthetic-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.installed = self.root / "installed"
        self.entry = self.installed / "skills/dcp-fpt/SKILL.md"
        self.entry.parent.mkdir(parents=True)
        self.entry.write_text("fixture\nseconde ligne\n", encoding="utf-8", newline="\n")
        self.event = {"type": "item.completed", "item": {
            "type": "command_execution", "status": "completed", "exit_code": 0,
            "command": f"Get-Content -LiteralPath '{self.entry}' -Encoding utf8",
            "aggregated_output": "fixture\nseconde ligne\n"}}
        self.diagnostic = self.root / "mesure/activation-implicite.read-refusal.json"

    def refuse(self, event: dict, message: str) -> dict:
        with self.assertRaisesRegex(ValueError, "^" + re.escape(message) + "$"):
            smoke.read_events([event], self.installed, diagnostic_path=self.diagnostic,
                              case_id="activation-implicite", plugin_commit=COMMIT)
        value = json.loads(self.diagnostic.read_text(encoding="utf-8"))
        self.assertEqual(value["refusal"], message)
        self.assertEqual(value["case_id"], "activation-implicite")
        self.assertEqual(value["plugin_commit"], COMMIT)
        self.assertTrue(value["diagnostic_only"])
        self.assertFalse(value["output_content_archived"])
        self.assertFalse(value["human_legal_validation"])
        self.assertNotIn("aggregated_output", value)
        return value

    def test_commande_hors_contrat_est_tracee_avant_le_meme_refus(self) -> None:
        self.event["item"].update(command="Write-Output fixture-only",
                                  aggregated_output="CONTENU_NE_JAMAIS_ARCHIVER", exit_code=7, status="failed")
        value = self.refuse(self.event, "Commande hors contrat de lecture installé")
        self.assertEqual(value["command_text"], "Write-Output fixture-only")
        self.assertEqual(value["exit_code"], 7)
        self.assertEqual(value["status"], "failed")
        self.assertEqual(value["output_chars"], len("CONTENU_NE_JAMAIS_ARCHIVER"))
        self.assertNotIn("CONTENU_NE_JAMAIS_ARCHIVER", self.diagnostic.read_text(encoding="utf-8"))

    def test_lecture_hors_skill_reste_refusee_et_sans_son_contenu(self) -> None:
        self.event["item"]["command"] = f"Get-Content -LiteralPath '{self.root / 'outside.md'}' -Encoding utf8"
        self.refuse(self.event, "Lecture hors skill installé")
        self.assertFalse((self.root / "outside.md").exists())

    def test_lecture_tronquee_ou_en_echec_reste_refusee(self) -> None:
        for changes in ({"aggregated_output": "fixture"}, {"exit_code": 1}, {"status": "failed"}):
            with self.subTest(changes=changes):
                event = copy.deepcopy(self.event)
                event["item"].update(changes)
                diagnostic = self.root / ("mesure/" + next(iter(changes)) + ".json")
                with self.assertRaisesRegex(ValueError, "^Lecture installée tronquée ou échouée$"):
                    smoke.read_events([event], self.installed, diagnostic_path=diagnostic, case_id="fixture", plugin_commit=COMMIT)
                self.assertTrue(json.loads(diagnostic.read_bytes())["diagnostic_only"])

    def test_succes_ne_cree_pas_de_diagnostic_et_ne_change_pas_la_lecture(self) -> None:
        reads = smoke.read_events([self.event], self.installed, diagnostic_path=self.diagnostic)
        self.assertTrue(smoke.complete_entry(reads, "dcp-fpt"))
        self.assertFalse(self.diagnostic.exists())

    def test_masquage_L12b_couvre_tous_les_motifs_avant_la_borne(self) -> None:
        samples = [
            'Get-Content "C:/fixture/auth.json"', "Get-Content C:/fixture/.env.local",
            "API_KEY='fixture-value'", "--token fixture-value",
            "https://fixture-user:fixture-value@example.invalid/path", "Bearer fixture-value",
            "sk-" + "x" * 32, "ghp_" + "x" * 32,
            "eyJfixture.eyJfixture.fixture-signature",
            "-----BEGIN PRIVATE KEY-----fixture-value-----END PRIVATE KEY-----",
        ]
        for command in samples:
            with self.subTest(command=command):
                public = smoke.public_command(command)
                self.assertIn("[MASQUE]", public["command_text"])
                self.assertNotIn("fixture-value", public["command_text"])
                self.assertEqual(len(public["masked_command_sha256"]), 64)
        public = smoke.public_command("x" * 1950 + " TOKEN='" + "z" * 300 + "' " + "y" * 300)
        self.assertEqual(len(public["command_text"]), 2000)
        self.assertTrue(public["command_truncated"])
        self.assertNotIn("zzz", public["command_text"])
        self.assertIn("[MASQUE]", public["command_text"])
        masked = "x" * 1950 + " [MASQUE] " + "y" * 300
        self.assertEqual(public["masked_command_sha256"], hashlib.sha256(masked.encode()).hexdigest())

    def test_diagnostic_masque_la_commande_et_ne_conserve_pas_statut_arbitraire(self) -> None:
        self.event["item"].update(command="Write-Output --password fixture-value", status="Bearer fixture-value")
        value = self.refuse(self.event, "Commande hors contrat de lecture installé")
        self.assertNotIn("fixture-value", self.diagnostic.read_text(encoding="utf-8"))
        self.assertEqual(value["status"], "unrecognized")
        self.assertIn("[MASQUE]", value["command_text"])

    def test_diagnostic_existant_intact_et_refus_inchange(self) -> None:
        self.diagnostic.parent.mkdir()
        self.diagnostic.write_bytes(b"preuve precedente")
        self.event["item"]["command"] = "Write-Output fixture-only"
        with self.assertRaisesRegex(ValueError, "^Commande hors contrat de lecture installé$"):
            smoke.read_events([self.event], self.installed, diagnostic_path=self.diagnostic)
        self.assertEqual(self.diagnostic.read_bytes(), b"preuve precedente")

    def test_run_ecrit_dans_mesure_et_arrete_avant_le_second_cas(self) -> None:
        candidate = self.root / "candidate"
        candidate.mkdir()
        (candidate / "upstream.json").write_text('{"skills": {}}', encoding="utf-8")
        (candidate / ".mcp.json").write_text('{"mcpServers":{"droit-francais":{"url":"https://fixture.invalid"}}}', encoding="utf-8")
        prepared = self.root / "prepared"
        prepared.mkdir()
        output = self.root / "run-mesure"
        data = {"cli_sha256": "fixture", "environment_path": "env", "installed_path": "env/plugin"}
        bad = copy.deepcopy(self.event)
        bad["item"]["command"] = "Write-Output fixture-only"
        with patch.object(smoke, "candidate", return_value={}), \
             patch.object(smoke, "verify_codex_cli", return_value={}), \
             patch.object(smoke, "checked", return_value=data), \
             patch.object(smoke, "fingerprint", return_value="fixture"), \
             patch.object(smoke, "verify_plugin_read"), \
             patch.object(smoke.subprocess, "run", return_value=Mock(returncode=0)), \
             patch.object(smoke, "main_config_hash", return_value=None), \
             patch.object(smoke, "installed_snapshot", return_value={}), \
             patch.object(smoke, "visible_skills", return_value={}), \
             patch.object(smoke, "verify_visible", return_value=[]), \
             patch.object(smoke, "metadata", return_value=[{"enabled": True, "name": "fixture",
                 "transport": {"url": "https://fixture.invalid"}}]), \
             patch.object(smoke, "smoke_prompt", return_value="synthetic"), \
             patch.object(smoke, "run_cli", return_value=([bad], 1, {})) as run_cli:
            with self.assertRaisesRegex(ValueError, "^Commande hors contrat de lecture installé$"):
                smoke.run(candidate, COMMIT, "synthetic-cli", output, prepared, "synthetic-model", 1)
        run_cli.assert_called_once()
        path = output / "activation-implicite.read-refusal.json"
        self.assertTrue(path.is_file())
        self.assertEqual(json.loads(path.read_bytes())["plugin_commit"], COMMIT)
        self.assertFalse((output / "activation-implicite.json").exists())
        self.assertFalse((output / "installation-codex.json").exists())


if __name__ == "__main__":
    unittest.main()
