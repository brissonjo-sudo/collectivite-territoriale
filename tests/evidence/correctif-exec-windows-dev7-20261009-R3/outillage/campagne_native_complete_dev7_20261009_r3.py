"""Campagne native complète future ; l'import ne réalise aucune opération.

Les seuls modes avec effets sont explicitement appelés par le coordinateur.
Précontrôles sans modèle, aucune installation/configuration/login automatique.
Les preuves R3 et les cinq modules historiques ne sont jamais modifiés.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
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
from typing import Any, Callable
import uuid

ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "protocole-native-dev7-complet-20261009-r3.json"
DEFAULT_RUN = ROOT / "qualification-coactivation-dev7-complet-20261009-r3"
STATE = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90/codex-state"
PS = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
MAX_RPC_BYTES = 8 * 1024 * 1024


class GateError(ValueError):
    """Le précontrôle bloque sans corriger ni recommencer implicitement."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def write_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def destination(path: Path) -> Path:
    path = path.resolve()
    require(path.is_relative_to(ROOT) and path != ROOT and not path.is_relative_to(STATE),
            "Destination hors workspace ou dans l'état protégé")
    require(not any(part.startswith("qualification-coactivation-dev7-cli-r") for part in path.parts),
            "Destination historique protégée")
    return path


def environment(source: dict[str, str] | None = None) -> tuple[dict[str, str], list[str]]:
    """Noms d'identité seulement ; aucune valeur de secret ou auth lue."""
    source = dict(os.environ) if source is None else source
    removed = sorted(k for k in source if k.upper().startswith("CODEX"))
    env = {k: v for k, v in source.items() if not k.upper().startswith("CODEX")
           and not re.search(r"TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|AUTHORIZATION", k, re.I)}
    env.update(CODEX_HOME=str(STATE), CODEX_SQLITE_HOME=str(STATE))
    return env, removed


def inventory(folder: Path) -> dict[str, str]:
    require(folder.is_dir(), "Cache installé absent")
    return {p.relative_to(folder).as_posix(): sha(p.read_bytes()) for p in folder.rglob("*") if p.is_file()}


def validate_protocol(value: dict[str, Any], proposal: dict[str, Any], suite: list[dict[str, Any]]) -> None:
    """Compare la suite complète, les prompts, les modes et les oracles."""
    require(value["candidate_commit"] == proposal["candidate_commit"]
            and value["candidate_tree"] == proposal["candidate_tree"]
            and value["plugin_version"] == "1.2.0-dev.7", "Candidat différent")
    require(value["cases"] == proposal["cases"], "Prompt, question ou entrée juge modifiés")
    require(len(suite) == len(value["cases"]) == 16 and len({c["id"] for c in suite}) == 16,
            "Suite différente des seize cas")
    require(sum(len(c["invariant_objects"]) for c in suite) == 124, "Nombre d'atomes différent")
    by_id = {c["id"]: c for c in suite}
    forced = 0
    for case in value["cases"]:
        original = by_id[case["case_id"]]
        require(case["historical_question"] == original["prompt"]
                and case["judge_only_invariant_objects"] == original["invariant_objects"],
                "Questions/atomes divergents")
        require(case["judge_only_oracle"] == {k: original[k] for k in
                ("skills", "activation_sequence", "activation_sequence_semantics")}, "Oracle divergent")
        require(case["source_requirements_unchanged"] == {k: original[k] for k in
                ("mcp_mode", "web_mode", "source_evidence_policy")}, "Modes de sources divergents")
        require(sha(canonical(original)) == case["original_case_canonical_sha256"], "Cas source divergent")
        require(sha(case["native_prompt"].encode("utf-8")) == case["prompt_sha256_utf8"], "Prompt divergent")
        require(sha(original["prompt"].encode("utf-8")) == case["historical_question_sha256_utf8"],
                "Empreinte question divergente")
        if case["activation_mode"] == "spontaneous":
            require("$collectivite-territoriale:" not in case["native_prompt"]
                    and all(name not in case["native_prompt"] for name in original["skills"]),
                    "Oracle divulgué dans le prompt spontané")
        else:
            forced += 1
            markers = " ".join("$collectivite-territoriale:" + name for name in original["activation_sequence"])
            require(case["native_prompt"].startswith(markers + "\n" + original["prompt"]),
                    "Ordre des marqueurs forcés divergent")
    require(forced == 11 and value["attempts_per_case"] == 1
            and value["timeout_seconds_per_case"] == 240, "Limites ou modes modifiés")


