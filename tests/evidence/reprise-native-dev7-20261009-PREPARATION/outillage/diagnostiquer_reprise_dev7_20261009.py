"""Scelle un diagnostic nouveau sans modifier les preuves de la mesure R3."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90/codex-state"
PRECEDING = ROOT / "diagnostic-reprise-dev7-20261009"
OUT = ROOT / "diagnostic-reprise-dev7-20261009-v2"

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def write(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

def main() -> None:
    assert not OUT.exists(), "Diagnostic existant : aucune réécriture"
    # Le snapshot v1 est conservé ; harmonise les SHA de lignes avec R3 (sans EOL).
    snapshot = (PRECEDING / "sandbox-snapshot.local.txt").read_bytes()
    lines = snapshot.splitlines(keepends=True)
    links = [(68,"plugin-mcp-indisponible",17), (81,"plugin-dsi-technique",16),
             (94,"plugin-dsi-technique",39), (107,"plugin-dsi-source-indisponible",18)]
    correlations = []
    for log_no, case, native_no in links:
        log = lines[log_no-1].decode("utf-8")
        assert "(os error 32)" in log and "\\bin\\node.exe" in log
        assert "open ACL target for root-only update" in log
        logged_at = re.match(r"^\[([^]]+)\]", log).group(1)
        native_path = ROOT / "qualification-coactivation-dev7-cli-r3" / case / "native-rollout.local.jsonl"
        native_bytes = native_path.read_bytes()
        execution = json.loads((native_path.parent / "execution.json").read_bytes())
        assert digest(native_bytes) == execution["native_rollout_sha256"]
        native_line = native_bytes.splitlines(keepends=True)[native_no-1]
        row = json.loads(native_line)
        assert "setup refresh had errors" in json.dumps(row)
        assert row["type"] == "response_item" and row["payload"]["type"] == "custom_tool_call_output"
        gap = (datetime.fromisoformat(row["timestamp"]) - datetime.fromisoformat(logged_at)).total_seconds()
        assert 0 <= gap <= 2, "Chronologie ambiguë"
        correlations.append({"case_id":case,"native_event_id":f"native-L{native_no:06d}",
            "native_rollout_sha256":digest(native_bytes), "native_line_sha256":digest(native_line.rstrip(b"\r\n")),
            "native_timestamp":row["timestamp"], "sandbox_log_line":log_no,
            "sandbox_log_line_sha256":digest(lines[log_no-1].rstrip(b"\r\n")), "sandbox_timestamp":logged_at,
            "timestamp_gap_seconds":gap, "windows_error":32,
            "mechanism":"runtime_acl_refresh_file_in_use", "runtime_binary":"node.exe",
            "historical_owner_pid_verified":False, "auto_review_rejection_established":False})
    probe_names = ["lecture-sandbox-capacites-20261008-r1", "lecture-sandbox-capacites-20261008-r2-service",
        "lecture-sandbox-capacites-20261008-r4-node", "lecture-sandbox-capacites-20261009-r5-dependances"]
    probes = []
    for name in probe_names:
        raw = (ROOT / name / "controle.json").read_bytes()
        value = json.loads(raw)
        assert value["success"] is False and value["model_inference"] is False
        assert value["configuration_file_unchanged"] and value["installed_files_unchanged"]
        probes.append({"probe_id":name,"receipt_sha256":digest(raw),"success":False,
            "model_inference":False,"configuration_file_unchanged":True,"installed_files_unchanged":True,
            "windows_sandbox_service_requested":value.get("windows_sandbox_service_requested",False),
            "node_path_override_requested":bool(value.get("node_override_returned")),
            "workspace_dependencies_disabled":value.get("workspace_dependencies_disabled",False)})
    mcp_path = ROOT / "precontrole-mcp-dev7-20261008-r1/precontrole-mcp-assaini.json"
    mcp = json.loads(mcp_path.read_bytes())
    assert mcp["servers"][0]["authStatus"] == "notLoggedIn" and mcp["servers"][0]["tool_count"] == 0
    oauth_path = ROOT / "connexion-mcp-juridique-20261009-r1/resultat-assaini.json"
    oauth = json.loads(oauth_path.read_bytes())
    assert oauth["completed"] is False and oauth["flow_timeout"] is True
    assert oauth["configuration_file_unchanged"] and oauth["automatic_retry"] is False
    result = {"created_at":datetime.now(timezone.utc).isoformat(),"schema_version":"dev7-reprise-diagnostic-v2",
        "preceding_diagnostic_sha256":digest((PRECEDING/"diagnostic-assaini.json").read_bytes()),
        "line_hash_policy":"UTF-8 native line bytes excluding CR/LF terminators, as in R3",
        "candidate_commit":"fb186b4951b95adabf05904f8a34995720588be3",
        "sandbox_log_snapshot_sha256":digest(snapshot),"sandbox_log_snapshot_private":True,
        "correlations":correlations,"correlation_method":"chronology_and_identical_failure_mechanism",
        "historical_process_owner_not_inferred":True,"app_open_fix_verified":False,
        "cold_launcher_fix_verified":False,"safe_probes":probes,
        "incomplete_probe_excluded":"lecture-sandbox-capacites-20261008-r3-node failed before RPC: missing runtime path",
        "mcp_preflight_receipt_sha256":digest(mcp_path.read_bytes()),
        "mcp_auth_status_observed":"notLoggedIn","legal_tool_count_observed":0,
        "primary_text_retrieved":False,"oauth_receipt_sha256":digest(oauth_path.read_bytes()),
        "oauth_attempt":{"started_at":oauth["started_at"],"completed_at":oauth["completed_at"],
            "completed":False,"flow_timeout":True,"automatic_retry":False,"auth_secrets_read":False},
        "persisted_config_unchanged":True,"historical_respondents_rerun":False,
        "new_campaign_measured":False,"historical_scores_reused":False,"release_ready":False}
    OUT.mkdir()
    with (OUT / "sandbox-snapshot.local.txt").open("xb") as stream:
        stream.write(snapshot)
    write(OUT / "diagnostic-assaini.json", result)
    write(OUT / "precontrole-mcp-assaini.json", mcp)
    write(OUT / "oauth-resultat-assaini.json", oauth)
    print(json.dumps({"diagnostic_created":True,"correlations":len(correlations),"oauth_timeout":True,"release_ready":False}))

if __name__ == "__main__":
    main()
