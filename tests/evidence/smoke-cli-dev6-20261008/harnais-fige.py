"""Gèle puis exécute un smoke CLI borné, sans lire les identifiants."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
STATE_PARENT = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90"
STATE = STATE_PARENT / "codex-state"
RUN = ROOT / "qualification-smoke-dev6-cli-20261008-r1"
PROTOCOL = ROOT / "protocole-smoke-dev6-20261008.json"
PLUGIN = ROOT / "Collectivite-corrections-pr5"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read(path: Path):
    return json.loads(path.read_bytes())

def write_new(path: Path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as f:
        f.write(raw)

def environment():
    env = {k: v for k, v in os.environ.items()
           if not re.search(r"TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|AUTHORIZATION", k, re.I)}
    env["CODEX_HOME"] = str(STATE)
    env["CODEX_SQLITE_HOME"] = str(STATE)
    return env

def check_cache(manifest):
    cache = Path(manifest["installed_path"])
    for p, expected in manifest["installed_files"].items():
        assert sha((cache / p).read_bytes()) == expected, f"Cache modifié : {p}"
    assert sha((STATE / "config.toml").read_bytes()) == manifest["config_sha256"]

def prepare(cli: Path):
    assert cli.is_file(), "Exécutable absent"
    assert not RUN.exists(), "Run déjà présent : aucun écrasement"
    protocol = read(PROTOCOL)
    cases = protocol["cases"]
    assert len(cases) == 4 and len({c["id"] for c in cases}) == 4
    installation = read(STATE_PARENT / "installation.json")
    frozen = read(PLUGIN / "docs/qualification/gel-dev6-non-mesure.json")
    assert installation["candidate_commit"] == frozen["candidate_commit"]
    assert installation["installed_manifest_version"] == "1.2.0-dev.6"
    cache = Path(installation["installed_path"])
    files = {p.relative_to(cache).as_posix(): sha(p.read_bytes())
             for p in cache.rglob("*") if p.is_file()}
    assert len(files) == 214
    for p, h in frozen["files"].items():
        assert files[p] == h, f"Gel divergent : {p}"
    assert len([p for p in files if p.startswith("skills/")]) == 166
    config = (STATE / "config.toml").read_bytes()
    assert b'web_search = "disabled"' in config
    assert b'[plugins."collectivite-territoriale@smoke-dev6".mcp_servers."droit-francais"]\nenabled = false' in config.replace(b"\r\n", b"\n")
    version = subprocess.run([str(cli), "--version"], env=environment(), capture_output=True,
                             timeout=20, check=True).stdout.decode("utf-8").strip()
    auth = subprocess.run([str(cli), "login", "status"], env=environment(), capture_output=True, timeout=30)
    assert auth.returncode == 0, "Connexion isolée non confirmée"
    RUN.mkdir()
    (RUN / "workspace").mkdir()
    (RUN / "workspace/README.md").write_bytes(b"# Espace de smoke fictif\nAucune infrastructure reelle ni secret.\n")
    (RUN / "protocole.json").write_bytes(PROTOCOL.read_bytes())
    (RUN / "harnais-fige.py").write_bytes(Path(__file__).read_bytes())
    for c in cases:
        assert re.fullmatch(r"[a-z0-9-]+", c["id"])
        folder = RUN / c["id"]
        folder.mkdir()
        (folder / "prompt.txt").write_bytes(c["prompt"].encode("utf-8"))
    manifest = {"created_at": now(), "host": "Codex CLI", "scope": "native_cli_usage_smoke_four_cases",
        "cli": str(cli), "cli_sha256": sha(cli.read_bytes()), "cli_version": version,
        "runtime_source_commit": frozen["candidate_commit"], "plugin_version": "1.2.0-dev.6",
        "installed_path": str(cache), "installed_files": files, "installed_file_count": 214,
        "runtime_file_count": 166, "config_sha256": sha(config),
        "protocol_sha256": sha(PROTOCOL.read_bytes()), "harness_sha256": sha(Path(__file__).read_bytes()),
        "auth_status_exit_code": auth.returncode, "auth_status": "credentials_present_local",
        "upstream_authentication_verified": False, "model_override": None,
        "attempts_per_case": 1, "timeout_seconds": 240, "sandbox": "read-only",
        "mcp_configured_disabled": True, "web_configured_disabled": True,
        "historical_scores_reused": False, "release_ready": False,
        "raw_rollout_and_stderr_local_only": True,
        "cases": [{"id": c["id"], "prompt_sha256": sha(c["prompt"].encode("utf-8"))} for c in cases]}
    write_new(RUN / "manifest.json", manifest)
    print(json.dumps({"prepared": True, "cases": 4, "cli_version": version, "local_credentials_present": True}))

def execute(case_id):
    manifest = read(RUN / "manifest.json")
    assert sha((RUN / "protocole.json").read_bytes()) == manifest["protocol_sha256"]
    assert sha(Path(__file__).read_bytes()) == manifest["harness_sha256"]
    cli = Path(manifest["cli"])
    assert sha(cli.read_bytes()) == manifest["cli_sha256"]
    case = next(c for c in manifest["cases"] if c["id"] == case_id)
    folder = RUN / case_id
    prompt = (folder / "prompt.txt").read_bytes()
    assert sha(prompt) == case["prompt_sha256"]
    assert not (folder / "start.json").exists(), "Tentative déjà créée : aucune reprise"
    check_cache(manifest)
    argv = [str(cli), "--no-daemon", "--cd", str(RUN / "workspace"),
        "--sandbox", "read-only", "--ask-for-approval", "never", "exec",
        "--skip-git-repo-check", "--json", "--color", "never",
        "--output-last-message", str(folder / "response.md"), "-"]
    write_new(folder / "start.json", {"started_at": now(), "argv": argv, "prompt_sha256": sha(prompt),
        "manifest_sha256": sha((RUN / "manifest.json").read_bytes()), "attempt": 1})
    start = time.monotonic()
    timed_out = False
    with (folder / "stdout.jsonl").open("xb") as out, (folder / "stderr.txt").open("xb") as err:
        process = subprocess.Popen(argv, cwd=RUN / "workspace", env=environment(),
                                   stdin=subprocess.PIPE, stdout=out, stderr=err)
        try:
            process.communicate(input=prompt, timeout=manifest["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            process.communicate(timeout=10)
    cache_unchanged = True
    try:
        check_cache(manifest)
    except AssertionError:
        cache_unchanged = False
    events, invalid_lines = [], 0
    for line in (folder / "stdout.jsonl").read_bytes().splitlines():
        try:
            events.append(json.loads(line))
        except (ValueError, UnicodeError):
            invalid_lines += 1
    starts = [e for e in events if e.get("type") == "thread.started"]
    record = {"completed_at": now(), "exit_code": process.returncode, "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic()-start, 3), "attempt": 1, "event_count": len(events),
        "invalid_jsonl_lines": invalid_lines, "thread_id": starts[0].get("thread_id") if starts else None,
        "candidate_cache_config_unchanged": cache_unchanged,
        "stdout_sha256": sha((folder / "stdout.jsonl").read_bytes()),
        "stderr_sha256": sha((folder / "stderr.txt").read_bytes()),
        "response_sha256": sha((folder / "response.md").read_bytes()) if (folder / "response.md").exists() else None,
        "upstream_authentication_verified": process.returncode == 0 and any(e.get("type") == "turn.completed" for e in events),
        "strict_activation_verified": None, "release_ready": False}
    write_new(folder / "execution.json", record)
    print(json.dumps({"case_id": case_id, **record}, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "run"])
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--case")
    args = parser.parse_args()
    if args.action == "prepare":
        assert args.cli
        prepare(args.cli)
    else:
        execute(args.case)