def inputs(check_source: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    """Lecture explicite ; aucun appel à un modèle, ni import exécutant un harnais."""
    value = read(PROTOCOL)
    for name, digest in value["predecessor_tools_sha256"].items():
        require(sha((ROOT / name).read_bytes()) == digest, "Outillage v1 modifié : " + name)
    proposal_path = ROOT / value["proposal_path"]
    require(sha(proposal_path.read_bytes()) == value["proposal_sha256"], "Proposition historique modifiée")
    proposal = read(proposal_path)
    for kind in ("suite", "rubric", "candidate_gel"):
        require(sha(Path(proposal[kind + "_path"]).read_bytes())
                == proposal[kind + "_sha256"] == value[kind + "_sha256"], "Source figée modifiée : " + kind)
    for name, digest in value["immutable_tools_sha256"].items():
        require(sha((ROOT / name).read_bytes()) == digest, "Module historique modifié : " + name)
    validate_protocol(value, proposal, read(Path(proposal["suite_path"])))
    r3 = read(ROOT / value["r3_manifest_path"])
    require(sha((ROOT / value["r3_manifest_path"]).read_bytes()) == value["r3_manifest_sha256"],
            "Manifeste R3 modifié")
    require(r3["installed_path"] == value["installed_path"] and len(r3["installed_files"]) == 214,
            "Cache de référence divergent")
    require(sha(Path(value["cli"]).read_bytes()) == value["cli_sha256"], "Binaire CLI divergent")
    require(inventory(Path(value["installed_path"])) == r3["installed_files"], "Cache candidat modifié")
    if check_source:
        # Module pur dont l'empreinte vient d'être vérifiée ; ni prepare ni run appelés.
        import socle_campagne_native_dev7_20261008 as historical
        blobs, _ = historical.source_blobs(proposal)
        require({name: sha(raw) for name, raw in blobs.items()} == r3["installed_files"],
                "Source Git différente du cache installé")
    return value, r3


def overrides(protocol: dict[str, Any], case: dict[str, Any]) -> list[str]:
    """Overrides ponctuels seulement, jamais écrits dans config.toml."""
    mode = case["source_requirements_unchanged"]
    require(mode["mcp_mode"] in ("required", "disabled")
            and mode["web_mode"] in ("official_source", "disabled"), "Mode source inconnu")
    candidate = "collectivite-territoriale@campagne-dev7-20261008-r3"
    old = ("collectivite-territoriale@smoke-dev6", "collectivite-territoriale@campagne-dev7-20261008")
    values = ['windows.sandbox="elevated"', 'sandbox_mode="read-only"', 'approval_policy="never"',
              'web_search="' + ("live" if mode["web_mode"] == "official_source" else "disabled") + '"']
    values += [f"features.{feature}=false" for feature in protocol["disabled_features"]]
    for name in old:
        values += [f"plugins.{name}.enabled=false", f"plugins.{name}.mcp_servers.droit-francais.enabled=false"]
    values += [f"plugins.{candidate}.enabled=true",
               f"plugins.{candidate}.mcp_servers.droit-francais.enabled="
               + ("true" if mode["mcp_mode"] == "required" else "false")]
    return [part for value in values for part in ("-c", value)]


def configuration_check(config: dict[str, Any], protocol: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Valide les valeurs effectivement retournées, pas la seule ligne de commande."""
    mode = case["source_requirements_unchanged"]
    require(config.get("windows", {}).get("sandbox") == "elevated"
            and config.get("sandbox_mode") == "read-only"
            and config.get("approval_policy") == "never", "Permissions effectives non conformes")
    web = "live" if mode["web_mode"] == "official_source" else "disabled"
    require(config.get("web_search") == web, "Web effectif différent du cas")
    features = config.get("features", {})
    require(all(features.get(name) is False for name in protocol["disabled_features"]),
            "Capacité navigateur/ordinateur/code-mode/apps non désactivée effectivement")
    expected = "collectivite-territoriale@campagne-dev7-20261008-r3"
    plugins = config.get("plugins", {})
    candidate = plugins.get(expected, {})
    require(candidate.get("enabled") is True and candidate.get("mcp_servers", {}).get("droit-francais", {})
            .get("enabled") is (mode["mcp_mode"] == "required"), "Plugin ou MCP effectif divergent")
    require(all(setting.get("enabled") is False for name, setting in plugins.items() if name != expected),
            "Autre plugin effectif activé")
    require(not any(setting.get("enabled", True) is not False
                    for setting in config.get("mcp_servers", {}).values()), "MCP global non isolé")
    return {"windows_backend": "elevated", "sandbox": "read-only", "approval_policy": "never",
            "web_search": web, "disabled_features": protocol["disabled_features"],
            "candidate_plugin_id": expected, "legal_mcp_enabled": mode["mcp_mode"] == "required",
            "effective_config_private_sha256": sha(canonical(config))}


def legal_inventory_check(servers: list[dict[str, Any]], case: dict[str, Any]) -> dict[str, Any]:
    """Schémas réellement découverts ; leur présence n'atteste aucune règle de droit."""
    wanted = "collectivite-territoriale@campagne-dev7-20261008-r3"
    required = case["source_requirements_unchanged"]["mcp_mode"] == "required"
    require(all(server.get("pluginId") == wanted and server.get("name") == "droit-francais"
                for server in servers), "Serveur MCP étranger effectivement exposé")
    if not required:
        require(not servers, "MCP exposé dans un cas sans sources")
        return {"mcp_mode": "disabled", "servers": [], "source_primary_verified": False}
    require(len(servers) == 1, "Serveur juridique absent ou ambigu")
    server = servers[0]
    require(server.get("authStatus") in ("oAuth", "bearerToken")
            and server.get("toolsError") is None, "MCP juridique non authentifié ou découverte échouée")
    require(server.get("httpOrigin") == "https://droit-francais-skill.onrender.com",
            "Origine effective du serveur juridique divergente ou absente")
    tools = server.get("tools")
    require(isinstance(tools, dict) and bool(tools), "Aucun outil juridique découvert")
    require(all(isinstance(tool, dict) and isinstance(tool.get("inputSchema"), dict)
                and tool["inputSchema"].get("type") == "object" for tool in tools.values()),
            "Schéma d'outil juridique absent ou inconnu")
    schema_names = sorted(tools)
    require(any(re.search(r"fetch|get_article|article|get_decision", name, re.I) for name in schema_names),
            "Aucun outil annoncé de récupération documentaire primaire")
    return {"mcp_mode": "required", "server_name": "droit-francais", "plugin_id": wanted,
            "auth_status": server["authStatus"], "http_origin": server["httpOrigin"],
            "schema_count": len(tools), "schemas": tools, "schemas_sha256": sha(canonical(tools)),
            "source_primary_verified": None, "legal_currentness_verified": None}


def node_gate(env: dict[str, str], handler: Callable[[list[str], dict[str, str]], Any] | None = None,
              private_sink: Path | None = None) -> dict[str, Any]:
    """CIM natif hors application ; toute inconnue bloque, aucun processus terminé."""
    script = ("$ErrorActionPreference='Stop'; $items=@(Get-CimInstance Win32_Process | "
              "Where-Object {$_.Name -in @('node.exe','node_repl.exe')}); "
              "[pscustomobject]@{processes=@($items | ForEach-Object {"
              "[pscustomobject]@{name=$_.Name;pid=$_.ProcessId;path=$_.ExecutablePath}})} "
              "| ConvertTo-Json -Depth 4 -Compress")
    argv = [str(PS), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", script]
    if handler is None:
        result = subprocess.run(argv, env=env, capture_output=True, timeout=20, cwd=ROOT)
        if private_sink is not None:
            write_new(private_sink / "cim.private.json", {"argv": argv, "exit_code": result.returncode,
                "stdout": result.stdout.decode("utf-8-sig", errors="replace")[:128*1024],
                "stderr": result.stderr.decode("utf-8-sig", errors="replace")[:128*1024],
                "stdout_complete": len(result.stdout) <= 128*1024,
                "stderr_complete": len(result.stderr) <= 128*1024})
        require(result.returncode == 0, "Inventaire CIM inaccessible ; fermer Codex et utiliser le caller natif")
        require(len(result.stdout) <= 128 * 1024, "Inventaire CIM tronqué ou trop volumineux")
        record = json.loads(result.stdout.decode("utf-8-sig"))
    else:
        record = handler(argv, env)
    require(isinstance(record, dict) and isinstance(record.get("processes"), list), "Inventaire CIM incomplet")
    bin_path = read(PROTOCOL)["process_gate"]["cua_bin_path"].replace("\\", "/").casefold().rstrip("/")
    blocked = []
    for process in record["processes"]:
        require(isinstance(process, dict) and isinstance(process.get("path"), str)
                and bool(process["path"]) and isinstance(process.get("pid"), int)
                and process.get("name", "").casefold() in ("node.exe", "node_repl.exe"),
                "Chemin ou identité d'un processus Node inaccessible")
        require(Path(process["path"]).is_absolute(), "Chemin CIM non absolu")
        resolved = Path(process["path"]).resolve().as_posix().casefold()
        if resolved in (bin_path + "/node.exe", bin_path + "/node_repl.exe"):
            blocked.append(process["pid"])
    require(not blocked, "Runtime CUA Node encore actif ; aucune terminaison automatique")
    return {"checked_at": now(), "checked_names": ["node.exe", "node_repl.exe"],
            "checked_bin_path": bin_path, "process_inventory_verified": True,
            "blocked_pids": [], "unknown_paths": 0, "processes_terminated": False,
            "app_open_fix_verified": False}


class Client:
    """RPC stdio strictement sans thread ni tour ; sorties privées bornées."""
    def __init__(self, cli: Path, cwd: Path, args: list[str], env: dict[str, str]):
        self.argv = [str(cli), "--no-daemon", "--cd", str(cwd), *args,
                     "--sandbox", "read-only", "--ask-for-approval", "never", "app-server", "--listen", "stdio://"]
        self.process = subprocess.Popen(self.argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.messages: queue.Queue = queue.Queue()
        self.bytes_received = 0
        self.private_events: list[dict[str, Any]] = []
        self.stderr = bytearray()
        self.counter = 0
        def output_reader():
            try:
                for raw in self.process.stdout:
                    self.bytes_received += len(raw)
                    if self.bytes_received > MAX_RPC_BYTES:
                        self.messages.put({"capture_limit": True})
                        continue
                    try:
                        self.messages.put(json.loads(raw))
                    except (ValueError, UnicodeError):
                        self.messages.put({"invalid_jsonl": True})
            finally:
                self.messages.put({"server_eof": True})
        def error_reader():
            while block := self.process.stderr.read(65536):
                if len(self.stderr) < MAX_RPC_BYTES:
                    self.stderr.extend(block[:MAX_RPC_BYTES-len(self.stderr)])
        threading.Thread(target=output_reader, daemon=True).start()
        threading.Thread(target=error_reader, daemon=True).start()

    def send(self, value: dict[str, Any]) -> None:
        self.process.stdin.write(canonical(value) + b"\n")
        self.process.stdin.flush()

    def request(self, method: str, params: dict[str, Any], timeout: float = 30) -> dict[str, Any]:
        self.counter += 1
        identifier = self.counter
        request = {"id": identifier, "method": method, "params": params}
        self.private_events.append({"request": request})
        self.send(request)
        deadline = time.monotonic() + timeout
        while True:
            message = self.messages.get(timeout=max(0.01, deadline-time.monotonic()))
            require(not any(message.get(k) for k in ("server_eof", "invalid_jsonl", "capture_limit")),
                    "RPC fermée/incomplète ou capture dépassée")
            self.private_events.append({"response": message})
            require(not ("method" in message and "id" in message), "Demande serveur interactive non autorisée")
            if message.get("id") == identifier:
                require("error" not in message and "result" in message, "RPC échouée : " + method)
                return message["result"]
            require(time.monotonic() < deadline, "Délai RPC dépassé")

    def initialized(self) -> None:
        self.request("initialize", {"clientInfo": {"name": "qualification_complete_native", "version": "1.0.0"},
                                   "capabilities": {"experimentalApi": True}})
        self.send({"method": "initialized", "params": {}})

    def close(self) -> None:
        self.process.stdin.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate()  # Son propre enfant seulement.
            self.process.wait(timeout=10)


def validate_sandbox_read(response: dict[str, Any], expected_hash: str) -> None:
    """Valide strictement la sortie bornée de la seule commande de lecture SHA."""
    require(isinstance(response, dict) and type(response.get("exitCode")) is int
            and response["exitCode"] == 0, "Lecture sandbox réelle non établie")
    stdout, stderr = response.get("stdout"), response.get("stderr")
    require(isinstance(stdout, str) and isinstance(stderr, str), "Capture de lecture absente ou malformée")
    require(len(stdout.encode("utf-8")) <= 4096 and len(stderr.encode("utf-8")) <= 4096,
            "Capture de lecture trop grande")
    require(not any(response.get(k) is True for k in
                    ("truncated", "stdoutTruncated", "stderrTruncated", "stdout_truncated", "stderr_truncated")),
            "Capture de lecture tronquée")
    require(stdout.strip().casefold() == expected_hash.casefold() and not stderr.strip(),
            "Empreinte de lecture inexacte ou erreur sur stderr")


def preflight(protocol: dict[str, Any], r3: dict[str, Any], case: dict[str, Any],
              workspace: Path, client_factory: Callable[..., Any] = Client,
              process_handler: Callable[..., Any] | None = None) -> dict[str, Any]:
    """Avant prepare et avant chaque tentative ; ne lance aucune inférence."""
    env, removed = environment()
    config_before = (STATE / "config.toml").read_bytes()
    cache = Path(protocol["installed_path"])
    receipt_folder = destination(ROOT / ("precontrole-complet-dev7-" +
        datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]))
    receipt_folder.mkdir()
    record = {"started_at": now(), "case_id": case["case_id"], "status": "blocked",
              "step": "process_inventory", "model_inference": False, "setup_attempted": False,
              "oauth_login_attempted": False, "persistent_config_mutation_requested": False,
              "release_ready": False, "receipt_directory": str(receipt_folder)}
    client = None
    try:
        require(inventory(cache) == r3["installed_files"], "Cache divergent avant précontrôle")
        processes = node_gate(env, process_handler, receipt_folder)
        record["processes"] = processes
        record["step"] = "effective_configuration"
        client = client_factory(Path(protocol["cli"]), workspace, overrides(protocol, case), env)
        client.initialized()
        effective = client.request("config/read", {"includeLayers": False}, timeout=15)
        selected = configuration_check(effective.get("config", {}), protocol, case)
        record["configuration"] = selected
        record["step"] = "legal_source_discovery"
        servers = []
        cursor = None
        pages = 0
        while True:
            params = {"detail": "toolsAndAuthOnly", "limit": 100}
            if cursor:
                params["cursor"] = cursor
            result = client.request("mcpServerStatus/list", params, timeout=45)
            require(isinstance(result.get("data"), list), "Inventaire MCP absent")
            servers.extend(result["data"])
            pages += 1
            cursor = result.get("nextCursor")
            require(pages <= 10, "Inventaire MCP incomplet ou pagination non bornée")
            if not cursor:
                break
        legal = legal_inventory_check(servers, case)
        record["legal_inventory"] = legal
        record["step"] = "sandbox_read"
        # Même chaîne command/exec lecture seule que le caller prévu, sans modèle.
        skill = cache / "skills/dsi-fpt/SKILL.md"
        literal = str(skill).replace("'", "''")
        command = "$ErrorActionPreference='Stop'; (Get-FileHash -LiteralPath '" + literal + "' -Algorithm SHA256).Hash"
        response = client.request("command/exec", {"command": [str(PS), "-NoLogo", "-NoProfile", "-NonInteractive",
                    "-Command", command], "cwd": str(workspace), "sandboxPolicy": {"type": "readOnly"},
                    "timeoutMs": 20000}, timeout=35)
        validate_sandbox_read(response, r3["installed_files"]["skills/dsi-fpt/SKILL.md"])
        require((STATE / "config.toml").read_bytes() == config_before
                and inventory(cache) == r3["installed_files"], "Configuration/cache modifiés durant précontrôle")
        record.update({"status": "passed", "step": "complete", "checked_at": now(), "case_id": case["case_id"], "configuration": selected,
                "config_sha256": sha(config_before), "processes": processes, "legal_inventory": legal,
                "sandbox_read_succeeded": True, "candidate_cache_unchanged": True,
                "persistent_config_unchanged": True, "environment_identity_names_removed": removed,
                "model_inference": False, "oauth_login_attempted": False, "setup_attempted": False,
                "private_rpc_sha256": sha(canonical(client.private_events)), "release_ready": False})
        return record
    except (GateError, OSError, ValueError, queue.Empty, subprocess.SubprocessError) as error:
        record.update(error_type=type(error).__name__, reason=str(error)[:300])
        raise
    finally:
        if client is not None:
            write_new(receipt_folder / "rpc.private.json", client.private_events)
            with (receipt_folder / "stderr.private.txt").open("xb") as stream:
                stream.write(bytes(client.stderr))
            client.close()
        unchanged = (STATE / "config.toml").read_bytes() == config_before and inventory(cache) == r3["installed_files"]
        record.update(completed_at=now(), persistent_config_unchanged=unchanged,
                      candidate_cache_unchanged=inventory(cache) == r3["installed_files"])
        if not unchanged:
            record["status"] = "blocked"
            record["reason"] = "Configuration/cache modifiés au précontrôle"
        write_new(receipt_folder / "precontrole-assaini.json", record)
        require(unchanged, "Configuration/cache modifiés au précontrôle")


def prepare(run: Path, gate: Callable[..., Any] = preflight) -> dict[str, Any]:
    """Ne crée le run qu'après réussite de tous les précontrôles source."""
    run = destination(run)
    require(not run.exists(), "Run existant ; aucune reprise ni remplacement")
    protocol, r3 = inputs()
    env, removed = environment()
    version = subprocess.run([protocol["cli"], "--version"], env=env, capture_output=True, timeout=20)
    require(version.returncode == 0 and version.stdout.decode("utf-8").strip() == protocol["cli_version"],
            "Version CLI divergente")
    # Pas de dossier de run, sentinel ou copie avant le gate ; ROOT est une cwd de lecture.
    receipts = [gate(protocol, r3, case, ROOT) for case in protocol["cases"]]
    require(all(r.get("sandbox_read_succeeded") is True and r.get("persistent_config_unchanged") is True
                for r in receipts), "Précontrôle incomplet ; aucune préparation")
    require(all(r["config_sha256"] == receipts[0]["config_sha256"] for r in receipts),
            "Configuration persistée instable durant préparation ; aucun run créé")
    tools = {name: sha((ROOT / name).read_bytes()) for name in protocol["new_tools"]}
    run.mkdir()
    (run / "workspace").mkdir()
    (run / "workspace/README.md").write_bytes(b"# Qualification fictive\nAucune infrastructure reelle.\n")
    for folder in ("outils-figes", "cases", "judge-inputs", "judge-packets"):
        (run / folder).mkdir()
    for name in tools:
        (run / "outils-figes" / name).write_bytes((ROOT / name).read_bytes())
    proposal = read(ROOT / protocol["proposal_path"])
    (run / "rubric-original.md").write_bytes(Path(proposal["rubric_path"]).read_bytes())
    (run / "suite-originale.json").write_bytes(Path(proposal["suite_path"]).read_bytes())
    entries = []
    for case, receipt in zip(protocol["cases"], receipts, strict=True):
        folder = run / "cases" / case["case_id"]
        folder.mkdir()
        (folder / "prompt.txt").write_bytes(case["native_prompt"].encode("utf-8"))
        write_new(folder / "preflight-preparation.json", receipt)
        write_new(run / "judge-inputs" / (case["case_id"] + ".json"), case)
        entries.append({"case_id": case["case_id"], "prompt_sha256": case["prompt_sha256_utf8"],
                        "judge_input_sha256": sha((run / "judge-inputs" / (case["case_id"] + ".json")).read_bytes()),
                        "preflight_sha256": sha((folder / "preflight-preparation.json").read_bytes()),
                        "source_requirements": case["source_requirements_unchanged"],
                        "effective_overrides": overrides(protocol, case)})
    manifest = {"schema_version": "dev7-native-complete-manifest-v1", "created_at": now(),
                "status": "prepared_not_measured", "protocol_sha256": sha(PROTOCOL.read_bytes()),
                "candidate_commit": protocol["candidate_commit"], "candidate_tree": protocol["candidate_tree"],
                "installed_path": protocol["installed_path"], "installed_files": r3["installed_files"],
                "cli": protocol["cli"], "cli_sha256": protocol["cli_sha256"], "tools_sha256": tools,
                "config_sha256": receipts[0]["config_sha256"], "cases": entries,
                "source_preflights": receipts, "case_count": 16, "atomic_count": 124,
                "environment_identity_names_removed": removed, "model_override": None,
                "historical_scores_reused": False, "release_ready": False}
    require(all(r["config_sha256"] == manifest["config_sha256"] for r in receipts),
            "Configuration persistée instable durant préparation")
    write_new(run / "manifest.json", manifest)
    return {"prepared": True, "manifest_sha256": sha((run / "manifest.json").read_bytes()),
            "case_count": 16, "atomic_count": 124, "model_inference": False, "release_ready": False}


def verify(run: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Contrôle le gel sans modifier la préparation."""
    run = destination(run)
    protocol, r3 = inputs()
    manifest = read(run / "manifest.json")
    require(manifest["protocol_sha256"] == sha(PROTOCOL.read_bytes())
            and manifest["candidate_commit"] == protocol["candidate_commit"], "Run d'un autre protocole")
    require(sha((STATE / "config.toml").read_bytes()) == manifest["config_sha256"], "Config persistée modifiée")
    for name, digest in manifest["tools_sha256"].items():
        require(sha((ROOT / name).read_bytes()) == digest == sha((run / "outils-figes" / name).read_bytes()),
                "Outil nouveau modifié après préparation")
    require(sha((run / "rubric-original.md").read_bytes()) == protocol["rubric_sha256"]
            and sha((run / "suite-originale.json").read_bytes()) == protocol["suite_sha256"], "Suite/barème du run modifiés")
    require(len(manifest["cases"]) == 16, "Manifeste de cas incomplet")
    for entry, case in zip(manifest["cases"], protocol["cases"], strict=True):
        require(entry["case_id"] == case["case_id"] and entry["effective_overrides"] == overrides(protocol, case),
                "Ordre ou configuration de cas divergent")
        require(sha((run / "cases" / entry["case_id"] / "prompt.txt").read_bytes()) == entry["prompt_sha256"],
                "Prompt du run modifié")
        require(sha((run / "judge-inputs" / (entry["case_id"] + ".json")).read_bytes()) == entry["judge_input_sha256"],
                "Entrée juge modifiée")
    return protocol, r3, manifest


@contextmanager
def sequential_lock(run: Path):
    """Verrou OS ; toute tentative commencée reste scellée après libération."""
    import msvcrt
    with (run / "execution.lock").open("a+b") as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise GateError("Autre répondant actif") from error
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def bounded_process(argv: list[str], prompt: bytes, folder: Path, cwd: Path,
                    env: dict[str, str], limits: dict[str, int]) -> dict[str, Any]:
    """Une tentative ; captures bornées et arrêt de son propre enfant à échéance."""
    started = time.monotonic()
    overflows: list[str] = []
    counters = {"stdout": 0, "stderr": 0}
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def pump(name: str, stream: Any):
        with (folder / ("stdout.jsonl" if name == "stdout" else "stderr.local.txt")).open("xb") as target:
            while block := stream.read(65536):
                remaining = max(0, limits[name]-counters[name])
                target.write(block[:remaining])
                counters[name] += len(block)
                if counters[name] > limits[name] and name not in overflows:
                    overflows.append(name)
    readers = [threading.Thread(target=pump, args=(name, getattr(process, name))) for name in counters]
    for reader in readers:
        reader.start()
    timed_out = False
    try:
        try:
            process.stdin.write(prompt)
            process.stdin.close()
        except BrokenPipeError:
            # Le processus est déjà sorti ; son code et ses captures restent la preuve.
            if not process.stdin.closed:
                process.stdin.close()
        process.wait(timeout=240)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run([str(Path(env.get("SystemRoot", r"C:\Windows")) / "System32/taskkill.exe"),
                        "/PID", str(process.pid), "/T", "/F"], env=env, capture_output=True, timeout=10, check=False)
        if process.poll() is None:
            process.kill()
        process.wait(timeout=10)
    except OSError:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=10)
        raise
    finally:
        for reader in readers:
            reader.join(timeout=10)
        require(not any(reader.is_alive() for reader in readers), "Capture enfant non terminée")
    return {"exit_code": process.returncode, "timed_out": timed_out, "capture_overflow": overflows,
            "capture_original_bytes": counters, "elapsed_seconds": round(time.monotonic()-started, 3)}


def execute_case(run: Path, identifier: str, gate: Callable[..., Any] = preflight) -> dict[str, Any]:
    """Action future explicite uniquement, précontrôle frais puis session CLI neuve."""
    run = destination(run)
    with sequential_lock(run):
        protocol, r3, manifest = verify(run)
        cases = protocol["cases"]
        position = next((i for i, c in enumerate(cases) if c["case_id"] == identifier), None)
        require(position is not None, "Cas inconnu")
        require(all((run / "cases" / c["case_id"] / "execution.json").is_file() for c in cases[:position]),
                "Séquence nominale interrompue ; aucun saut de cas")
        folder = run / "cases" / identifier
        require(not (folder / "start.json").exists(), "Tentative déjà commencée ; aucun retry/reprise")
        receipt = gate(protocol, r3, cases[position], run / "workspace")
        reference = manifest["source_preflights"][position]
        require(receipt["config_sha256"] == manifest["config_sha256"]
                and receipt["configuration"] == reference["configuration"]
                and receipt["legal_inventory"] == reference["legal_inventory"],
                "Configuration ou schémas de source modifiés ; nouveau protocole requis")
        verify(run)
        write_new(folder / "preflight-execution.json", receipt)
        env, removed = environment()
        argv = [protocol["cli"], "--no-daemon", "--cd", str(run / "workspace"), *overrides(protocol, cases[position]),
                "--sandbox", "read-only", "--ask-for-approval", "never", "exec", "--skip-git-repo-check",
                "--json", "--color", "never", "--output-last-message", str(folder / "response.md"), "-"]
        prompt = (folder / "prompt.txt").read_bytes()
        write_new(folder / "start.json", {"started_at": now(), "argv": argv, "attempt": 1,
                  "prompt_sha256": sha(prompt), "manifest_sha256": sha((run / "manifest.json").read_bytes()),
                  "environment_identity_names_removed": removed, "model_override": None})
        record: dict[str, Any] = {"case_id": identifier, "attempt": 1, "release_ready": False}
        try:
            record.update(bounded_process(argv, prompt, folder, run / "workspace", env,
                                         protocol["bounded_capture_bytes"]))
            rows = [json.loads(line) for line in (folder / "stdout.jsonl").read_bytes().splitlines()]
            ids = [r.get("thread_id") for r in rows if r.get("type") == "thread.started"]
            require(len(ids) == 1 and isinstance(ids[0], str), "Identité native absente ou ambiguë")
            identifier_native = ids[0]
            require(re.fullmatch(r"[0-9a-f-]{36}", identifier_native) is not None, "Identité native malformée")
            native_paths = list((STATE / "sessions").rglob("*" + identifier_native + ".jsonl"))
            require(len(native_paths) == 1, "Rollout natif absent ou ambigu")
            require(native_paths[0].stat().st_size <= protocol["bounded_capture_bytes"]["rollout"], "Rollout trop volumineux")
            raw = native_paths[0].read_bytes()
            require(json.loads(raw.splitlines()[0]).get("payload", {}).get("id") == identifier_native,
                    "Rollout d'un autre répondant")
            with (folder / "native-rollout.local.jsonl").open("xb") as stream:
                stream.write(raw)
            record.update(thread_id=identifier_native, native_rollout_sha256=sha(raw))
            verify(run)
            record["candidate_cache_config_unchanged"] = True
        except (GateError, OSError, ValueError, subprocess.SubprocessError) as error:
            record.update(technical_error_type=type(error).__name__, technical_error=str(error)[:240],
                          candidate_cache_config_unchanged=False)
        record["completed_at"] = now()
        record["capture_sha256"] = {name: sha((folder / name).read_bytes()) for name in
            ("stdout.jsonl", "stderr.local.txt", "response.md") if (folder / name).exists()}
        write_new(folder / "execution.json", record)
        return record


def export_case(run: Path, identifier: str) -> dict[str, Any]:
    """Paquet juge après scellement, hors cwd du répondant ; aucun juge créé ici."""
    import normaliseur_native_complete_dev7_20261009_r2 as normalizer
    protocol, _, manifest = verify(run)
    case = next(c for c in protocol["cases"] if c["case_id"] == identifier)
    folder = run / "cases" / identifier
    execution = read(folder / "execution.json")
    require(execution.get("native_rollout_sha256") == sha((folder / "native-rollout.local.jsonl").read_bytes()),
            "Trace native non scellée ou différente")
    for name, digest in execution["capture_sha256"].items():
        require(sha((folder / name).read_bytes()) == digest, "Capture scellée modifiée")
    trace = normalizer.normalize((folder / "native-rollout.local.jsonl").read_bytes(), case["native_prompt"],
        execution["thread_id"], Path(protocol["installed_path"]), manifest["installed_files"],
        case["source_requirements_unchanged"], case["judge_only_oracle"]["skills"])
    issues = trace["technical_issues"]
    if execution.get("exit_code") != 0:
        issues.append("native_process_exit_not_zero")
    if execution.get("timed_out") is True:
        issues.append("native_process_timeout")
    if execution.get("capture_overflow"):
        issues.append("native_capture_incomplete")
    if execution.get("technical_error_type") or execution.get("candidate_cache_config_unchanged") is not True:
        issues.append("execution_freeze_or_capture_not_verified")
    if any(e.get("type") == "derived_native_process_failure" for e in trace["events"]):
        issues.append("sandbox_native_process_failure")
    native_rows = [json.loads(line) for line in (folder / "native-rollout.local.jsonl").read_bytes().splitlines()]
    finals = []
    for row in native_rows:
        payload = row.get("payload", {})
        if row.get("type") == "response_item" and payload.get("type") == "message" \
                and payload.get("role") == "assistant" \
                and (payload.get("phase") == "final_answer" or payload.get("channel") == "final"):
            finals.append("\n".join(p.get("text", "") for p in payload.get("content", [])
                if p.get("type") in ("input_text", "output_text", "text")))
    if len(finals) != 1 or not (folder / "response.md").is_file():
        issues.append("native_final_response_unbound")
    else:
        def normalize_lines(text: str) -> str:
            return text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
        if normalize_lines(finals[0]) != normalize_lines((folder / "response.md").read_text(encoding="utf-8")):
            issues.append("native_final_response_mismatch")
    trace["technical_issues"] = sorted(set(issues))
    trace["execution_receipt"] = {k: execution.get(k) for k in ("exit_code", "timed_out", "capture_overflow",
        "technical_error_type", "candidate_cache_config_unchanged", "attempt", "native_rollout_sha256")}
    trace["transport_provenance_verified"] = execution.get("candidate_cache_config_unchanged") is True \
        and execution.get("exit_code") == 0 and execution.get("timed_out") is False \
        and not execution.get("capture_overflow") and not execution.get("technical_error_type")
    packet = normalizer.judge_packet(case, trace, (run / "rubric-original.md").read_text(encoding="utf-8"),
                                    normalizer.HOST_ADDENDUM,
                                    transport_provenance_verified=trace["transport_provenance_verified"])
    target = run / "judge-packets" / identifier
    require(not target.exists(), "Export déjà scellé ; aucun remplacement")
    target.mkdir()
    write_new(target / "trace.json", trace)
    write_new(target / "packet.json", packet)
    write_new(target / "export.json", {"exported_at": now(), "case_id": identifier,
        "native_sha256": execution["native_rollout_sha256"], "trace_sha256": sha((target / "trace.json").read_bytes()),
        "packet_sha256": sha((target / "packet.json").read_bytes()), "judge_created": False,
        "physical_filesystem_isolation_claimed": False, "release_ready": False})
    return {"case_id": identifier, "packet": str(target / "packet.json"), "judge_created": False,
            "packet_sha256": sha((target / "packet.json").read_bytes()),
            "technical_issues": trace["technical_issues"], "release_ready": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "prepare", "run-all", "export"))
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--case")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if args.action == "check":
        protocol, _ = inputs()
        result = {"inputs_verified": True, "source_cases": sum(c["source_requirements_unchanged"]["mcp_mode"]
                  == "required" for c in protocol["cases"]), "model_inference": False,
                  "source_auth_verified": False, "sandbox_read_verified": False, "release_ready": False}
    elif args.action == "prepare":
        require(args.offline, "Caller hors application requis ; aucune préparation lancée")
        result = prepare(args.run)
    elif args.action == "run-all":
        require(args.offline, "Caller hors application requis ; aucune inférence lancée")
        protocol, _, _ = verify(args.run)
        require(not any((args.run / "cases" / c["case_id"] / "start.json").exists() for c in protocol["cases"]),
                "Run déjà commencé ; aucune reprise/remplacement")
        outcomes = []
        stop_reason = None
        for case in protocol["cases"]:
            outcome = execute_case(args.run, case["case_id"])
            outcomes.append(outcome)
            if outcome.get("native_rollout_sha256"):
                exported = export_case(args.run, case["case_id"])
                if exported["technical_issues"]:
                    stop_reason = exported["technical_issues"]
            if outcome.get("timed_out") or outcome.get("capture_overflow") \
                    or outcome.get("exit_code") != 0 or outcome.get("candidate_cache_config_unchanged") is not True:
                stop_reason = stop_reason or ["execution_failed_or_capture_incomplete"]
            if stop_reason:
                break
        result = {"executed_cases": len(outcomes), "stopped_on_technical_failure": bool(stop_reason),
                  "stop_reason": stop_reason, "judges_created": False, "release_ready": False}
        write_new(args.run / "execution-bilan.json", {"completed_at": now(), **result})
    else:
        require(bool(args.case), "Cas requis")
        result = export_case(args.run, args.case)
    print(json.dumps(result, ensure_ascii=False))
    if result.get("stopped_on_technical_failure"):
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except (GateError, OSError, ValueError, queue.Empty, subprocess.SubprocessError) as error:
        failure = {"failed_at": now(), "blocked": True, "error_type": type(error).__name__,
                   "reason": str(error)[:300], "automatic_retry": False, "release_ready": False}
        # Reçu indépendant même pour les erreurs avant création du run.
        receipt = destination(ROOT / ("blocage-outillage-complet-dev7-" +
            datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8] + ".json"))
        write_new(receipt, failure)
        print(json.dumps({**failure, "receipt": str(receipt)}, ensure_ascii=False))
        raise SystemExit(2)
