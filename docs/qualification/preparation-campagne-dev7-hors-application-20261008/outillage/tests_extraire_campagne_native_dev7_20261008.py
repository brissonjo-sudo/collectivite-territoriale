"""Fixtures de transport natives synthétiques ; aucun modèle, profil ou verdict réel."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

import extraire_campagne_native_dev7_20261008 as module


class NativeFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="fixture-dev7-", dir=module.ROOT)
        self.addCleanup(self.temp.cleanup)
        self.cache = Path(self.temp.name) / "cache"
        self.skill = self.cache / "skills/dsi-fpt/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.body = "# DSI\nSTOP avant le premier texte visible.\n"
        self.skill.write_bytes(self.body.encode("utf-8"))
        self.files = {"skills/dsi-fpt/SKILL.md": module.sha(self.skill.read_bytes())}

    def base(self) -> list[dict]:
        return [
            {"type": "session_meta", "payload": {"id": "fixture-thread", "cli_version": "fixture", "source": "exec"}},
            {"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [{"type": "input_text", "text": "PRIVATE_DEVELOPER_CONTEXT_AUTH_METADATA"}]}},
            {"type": "turn_context", "payload": {"model": "fixture-model", "approval_policy": "never", "sandbox_policy": {"type": "read-only"}}},
            self.message("user", "QUESTION_FICTIVE"),
        ]

    @staticmethod
    def message(role: str, text: str, phase: str | None = None) -> dict:
        return {"type": "response_item", "payload": {"type": "message", "role": role, "phase": phase,
                "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]}}

    def parse(self, records: list[dict]) -> dict:
        for record in records:
            record["timestamp"] = "2026-10-08T00:00:00Z"
        raw = b"\n".join(json.dumps(r, ensure_ascii=False).encode("utf-8") for r in records) + b"\n"
        return module.normalize(raw, "QUESTION_FICTIVE", "fixture-thread", self.cache, self.files)

    def test_import_has_no_execution_side_effects(self) -> None:
        before = set(module.ROOT.iterdir())
        importlib.reload(module)
        self.assertEqual(before, set(module.ROOT.iterdir()))

    def test_full_injection_versus_mention(self) -> None:
        records = self.base() + [self.message("assistant", "J’utilise dsi-fpt.", "commentary")]
        mention = self.parse(records)
        self.assertFalse(any(e["type"] == "derived_native_skill_injection" for e in mention["events"]))
        records = self.base() + [self.message("user", f"<skill><name>collectivite-territoriale:dsi-fpt</name><path>{self.skill}</path>\n{self.body}</skill>")]
        full = self.parse(records)
        injection = next(e for e in full["events"] if e["type"] == "derived_native_skill_injection")
        self.assertTrue(injection["full_installed_text_present"])
        self.assertNotIn(self.body, json.dumps(injection))
        self.assertEqual(injection["native_line"], 5)

    def test_partial_injection_cannot_prove_full_loading(self) -> None:
        records = self.base() + [self.message("user", f"<skill><name>dsi-fpt</name><path>{self.skill}</path>EXTRAIT</skill>")]
        trace = self.parse(records)
        self.assertFalse(trace["events"][-1]["full_installed_text_present"])
        self.assertIn("skill_injection_partial_foreign_or_unbound", trace["technical_issues"])

    def test_multiple_native_wrappers_keep_order_and_distinct_pointers(self) -> None:
        wrapper = f"<skill><name>dsi-fpt</name><path>{self.skill}</path>\n{self.body}</skill>"
        trace = self.parse(self.base() + [self.message("user", wrapper + "\n" + wrapper)])
        injections = [e for e in trace["events"] if e["type"] == "derived_native_skill_injection"]
        self.assertEqual(len(injections), 2)
        self.assertTrue(all(e["full_installed_text_present"] for e in injections))
        self.assertEqual([e["native_text_block"] for e in injections], [1, 2])
        self.assertEqual(injections[0]["native_line_sha256"], injections[1]["native_line_sha256"])
        self.assertNotEqual(injections[0]["event_id"], injections[1]["event_id"])

    def test_stop_in_final_does_not_erase_commentary(self) -> None:
        trace = self.parse(self.base() + [self.message("assistant", "Je vais lire les instructions.", "commentary"), self.message("assistant", "**STOP** — incident.", "final_answer")])
        self.assertFalse(trace["first_visible_starts_STOP"])
        self.assertTrue(trace["events"][-1]["starts_STOP"])
        self.assertTrue(module.starts_stop("# **STOP** — incident"))
        self.assertFalse(module.starts_stop("---\nSTOP — incident"))

    def test_custom_calls_survive_missing_stdout_items_and_blocked_pairing(self) -> None:
        stdout = [{"type": "thread.started", "thread_id": "fixture-thread"}, {"type": "turn.completed"}]
        self.assertFalse(any("tool" in e["type"] for e in stdout))
        records = self.base() + [
            {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "call_id": "c1", "input": "text(await tools.exec_command({cmd:'Get-Content SKILL.md'}));"}},
            {"type": "response_item", "payload": {"type": "custom_tool_call_output", "call_id": "c1", "output": "blocked by policy"}},
        ]
        trace = self.parse(records)
        call, result = trace["events"][-2:]
        self.assertEqual(result["call_event_id"], call["event_id"])
        self.assertTrue(result["blocked_by_policy"])
        self.assertIsNone(result["successful_skill_read_verified"])
        self.assertNotIn("PRIVATE_DEVELOPER_CONTEXT_AUTH_METADATA", json.dumps(trace))
        self.assertNotIn("blocked by policy", json.dumps(result))

    def test_summary_legal_output_is_never_primary(self) -> None:
        records = self.base() + [
            {"type": "response_item", "payload": {"type": "function_call", "name": "legal_fixture", "call_id": "c2", "arguments": '{"query":"NIS2"}'}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c2", "output": {"kind": "tool_summary", "summary": "PRIVÉ_RÉSUMÉ_JURIDIQUE", "truncated": True}}},
        ]
        trace = self.parse(records)
        result = trace["events"][-1]
        self.assertTrue(result["summary_indicator_observed"])
        self.assertTrue(result["truncation_observed"])
        self.assertFalse(result["primary_text_verified"])
        self.assertNotIn("PRIVÉ_RÉSUMÉ_JURIDIQUE", json.dumps(trace))
        self.assertFalse(any(e["type"] == "source_evidence" for e in trace["events"]))

    def test_tool_read_requires_success_and_complete_frozen_content(self) -> None:
        records = self.base() + [
            {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "call_id": "c3", "input": "lecture de SKILL.md"}},
            {"type": "response_item", "payload": {"type": "custom_tool_call_output", "call_id": "c3", "output": {"exit_code": 0, "output": self.body}}},
        ]
        trace = self.parse(records)
        self.assertTrue(trace["events"][-1]["successful_skill_read_verified"])
        self.assertFalse(any(e["type"] == "derived_native_skill_injection" for e in trace["events"]))
        records[-1]["payload"]["output"]["exit_code"] = 1
        self.assertIsNone(self.parse(records)["events"][-1]["successful_skill_read_verified"])

    def test_inventory_and_secrets_are_omitted_without_fake_success(self) -> None:
        records = self.base() + [
            {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "call_id": "c4", "input": "text(ALL_TOOLS)"}},
            {"type": "response_item", "payload": {"type": "custom_tool_call_output", "call_id": "c4", "output": "PRIVATE_CONNECTOR_METADATA"}},
            self.message("assistant", "api_key=supersecret12345", "final_answer"),
        ]
        trace = self.parse(records)
        text = json.dumps(trace)
        self.assertNotIn("PRIVATE_CONNECTOR_METADATA", text)
        self.assertNotIn("supersecret12345", text)
        self.assertIn("visible_text_redacted", trace["technical_issues"])
        self.assertIsNone(trace["events"][-3]["arguments"])

    def test_unlinked_results_and_wrong_session_are_rejected_or_flagged(self) -> None:
        records = self.base() + [{"type": "response_item", "payload": {"type": "function_call_output", "call_id": "absent", "output": "OK"}}]
        self.assertIn("unlinked_or_duplicate_tool_result", self.parse(records)["technical_issues"])
        records[0]["payload"]["id"] = "other-session"
        with self.assertRaises(module.EvidenceError):
            self.parse(records)

    def test_missing_run_never_creates_native_packet(self) -> None:
        absent = Path(self.temp.name) / "never-executed"
        with self.assertRaises(FileNotFoundError):
            module.extract_and_export(absent, "plugin-dsi-technique", module.ROOT / "proposition-protocole-campagne-dev7-20261008.json")
        self.assertFalse(absent.exists())

    def test_protocol_preserves_16_cases_and_124_atoms(self) -> None:
        p, _ = module.protocol_inputs(module.ROOT / "proposition-protocole-campagne-dev7-20261008.json")
        self.assertEqual(len(p["cases"]), 16)
        self.assertEqual(sum(len(c["judge_only_invariant_objects"]) for c in p["cases"]), 124)
        self.assertEqual(sum(len(c["judge_only_invariant_objects"]) for c in p["cases"] if c["case_id"] in module.ALLOWED), 23)


if __name__ == "__main__":
    unittest.main()
