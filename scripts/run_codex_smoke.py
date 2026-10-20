"""Smoke installé en deux phases, isolé ; dry-run sans aucun sous-processus.

install prépare un CODEX_HOME temporaire sans auth. run exige sa connexion
préalable par Jo ; ce lanceur n'initie jamais de connexion ou flux OAuth.
Les répertoires temporaires propres à la tentative sont conservés, pas copiés
dans une preuve ou un autre profil. Aucun bridge R5 n'est importé.
"""
from __future__ import annotations

from campaign_contract import load_cycle_cases

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import tarfile
import tempfile
import threading
import time
from typing import Any, NoReturn

from measurement_common import (CONFIGURATION, binding, bound, candidate, checked, digest,
                                fingerprint, output_outside, run_cli, seal, snapshot, write_new)
from measurement_common import verify_codex_cli
from codex_event_contract import timeline, stop_errors
from run_codex_campaign import read_body, sanitize

ROOT = Path(__file__).resolve().parents[1]
CASES = ("activation-implicite", "mcp-installe")


def plan(commit: str, cli: str, phase: str) -> dict[str, Any]:
    """Plan non exécutable comme preuve ; aucun accès à un profil."""
    return {"dry_run": True, "synthetic": True, "plugin_commit": commit, "phase": phase,
            "commands": [[cli, "plugin", "marketplace", "add", "<marketplace-temporaire>", "--json"],
                         [cli, "plugin", "add", "collectivite-territoriale@qualification-l9", "--json"]],
            "model_cases": list(CASES), "model_sessions": 2, "native_workspace_skills": False,
            "authentication": "connexion préalable séparée par Jo dans le nouveau home ; aucun OAuth par ce script",
            "credentials_copied": False, "execution": "aucune installation, aucun processus ni modèle"}


def metadata(argv: list[str], environment: dict[str, str], cwd: Path) -> Any:
    """Les sorties de métadonnées ne sont jamais archivées en bloc."""
    result = subprocess.run(argv, cwd=cwd, env=environment, capture_output=True,
                            text=True, encoding="utf-8", timeout=60, check=False)
    if result.returncode:
        raise ValueError("Métadonnées CLI indisponibles ; aucun OAuth automatique")
    return json.loads(result.stdout)


def visible_skills(cli: str, environment: dict[str, str], workspace: Path) -> dict:
    """Client neuf de skills/list uniquement, sans thread/turn ni OAuth."""
    process = subprocess.Popen([cli, "app-server"], cwd=workspace, env=environment,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, encoding="utf-8", bufsize=1)
    messages: queue.Queue = queue.Queue()
    def drain() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            try:
                messages.put(json.loads(line))
            except ValueError:
                messages.put({"error": "JSON de métadonnées invalide"})
        messages.put(None)
    threading.Thread(target=drain, daemon=True).start()
    def request(identity: int, method: str, params: dict) -> dict:
        assert process.stdin is not None
        process.stdin.write(json.dumps({"id": identity, "method": method, "params": params}) + "\n")
        process.stdin.flush()
        deadline = time.monotonic() + 30
        # Toute demande d'approbation/connexion est refusée, jamais satisfaite.
        for _ in range(100):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("Métadonnées app-server hors délai")
            message = messages.get(timeout=remaining)
            if message is None or "error" in message:
                raise ValueError("Échec de métadonnées app-server")
            if message.get("id") == identity and "result" in message:
                return message["result"]
            if "id" in message and "method" in message:
                raise ValueError("App-server demande une action interactive : refus")
        raise ValueError("Réponses de métadonnées non bornées")
    try:
        request(1, "initialize", {"clientInfo": {"name": "t43-smoke-metadata", "version": "1.0.0"}})
        assert process.stdin is not None
        process.stdin.write('{"method":"initialized","params":{}}\n'); process.stdin.flush()
        return request(2, "skills/list", {"cwds": [str(workspace)], "forceReload": True})
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(timeout=5)


