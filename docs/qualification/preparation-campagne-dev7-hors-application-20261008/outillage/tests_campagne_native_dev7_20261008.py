"""Fixtures sans modèle, sans installation et sans mutation du profil."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import campagne_native_dev7_20261008 as harness
import socle_campagne_native_dev7_20261008 as s


class Fixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.proposal = s.read(s.PROPOSAL)

    def test_original_questions_oracles_atoms_and_scope(self) -> None:
        cases = s.validate_cases(self.proposal)
        self.assertEqual(len(cases), 16)
        self.assertEqual(sum(len(c["judge_only_invariant_objects"]) for c in cases), 124)
        self.assertEqual(sum(c["activation_mode"] == "spontaneous" for c in cases), 5)
        self.assertEqual(sum(c["case_id"] in s.ALLOWED for c in cases), 3)

    def test_oracle_change_rejected(self) -> None:
        changed = deepcopy(self.proposal)
        changed["cases"][0]["judge_only_invariant_objects"][0]["expectation"] = "altéré"
        with self.assertRaises(s.GateError):
            s.validate_cases(changed)

    def test_source_requirement_change_rejected(self) -> None:
        changed = deepcopy(self.proposal)
        changed["cases"][0]["source_requirements_unchanged"]["mcp_mode"] = "disabled"
        with self.assertRaises(s.GateError):
            s.validate_cases(changed)

    def test_spontaneous_marker_rejected(self) -> None:
        changed = deepcopy(self.proposal)
        case = next(c for c in changed["cases"] if c["activation_mode"] == "spontaneous")
        case["native_prompt"] = "$collectivite-territoriale:dsi-fpt\n" + case["native_prompt"]
        case["prompt_sha256_utf8"] = s.sha(case["native_prompt"].encode("utf-8"))
        with self.assertRaises(s.GateError):
            s.validate_cases(changed)

    def test_parent_identities_and_secrets_are_not_inherited(self) -> None:
        env, removed = s.environment({"CODEX_THREAD_ID": "parent", "CODEX_CI": "1", "CODEX_UNKNOWN": "value",
                                      "API_KEY": "secret", "PATH": "runtime", "CODEX_HOME": "foreign"})
        self.assertEqual(removed, ["CODEX_CI", "CODEX_HOME", "CODEX_THREAD_ID", "CODEX_UNKNOWN"])
        self.assertNotIn("API_KEY", env)
        self.assertEqual(set(k for k in env if k.startswith("CODEX")), {"CODEX_HOME", "CODEX_SQLITE_HOME"})
        self.assertEqual(env["CODEX_HOME"], str(s.STATE))

    def test_source_pin_rejects_head_and_foreign_commit(self) -> None:
        changed = deepcopy(self.proposal)
        changed["candidate_commit"] = "HEAD"
        with patch.object(s.subprocess, "check_output") as git:
            with self.assertRaises(s.GateError):
                s.source_blobs(changed)
            git.assert_not_called()

    def test_git_blobs_match_213_plus_icon(self) -> None:
        blobs, frozen = s.source_blobs(self.proposal)
        self.assertEqual(len(blobs), 214)
        self.assertEqual(len(frozen["files"]), 213)
        self.assertEqual(s.sha(blobs["skills/dsi-fpt/SKILL.md"]),
                         "2b9df5adb10f8dfdb7e1cc86b454b587c39e3194692f91388212cc38aa02fded")

    def receipt_fixture(self, folder: Path, success: object = True) -> str:
        digest = "a" * 64
        s.write_new(folder / "inspection.json", {"model_inference": False})
        s.write_new(folder / "setup-result.json", {"success": success, "cache_unchanged": True,
                    "persisted_windows_sandbox": "elevated", "persisted_sandbox_mode": "read-only",
                    "persisted_web_search": "disabled"})
        s.write_new(folder / "lecture-result.json", {"success": True, "expected_skill_sha256": digest,
                    "model_inference": False, "auth_secrets_read": False,
                    "request": {"sandboxPolicy": {"type": "readOnly"}},
                    "response": {"result": {"exitCode": 0, "stdout": "LECTURE_SANDBOX_ISOLE_20261008\n" + digest}}})
        return digest

    def test_cancelled_uac_cannot_satisfy_gate(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            folder = Path(temp)
            digest = self.receipt_fixture(folder, False)
            with self.assertRaises(s.GateError):
                s.validate_receipts(folder, digest)

    def test_truthy_string_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            folder = Path(temp)
            digest = self.receipt_fixture(folder, "true")
            with self.assertRaises(s.GateError):
                s.validate_receipts(folder, digest)

    def test_receipt_declared_success_needs_exact_content_and_hash(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            folder = Path(temp)
            digest = self.receipt_fixture(folder)
            self.assertEqual(len(s.validate_receipts(folder, digest)), 3)
            value = s.read(folder / "lecture-result.json")
            value["response"]["result"]["stdout"] = "PREFIX_LECTURE_SANDBOX_ISOLE_20261008\n" + digest
            (folder / "lecture-result.json").write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(s.GateError):
                s.validate_receipts(folder, digest)

    def test_gate_failure_never_writes_run_or_invokes_cli(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            root = Path(temp)
            cli = root / "fake-cli.exe"
            cli.write_bytes(b"fake")
            run = root / "run"
            with patch.object(s, "CLI_SHA", s.sha(b"fake")), patch.object(s, "inventory", return_value={
                **{str(i): "hash" for i in range(213)}, "skills/dsi-fpt/SKILL.md": "digest"}), \
                patch.object(s, "validate_receipts", side_effect=s.GateError("UAC annulée")), \
                patch.object(harness.subprocess, "run") as cli_run:
                with self.assertRaises(s.GateError):
                    harness.prepare(cli, root, run)
                self.assertFalse(run.exists())
                cli_run.assert_not_called()

    def test_thirteen_cases_rejected_before_any_run_access(self) -> None:
        with patch.object(harness, "sequential_run") as lock:
            for case in self.proposal["cases"]:
                if case["case_id"] not in s.ALLOWED:
                    with self.assertRaises(s.GateError):
                        harness.execute(s.ROOT / "absent-test-run", case["case_id"])
            lock.assert_not_called()

    def test_one_attempt_cannot_restart(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            run = Path(temp)
            folder = run / "plugin-dsi-technique"
            folder.mkdir()
            s.write_new(folder / "start.json", {"attempt": 1})
            s.write_new(run / "manifest.json", {"cases": [{"id": folder.name, "execution_allowed": True}]})
            with patch.object(harness, "verify"), patch.object(harness.subprocess, "Popen") as process:
                with self.assertRaises(s.GateError):
                    harness.execute_locked(run, folder.name)
                process.assert_not_called()

    def test_permissions_and_activation_overrides_no_model_or_bypass(self) -> None:
        args = s.overrides()
        values = args[1::2]
        self.assertIn('windows.sandbox="elevated"', values)
        self.assertIn('approval_policy="never"', values)
        self.assertIn('plugins.collectivite-territoriale@smoke-dev6.enabled=false', values)
        self.assertIn(f'plugins.{s.PLUGIN_ID}.enabled=true', values)
        self.assertIn(f'plugins.{s.PLUGIN_ID}.mcp_servers.droit-francais.enabled=false', values)
        self.assertFalse(any('"' in v.split("=", 1)[0] for v in values))
        self.assertFalse(any("model=" in v or "bypass" in v or "ignore" in v for v in values))

    def test_catalogue_requires_six_actual_dev7_paths(self) -> None:
        files = {"skills/" + name + "/SKILL.md": "hash" for name in
                 ("dsi-fpt", "dpo-ct", "drh-fpt", "dirfi-fpt", "dpm-fpt", "recherche-juridique")}
        cache = s.ROOT / "test-native-cache"
        paths = "\n".join("- skill: description (file: " + str(cache / name) + ")" for name in files)
        value = harness.catalogue_evidence(json.dumps([{"content": [{"text": paths}]}]).encode(), cache, files)
        self.assertFalse(value["native_skill_activation_proven"])
        self.assertFalse(value["global_discovery_completely_isolated"])
        with self.assertRaises(s.GateError):
            harness.catalogue_evidence(json.dumps(paths.replace("dsi-fpt", "wrong")).encode(), cache, files)

    def catalogue_fixture(self, *, roots: str = "", extra: str = "", alias: str = "r8"):
        files = {"skills/" + name + "/SKILL.md": "hash" for name in
                 ("dsi-fpt", "dpo-ct", "drh-fpt", "dirfi-fpt", "dpm-fpt", "recherche-juridique")}
        cache = s.ROOT / "test-native-cache"
        roots = roots or f'- `{alias}` = `{(cache / "skills").as_posix()}`'
        lines = [f'- skill: description (file: {alias}/{name.removeprefix("skills/")})' for name in files]
        raw = json.dumps([{"content": [{"text": roots + "\n" + "\n".join(lines) + extra}]}]).encode()
        return raw, cache, files

    def test_catalogue_resolves_actual_native_aliases(self) -> None:
        raw, cache, files = self.catalogue_fixture()
        result = harness.catalogue_evidence(raw, cache, files)
        self.assertEqual(result["candidate_aliases_resolved"], ["r8"])
        self.assertTrue(result["dev6_skill_references_absent"])
        self.assertFalse(result["native_skill_activation_proven"])

    def test_catalogue_root_and_free_mentions_do_not_establish_discovery(self) -> None:
        raw, cache, files = self.catalogue_fixture()
        text = f'- `r8` = `{(cache / "skills").as_posix()}`\n' + "\n".join(str(cache / name) for name in files)
        with self.assertRaises(s.GateError):
            harness.catalogue_evidence(json.dumps(text).encode(), cache, files)

    def test_catalogue_rejects_old_dev6_even_when_candidate_is_complete(self) -> None:
        extra = f'\n- old skill: description (file: {(s.DEV6 / "skills/dsi-fpt/SKILL.md").as_posix()})'
        with self.assertRaises(s.GateError):
            harness.catalogue_evidence(*self.catalogue_fixture(extra=extra))
        roots = f'- `r8` = `{(s.ROOT / "test-native-cache/skills").as_posix()}`\n- `r9` = `{(s.DEV6 / "skills").as_posix()}`'
        with self.assertRaises(s.GateError):
            harness.catalogue_evidence(*self.catalogue_fixture(roots=roots,
                extra='\n- old skill: description (file: r9/dsi-fpt/SKILL.md)'))

    def test_catalogue_rejects_unknown_conflicting_or_traversing_aliases(self) -> None:
        raw, cache, files = self.catalogue_fixture()
        for changed in (raw.replace(b"r8/dsi-fpt/", b"r9/dsi-fpt/"),
                        raw.replace(b"r8/dsi-fpt/", b"r8/../skills/dsi-fpt/"),
                        json.dumps('- `r8` = `C:/wrong`\n' + json.loads(raw)[0]["content"][0]["text"]).encode()):
            with self.assertRaises(s.GateError):
                harness.catalogue_evidence(changed, cache, files)

    def test_native_capture_checks_session_identity(self) -> None:
        with tempfile.TemporaryDirectory(dir=s.ROOT) as temp:
            root = Path(temp)
            (root / "sessions").mkdir()
            path = root / "sessions/rollout-abc.jsonl"
            path.write_text(json.dumps({"type": "session_meta", "payload": {"id": "different"}}) + "\n", encoding="utf-8")
            with patch.object(s, "STATE", root):
                self.assertEqual(harness.native_rollout("abc", root)[2], "native_rollout_identity_mismatch")
                self.assertFalse((root / "native-rollout.local.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
