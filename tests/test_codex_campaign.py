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
from support_preuves_historiques import runtime_at


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

    def test_commande_mixte_ou_lecture_partielle_ne_vaut_pas_lecture_native(self):
        path = ".agents/skills/dcp-fpt/SKILL.md"
        for text in (f'Write-Output "Get-Content {path}"', f"Get-Content {path} -Tail 1",
                     f"Get-Content {path}; Write-Output secret", "Get-Content .agents/skills/../../secret"):
            with self.subTest(commande=text):
                self.assertEqual(campaign.read_command_paths(text), [])
        self.assertEqual(campaign.read_command_paths(f"Get-Content -LiteralPath '{path}'"), [path])

    def test_sortie_tronquee_ne_prouve_pas_entree_complete(self):
        path = ".agents/skills/dcp-fpt/SKILL.md"
        event = {"type": "item.completed", "item": {"type": "command_execution",
                 "command": f"Get-Content -LiteralPath '{path}'", "exit_code": 0,
                 "status": "completed", "aggregated_output": "Extrait tronqué"}}
        clean = campaign.sanitize([event])
        self.assertIn("native_entry_content_unverified", campaign.failures(clean, self.case, 0))
        event["item"]["aggregated_output"] = (campaign.ROOT / "skills/dcp-fpt/SKILL.md").read_text(encoding="utf-8")
        clean = campaign.sanitize([event])
        self.assertNotIn("native_entry_content_unverified", campaign.failures(clean, self.case, 0))

    def test_segments_couvrent_toute_entree_et_refusent_trou_ou_doublon(self):
        case = next(c for c in campaign.load_cases() if c["id"] == "plugin-dcp-mcp-indisponible")
        clean = []
        for name in case["activation_sequence"]:
            path = f".agents/skills/{name}/SKILL.md"
            chunks = campaign.entry_chunks(path)
            self.assertEqual("".join(c["content"] for c in chunks), (campaign.ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8"))
            for chunk in chunks:
                self.assertLessEqual(len(chunk["content"].encode()), campaign.CHUNK_BYTES)
                command = f"Get-Content -LiteralPath '{path}' -Encoding utf8 | Select-Object -Skip {chunk['start']} -First {chunk['count']}"
                events = [{"type":"item.completed", "item":{"type":"command_execution",
                    "command":command,"aggregated_output":chunk["content"],"status":"completed","exit_code":0}}]
                clean.extend(campaign.sanitize(events))
        clean += [{"type":"reply","text":"Réponse factice, aucun score"},{"type":"turn_completed"}]
        self.assertEqual(campaign.failures(clean, case, 0, campaign.PROFILE), [])
        self.assertIn("native_entry_coverage_mismatch", campaign.failures(clean[1:], case, 0, campaign.PROFILE))
        self.assertIn("native_entry_coverage_mismatch", campaign.failures([clean[0]]+clean, case, 0, campaign.PROFILE))
        clean[0]["chunk"]["content_verified"] = False
        self.assertIn("native_entry_content_unverified", campaign.failures(clean, case, 0, campaign.PROFILE))

    def test_pipeline_libre_ne_vaut_pas_segment(self):
        path = ".agents/skills/dcp-fpt/SKILL.md"
        for command in (f"Get-Content '{path}' | Write-Output", f"Get-Content -LiteralPath '{path}' -Encoding utf8 | Select-Object -Skip 0 -First 1; Write-Output secret"):
            self.assertEqual(campaign.read_command_paths(command), [])

    def test_preuves_exportees_rattachees_aux_cas_et_runtime(self):
        root = campaign.ROOT
        folder = root / "tests/evidence/2026-10-07-codex-natif"
        summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
        cases = {c["id"]: c for c in campaign.load_cases()}
        self.assertEqual({r["case_id"] for r in summary["runs"]}, set(cases))
        self.assertEqual(len(summary["runs"]), len(cases))
        runtime = runtime_at(root, summary["plugin_commit"])
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
        runtime = runtime_at(root, "85011f7f86b488330fe00ff7a30ce42d6dbe9a84")
        for name, digest in evidence["summary"]["runtime_sha256"].items():
            self.assertEqual(runtime["skills/dcp-fpt/" + name], digest)
        self.assertFalse(evidence["human_legal_validation"])

    def test_smoke_installe_charge_six_skills_et_conserve_leurs_octets(self):
        root = campaign.ROOT
        path = root / "tests/evidence/2026-10-07-correctif/installation-codex.json"
        evidence = json.loads(path.read_text(encoding="utf-8"))
        expected = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (root / "skills").rglob("*") if p.is_file()}
        self.assertEqual(evidence["runtime_sha256"], expected)
        upstream = json.loads((root / "upstream.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["source_dcp_commit"], upstream["skills"]["dcp-fpt"]["commit"])
        self.assertEqual({s["name"] for s in evidence["skills"]},
                         {"collectivite-territoriale:"+name for name in upstream["skills"]})
        self.assertTrue(all(s["enabled"] and s["pluginId"] == "collectivite-territoriale@qualification-locale"
                            for s in evidence["skills"]))
        self.assertFalse(evidence["credentials_copied"])
        self.assertFalse(evidence["global_installation_modified"])
        self.assertFalse(evidence["model_called"])


if __name__ == "__main__":
    unittest.main()
