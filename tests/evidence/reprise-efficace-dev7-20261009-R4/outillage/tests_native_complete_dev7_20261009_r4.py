"""Fixtures adversariales hors inférence, réseau, authentification ou préparation."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import campagne_native_complete_dev7_20261009_r4 as harness
import normaliseur_native_complete_dev7_20261009_r2 as normalizer

ROOT = Path(__file__).resolve().parent
STAMP = "2026-10-09T00:00:00Z"
PROMPT = "Question fictive inchangée."
THREAD = "01234567-89ab-cdef-0123-456789abcdef"
REQUIRED = {"mcp_mode": "required", "web_mode": "disabled", "source_evidence_policy": "required"}


def record(payload: dict, kind: str = "response_item") -> dict:
    return {"type": kind, "timestamp": STAMP, "payload": payload}


def message(text: str, role: str = "assistant", phase: str = "commentary") -> dict:
    return record({"type": "message", "role": role, "phase": phase,
                   "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]})


def native(records: list[dict]) -> bytes:
    base = [record({"id": THREAD, "cli_version": "0.162.0-alpha.2"}, "session_meta"),
            message(PROMPT, "user"),
            record({"approval_policy": "never", "sandbox_policy": {"type": "read-only"}}, "turn_context")]
    return b"\n".join(json.dumps(row, ensure_ascii=False).encode("utf-8") for row in base + records) + b"\n"


def call_rows(output: dict | str, name: str = "mcp__droit-francais__get_article", call_id: str = "call_fixture") -> list[dict]:
    return [record({"type": "function_call", "name": name, "call_id": call_id, "arguments": "{}"}),
            record({"type": "function_call_output", "call_id": call_id, "output": output})]


def primary_doc() -> dict:
    return {"id": "synthetic-article", "title": "Titre purement synthétique",
            "url": "https://www.legifrance.gouv.fr/codes/article_lc/synthetic",
            "text": "Disposition purement synthétique ; aucune règle de droit réelle.",
            "metadata": {"start_date": "2020-01-01", "as_of_date": "2026-10-09", "legal_status": "VIGUEUR"}}


class CompleteFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixture-native-complete-", dir=ROOT)
        self.cache = Path(self.temp.name)
        self.protocol = harness.read(harness.PROTOCOL)
        self.proposal = harness.read(ROOT / self.protocol["proposal_path"])
        self.suite = harness.read(Path(self.proposal["suite_path"]))

    def tearDown(self):
        self.assertTrue(self.cache.resolve().is_relative_to(ROOT))
        self.temp.cleanup()

    def trace(self, rows: list[dict], modes: dict | None = None, files: dict | None = None) -> dict:
        return normalizer.normalize(native(rows), PROMPT, THREAD, self.cache, files or {}, modes or REQUIRED)

    def test_imports_do_not_launch_or_prepare(self):
        for name in ("campagne_native_complete_dev7_20261009_r4.py", "normaliseur_native_complete_dev7_20261009_r2.py"):
            spec = importlib.util.spec_from_file_location("fixture_" + name.split(".")[0], ROOT / name)
            module = importlib.util.module_from_spec(spec)
            with patch("subprocess.Popen", side_effect=AssertionError("Inférence interdite")), \
                    patch("subprocess.run", side_effect=AssertionError("Processus interdit")), \
                    patch.object(Path, "mkdir", side_effect=AssertionError("Préparation interdite")), \
                    patch.object(Path, "open", side_effect=AssertionError("Écriture interdite")):
                spec.loader.exec_module(module)

    def test_exact_historical_cases_and_sha(self):
        harness.validate_protocol(self.protocol, self.proposal, self.suite)
        self.assertEqual(16, len(self.protocol["cases"]))
        self.assertEqual(124, sum(len(c["judge_only_invariant_objects"]) for c in self.protocol["cases"]))
        for name, digest in self.protocol["immutable_tools_sha256"].items():
            self.assertEqual(digest, harness.sha((ROOT / name).read_bytes()))
        self.assertEqual(self.protocol["suite_sha256"], harness.sha(Path(self.proposal["suite_path"]).read_bytes()))
        self.assertEqual(self.protocol["rubric_sha256"], harness.sha(Path(self.proposal["rubric_path"]).read_bytes()))

    def test_question_or_atom_change_rejected(self):
        for field in ("historical_question", "judge_only_invariant_objects", "judge_only_oracle"):
            modified = copy.deepcopy(self.protocol)
            modified["cases"][0][field] = "Mutation interdite"
            with self.assertRaises(harness.GateError):
                harness.validate_protocol(modified, self.proposal, self.suite)

    def test_spontaneous_oracle_leak_rejected_even_if_prompt_sha_repaired(self):
        modified = copy.deepcopy(self.protocol)
        proposal = copy.deepcopy(self.proposal)
        case = next(c for c in modified["cases"] if c["activation_mode"] == "spontaneous")
        case["native_prompt"] += "\ndsi-fpt"
        case["prompt_sha256_utf8"] = harness.sha(case["native_prompt"].encode("utf-8"))
        proposal["cases"] = copy.deepcopy(modified["cases"])
        with self.assertRaisesRegex(harness.GateError, "Oracle divulgué"):
            harness.validate_protocol(modified, proposal, self.suite)

    def test_source_modes_cannot_be_widened(self):
        counts = {"mcp": 0, "web": 0}
        for case in self.protocol["cases"]:
            values = harness.overrides(self.protocol, case)[1::2]
            mode = case["source_requirements_unchanged"]
            required = mode["mcp_mode"] == "required"
            web = mode["web_mode"] == "official_source"
            counts["mcp"] += required
            counts["web"] += web
            self.assertIn('web_search="' + ("live" if web else "disabled") + '"', values)
            self.assertIn("plugins.collectivite-territoriale@campagne-dev7-20261008-r3.mcp_servers.droit-francais.enabled="
                          + ("true" if required else "false"), values)
            self.assertNotIn('windows.sandbox="unelevated"', values)
            self.assertIn("features.code_mode_host=false", values)
        self.assertEqual({"mcp": 13, "web": 3}, counts)

    def config(self, case: dict) -> dict:
        return {"windows": {"sandbox": "elevated"}, "sandbox_mode": "read-only", "approval_policy": "never",
                "web_search": "live" if case["source_requirements_unchanged"]["web_mode"] == "official_source" else "disabled",
                "features": {name: False for name in self.protocol["disabled_features"]},
                "plugins": {"collectivite-territoriale@campagne-dev7-20261008-r3": {"enabled": True,
                    "mcp_servers": {"droit-francais": {"enabled": case["source_requirements_unchanged"]["mcp_mode"] == "required"}}}}}

    def test_effective_config_drift_rejected(self):
        case = self.protocol["cases"][0]
        config = self.config(case)
        harness.configuration_check(config, self.protocol, case)
        for mutation in (lambda c: c["features"].update(code_mode_host=True),
                         lambda c: c.update(web_search="live"),
                         lambda c: c["windows"].update(sandbox="unelevated"),
                         lambda c: c.update(approval_policy="on-request"),
                         lambda c: c.update(mcp_servers={"étranger": {"enabled": True}}),
                         lambda c: c["plugins"].update(étranger={})):
            other = copy.deepcopy(config)
            mutation(other)
            with self.assertRaises(harness.GateError):
                harness.configuration_check(other, self.protocol, case)

    def server(self) -> dict:
        return {"name": "droit-francais", "pluginId": "collectivite-territoriale@campagne-dev7-20261008-r3",
                "authStatus": "oAuth", "toolsError": None, "httpOrigin": "https://droit-francais-skill.onrender.com",
                "tools": {"get_article": {"inputSchema": {"type": "object", "properties": {"article_id": {"type": "string"}}}}}}

    def test_auth_missing_schema_foreign_endpoint_block(self):
        case = self.protocol["cases"][0]
        self.assertIsNone(harness.legal_inventory_check([self.server()], case)["source_primary_verified"])
        for field, value in (("authStatus", "notLoggedIn"), ("tools", {}), ("httpOrigin", None),
                             ("toolsError", "Auth required"), ("pluginId", "autre")):
            server = self.server()
            server[field] = value
            with self.assertRaises(harness.GateError):
                harness.legal_inventory_check([server], case)

    def test_no_sources_requires_no_mcp_exposure(self):
        case = next(c for c in self.protocol["cases"] if c["case_id"] == "plugin-mcp-indisponible")
        harness.legal_inventory_check([], case)
        with self.assertRaises(harness.GateError):
            harness.legal_inventory_check([self.server()], case)

    def inactive_server(self):
        return {"name": "droit-francais", "pluginId": "collectivite-territoriale@campagne-dev7-20261008-r3",
                "httpOrigin": "https://droit-francais-skill.onrender.com", "authStatus": "unsupported",
                "runtimeStatus": None, "tools": {}, "resources": [], "resourceTemplates": [],
                "toolsError": None, "serverInfo": None, "serverCapabilities": None}

    def test_inactive_catalogue_is_not_exposed_but_any_capability_or_unknown_field_blocks(self):
        case = next(c for c in self.protocol["cases"] if c["case_id"] == "plugin-mcp-indisponible")
        inactive = self.inactive_server()
        accepted = harness.legal_inventory_check([inactive], case)
        self.assertEqual(0, accepted["exposed_tools"])
        self.assertTrue(accepted["inactive_catalogue_present"])
        mutations = {"tools": {"search": {}}, "resources": [{}], "resourceTemplates": [{}],
                     "authStatus": "oAuth", "runtimeStatus": "connected", "toolsError": "erreur",
                     "serverInfo": {}, "serverCapabilities": {}, "httpOrigin": None,
                     "pluginId": "étranger", "name": "autre", "unknown_capability": True}
        for field, value in mutations.items():
            with self.subTest(field=field):
                with self.assertRaises(harness.GateError):
                    harness.legal_inventory_check([{**inactive, field: value}], case)
        for field in inactive:
            other = {k: v for k, v in inactive.items() if k != field}
            with self.subTest(missing=field):
                with self.assertRaises(harness.GateError):
                    harness.legal_inventory_check([other], case)
        with self.assertRaises(harness.GateError):
            harness.legal_inventory_check([inactive, inactive], case)

    def test_six_profiles_cover_sixteen_cases_without_override_or_policy_change(self):
        groups = harness.profile_groups(self.protocol)
        self.assertEqual(6, len(groups))
        covered = []
        for group in groups:
            representative = group["representative"]
            for case in group["cases"]:
                self.assertEqual(harness.overrides(self.protocol, representative), harness.overrides(self.protocol, case))
                self.assertEqual(representative["source_requirements_unchanged"], case["source_requirements_unchanged"])
                covered.append(case["case_id"])
        self.assertEqual({c["case_id"] for c in self.protocol["cases"]}, set(covered))
        self.assertEqual(16, len(covered))

    def test_profile_failures_are_all_collected_before_run_creation(self):
        seen = []
        def blocked(protocol, manifest, case, workspace):
            seen.append(case["case_id"])
            raise harness.GateError("échec synthétique de profil")
        with patch.object(harness, "ROOT", self.cache):
            with self.assertRaisesRegex(harness.GateError, "6 profil"):
                harness.preparation_preflights(self.protocol, {}, blocked)
        self.assertEqual(6, len(seen))
        reports = list(self.cache.glob("precontrole-profils-dev7-*.json"))
        self.assertEqual(1, len(reports))
        self.assertEqual(6, harness.read(reports[0])["failures"])

    def test_shared_preparation_receipts_keep_native_representative_identity(self):
        seen = []
        def passed(protocol, manifest, case, workspace):
            seen.append(case["case_id"])
            return {"case_id": case["case_id"], "sandbox_read_succeeded": True}
        with patch.object(harness, "ROOT", self.cache):
            receipts = harness.preparation_preflights(self.protocol, {}, passed)
        self.assertEqual(6, len(seen))
        self.assertEqual(16, len(receipts))
        for receipt in receipts:
            self.assertIn(receipt["native_representative_case_id"], seen)
            self.assertEqual(receipt["case_id"] == receipt["native_representative_case_id"],
                             receipt["individual_case_preflight_performed"])

    def test_cim_both_binaries_and_unknown_paths_block(self):
        binary = self.protocol["process_gate"]["cua_bin_path"]
        for name in ("node.exe", "node_repl.exe"):
            with self.assertRaises(harness.GateError):
                harness.node_gate({}, lambda argv, env: {"processes": [{"name": name, "pid": 41, "path": binary + "/" + name}]})
        with self.assertRaises(harness.GateError):
            harness.node_gate({}, lambda argv, env: {"processes": [{"name": "node.exe", "pid": 41, "path": None}]})
        seen = []
        def empty(argv, env):
            seen.append(argv[-1])
            return {"processes": []}
        result = harness.node_gate({}, empty)
        self.assertIn("'node.exe','node_repl.exe'", seen[0])
        self.assertFalse(result["processes_terminated"])

    def test_prepare_gate_failure_never_creates_run(self):
        target = self.cache / "fixture-must-not-be-prepared"
        self.assertFalse(target.exists())
        def blocked(*args):
            raise harness.GateError("Auth required")
        with patch.object(harness, "ROOT", self.cache), \
                patch.object(harness, "inputs", return_value=(self.protocol, {})), \
                patch("subprocess.run") as command:
            command.return_value.returncode = 0
            command.return_value.stdout = self.protocol["cli_version"].encode("utf-8")
            with self.assertRaisesRegex(harness.GateError, "Auth required"):
                harness.prepare(target, blocked)
        self.assertFalse(target.exists())

    def test_late_stop_and_reasoning_exclusion(self):
        trace = self.trace([message("Je consulte les sources."), message("STOP — suspension", phase="final_answer")])
        self.assertFalse(trace["first_visible_starts_STOP"])
        self.assertTrue(normalizer.starts_stop("**STOP** — suspension"))
        self.assertFalse(normalizer.starts_stop("Préambule\nSTOP — suspension"))
        reasoning = record({"type": "reasoning", "content": [{"type": "text", "text": "Avant STOP"}]})
        self.assertTrue(self.trace([reasoning, message("STOP — suspension")])["first_visible_starts_STOP"])

    def test_complete_primary_observed_not_currentness_certified(self):
        trace = self.trace(call_rows({"structuredContent": primary_doc()}))
        self.assertTrue(trace["source_primary_verified"])
        self.assertIsNone(trace["legal_currentness_verified"])
        source = next(e for e in trace["events"] if e["type"] == "derived_source_evidence")
        self.assertEqual("call_fixture", source["call_id"])
        self.assertTrue(source["native_call_id_verified"])

    def test_excerpt_only_does_not_become_primary(self):
        doc = primary_doc()
        doc["excerpt"] = doc.pop("text")
        self.assertFalse(self.trace(call_rows({"structuredContent": doc}))["source_primary_verified"])

    def test_truncation_within_text_and_nested_metadata_is_preserved(self):
        for mutation in (lambda d: d.update(text=d["text"] + " [truncated]"),
                         lambda d: d["metadata"].update(truncated=True),
                         lambda d: d.update(complete=False),
                         lambda d: d.update(status="incomplete"),
                         lambda d: d.update(text="x" * 12001)):
            doc = primary_doc()
            mutation(doc)
            self.assertFalse(self.trace(call_rows({"structuredContent": doc}))["source_primary_verified"])

    def test_summary_search_and_missing_metadata_not_promoted(self):
        self.assertFalse(self.trace(call_rows({"summary": "Résumé synthétique"}, "WebFetch"),
                                    {**REQUIRED, "web_mode": "official_source"})["source_primary_verified"])
        self.assertFalse(self.trace(call_rows({"results": [{"id": "x", "title": "Résultat"}]}))["source_primary_verified"])
        doc = primary_doc()
        doc.pop("metadata")
        self.assertFalse(self.trace(call_rows({"structuredContent": doc}))["source_primary_verified"])

    def test_official_web_only_when_case_permits(self):
        doc = primary_doc()
        doc["url"] = "https://eur-lex.europa.eu/legal-content/FR/TXT/synthetic"
        rows = call_rows({"structuredContent": doc}, "web__run")
        self.assertTrue(self.trace(rows, {**REQUIRED, "web_mode": "official_source"})["source_primary_verified"])
        self.assertFalse(self.trace(rows)["source_primary_verified"])

    def test_secrets_not_exported_and_document_becomes_incomplete(self):
        doc = primary_doc()
        doc["text"] += " api_key=sk-syntheticSecretToken12345"
        trace = self.trace(call_rows({"structuredContent": doc}))
        self.assertFalse(trace["source_primary_verified"])
        self.assertNotIn("syntheticSecretToken", json.dumps(trace))
        self.assertNotIn("syntheticSecretToken", json.dumps(self.trace([message("api_key=sk-syntheticSecretToken12345")])))

    def test_unlinked_and_duplicate_source_calls_cannot_verify(self):
        missing_call = call_rows({"structuredContent": primary_doc()})[1:]
        self.assertFalse(self.trace(missing_call)["source_primary_verified"])
        duplicate = call_rows({"structuredContent": primary_doc()})
        duplicate += call_rows({"structuredContent": primary_doc()})
        self.assertFalse(self.trace(duplicate)["source_primary_verified"])

    def test_wrapper_printed_primary_not_native_inner_call(self):
        rows = call_rows({"structuredContent": primary_doc()}, "functions.exec")
        self.assertFalse(self.trace(rows)["source_primary_verified"])

    def test_partial_foreign_and_complete_native_skill_injection(self):
        skill = self.cache / "skills/dsi-fpt/SKILL.md"
        skill.parent.mkdir(parents=True)
        text = "---\nname: dsi-fpt\n---\nTexte synthétique complet.\n"
        skill.write_text(text, encoding="utf-8", newline="\n")
        files = {"skills/dsi-fpt/SKILL.md": harness.sha(skill.read_bytes())}
        def wrapper(body: str, path: Path) -> str:
            return f"<skill>\n<name>collectivite-territoriale:dsi-fpt</name>\n<path>{path}</path>\n{body}</skill>"
        partial = self.trace([message(wrapper("Texte incomplet", skill), "user")], files=files)
        event = next(e for e in partial["events"] if e["type"] == "derived_native_skill_injection")
        self.assertFalse(event["full_installed_text_present"])
        complete = self.trace([message(wrapper(text, skill), "user")], files=files)
        event = next(e for e in complete["events"] if e["type"] == "derived_native_skill_injection")
        self.assertTrue(event["full_installed_text_present"])
        foreign = self.trace([message(wrapper(text, self.cache.parent / "foreign/SKILL.md"), "user")], files=files)
        event = next(e for e in foreign["events"] if e["type"] == "derived_native_skill_injection")
        self.assertFalse(event["full_installed_text_present"])

    def test_process_start_failure_is_not_approval_rejection(self):
        output = "exec_command failed: Failed to create unified exec process: helper_unknown_error: setup refresh had errors (os error 32)"
        trace = self.trace(call_rows(output, "functions.exec_command"))
        failure = next(e for e in trace["events"] if e["type"] == "derived_native_process_failure")
        observed = failure.get("failure_observation", failure)
        self.assertIn("windows_error_32", observed["failure_codes"])
        self.assertFalse(observed["auto_review_rejection_established"])

    def test_preflight_auth_failure_leaves_independent_receipt(self):
        case = self.protocol["cases"][0]
        state = self.cache / "state"
        state.mkdir()
        (state / "config.toml").write_bytes("configuration fictive inchangée".encode("utf-8"))
        cache = self.cache / "candidate"
        cache.mkdir()
        protocol = copy.deepcopy(self.protocol)
        protocol["installed_path"] = str(cache)
        server = self.server()
        server["authStatus"] = "notLoggedIn"
        class FakeClient:
            def __init__(inner, *args):
                inner.private_events = []
                inner.stderr = bytearray()
            def initialized(inner):
                return None
            def request(inner, method, params, timeout):
                return {"config": self.config(case)} if method == "config/read" else {"data": [server], "nextCursor": None}
            def close(inner):
                return None
        with patch.object(harness, "ROOT", self.cache), patch.object(harness, "STATE", state):
            with self.assertRaises(harness.GateError):
                harness.preflight(protocol, {"installed_files": {}}, case, self.cache, FakeClient,
                                  lambda argv, env: {"processes": []})
        receipts = list(self.cache.glob("precontrole-complet-dev7-*/precontrole-assaini.json"))
        self.assertEqual(1, len(receipts))
        receipt = harness.read(receipts[0])
        self.assertEqual("blocked", receipt["status"])
        self.assertEqual("legal_source_discovery", receipt["step"])
        self.assertTrue(receipt["persistent_config_unchanged"])
        self.assertFalse(receipt["model_inference"])

    def test_windows_preflight_omits_custom_output_cap_and_validates_real_contract(self):
        case = self.protocol["cases"][0]
        state = self.cache / "state"
        state.mkdir()
        (state / "config.toml").write_bytes(b"configuration fictive")
        candidate = self.cache / "candidate"
        candidate.mkdir()
        protocol = copy.deepcopy(self.protocol)
        protocol["installed_path"] = str(candidate)
        seen = []
        class WindowsClient:
            def __init__(inner, *args):
                inner.private_events = []
                inner.stderr = bytearray()
            def initialized(inner):
                return None
            def request(inner, method, params, timeout):
                if method == "config/read":
                    return {"config": self.config(case)}
                if method == "mcpServerStatus/list":
                    self.assertEqual("full", params["detail"])
                    return {"data": [self.server()], "nextCursor": None}
                self.assertEqual("command/exec", method)
                if "outputBytesCap" in params:
                    raise harness.GateError("custom outputBytesCap is not supported with windows sandbox")
                self.assertEqual(20000, params["timeoutMs"])
                self.assertEqual({"type": "readOnly"}, params["sandboxPolicy"])
                self.assertNotIn("disableOutputCap", params)
                seen.append(params)
                return {"exitCode": 0, "stdout": "A" * 64 + "\r\n", "stderr": ""}
            def close(inner):
                return None
        with patch.object(harness, "ROOT", self.cache), patch.object(harness, "STATE", state), \
                patch.object(harness, "inventory", return_value={"skills/dsi-fpt/SKILL.md": "a" * 64}):
            result = harness.preflight(protocol, {"installed_files": {"skills/dsi-fpt/SKILL.md": "a" * 64}},
                         case, self.cache, WindowsClient, lambda argv, env: {"processes": []})
        self.assertEqual(1, len(seen))
        self.assertTrue(result["sandbox_read_succeeded"])
        self.assertFalse(result["model_inference"])

    def test_sandbox_response_rejects_wrong_hash_errors_boolean_exit_and_truncation(self):
        good = {"exitCode": 0, "stdout": "a" * 64 + "\n", "stderr": ""}
        harness.validate_sandbox_read(good, "a" * 64)
        for altered in [
            {**good, "exitCode": False}, {**good, "exitCode": 1},
            {**good, "stdout": "b" * 64}, {**good, "stdout": "avant " + "a" * 64},
            {**good, "stderr": "erreur"}, {**good, "stdout": None},
            {**good, "stdoutTruncated": True}, {**good, "stderrTruncated": True},
            {**good, "stdout": "a" * 4097}, {**good, "stderr": "é" * 2049}]:
            with self.subTest(response=altered):
                with self.assertRaises(harness.GateError):
                    harness.validate_sandbox_read(altered, "a" * 64)

    def judgment_fixture(self):
        trace = self.trace([message("STOP — suspension immédiate.")] + call_rows({"structuredContent": primary_doc()}))
        atoms = [{"id": "fixture.stop", "category": "comportement", "deterministic_check": "stop_first"},
                 {"id": "fixture.source", "category": "preuve_source", "accepts_abstention": False}]
        case = {"case_id": "fixture", "historical_question": PROMPT,
                "prompt_sha256_utf8": harness.sha(PROMPT.encode("utf-8")),
                "judge_only_invariant_objects": atoms, "judge_only_oracle": {"skills": [],
                    "activation_sequence": [], "activation_sequence_semantics": "strict_set"},
                "source_requirements_unchanged": REQUIRED}
        packet = normalizer.judge_packet(case, trace, "Barème fictif", normalizer.HOST_ADDENDUM,
                                         transport_provenance_verified=True)
        stop_ref = trace["first_visible_event_id"]
        source_ref = trace["primary_source_event_ids"][0]
        judgment = {"case_id": "fixture", "trace_sha256": packet["trace_sha256"], "verdict": "reussite",
                    "invariants": {"fixture.stop": {"status": True, "basis": "observation",
                        "evidence_refs": [stop_ref], "rationale": "STOP initial visible."},
                        "fixture.source": {"status": True, "basis": "retrieval", "evidence_refs": [source_ref],
                                           "rationale": "Texte synthétique lié, aucune affirmation réelle."}}}
        return packet, judgment

    def test_judgment_rejects_coercible_values_and_fabricated_refs(self):
        packet, judgment = self.judgment_fixture()
        self.assertEqual("reussite", normalizer.validate_judgment(packet, judgment)["verdict"])
        for mutation in (lambda j: j["invariants"]["fixture.stop"].update(status=1),
                         lambda j: j["invariants"]["fixture.source"].update(evidence_refs=["inventé"]),
                         lambda j: j["invariants"]["fixture.source"].update(basis="observation"),
                         lambda j: j["invariants"].pop("fixture.source")):
            altered = copy.deepcopy(judgment)
            mutation(altered)
            with self.assertRaises(normalizer.EvidenceError):
                normalizer.validate_judgment(packet, altered)

    def test_explicit_unverified_source_never_becomes_usable_primary(self):
        doc = primary_doc()
        doc["metadata"]["verified"] = False
        trace = self.trace(call_rows({"structuredContent": doc}))
        self.assertFalse(trace["source_primary_verified"])
        source = next(e for e in trace["events"] if e["type"] == "derived_source_evidence")
        self.assertIn("source_declared_unverified", source["documents"][0]["reasons"])
        self.assertFalse(source["documents"][0]["metadata"]["verified"])

    def test_content_complete_false_at_document_or_metadata_blocks_primary(self):
        for location in ("document", "metadata"):
            doc = primary_doc()
            target = doc if location == "document" else doc["metadata"]
            target["content_complete"] = False
            with self.subTest(location=location):
                self.assertFalse(self.trace(call_rows({"structuredContent": doc}))["source_primary_verified"])

    def test_unobserved_text_and_section_contracts_are_explicit_source_gaps(self):
        for operation in ("get_text", "get_section"):
            trace = self.trace(call_rows({"structuredContent": primary_doc()},
                                        "mcp__droit-francais__" + operation))
            with self.subTest(operation=operation):
                source = next(e for e in trace["events"] if e["type"] == "derived_source_evidence")
                self.assertEqual("unobserved_document_contract", source["reason"])
                self.assertEqual("missing", source["status"])
                self.assertFalse(source["operation_contract_supported"])
                self.assertFalse(source["primary_text_verified"])
                self.assertFalse(trace["technical_issues"])

    def test_fetch_hierarchical_contract_remains_unverified(self):
        for identifier in ("LEGITEXT-synthetic", "LEGISCTA-synthetic"):
            doc = primary_doc()
            doc["id"] = identifier
            trace = self.trace(call_rows({"structuredContent": doc}, "mcp__droit-francais__fetch"))
            with self.subTest(identifier=identifier):
                source = next(e for e in trace["events"] if e["type"] == "derived_source_evidence")
                self.assertEqual("unobserved_document_contract", source["reason"])
                self.assertFalse(trace["source_primary_verified"])
                self.assertFalse(trace["technical_issues"])

    def test_readable_fetch_article_does_not_certify_currentness(self):
        doc = primary_doc()
        doc["metadata"]["verified"] = True
        trace = self.trace(call_rows({"structuredContent": doc}, "mcp__droit-francais__fetch"))
        self.assertTrue(trace["source_primary_verified"])
        self.assertIsNone(trace["legal_currentness_verified"])

    def test_judgment_unsealed_transport_and_missing_primary_not_green(self):
        packet, judgment = self.judgment_fixture()
        packet["technical_control"]["sealed_native_transport_verified"] = False
        with self.assertRaises(normalizer.EvidenceError):
            normalizer.validate_judgment(packet, judgment)
        judgment["verdict"] = "bloque"
        self.assertEqual("bloque", normalizer.validate_judgment(packet, judgment)["verdict"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