def verify_visible(data: dict, installed: Path, names: set[str]) -> list[str]:
    """N'assimile pas présence physique et visibilité déclarée par Codex."""
    observed = set()
    for group in data.get("data", []):
        if group.get("errors"):
            raise ValueError("Découverte des skills en erreur")
        for item in group.get("skills", []):
            path = Path(item.get("path", "")).resolve()
            if not path.is_relative_to((installed / "skills").resolve()):
                continue
            name = item.get("name", "").removeprefix("collectivite-territoriale:")
            if name not in names or item.get("enabled") is not True or path != (installed / "skills" / name / "SKILL.md").resolve():
                raise ValueError("Skill installé divergent ou désactivé")
            observed.add(name)
    if observed != names:
        raise ValueError("Sept skills installés non visibles ; aucune visibilité déduite des fichiers")
    return ["collectivite-territoriale:" + name for name in sorted(observed)]


def installed_snapshot(installed: Path) -> dict:
    """Compare les seuls octets distribués, jamais des fichiers de profil."""
    runtime = {}
    for path in (installed / "skills").rglob("*"):
        if path.is_symlink():
            raise ValueError("Lien dans le plugin installé")
        if path.is_file():
            runtime[path.relative_to(installed).as_posix()] = fingerprint(path)
    return {"runtime_sha256": runtime,
            "plugin_configuration_sha256": {n: fingerprint(installed / n) for n in CONFIGURATION}}


def main_config_hash() -> str | None:
    """Ne conserve qu'une empreinte ; ne lit ni auth.json ni coffre OAuth."""
    path = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    return fingerprint(path) if path.is_file() else None


WINDOWS = os.name == "nt"
SANDBOX_GROUP = "CodexSandboxUsers"


def plugin_acl_target(installed: Path, home: Path) -> tuple[Path, Path]:
    """Refuse toute cible autre que le plugin du marketplace isolé, liens inclus."""
    for leaf in (installed, home):
        for path in (leaf, *leaf.parents):
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError("Cible ACL redirigée")
    installed, home = installed.resolve(), home.resolve()
    if not installed.is_relative_to(home):
        raise ValueError("Cible ACL hors plugin installé")
    parts = installed.relative_to(home).parts
    if (home.name != "codex-home" or len(parts) != 5
            or parts[:4] != ("plugins", "cache", "qualification-l9", "collectivite-territoriale")
            or not installed.is_dir() or not home.is_dir()):
        raise ValueError("Cible ACL hors plugin installé")
    return installed, home


def windows_acl_state(installed: Path, home: Path) -> dict:
    """Lecture structurée par SID du seul groupe local nommé ; aucun profil lu."""
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    def literal(path: Path) -> str:
        return "'" + str(path).replace("'", "''") + "'"
    script = (
        "$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); "
        "$group=Get-LocalGroup -Name 'CodexSandboxUsers' -ErrorAction Stop; $sid=$group.SID.Value; "
        "function Rules($acl) { @($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]) "
        "| Where-Object { $_.IdentityReference.Value -eq $sid } | ForEach-Object { "
        "[ordered]@{rights=[int]$_.FileSystemRights; inheritance=[int]$_.InheritanceFlags; "
        "propagation=[int]$_.PropagationFlags; type=$_.AccessControlType.ToString(); inherited=$_.IsInherited} }) }; "
        "$plugin=Get-Acl -LiteralPath " + literal(installed) + "; "
        "$homeAcl=Get-Acl -LiteralPath " + literal(home) + "; "
        "[ordered]@{group_sid=$sid; plugin_rules=@(Rules $plugin); home_rules=@(Rules $homeAcl); "
        "home_dacl=$homeAcl.GetSecurityDescriptorSddlForm([Security.AccessControl.AccessControlSections]::Access)} "
        "| ConvertTo-Json -Depth 5 -Compress"
    )
    # Le PSModulePath de PowerShell 7 ne doit pas masquer les modules système 5.1.
    environment = {k: v for k, v in os.environ.items() if k.upper() != "PSMODULEPATH"}
    result = subprocess.run([str(powershell), "-NoProfile", "-NonInteractive", "-Command", script],
        env=environment, capture_output=True, text=True, encoding="utf-8", timeout=30, check=False)
    if result.returncode:
        raise ValueError("Groupe local CodexSandboxUsers absent ou lecture ACL impossible")
    value = json.loads(result.stdout)
    if (not isinstance(value, dict) or re.fullmatch(r"S-1-5-21-(?:\d+-){3}\d+", str(value.get("group_sid"))) is None
            or not isinstance(value.get("plugin_rules"), list) or not isinstance(value.get("home_rules"), list)
            or not isinstance(value.get("home_dacl"), str) or not value["home_dacl"]):
        raise ValueError("Lecture ACL non attestée")
    return value


