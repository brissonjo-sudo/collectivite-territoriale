"""Contrôles des frontières introduites par l'adaptateur Vibe, sans dépendance Vibe."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from configure_vibe import MCP_ALIAS, config_text, oauth_server, write_profile
from run_vibe_campaign import allow_effect, build_prompt, enabled_tools, sanitize_entry, technical_failures

CASES = json.loads((ROOT / "tests/cas-plugin.json").read_text(encoding="utf-8"))


class VibeTests(unittest.TestCase):
    def test_oauth_preserves_public_client_and_port_without_static_credentials(self):
        cfg = tomllib.loads(config_text(ROOT))
        source = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]["droit-francais"]
        self.assertEqual(len(cfg["mcp_servers"]), 1)
        server = cfg["mcp_servers"][0]
        self.assertEqual(server["auth"], {"type": "oauth", "scopes": [],
            "client_id": source["oauth"]["clientId"], "redirect_port": source["oauth"]["callbackPort"]})
        self.assertFalse(server["sampling_enabled"])
        self.assertFalse(cfg["session_logging"]["enabled"])
        self.assertNotIn("headers", server)
        overridden = oauth_server(ROOT, client_id="vibe-public", port=45454)
        self.assertEqual(overridden["auth"]["client_id"], "vibe-public")

    def test_degraded_profile_has_no_mcp_or_mcp_tool(self):
        cfg = tomllib.loads(config_text(ROOT, mcp=False))
        self.assertEqual(cfg["mcp_servers"], [])
        self.assertFalse(any(x.startswith(MCP_ALIAS) for x in cfg["enabled_tools"]))
        self.assertEqual(enabled_tools(CASES[-1]), ["skill", "read_file"])

    def test_profile_never_overwrites_different_config_or_existing_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "new"
            path = write_profile(home, "first\n")
            self.assertEqual(write_profile(home, "first\n"), path)
            with self.assertRaises(ValueError):
                write_profile(home, "second\n")
            self.assertEqual(path.read_text(), "first\n")
            unrelated = Path(tmp) / "existing"
            unrelated.mkdir()
            (unrelated / "notes.txt").write_text("keep")
            with self.assertRaises(ValueError):
                write_profile(unrelated, "config")

    def test_unknown_mcp_fields_and_credential_urls_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = json.loads((ROOT / ".mcp.json").read_text())
            source["mcpServers"]["droit-francais"]["headers"] = {"Authorization": "secret"}
            (root / ".mcp.json").write_text(json.dumps(source))
            with self.assertRaises(ValueError):
                oauth_server(root)
            del source["mcpServers"]["droit-francais"]["headers"]
            source["mcpServers"]["droit-francais"]["url"] = "https://token@example.org/mcp"
            (root / ".mcp.json").write_text(json.dumps(source))
            with self.assertRaises(ValueError):
                oauth_server(root)

    def test_natural_prompt_contains_no_added_activation_instruction(self):
        for case in CASES:
            self.assertEqual(build_prompt(case, "natural"), case["prompt"])
            self.assertIn("Charge avec l'outil skill", build_prompt(case, "guided"))

    def test_permissions_deny_other_files_tools_sources_and_symlink_escape(self):
        dpo = CASES[2]
        self.assertTrue(allow_effect({"kind":"web_fetch", "toolName":"web_fetch",
                                     "input":{"url":"https://www.cnil.fr/fr/x"}}, dpo, ROOT))
        for url in ["https://www.cnil.fr.evil.test/x", "http://www.cnil.fr/x",
                    "https://user@www.cnil.fr/x", "https://www.cnil.fr:444/x"]:
            self.assertFalse(allow_effect({"kind":"web_fetch", "toolName":"web_fetch",
                                          "input":{"url":url}}, dpo, ROOT))
        self.assertFalse(allow_effect({"kind":"web_fetch", "toolName":"web_fetch",
                         "input":{"url":"https://www.cnil.fr/"}}, CASES[-1], ROOT))
        detail = {"kind":"file_read", "toolName":"read_file", "input":{"filePath":str(ROOT / "README.md")}}
        self.assertFalse(allow_effect(detail, dpo, ROOT))
        detail["input"]["filePath"] = str(ROOT / "skills/dpm-fpt/SKILL.md")
        self.assertTrue(allow_effect(detail, dpo, ROOT))
        detail["toolName"] = "foreign_read"
        self.assertFalse(allow_effect(detail, dpo, ROOT))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skills").mkdir()
            (root / "secret.txt").write_text("private")
            (root / "skills/escape.txt").symlink_to(root / "secret.txt")
            self.assertFalse(allow_effect({"kind":"file_read", "toolName":"read_file",
                "input":{"filePath":str(root / "skills/escape.txt")}}, dpo, root))

    def test_sanitizer_discards_reasoning_payloads_and_protocol_errors_are_failures(self):
        self.assertIsNone(sanitize_entry({"type":"reasoning", "text":"PRIVATE"}, CASES[0], ROOT))
        entry = {"type":"effect", "reasoning":"PRIVATE", "detail":{"kind":"tool",
                 "toolName":MCP_ALIAS + "_get_article", "input":{"token":"SECRET"}},
                 "state":{"status":"completed", "output":{"isError":True,"text":"SECRET"}}}
        clean = sanitize_entry(entry, CASES[0], ROOT)
        self.assertFalse(clean["succeeded"])
        self.assertNotIn("PRIVATE", json.dumps(clean))
        self.assertNotIn("SECRET", json.dumps(clean))
        self.assertNotIn("input", clean)
        entry["state"]["output"] = {"ok": False}
        self.assertFalse(sanitize_entry(entry, CASES[0], ROOT)["succeeded"])
        entry["state"]["output"] = {}
        entry["state"]["display"] = {"success": False}
        self.assertFalse(sanitize_entry(entry, CASES[0], ROOT)["succeeded"])

    def test_degraded_even_failed_mcp_call_invalidates_evidence(self):
        trace = [{"type":"tool", "name":MCP_ALIAS + "_get_article", "succeeded":False, "allowed":False}]
        self.assertIn("plugin_mcp_call_unexpected", technical_failures(trace, CASES[-1], "natural"))

    def test_complete_guided_trace_still_requires_separate_human_review(self):
        case = CASES[0]
        trace = [{"type":"tool", "skill":n, "succeeded":True,"allowed":True} for n in case["skills"]]
        trace += [{"type":"tool", "name":MCP_ALIAS + "_get_article", "succeeded":True,"allowed":True},
                  {"type":"assistant", "text":"Réponse"}]
        self.assertEqual(technical_failures(trace, case, "guided"), [])
        reverse = copy.deepcopy(trace)
        reverse[0], reverse[1] = reverse[1], reverse[0]
        self.assertIn("guided_activation_sequence_mismatch", technical_failures(reverse, case, "guided"))
        self.assertNotIn("guided_activation_sequence_mismatch", technical_failures(reverse, case, "natural"))
        trace.append({"type":"tool","name":MCP_ALIAS + "_get_article", "succeeded":True,"allowed":True})
        self.assertIn("final_response_missing", technical_failures(trace, case, "natural"))


if __name__ == "__main__":
    unittest.main()
