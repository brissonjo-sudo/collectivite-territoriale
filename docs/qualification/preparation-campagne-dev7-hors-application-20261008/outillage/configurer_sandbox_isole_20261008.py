"""Configure le sandbox Windows autorisé, sans modèle ni lecture de secrets."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import threading
import time
import tomllib

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90/codex-state"
CLI = Path(r"C:\Users\Krn\AppData\Local\OpenAI\Codex\bin\9691020b546a15b2\codex.exe")
RUN = ROOT / "configuration-sandbox-isole-20261008-r2"
CACHE = STATE / "plugins/cache/smoke-dev6/collectivite-territoriale/1.2.0-dev.6"
POWERSHELL = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def write_new(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")

def environment() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not re.search(r"TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|AUTHORIZATION", k, re.I) and k not in ("CODEX_CI", "CODEX_SESSION_ID", "CODEX_THREAD_ID", "CODEX_VERSION")}
    env["CODEX_HOME"] = str(STATE)
    env["CODEX_SQLITE_HOME"] = str(STATE)
    return env

def config_summary(value: dict) -> dict:
    c = value.get("config", value)
    keys = ("approval_policy", "approvalPolicy", "sandbox_mode", "sandboxMode", "permissions", "web_search", "webSearch", "windows", "features")
    return {k: c[k] for k in keys if k in c}

def cache_hashes() -> dict[str, str]:
    return {p.relative_to(CACHE).as_posix(): sha(p.read_bytes()) for p in CACHE.rglob("*") if p.is_file()}

class Client:
    """Client JSONL local : aucun thread ni tour modèle n'est créé."""
    def __init__(self, action: str, overrides: list[str] | None = None):
        self.action = action
        self.events: list[dict] = []
        self.pending: list[dict] = []
        self.messages = queue.Queue()
        self.stderr = (RUN / f"{action}-stderr-local.txt").open("xb")
        self.argv = [str(CLI), *(overrides or []), "--no-daemon", "--cd", str(RUN / "workspace"), "--sandbox", "read-only", "--ask-for-approval", "never", "app-server", "--listen", "stdio://"]
        self.process = subprocess.Popen(self.argv, cwd=RUN / "workspace", env=environment(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr)
        def reader():
            for raw in self.process.stdout:
                try:
                    self.messages.put(json.loads(raw))
                except (ValueError, UnicodeError):
                    self.messages.put({"invalid_json_line_sha256": sha(raw)})
            self.messages.put({"server_eof": True})
        threading.Thread(target=reader, daemon=True).start()
        self.counter = 0

    def send(self, value: dict) -> None:
        self.process.stdin.write((json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8"))
        self.process.stdin.flush()

    def next(self, timeout: float) -> dict:
        value = self.messages.get(timeout=timeout)
        if value.get("server_eof"):
            raise RuntimeError("App-server fermé avant la réponse")
        return value

    def request(self, method: str, params: dict, timeout: float = 30) -> dict:
        self.counter += 1
        identifier = self.counter
        self.send({"id": identifier, "method": method, "params": params})
        end = time.monotonic() + timeout
        while True:
            message = self.next(max(0.01, end - time.monotonic()))
            if message.get("id") == identifier:
                return message
            self.pending.append(message)

    def initialized(self) -> dict:
        result = self.request("initialize", {"clientInfo": {"name": "qualification_sandbox_local", "title": "Contrôle sandbox Windows isolé", "version": "1.0.0"}, "capabilities": {"experimentalApi": True}})
        assert "result" in result, result
        self.send({"method": "initialized", "params": {}})
        return result

    def close(self) -> None:
        self.process.stdin.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=10)
        self.stderr.close()

def inspect() -> None:
    assert not RUN.exists(), "Inspection déjà enregistrée"
    RUN.mkdir()
    (RUN / "workspace").mkdir()
    (RUN / "workspace/lecture-synthetique.txt").write_bytes(b"LECTURE_SANDBOX_ISOLE_20261008\n")
    base_config = (STATE / "config.toml").read_bytes()
    (RUN / "config-avant-local.toml").write_bytes(base_config)
    hashes = cache_hashes()
    assert len(hashes) == 214
    schema_process = subprocess.run([str(CLI), "app-server", "generate-json-schema", "--out", str(RUN / "schemas")], env=environment(), cwd=RUN / "workspace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=40)
    assert schema_process.returncode == 0, "Génération du schéma local refusée"
    methods = []
    for path in (RUN / "schemas").rglob("*.json"):
        if "windows" in path.name.lower() or path.name in ("CommandExecParams.json", "SandboxPolicy.json", "ConfigReadParams.json"):
            methods.append(path.relative_to(RUN).as_posix())
    client = Client("inspection")
    try:
        initialization = client.initialized()
        requirements = client.request("configRequirements/read", {})
        effective = client.request("config/read", {"includeLayers": False})
        readiness = client.request("windowsSandbox/readiness", {})
        record = {"created_at": now(), "scope": "isolated_authenticated_profile_read_only_inspection", "authorization": "user_oui_after_concrete_windows_setup_proposal", "cli_version": subprocess.check_output([str(CLI), "--version"], env=environment()).decode().strip(), "cli_sha256": sha(CLI.read_bytes()), "config_before_sha256": sha(base_config), "cache_hashes_before": hashes, "cache_files": 214, "argv": client.argv, "environment_identity_names_removed": ["CODEX_CI", "CODEX_SESSION_ID", "CODEX_THREAD_ID", "CODEX_VERSION"], "initialize_result_keys": list(initialization["result"]), "requirements": requirements, "effective_config_selected": config_summary(effective.get("result", {})), "effective_config_error": effective.get("error"), "readiness": readiness, "generated_schema_paths": methods, "model_inference": False, "auth_secrets_read": False, "raw_stderr_local_only": True}
        assert (STATE / "config.toml").read_bytes() == base_config
        assert cache_hashes() == hashes
        write_new(RUN / "inspection.json", record)
        print(json.dumps({"inspection": "done", "requirements": requirements, "readiness": readiness, "selected_config": record["effective_config_selected"], "schemas": methods}, ensure_ascii=False))
    finally:
        client.close()

def setup() -> None:
    previous = json.loads((RUN / "inspection.json").read_bytes())
    assert not (RUN / "setup-start.json").exists(), "Setup déjà tenté : aucun remplacement"
    assert cache_hashes() == previous["cache_hashes_before"]
    assert sha((STATE / "config.toml").read_bytes()) == previous["config_before_sha256"]
    write_new(RUN / "setup-start.json", {"started_at": now(), "mode": "elevated", "authorization": "explicit_user_oui", "profile": str(STATE), "model_inference": False})
    client = Client("setup")
    record = {"started_at": now(), "mode": "elevated", "success": False, "model_inference": False, "auth_secrets_read": False}
    try:
        client.initialized()
        response = client.request("windowsSandbox/setupStart", {"mode": "elevated", "cwd": str(RUN / "workspace")}, timeout=30)
        record["setup_start_response"] = response
        print(json.dumps({"setupStart": response}, ensure_ascii=False), flush=True)
        if response.get("result", {}).get("started"):
            end = time.monotonic() + 180
            while True:
                pending = next((m for m in client.pending if m.get("method") == "windowsSandbox/setupCompleted"), None)
                message = pending or client.next(max(0.01, end - time.monotonic()))
                if message.get("method") == "windowsSandbox/setupCompleted":
                    record["setup_completed"] = message["params"]
                    record["success"] = message["params"].get("success") is True
                    break
                client.events.append({"method": message.get("method"), "id": message.get("id")})
        record["readiness_after"] = client.request("windowsSandbox/readiness", {})
        effective = client.request("config/read", {"includeLayers": False})
        record["effective_config_after_selected"] = config_summary(effective.get("result", {}))
    except (queue.Empty, RuntimeError, AssertionError) as error:
        record["client_error"] = type(error).__name__ + ": " + str(error)
    finally:
        client.close()
        record["completed_at"] = now()
        record["config_after_sha256"] = sha((STATE / "config.toml").read_bytes())
        record["cache_unchanged"] = cache_hashes() == previous["cache_hashes_before"]
        config = tomllib.loads((STATE / "config.toml").read_text(encoding="utf-8"))
        record["persisted_windows_sandbox"] = config.get("windows", {}).get("sandbox")
        record["persisted_sandbox_mode"] = config.get("sandbox_mode")
        record["persisted_web_search"] = config.get("web_search")
        record["system_changes_audited"] = False
        write_new(RUN / "setup-result.json", record)
    print(json.dumps(record, ensure_ascii=False))

def probe() -> None:
    result = json.loads((RUN / "setup-result.json").read_bytes())
    assert result["success"] and result["cache_unchanged"]
    assert result["persisted_windows_sandbox"] == "elevated"
    assert result["persisted_sandbox_mode"] == "read-only" and result["persisted_web_search"] == "disabled"
    assert not (RUN / "lecture-result.json").exists()
    literal = str(RUN / "workspace/lecture-synthetique.txt").replace("'", "''")
    skill = str(CACHE / "skills/dsi-fpt/SKILL.md").replace("'", "''")
    command = f"$ErrorActionPreference='Stop'; Get-Content -LiteralPath '{literal}'; (Get-FileHash -LiteralPath '{skill}' -Algorithm SHA256).Hash"
    params = {"command": [str(POWERSHELL), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command], "cwd": str(RUN / "workspace"), "sandboxPolicy": {"type": "readOnly"}, "timeoutMs": 20000}
    client = Client("lecture")
    try:
        client.initialized()
        response = client.request("command/exec", params, timeout=40)
        expected = sha((CACHE / "skills/dsi-fpt/SKILL.md").read_bytes())
        received = response.get("result", {})
        success = received.get("exitCode") == 0 and "LECTURE_SANDBOX_ISOLE_20261008" in received.get("stdout", "") and expected.lower() in received.get("stdout", "").lower()
        record = {"created_at": now(), "request": params, "response": response, "success": success, "expected_skill_sha256": expected, "model_inference": False, "auth_secrets_read": False, "release_ready": False}
        write_new(RUN / "lecture-result.json", record)
        print(json.dumps(record, ensure_ascii=False))
    finally:
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["inspect", "setup", "probe"])
    args = parser.parse_args()
    {"inspect": inspect, "setup": setup, "probe": probe}[args.action]()
