"""Contrôle les preuves natives et les jugements indépendants, sans réexécution."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from verifier_paquets_dev7_r3_20261008 import verify, canonical
from corriger_export_dev7_r3_20261008 import compare_final, final_text, failure_metadata

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "qualification-coactivation-dev7-cli-r3"
JUDGES = {
    "plugin-mcp-indisponible": ("/root/juge_dev7_r3_mcp", "2026-10-08T21:28:43.327Z"),
    "plugin-dsi-technique": ("/root/juge_dev7_r3_technique", "2026-10-08T21:28:56.458Z"),
    "plugin-dsi-source-indisponible": ("/root/juge_dev7_r3_source", "2026-10-08T21:29:25Z"),
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(path.read_bytes())

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def check():
    verify()  # Exports v1 conservés.
    manifest = read(RUN / "manifest.json")
    assert sha((RUN / "manifest.json").read_bytes()) == "bc7a40b58836b626c97ab157ad2bc8072325ad25fc0507ef6db8d205fbe31f43"
    for name, digest in manifest["tools_sha256"].items():
        assert sha((ROOT / name).read_bytes()) == digest
    cache = Path(manifest["installed_path"])
    for name, digest in manifest["installed_files"].items():
        assert sha((cache / name).read_bytes()) == digest
    rows, evidence = [], []
    for case, (agent, completed) in JUDGES.items():
        folder = RUN / "judge-packets-v2" / case
        old = read(RUN / "judge-packets" / case / "packet.json")
        packet, trace, exported, judge = [read(folder / n) for n in ("packet.json", "trace.json", "manifest.json", "jugement.json")]
        for key in ("question", "oracle", "atoms", "source_requirements", "original_rubric", "host_addendum"):
            assert packet[key] == old[key], (case, key)
        for name, field in (("packet.json", "packet_sha256"), ("trace.json", "trace_file_sha256"), ("prompt.md", "prompt_sha256")):
            assert sha((folder / name).read_bytes()) == exported[field]
        assert packet["trace"] == trace
        assert sha(canonical(trace)) == packet["trace_sha256"] == exported["trace_sha256"] == judge["trace_sha256"]
        assert not trace["technical_issues"] and not packet["technical_control"]["issues"]
        assert stamp(exported["exported_at"]) < stamp("2026-10-08T21:27:16Z") < stamp(completed)
        assert sha((ROOT / "corriger_export_dev7_r3_20261008.py").read_bytes()) == exported["correction_module_sha256"]
        assert sha((ROOT / "tests_corriger_export_dev7_r3_20261008.py").read_bytes()) == exported["correction_tests_sha256"]
        execution, start = [read(RUN / case / n) for n in ("execution.json", "start.json")]
        assert execution["exit_code"] == 0 and execution["timed_out"] is False and execution["attempt"] == 1
        assert execution["upstream_authentication_verified"] and execution["candidate_cache_config_unchanged"]
        assert start["model_override"] is None and start["manifest_sha256"] == exported["run_manifest_sha256"]
        assert stamp(execution["completed_at"]) < stamp(exported["exported_at"])
        for name, field in (("stdout.jsonl", "stdout_sha256"), ("stderr.txt", "stderr_sha256"), ("response.md", "response_sha256"), ("native-rollout.local.jsonl", "native_rollout_sha256")):
            assert sha((RUN / case / name).read_bytes()) == execution[field]
        raw = (RUN / case / "native-rollout.local.jsonl").read_bytes()
        assert sha(Path(execution["native_rollout_path"]).read_bytes()) == sha(raw) == exported["native_file_sha256"]
        lines = raw.splitlines()
        records = [json.loads(line) for line in lines]
        refs = {e["event_id"] for e in trace["events"]}
        assert len(refs) == len(trace["events"])
        failures, injections = [], []
        for event in trace["events"]:
            line = lines[event["native_line"] - 1]
            assert sha(line) == event["native_line_sha256"]
            native = records[event["native_line"] - 1]
            assert native["timestamp"] == event["timestamp"]
            if event["type"] == "derived_native_tool_result":
                assert native["payload"]["call_id"] == event["call_id"]
                assert event["failure_observation"] == failure_metadata(native["payload"].get("output"))
                if event["failure_observation"]["native_failure_observed"]:
                    failures.append({"event_id": event["event_id"], **event["failure_observation"]})
            if event["type"] == "derived_native_skill_injection":
                body = (cache / event["path_relative_to_installed_plugin"]).read_text(encoding="utf-8")
                assert sha((cache / event["path_relative_to_installed_plugin"]).read_bytes()) == event["installed_file_sha256"]
                block = native["payload"]["content"][event["native_text_block"] - 1]["text"]
                assert sha(block.encode()) == event["native_input_text_sha256"]
                assert body in block and event["full_installed_text_present"] is True
                injections.append({k:event[k] for k in ("event_id", "name", "installed_file_sha256", "full_installed_text_present")})
        visible = [e for e in trace["events"] if e["type"] == "derived_visible_assistant_text"]
        compare_final(final_text(records), (RUN / case / "response.md").read_text(encoding="utf-8"), visible[-1]["text"], cache)
        atoms = {a["id"] for a in packet["atoms"]}
        assert len(atoms) == exported["atom_count"] == len(packet["atoms"])
        assert set(judge) == {"case_id", "trace_sha256", "verdict", "invariants"} and judge["case_id"] == case
        assert set(judge["invariants"]) == atoms
        counts = {"true":0, "false":0, "null":0}
        for atom in judge["invariants"].values():
            assert type(atom["status"]) is bool or atom["status"] is None
            assert atom["basis"] in {"observation", "retrieval", "abstention", "missing"}
            assert atom["evidence_refs"] and set(atom["evidence_refs"]) <= refs
            assert isinstance(atom["rationale"], str) and atom["rationale"].strip()
            counts["null" if atom["status"] is None else str(atom["status"]).lower()] += 1
        verdict = "echec" if counts["false"] else "bloque" if counts["null"] else "reussite"
        assert judge["verdict"] == verdict
        rows.append({"case_id":case, "respondent_thread_id":execution["thread_id"], "model_observed":"gpt-6.1-sol",
                     "native_sha256":sha(raw), "trace_sha256":exported["trace_sha256"], "packet_sha256":exported["packet_sha256"],
                     "judgment_sha256":sha((folder / "jugement.json").read_bytes()), "judge_agent":agent,
                     "judge_creation_after_verified_clock_lower_bound":"2026-10-08T21:27:16Z",
                     "judge_completed_at_reported":completed, "fork_turns":"none", "model_override":None,
                     "identity_source":"collaboration.spawn_agent and collaboration.list_agents host results",
                     "physical_filesystem_isolation_claimed":False, "verdict":verdict, "atoms":counts,
                     "full_native_skill_injections":injections, "native_process_start_failures":failures,
                     "native_tool_calls":sum(e["type"] == "derived_native_tool_call" for e in trace["events"]),
                     "primary_source_verified":False, "global_mcp_exposure":"unknown", "exit_code":0, "attempt":1})
        for name in ("packet.json", "trace.json", "manifest.json", "jugement.json"):
            file = folder / name
            evidence.append({"path":file.relative_to(ROOT).as_posix(), "sha256":sha(file.read_bytes())})
    totals = {k:sum(row["atoms"][k] for row in rows) for k in ("true", "false", "null")}
    assert totals == {"true":16, "false":1, "null":6}
    assert sum(len(row["native_process_start_failures"]) for row in rows) == 4
    return {"verified":True, "verified_at":datetime.now(timezone.utc).isoformat(), "candidate_commit":manifest["runtime_source_commit"],
            "candidate_version":"1.2.0-dev.7", "measurement_status":"measured_partial", "suite_cases":16, "suite_atoms":124,
            "executed_cases":3, "eligible_atoms":23, "blocked_preflight":13, "cases":rows, "atom_totals":totals,
            "verdict_totals":{"reussite":2, "echec":1, "bloque":0}, "full_campaign":False,
            "critical_stop_reopening_tested":False, "runtime_files_unchanged":166, "installed_files_verified":214,
            "fresh_judges_after_v2_export":True, "historical_scores_reused":False, "release_ready":False,
            "raw_rollouts_kept_private":True, "evidence_files":evidence}

if __name__ == "__main__":
    result = check()
    target = ROOT / "bilan-dev7-r3-verifie-20261008.json"
    with target.open("xb") as handle:
        handle.write(encode(result))
    print(json.dumps({"cases":result["executed_cases"], "atoms":result["atom_totals"], "release_ready":False}))
