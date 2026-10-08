"""Trois tentatives natives hors application, après une lecture réelle sans modèle.

Aucun setup, installation, jugement, reprise ou remplacement de tentative.
L'import ne réalise aucune action. Les traces privées restent dans ROOT.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any
import uuid

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "qualification-coactivation-dev7-cli-r3"
EXPECTED_RUN_MANIFEST_SHA256 = "bc7a40b58836b626c97ab157ad2bc8072325ad25fc0507ef6db8d205fbe31f43"
PS = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
NODE = Path(r"C:\Users\Krn\AppData\Local\OpenAI\Codex\runtimes\cua_node\3dd31cfff853001c\bin\node_repl.exe")
SENTINEL = "LECTURE_SANDBOX_ISOLE_20261008"
WRAPPERS = ("lancer-campagne-dev7-hors-codex.ps1", Path(__file__).name)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def node_gate(environment: dict[str, str]) -> dict[str, Any]:
    """Refuse aussi un chemin inaccessible : aucune terminaison de processus."""
    script = (
        "$ErrorActionPreference='Stop'; "
        "$items=@(Get-CimInstance Win32_Process -Filter \"Name='node_repl.exe'\"); "
        "$unknown=@($items|Where-Object {-not $_.ExecutablePath}); "
        "$blocked=@($items|Where-Object {$_.ExecutablePath -and "
        "[string]::Equals($_.ExecutablePath,'" + str(NODE).replace("'", "''") +
        "',[StringComparison]::OrdinalIgnoreCase)}); "
        "[pscustomobject]@{unknown_paths=$unknown.Count; "
        "blocked_pids=@($blocked|Select-Object -ExpandProperty ProcessId)}|ConvertTo-Json -Compress"
    )
    result = subprocess.run([str(PS), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", script],
                            capture_output=True, timeout=20, env=environment, cwd=ROOT)
    if result.returncode != 0:
        raise RuntimeError("Contrôle des processus inaccessible ; aucune inférence autorisée")
    record = json.loads(result.stdout.decode("utf-8-sig"))
    if record["unknown_paths"] or record["blocked_pids"]:
        raise RuntimeError("Runtime Codex encore actif ou chemin inaccessible ; fermer complètement Codex")
    return {"checked_at": now(), "runtime_path": str(NODE), **record,
            "processes_terminated": False, "success": True}


def fresh_probe(receipt: Path, manifest: dict[str, Any], environment: dict[str, str]) -> bool:
    """API officielle command/exec readOnly ; aucune API de setup ou de modèle."""
    import configurer_sandbox_isole_20261008 as base
    import socle_campagne_native_dev7_20261008 as socle
    base.RUN = receipt
    base.CLI = Path(manifest["cli"])
    base.environment = lambda: dict(environment)
    workspace = receipt / "workspace"
    workspace.mkdir()
    sentinel = workspace / "lecture-synthetique.txt"
    sentinel.write_bytes((SENTINEL + "\n").encode("ascii"))
    skill = socle.DEV6 / "skills/dsi-fpt/SKILL.md"
    expected = manifest["dev6_files_preserved"]["skills/dsi-fpt/SKILL.md"]
    if sha(skill) != expected:
        raise RuntimeError("Skill dev.6 divergent avant la sonde")
    command = ("$ErrorActionPreference='Stop'; Get-Content -LiteralPath '" +
               str(sentinel).replace("'", "''") + "'; (Get-FileHash -LiteralPath '" +
               str(skill).replace("'", "''") + "' -Algorithm SHA256).Hash")
    params = {"command": [str(PS), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
              "cwd": str(workspace), "sandboxPolicy": {"type": "readOnly"}, "timeoutMs": 20000}
    record: dict[str, Any] = {"started_at": now(), "request": params, "success": False,
                             "expected_skill_sha256": expected, "model_inference": False,
                             "auth_secrets_read": False, "setup_requested": False, "release_ready": False}
    client = None
    try:
        client = base.Client("lecture-fraiche", overrides=socle.overrides())
        record["app_server_argv"] = client.argv
        client.initialized()
        record["readiness_before"] = client.request("windowsSandbox/readiness", {}, timeout=10)
        effective = client.request("config/read", {"includeLayers": False}, timeout=10)
        record["effective_config_selected"] = base.config_summary(effective.get("result", {}))
        record["effective_config_error"] = effective.get("error")
        selected = effective.get("result", {}).get("config", {})
        plugin_names = ("collectivite-territoriale@smoke-dev6",
                        "collectivite-territoriale@campagne-dev7-20261008", socle.PLUGIN_ID)
        plugins = selected.get("plugins", {})
        record["effective_plugins_selected"] = {
            name: {"enabled": plugins.get(name, {}).get("enabled"),
                   "droit_francais_enabled": plugins.get(name, {}).get("mcp_servers", {})
                   .get("droit-francais", {}).get("enabled")}
            for name in plugin_names}
        record["effective_permissions_confirmed"] = (
            selected.get("windows", {}).get("sandbox") == "elevated" and
            selected.get("sandbox_mode") == "read-only" and selected.get("web_search") == "disabled" and
            all(record["effective_plugins_selected"][name]["droit_francais_enabled"] is False
                for name in plugin_names) and
            record["effective_plugins_selected"][plugin_names[0]]["enabled"] is False and
            record["effective_plugins_selected"][plugin_names[1]]["enabled"] is False and
            record["effective_plugins_selected"][plugin_names[2]]["enabled"] is True)
        if not record["effective_permissions_confirmed"]:
            raise RuntimeError("Permissions ou désactivation MCP non confirmées ; lecture non lancée")
        response = client.request("command/exec", params, timeout=40)
        record["response"] = response
        received = response.get("result", {})
        lines = [line.strip() for line in received.get("stdout", "").splitlines() if line.strip()]
        record["success"] = (received.get("exitCode") == 0 and SENTINEL in lines and
                             expected.lower() in [line.lower() for line in lines] and
                             "error" not in response)
        # Readiness peut contredire le setup antérieur : garder la réponse, jamais
        # transformer une erreur réelle de lecture/health en résultat réussi.
        record["readiness_after"] = client.request("windowsSandbox/readiness", {}, timeout=10)
        if "error" in record["readiness_before"] or "error" in record["readiness_after"] or "error" in effective:
            record["success"] = False
    except Exception as error:
        record["success"] = False
        record["exception_type"] = type(error).__name__
    finally:
        if client is not None:
            try:
                client.close()
            except Exception as error:
                record["success"] = False
                record["close_error_type"] = type(error).__name__
        record["completed_at"] = now()
        new_json(receipt / "lecture-result.json", record)
    return record["success"] is True


def bounded_child(argv: list[str], environment: dict[str, str], out: Any, err: Any,
                  timeout: float) -> int:
    """À échéance, conserve les traces et arrête uniquement son propre arbre enfant."""
    process = subprocess.Popen(argv, cwd=ROOT, env=environment, stdout=out, stderr=err)
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        if process.poll() is None:
            subprocess.run([str(Path(environment.get("SystemRoot", r"C:\Windows")) / "System32/taskkill.exe"),
                            "/PID", str(process.pid), "/T", "/F"],
                           env=environment, capture_output=True, timeout=10, check=False)
            if process.poll() is None:
                process.kill()
            process.wait(timeout=10)
        raise


def case_once(identifier: str, receipt: Path, frozen: dict[str, Any], environment: dict[str, str],
              deadline: float) -> dict[str, Any]:
    """Un appel au harnais puis un export ; pas de nouvelle tentative implicite."""
    record: dict[str, Any] = {"case_id": identifier, "started_at": now(), "execution_started": False,
                             "execution_exit_code": None, "extraction_started": False,
                             "extraction_exit_code": None, "release_ready": False}
    try:
        if time.monotonic() + 260 > deadline:
            raise RuntimeError("Budget total insuffisant ; tentative non lancée")
        node_gate(environment)
        if sha(RUN / "manifest.json") != frozen["run_manifest_sha256"]:
            raise RuntimeError("Manifest modifié depuis le gel hors application")
        for name, digest in frozen["tools_sha256"].items():
            if sha(ROOT / name) != digest:
                raise RuntimeError("Outillage modifié depuis le gel hors application")
        if (RUN / identifier / "start.json").exists():
            raise RuntimeError("Tentative déjà présente ; aucune reprise ni remplacement")
        argv = [sys.executable, str(ROOT / "campagne_native_dev7_20261008.py"),
                "run", "--run", str(RUN), "--case", identifier]
        record["execution_started"] = True
        with (receipt / (identifier + ".run.stdout.local")).open("xb") as out, \
                (receipt / (identifier + ".run.stderr.local")).open("xb") as err:
            exit_code = bounded_child(argv, environment, out, err,
                                      min(270, max(1, deadline - time.monotonic())))
        record["execution_exit_code"] = exit_code
        folder = RUN / identifier
        record["execution_receipt"] = str(folder / "execution.json")
        # Un échec demeure une preuve : l'exporteur qualifie ses limites.
        if (folder / "execution.json").exists() and (folder / "native-rollout.local.jsonl").exists():
            record["extraction_started"] = True
            with (receipt / (identifier + ".extract.stdout.local")).open("xb") as out, \
                    (receipt / (identifier + ".extract.stderr.local")).open("xb") as err:
                exported_code = bounded_child(
                    [sys.executable, str(ROOT / "extraire_campagne_native_dev7_20261008.py"),
                     "extract", "--run", str(RUN), "--case", identifier], environment, out, err,
                    min(30, max(1, deadline - time.monotonic())))
            record["extraction_exit_code"] = exported_code
            record["judge_packet"] = str(RUN / "judge-packets" / identifier / "packet.json")
        else:
            record["extraction_blocked_reason"] = "trace_native_or_execution_receipt_absent"
    except Exception as error:
        record["exception_type"] = type(error).__name__
        record["exception_summary"] = str(error)[:200] if isinstance(error, RuntimeError) else None
    record["completed_at"] = now()
    new_json(receipt / (identifier + ".json"), record)
    print(json.dumps({"case_id": identifier, "execution_exit_code": record["execution_exit_code"],
                      "extraction_exit_code": record["extraction_exit_code"],
                      "exception_type": record.get("exception_type")}, ensure_ascii=False), flush=True)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controle-seulement", action="store_true")
    args = parser.parse_args()
    import campagne_native_dev7_20261008 as harness
    import socle_campagne_native_dev7_20261008 as socle
    environment, removed = socle.environment()
    node_control = node_gate(environment)
    if not (RUN / "manifest.json").is_file():
        raise RuntimeError("Manifest préparé absent ; aucune préparation, installation ou inférence lancée")
    if sha(RUN / "manifest.json") != EXPECTED_RUN_MANIFEST_SHA256:
        raise RuntimeError("Manifest différent du run R3 gelé ; aucune sonde ni inférence lancée")
    manifest = socle.read(RUN / "manifest.json")
    harness.verify(RUN, manifest)
    for identifier in ("plugin-mcp-indisponible", "plugin-dsi-technique", "plugin-dsi-source-indisponible"):
        if (RUN / identifier / "start.json").exists():
            raise RuntimeError("Run déjà commencé ; aucune reprise ni remplacement")
    if args.controle_seulement:
        print("Précontrôle hors application réussi ; aucune sonde ni inférence lancée.")
        return 0
    lock = RUN / "outside-app-wrapper.lock"
    with lock.open("x", encoding="ascii") as stream:
        stream.write(now())
    receipt = ROOT / ("campagne-dev7-hors-codex-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") +
                      "-" + uuid.uuid4().hex[:8])
    receipt.mkdir()
    deadline = time.monotonic() + 900
    summary: dict[str, Any] = {"started_at": now(), "run": str(RUN), "receipt": str(receipt),
                              "fresh_read_success": False, "cases": [], "judges_started": False,
                              "setup_requested": False, "auth_secrets_read": False,
                              "release_ready": False, "automatic_retry": False}
    try:
        tools = (*WRAPPERS, "configurer_sandbox_isole_20261008.py", *socle.MODULES)
        frozen = {"created_at": now(), "run_manifest_sha256": sha(RUN / "manifest.json"),
                  "tools_sha256": {name: sha(ROOT / name) for name in tools},
                  "node_control": node_control, "environment_identity_names_removed": removed,
                  "model_override": None, "attempt_limit_per_case": 1, "timeout_per_case_seconds": 240,
                  "maximum_wrapper_seconds": 900, "release_ready": False}
        new_json(receipt / "manifest-avant-inference.json", frozen)
        print("Lecture fraîche sans modèle en cours. Aucun setup ni UAC demandé.", flush=True)
        summary["fresh_read_success"] = fresh_probe(receipt, manifest, environment)
        if not summary["fresh_read_success"]:
            print("Lecture fraîche refusée ou échouée ; aucune campagne lancée.", flush=True)
            return 2
        harness.verify(RUN, manifest)
        # Trois appels explicites distincts, dans l'ordre du protocole autorisé.
        summary["cases"].append(case_once("plugin-mcp-indisponible", receipt, frozen, environment, deadline))
        summary["cases"].append(case_once("plugin-dsi-technique", receipt, frozen, environment, deadline))
        summary["cases"].append(case_once("plugin-dsi-source-indisponible", receipt, frozen, environment, deadline))
        return 0 if all(c["execution_exit_code"] == 0 and c["extraction_exit_code"] == 0
                        for c in summary["cases"]) else 2
    except Exception as error:
        summary["exception_type"] = type(error).__name__
        return 2
    finally:
        summary["completed_at"] = now()
        new_json(receipt / "terminee.json", summary)
        lock.unlink()
        print("Reçu local : " + str(receipt / "terminee.json"), flush=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as error:
        print("Précontrôle bloqué : " + str(error)[:250], file=sys.stderr)
        raise SystemExit(2)
