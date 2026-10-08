"""Extrait les seuls événements du smoke ; contextes et inventaires restent privés."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "qualification-smoke-dev6-cli-20261008-r1"
STATE = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90/codex-state"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_new(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")

manifest = json.loads((RUN / "manifest.json").read_bytes())
cache = Path(manifest["installed_path"])
all_cases = []
for case in manifest["cases"]:
    folder = RUN / case["id"]
    execution = json.loads((folder / "execution.json").read_bytes())
    tid = execution["thread_id"]
    matches = list((STATE / "sessions").rglob(f"*{tid}.jsonl"))
    assert len(matches) == 1
    native = matches[0]
    raw_lines = native.read_bytes().splitlines()
    events, injections, assistants, tool_calls, exclusions = [], [], [], [], []
    model = None
    for index, raw in enumerate(raw_lines, 1):
        event = json.loads(raw)
        payload = event.get("payload", {})
        kind = event.get("type")
        origin = {"native_line": index, "native_line_sha256": sha(raw), "timestamp": event.get("timestamp")}
        if kind == "session_meta":
            assert payload["id"] == tid
            events.append({**origin, "type": kind, "id": tid, "cli_version": payload.get("cli_version"), "source": payload.get("source")})
        elif kind == "turn_context":
            model = payload.get("model")
            assert payload.get("approval_policy") == "never"
            assert payload.get("sandbox_policy", {}).get("type") == "read-only"
            events.append({**origin, "type": kind, "model": model, "approval_policy": "never", "sandbox_policy": {"type": "read-only"}})
        elif kind == "response_item" and payload.get("type") == "message":
            role = payload.get("role")
            texts = [c.get("text", "") for c in payload.get("content", [])]
            if role == "assistant":
                text = "\n".join(texts)
                item = {**origin, "type": "assistant_message", "phase": payload.get("phase"), "channel": payload.get("channel"), "text": text}
                assistants.append(item)
                events.append(item)
            elif role == "user":
                for text in texts:
                    if text == (folder / "prompt.txt").read_text(encoding="utf-8"):
                        events.append({**origin, "type": "submitted_prompt", "sha256": sha(text.encode("utf-8"))})
                    elif "<skill>" in text:
                        names = re.findall(r"<name>(.*?)</name>", text)
                        paths = re.findall(r"<path>(.*?)</path>", text)
                        assert len(names) == len(paths) == 1
                        skill_path = Path(paths[0])
                        relative = skill_path.resolve().relative_to(cache.resolve()).as_posix()
                        expected = (cache / relative).read_bytes()
                        assert sha(expected) == manifest["installed_files"][relative]
                        complete = expected.decode("utf-8") in text
                        assert complete, "Injection partielle : ne pas confirmer l'activation"
                        item = {**origin, "type": "native_skill_injection", "name": names[0], "path_relative_to_installed_plugin": relative,
                            "installed_file_sha256": sha(expected), "full_installed_text_present": complete,
                            "native_input_text_sha256": sha(text.encode("utf-8")), "native_input_text_chars": len(text),
                            "source_body_omitted_from_public_extract": True}
                        injections.append(item)
                        events.append(item)
                    else:
                        exclusions.append({**origin, "reason": "environment_or_other_user_context_omitted"})
            else:
                exclusions.append({**origin, "reason": "system_or_developer_context_omitted"})
        elif kind == "response_item" and payload.get("type") in ("custom_tool_call", "function_call"):
            item = {**origin, "type": "tool_call", "tool": payload.get("name"), "call_id": payload.get("call_id"),
                "input": payload.get("input", payload.get("arguments"))}
            tool_calls.append(item)
            events.append(item)
        elif kind == "response_item" and payload.get("type") in ("custom_tool_call_output", "function_call_output"):
            output = payload.get("output", "")
            serialized = json.dumps(output, ensure_ascii=False)
            blocked = "blocked by policy" in serialized
            inventory = "ALL_TOOLS" in json.dumps(tool_calls[-1] if tool_calls else {})
            events.append({**origin, "type": "tool_result", "call_id": payload.get("call_id"),
                "blocked_by_policy": blocked, "tool_inventory_result_omitted": inventory,
                "raw_output_omitted": True, "raw_output_sha256": sha(serialized.encode("utf-8")),
                "tool_read_succeeded": False if blocked else None})
        else:
            exclusions.append({**origin, "reason": "duplicate_status_internal_or_other_record_omitted"})
    assert assistants and execution["exit_code"] == 0 and not execution["timed_out"]
    assert model == "gpt-6.1-sol"
    last = assistants[-1]["text"]
    assert last == (folder / "response.md").read_text(encoding="utf-8").strip("\n") or last.strip("\n") == (folder / "response.md").read_text(encoding="utf-8").strip("\n")
    report = {"case_id": case["id"], "thread_id": tid, "model_observed": model,
        "native_session_basename": native.name, "native_session_sha256": sha(native.read_bytes()),
        "native_line_count": len(raw_lines), "events": events, "excluded_records": exclusions,
        "actual_native_injections": injections, "first_visible_assistant_text": assistants[0]["text"],
        "first_visible_assistant_starts_STOP": assistants[0]["text"].lstrip().startswith("STOP"),
        "tool_call_count": len(tool_calls), "policy_rejection_count": sum(e.get("blocked_by_policy", False) for e in events),
        "final_response_sha256": execution["response_sha256"], "historical_scores_reused": False,
        "source_provenance_limit": "Raw rollout, developer context, installed skill bodies and tool inventories remain local; line hashes and injection attestations retained.",
        "effective_mcp_exposure_verified": False, "release_ready": False}
    write_new(folder / "native-sanitise.json", report)
    all_cases.append({k: report[k] for k in ("case_id", "thread_id", "model_observed", "first_visible_assistant_starts_STOP", "tool_call_count", "policy_rejection_count")}
                   | {"native_injected_skills": [s["name"] for s in injections], "native_extract_sha256": sha((folder / "native-sanitise.json").read_bytes())})
write_new(RUN / "extraction-native.json", {"created_at": datetime.now(timezone.utc).isoformat(), "cases": all_cases,
    "extractor_sha256": sha(Path(__file__).read_bytes()), "runtime_source_commit": manifest["runtime_source_commit"],
    "scope": "four_case_cli_smoke", "full_campaign": False, "release_ready": False})
print(json.dumps(all_cases, ensure_ascii=False))