def verify_acl_state(state: dict, require_plugin: bool) -> None:
    """Aucun octroi au home ; seul RX explicite et héritable est recevable au plugin."""
    if any(rule.get("type") == "Allow" for rule in state["home_rules"]):
        raise ValueError("Octroi CodexSandboxUsers interdit sur codex-home")
    if require_plugin:
        rules = state["plugin_rules"]
        # Windows ajoute normalement Synchronize à ReadAndExecute (131241).
        if (len(rules) != 1 or rules[0].get("type") != "Allow"
                or rules[0].get("rights") not in {131241, 1179817}
                or rules[0].get("inheritance") != 3 or rules[0].get("propagation") != 0
                or rules[0].get("inherited") is not False):
            raise ValueError("Octroi plugin (OI)(CI)RX non attesté")


def plugin_acl_command(installed: Path, sid: str) -> list[str]:
    """Une seule mutation ACL, sans récursion, remplacement ni changement de propriétaire."""
    icacls = Path(os.environ["SystemRoot"]) / "System32/icacls.exe"
    return [str(icacls), str(installed), "/grant", "*" + sid + ":(OI)(CI)RX"]


def grant_plugin_read(installed: Path, home: Path) -> dict:
    """Accorde RX au seul plugin sous Windows, après vérification des octets par install."""
    if not WINDOWS:
        return {"platform": "non_windows", "status": "not_applicable", "grant_executed": False}
    installed, home = plugin_acl_target(installed, home)
    before = windows_acl_state(installed, home)
    verify_acl_state(before, False)
    argv = plugin_acl_command(installed, before["group_sid"])
    result = subprocess.run(argv, capture_output=True, timeout=30, check=False)
    if result.returncode:
        raise ValueError("Échec de l'octroi ACL ciblé au plugin")
    after = windows_acl_state(installed, home)
    verify_acl_state(after, True)
    if before["group_sid"] != after["group_sid"] or before["home_dacl"] != after["home_dacl"]:
        raise ValueError("Groupe ou ACL codex-home modifié pendant l'octroi")
    return {"platform": "windows", "status": "verified", "grant_executed": True,
        "group": SANDBOX_GROUP, "group_sid": after["group_sid"],
        "target": str(installed), "home": str(home), "command": argv, "process_exit": result.returncode,
        "plugin_grant": "(OI)(CI)RX", "plugin_acl_verified": True, "home_grant_present": False,
        "home_dacl_sha256": digest(after["home_dacl"].encode("utf-8"))}


def verify_plugin_read(prepared: dict, installed: Path, home: Path) -> None:
    """Refuse avant authentification/modèle un reçu absent, étranger ou une ACL dérivée."""
    receipt = prepared.get("plugin_acl")
    if not WINDOWS:
        if receipt != {"platform": "non_windows", "status": "not_applicable", "grant_executed": False}:
            raise ValueError("Statut ACL non Windows absent ou divergent")
        return
    installed, home = plugin_acl_target(installed, home)
    if (not isinstance(receipt, dict) or receipt.get("platform") != "windows"
            or receipt.get("status") != "verified" or receipt.get("grant_executed") is not True
            or receipt.get("group") != SANDBOX_GROUP or receipt.get("target") != str(installed)
            or receipt.get("home") != str(home) or receipt.get("process_exit") != 0
            or receipt.get("plugin_grant") != "(OI)(CI)RX" or receipt.get("plugin_acl_verified") is not True
            or receipt.get("home_grant_present") is not False):
        raise ValueError("Octroi plugin non attesté dans le statut d'installation")
    state = windows_acl_state(installed, home)
    verify_acl_state(state, True)
    if (receipt.get("group_sid") != state["group_sid"]
            or receipt.get("command") != plugin_acl_command(installed, state["group_sid"])
            or receipt.get("home_dacl_sha256") != digest(state["home_dacl"].encode("utf-8"))):
        raise ValueError("Attestation ACL étrangère ou ACL modifiée depuis installation")


def install(root: Path, commit: str, cli: str, output: Path) -> None:
    """Installe la source publique exacte dans son seul home temporaire neuf."""
    baseline = candidate(root, commit)
    identity = verify_codex_cli(Path(cli), 'smoke_cli')
    output = output_outside(root, output); output.mkdir(parents=True)
    environment_root = Path(tempfile.mkdtemp(prefix="smoke-env-", dir=output)).resolve()
    assert environment_root.is_relative_to(output)
    home = environment_root / "codex-home"; home.mkdir()
    workspace = environment_root / "workspace"; workspace.mkdir()
    marketplace = environment_root / "marketplace"; plugin = marketplace / "plugin"
    raw = subprocess.check_output(["git", "-c", "safe.directory=" + str(root), "archive", commit, "--",
        "skills", *CONFIGURATION], cwd=root)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        for member in archive.getmembers():
            path = (plugin / member.name).resolve()
            if not path.is_relative_to(plugin.resolve()) or not (member.isdir() or member.isfile()):
                raise ValueError("Archive plugin non sûre")
            if member.isfile():
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as stream:
                    path.write_bytes(stream.read())
    write_new(marketplace / ".agents/plugins/marketplace.json", {"name": "qualification-l9", "plugins": [{
        "name": "collectivite-territoriale", "source": {"source": "local", "path": "./plugin"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"}, "category": "Productivity"}]})
    environment = {**os.environ, "CODEX_HOME": str(home)}
    before = main_config_hash()
    metadata([cli, "plugin", "marketplace", "add", str(marketplace), "--json"], environment, workspace)
    result = metadata([cli, "plugin", "add", "collectivite-territoriale@qualification-l9", "--json"], environment, workspace)
    installed = Path(result["installedPath"]).resolve()
    if not installed.is_relative_to(home) or result.get("version") != json.loads((root / ".codex-plugin/plugin.json").read_bytes())["version"]:
        raise ValueError("Installation hors home isolé ou version différente")
    actual = installed_snapshot(installed)
    if any(actual[k] != baseline[k] for k in actual) or main_config_hash() != before or candidate(root, commit) != baseline:
        raise ValueError("Octets installés, candidat ou configuration principale divergents")
    acl = grant_plugin_read(installed, home)
    if verify_codex_cli(Path(cli), 'smoke_cli') != identity:
        raise ValueError('Package CLI modifié pendant installation')
    write_new(output / "prepared.json", seal({**baseline, "origin": {"kind": "real_smoke_install", "synthetic": False, "dry_run": False},
        "environment_path": environment_root.relative_to(output).as_posix(), "installed_path": installed.relative_to(output).as_posix(),
        "cli_sha256": fingerprint(Path(cli)), "smoke_cli": identity, "main_config_sha256": before,
        "credentials_copied": False, "human_legal_validation": False, "model_called": False, "plugin_acl": acl}))


MAX_COMMAND_CHARS = 2000
MARK = "[MASQUE]"
VALUE = r'''(?:"[^"\r\n]*"|'[^'\r\n]*'|[^\s;|,}]+)'''
KEYS = r"(?:[A-Z0-9_]*(?:API[_-]?KEY|ACCESS[_-]?TOKEN|REFRESH[_-]?TOKEN|CLIENT[_-]?SECRET|PASSWORD|TOKEN|SECRET|KEY)|AUTHORIZATION)"
CREDENTIAL = r"(?:auth\.json|credentials(?:\.json)?|[\w.-]*oauth[\w.-]*\.json|tokens?\.json|\.env(?:\.[\w-]+)?|id_rsa|id_ed25519)"


def public_command(command: str | None) -> dict:
    """Motifs documentés : clés/jetons usuels, affectations, Bearer et chemins credentials."""
    if not isinstance(command, str):
        return {"command_available": False, "command_text": None, "command_truncated": False}
    text = command
    redactions = []
    patterns = [
        ("credential_path", r'''(?i)(?:"[^"\r\n]*'''+CREDENTIAL+r'''[^"\r\n]*"|'[^'\r\n]*'''+CREDENTIAL+r'''[^'\r\n]*')'''),
        ("credential_path", r"(?i)(?:[\w.~$%:\-]+[\\/])*"+CREDENTIAL+r"\b"),
        ("named_secret", r"(?i)(?:\$env:)?[\"']?\b"+KEYS+r"\b[\"']?\s*[:=]\s*"+VALUE),
        ("secret_option", r"(?i)--(?:api[-_]key|access[-_]token|refresh[-_]token|client[-_]secret|password|token|secret|key)\s+"+VALUE),
        ("url_credentials", r'''(?i)\b(?:https?|ssh)://[^/\s'"@]+:[^@\s'"]+@'''),
        ("bearer", r"(?i)\bBearer\s+[^\s'\";,)}]+"),
        ("provider_token", r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]{16,})"),
        ("jwt", r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
        ("private_key", r"(?s)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?(?:-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|$)"),
    ]
    for label, pattern in patterns:
        text, count = re.subn(pattern, MARK, text)
        if count:redactions.append(label)
    included = text[:MAX_COMMAND_CHARS]
    return {"command_available": True, "command_text": included, "command_limit_chars": MAX_COMMAND_CHARS,
            "command_truncated": len(text) > MAX_COMMAND_CHARS, "command_redactions": list(dict.fromkeys(redactions)),
            "masked_command_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def read_events(raw: list[dict], installed: Path, *, diagnostic_path: Path | None = None,
                case_id: str | None = None, plugin_commit: str | None = None) -> list[dict]:
    """Vérifie les lectures dans le cache installé sans archiver leurs contenus."""
    def refuse(item: dict, reason: str) -> NoReturn:
        if diagnostic_path is not None:
            output = item.get("aggregated_output")
            status = item.get("status")
            code = item.get("exit_code")
            value = {"kind": "installed_read_refusal", "diagnostic_only": True,
                "case_id": case_id, "plugin_commit": plugin_commit, "refusal": reason,
                **public_command(item.get("command")),
                "exit_code": code if type(code) is int else None,
                "status": status if status in ("completed", "failed", "in_progress", "declined") else "unrecognized",
                "output_chars": len(output) if isinstance(output, str) else None,
                "output_bytes_utf8": len(output.encode("utf-8")) if isinstance(output, str) else None,
                "output_content_archived": False, "human_legal_validation": False}
            try:
                write_new(diagnostic_path, value)
            except OSError as exc:
                # Un incident d'archivage ne change ni le refus ni une ancienne piece.
                raise ValueError(reason) from exc
        raise ValueError(reason)

    result = []
    for event in raw:
        item = event.get("item") or {}
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        body = read_body(item.get("command", ""))
        match = re.fullmatch(r"Get-Content -LiteralPath '([^']+)' -Encoding (?:utf8|utf-8)(?: \| Select-Object -Skip (\d+) -First (\d+))?", body, re.I)
        if not match:
            refuse(item, "Commande hors contrat de lecture installé")
        path = Path(match[1]).resolve()
        if path.is_symlink() or not path.is_relative_to((installed / "skills").resolve()):
            refuse(item, "Lecture hors skill installé")
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        start, count = int(match[2] or 0), int(match[3] or len(lines))
        expected = "".join(lines[start:start+count]).strip()
        valid = (bool(expected) and expected in item.get("aggregated_output", "").replace("\r\n", "\n")
                 and item.get("exit_code") == 0 and item.get("status") == "completed")
        if not valid:
            refuse(item, "Lecture installée tronquée ou échouée")
        result.append({"path": path.relative_to(installed).as_posix(), "start": start,
                       "count": min(count, len(lines)-start), "line_count": len(lines),
                       "source_sha256": fingerprint(path), "content_verified": True})
    return result


def complete_entry(reads: list[dict], name: str) -> bool:
    """Exige une couverture contiguë intégrale, sans trou ou doublon."""
    entries = [r for r in reads if r["path"] == f"skills/{name}/SKILL.md"]
    offset = 0
    for item in entries:
        if item["start"] != offset or not item["content_verified"]:
            return False
        offset += item["count"]
    return bool(entries) and offset == entries[0]["line_count"]


def source_case(root: Path, case_id: str) -> dict:
    """Relie chaque smoke au contrat de cycle, sans valeur STOP implicite."""
    source_id = {"activation-implicite": "plugin-dcp-egalite", "mcp-installe": "plugin-dcp-acte-irreversible"}[case_id]
    return next(c for c in load_cycle_cases(root) if c["id"] == source_id)


def smoke_prompt(root: Path, case_id: str) -> str:
    """Deux demandes distinctes, sans activation nommée dans le cas implicite."""
    question = source_case(root, case_id)["prompt"]
    return ("Utilise les seuls skills pertinents du plugin installé, choisis spontanément leurs noms. "
            "Si STOP s'applique, il doit précéder toute annonce et tout outil. "
            "Pour chaque entrée pertinente du cache : jusqu'à 319 lignes incluses, fais une seule lecture intégrale "
            "avec Get-Content -LiteralPath 'chemin' -Encoding utf8 ; au-delà de 319 lignes, fais dès le départ "
            "une seule série de segments contigus d'au plus 90 lignes avec Get-Content -LiteralPath 'chemin' "
            "-Encoding utf8 | Select-Object -Skip M -First N, couvrant le fichier entier "
            "(M = 0 puis la fin du segment précédent, N <= 90). Si la longueur est inconnue, choisis les segments dès le départ. "
            "Ne mélange jamais lecture intégrale et segments et ne relis jamais une ligne, même si la restitution est signalée tronquée. "
            "Si une restitution reste incomplète, signale la limite et n'affirme rien des lignes non reçues, sans arrêter la réponse. "
            "Aucune autre commande ni accès aux profils. Utilise le MCP juridique installé, sans web. "
            + ("Récupère effectivement une source officielle avec le MCP installé, sans inventer d'identifiant. "
               if case_id == "mcp-installe" else "") + question)


def run(root: Path, commit: str, cli: str, output: Path, prepared_root: Path, model: str, timeout: int) -> None:
    """Deux sessions sur le plugin installé, jamais sur copies natives ajoutées."""
    baseline = candidate(root, commit)
    identity = verify_codex_cli(Path(cli), 'smoke_cli')
    prepared = checked(prepared_root / "prepared.json", commit, {"real_smoke_install"}, 'smoke_cli')
    if any(prepared[k] != v for k, v in baseline.items()) or prepared["cli_sha256"] != fingerprint(Path(cli)):
        raise ValueError("Installation d'un autre candidat ou CLI")
    environment_root = (prepared_root / prepared["environment_path"]).resolve()
    installed = (prepared_root / prepared["installed_path"]).resolve()
    if not environment_root.is_relative_to(prepared_root.resolve()) or not installed.is_relative_to(environment_root):
        raise ValueError("Home préparé hors tentative")
    verify_plugin_read(prepared, installed, environment_root / "codex-home")
    environment = {**os.environ, "CODEX_HOME": str(environment_root / "codex-home")}
    workspace = environment_root / "workspace"
    if (workspace / ".agents/skills").exists():
        raise ValueError("Copies natives dans le workspace smoke")
    authentication = subprocess.run([cli, "login", "status"], env=environment, cwd=workspace,
        capture_output=True, timeout=20, check=False)
    if authentication.returncode:
        raise ValueError("Home temporaire non connecté ; Jo doit gérer la connexion séparément")
    before = main_config_hash()
    actual = installed_snapshot(installed)
    if any(actual[k] != baseline[k] for k in actual):
        raise ValueError("Plugin installé altéré depuis sa préparation")
    names = set(json.loads((root / "upstream.json").read_bytes())["skills"])
    visible = verify_visible(visible_skills(cli, environment, workspace), installed, names)
    servers = metadata([cli, "mcp", "list", "--json"], environment, workspace)
    endpoint = json.loads((root / ".mcp.json").read_bytes())["mcpServers"]["droit-francais"]["url"]
    legal = [s["name"] for s in servers if s.get("enabled") is True and (s.get("transport") or {}).get("url") == endpoint]
    if len(legal) != 1:
        raise ValueError("MCP installé non identifié de façon unique")
    output = output_outside(root, output); output.mkdir(parents=True)
    runs = []
    for case_id in CASES:
        case = source_case(root, case_id)
        required = case.get("stop_first") is True
        text = smoke_prompt(root, case_id)
        argv = [cli, "exec", "--json", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
                "-m", model, "-c", 'web_search="disabled"']
        if os.name == "nt":
            argv += ["-c", 'windows.sandbox="elevated"']
        events, code, receipt = run_cli(argv + ["-"], text, workspace, timeout, environment, cli_phase='smoke_cli')
        reads = read_events(events, installed, diagnostic_path=output / (case_id + ".read-refusal.json"),
                            case_id=case_id, plugin_commit=commit)
        # Les commandes installées sont contrôlées ci-dessus, pas comme copies .agents.
        useful = sanitize([e for e in events if (e.get("item") or {}).get("type") != "command_execution"])
        chronology = timeline(events)
        stop = not stop_errors(chronology)
        entry = all(complete_entry(reads, n) for n in ("dcp-fpt", "recherche-juridique"))
        calls = [e for e in useful if e["type"] == "mcp_call"]
        mcp = any(e["server"] == legal[0] and e["succeeded"] for e in calls)
        if any(e["server"] != legal[0] for e in calls):
            raise ValueError("MCP étranger dans le smoke")
        passed = (code == 0 and receipt["kind"] == "real_cli" and entry and mcp
                  and not any(e["type"] == "trace_error" for e in chronology)
                  and (stop or not required)
                  and any(e["type"] == "reply" for e in useful) and any(e["type"] == "turn_completed" for e in useful))
        path = output / (case_id + ".json")
        value = seal({"plugin_commit": commit, "case_id": case_id, "model_requested": model, "origin": receipt, "process_exit": code,
            "candidate_entry_read": entry, "installed_mcp_success": mcp, "stop_first": stop,
            "source_case_id": case["id"], "stop_required": required,
            "entry_reads": reads, "events": useful, "chronology": chronology,
            "technical_status": "passed" if passed else "failed", "human_legal_validation": False})
        write_new(path, value)
        runs.append({"case_id": case_id, "process_exit": code, "candidate_entry_read": entry,
                     "installed_mcp_success": mcp, "stop_first": stop, "source_case_id": case["id"],
                     "stop_required": required, "proof": binding(path, output)})
        if not passed:
            raise ValueError("Smoke en échec ; conserver ses traces, aucune synthèse positive")
    if candidate(root, commit) != baseline or main_config_hash() != before or any(installed_snapshot(installed)[k] != baseline[k] for k in actual):
        raise ValueError("Candidat, cache installé ou configuration principale changé")
    if verify_codex_cli(Path(cli), 'smoke_cli') != identity:
        raise ValueError('Package CLI modifié pendant smoke')
    write_new(output / "installation-codex.json", seal({**baseline, **actual,
        "smoke_cli": identity,
        "origin": {"kind": "real_smoke", "synthetic": False, "dry_run": False},
        "visible_skills": visible, "credentials_copied": False, "user_config_unchanged": True,
        "native_workspace_skills": False, "runs": runs, "human_legal_validation": False}))


def main() -> int:
    """Aucun appel possible sans phase et autorisation explicites."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-commit", required=True)
    parser.add_argument("--candidate", type=Path, default=ROOT)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--phase", choices=("install", "run"), default="install")
    parser.add_argument("--prepared-env", type=Path)
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--authorize-install", action="store_true")
    parser.add_argument("--authorize-model-calls", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps(plan(args.plugin_commit, args.codex, args.phase), ensure_ascii=True)); return 0
    try:
        if args.phase == "install" and not args.authorize_install:
            raise ValueError("Autorisation Jo d'installation manquante")
        if args.phase == "run" and (not args.authorize_model_calls or args.prepared_env is None):
            raise ValueError("Autorisation Jo modèle ou environnement installé manquant")
        cli = shutil.which(args.codex)
        if not cli:
            raise ValueError("CLI Codex introuvable")
        if args.phase == "install":
            install(args.candidate.resolve(), args.plugin_commit, str(Path(cli).resolve()), args.output_dir)
        else:
            run(args.candidate.resolve(), args.plugin_commit, str(Path(cli).resolve()), args.output_dir,
                args.prepared_env.resolve(), args.model, args.timeout)
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError, queue.Empty) as exc:
        print(json.dumps({"status": "blocked", "reason_type": type(exc).__name__,
                          "reason_sha256": digest(str(exc).encode()), "human_legal_validation": False})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
