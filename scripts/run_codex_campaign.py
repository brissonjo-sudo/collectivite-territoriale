"""Mesure technique Codex des copies natives du candidat, hors installation.

Les neuf contrats métier restent inchangés. Une lecture native réussie n'est
pas une activation de l'outil Skill de Claude. Aucun raisonnement, signature
ou flux brut n'est conservé ; la relecture des invariants reste humaine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from run_plugin_campaign import ROOT, MCP_TOOLS, load_cases

PROFILE = "codex-copies-natives-mcp-v4"
CHUNK_BYTES = 6000


def entry_chunks(path: str) -> list[dict[str, Any]]:
    """Découpe le point d'entrée en plages contiguës sans changer ses octets."""
    source = ROOT / "skills" / path.removeprefix(".agents/skills/")
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    chunks = []
    start = 0
    while start < len(lines):
        end, size = start, 0
        while end < len(lines) and size + len(lines[end].encode()) <= CHUNK_BYTES:
            size += len(lines[end].encode())
            end += 1
        if end == start:
            raise ValueError("Ligne trop longue pour une restitution bornée : " + path)
        chunks.append({"path": path, "start": start, "count": end-start,
                       "content": "".join(lines[start:end])})
        start = end
    return chunks


def read_body(command_text: str) -> str:
    body = command_text.replace("\\", "/").strip()
    wrapper = re.search(r"\s-Command\s+(['\"])(.*)\1\s*$", body, re.S)
    return wrapper.group(2) if wrapper else body


def read_chunk(command_text: str) -> dict[str, Any] | None:
    """Autorise seulement le pipeline de lecture généré, sans expression libre."""
    match = re.fullmatch(
        r"Get-Content -LiteralPath '([\w./-]+)' -Encoding utf8 \| Select-Object -Skip (\d+) -First (\d+)",
        read_body(command_text), re.I)
    if not match:
        return None
    path, start, count = match.groups()
    if not re.fullmatch(r"\.agents/skills/[\w-]+/SKILL\.md", path):
        return None
    return {"path": path, "start": int(start), "count": int(count)}


def read_reference_slice(command_text: str) -> dict[str, Any] | None:
    """Une sélection bornée de référence est une lecture autorisée du runtime."""
    match = re.fullmatch(
        r"Get-Content -LiteralPath '(\.agents/skills/[\w-]+/(?:references|objets)/[\w./-]+\.md)' -Encoding utf8 \| Select-Object (?:-Skip (\d+) )?-First (\d+)",
        read_body(command_text),re.I)
    if not match:
        return None
    path,start,count = match.groups()
    if ".." in path.split("/") or int(count) <= 0:
        return None
    return {"path":path,"start":int(start or 0),"count":int(count)}


def read_command_paths(command_text: str) -> list[str]:
    """Accepte uniquement une commande de lecture et des chemins natifs."""
    chunk = read_chunk(command_text)
    if chunk:
        return [chunk["path"]]
    reference = read_reference_slice(command_text)
    if reference:
        return [reference["path"]]
    body = read_body(command_text)
    if any(char in body for char in (";", "|", ">", "<", "&", "$", "`", "\n", "\r")):
        return []
    try:
        tokens = shlex.split(body)
    except ValueError:
        return []
    if not tokens or tokens.pop(0).lower() != "get-content":
        return []
    paths = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if token.lower() in {"-literalpath", "-path", "-raw"}:
            continue
        if token.lower() == "-encoding":
            if index >= len(tokens) or tokens[index].lower() not in {"utf8", "utf-8"}:
                return []
            index += 1
            continue
        for path in token.split(","):
            if not path:
                continue
            if not re.fullmatch(r"\.agents/skills/[\w./-]+", path) or ".." in path.split("/"):
                return []
            paths.append(path)
    return paths


def command(case: dict[str, Any], cli: str, model: str) -> list[str]:
    """Isole la configuration d'outils sans changer les identifiants OAuth."""
    args = [cli, "exec", "--json", "--skip-git-repo-check", "--ignore-user-config",
            "--sandbox", "read-only", "-m", model, "-c",
            'web_search="live"' if case["web_mode"] == "official_source" else 'web_search="disabled"']
    if sys.platform == "win32":
        args.extend(["-c", 'windows.sandbox="elevated"'])
    if case["mcp_mode"] == "required":
        server = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["droit-francais"]
        values = {
            "url": server["url"], "required": True, "startup_timeout_sec": 40,
            "tool_timeout_sec": 60, "enabled_tools": list(MCP_TOOLS),
            "oauth.client_id": server["oauth"]["clientId"],
            "oauth.callback_port": server["oauth"]["callbackPort"],
        }
        for key, value in values.items():
            args.extend(["-c", f"mcp_servers.droit-francais.{key}=" + json.dumps(value)])
    return args + ["-"]


def prompt(case: dict[str, Any]) -> str:
    paths = [f".agents/skills/{name}/SKILL.md" for name in case["activation_sequence"]]
    plan = [chunk for path in paths for chunk in entry_chunks(path)]
    reads = "\n".join(
        f"{i+1}. Get-Content -LiteralPath '{c['path']}' -Encoding utf8 | Select-Object -Skip {c['start']} -First {c['count']}"
        for i, c in enumerate(plan))
    source_rule = (
        "Appelle au moins un outil du seul MCP droit-francais disponible ; une mention ne vaut pas un appel réussi."
        if case["mcp_mode"] == "required" else
        "MCP volontairement absent : applique la voie dégradée, aucune source officielle accessible."
    )
    web_rule = (
        "Vérifie les articles 33 et 34 du RGPD en ouvrant EUR-Lex ou la CNIL ; ne présume aucun délai si la récupération échoue. Seuls eur-lex.europa.eu et www.cnil.fr sont autorisés pour le web."
        if case["web_mode"] == "official_source" else "N'utilise aucun web."
    )
    return (
        "Contrat technique de campagne Codex, en français. Les six skills sont des copies natives du candidat. "
        "Avant de répondre, lis intégralement chaque SKILL.md, une fois, par les segments contigus ci-dessous. "
        "Exécute chaque segment dans un appel d'outil séparé, dans l'ordre exact. Ne groupe pas les appels, "
        "ne remplace pas ces lectures par une mention et ne relis pas le fichier entier :\n"
        + reads + "\nChaque segment contient au plus 6000 octets. Demande max_output_tokens=8000 à l'outil "
        "de commande pour chacun. Si une restitution reste tronquée, signale cette limite. "
        "Lis ensuite les références nécessaires uniquement sous .agents/skills/ avec Get-Content. "
        "Pour ces références, utilise soit Get-Content -LiteralPath 'chemin' -Encoding utf8, "
        "soit ce même appel suivi de | Select-Object -Skip N -First M avec N et M entiers positifs. "
        "Select-String et les autres pipelines ne font pas partie de ce protocole de mesure. "
        "N'exécute aucune autre commande, aucun script, aucune requête réseau par shell. "
        + source_rule + " " + web_rule + "\nProduis une réponse finale unique à la demande :\n\n" + case["prompt"]
    )


def sanitize(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """N'exporte que les preuves d'outils terminés et la réponse finale."""
    clean: list[dict[str, Any]] = []
    for event in events:
        item = event.get("item") or {}
        if event.get("type") == "turn.completed":
            clean.append({"type": "turn_completed", "usage": event.get("usage")})
        if event.get("type") != "item.completed":
            continue
        kind = item.get("type")
        if kind == "command_execution":
            paths = read_command_paths(item.get("command", ""))
            chunk = read_chunk(item.get("command", ""))
            output = item.get("aggregated_output", "").replace("\r\n", "\n")
            verified = []
            for path in paths:
                source = ROOT / "skills" / path.removeprefix(".agents/skills/")
                if source.is_file() and source.read_text(encoding="utf-8").strip() in output:
                    verified.append(path)
            record = {"type": "native_read" if paths else "unexpected_command",
                          "paths": paths, "complete_content_verified": verified,
                          "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
                          "exit_code": item.get("exit_code"), "status": item.get("status")}
            if chunk:
                chunk_source = ROOT / "skills" / chunk["path"].removeprefix(".agents/skills/")
                expected = next((c for c in entry_chunks(chunk["path"])
                                 if c["start"] == chunk["start"] and c["count"] == chunk["count"]), None) if chunk_source.is_file() else None
                record["chunk"] = {**chunk, "content_verified": bool(expected and expected["content"].strip() in output),
                    "expected_content_sha256": hashlib.sha256(expected["content"].encode()).hexdigest() if expected else None,
                    "source_bytes": len(expected["content"].encode()) if expected else None}
            clean.append(record)
        elif kind == "mcp_tool_call":
            result = item.get("result") or {}
            serialized = json.dumps(result, sort_keys=True, ensure_ascii=False)
            clean.append({"type": "mcp_call", "server": item.get("server"), "tool": item.get("tool"),
                          "status": item.get("status"),
                          "succeeded": item.get("status") == "completed" and bool(result)
                          and not result.get("isError", False) and item.get("error") is None,
                          "arguments_publics": {k:v for k,v in (item.get("arguments") or {}).items()
                                                if k in {"id", "code", "number", "date", "limit"}},
                          "identifiants_dans_resultat": sorted(set(re.findall(r"(?:LEGIARTI|JORFTEXT|CETATEXT|JURITEXT)\d+", serialized))),
                          "result_sha256": hashlib.sha256(serialized.encode()).hexdigest()})
        elif kind == "web_search":
            action = (item.get("action") or {}).get("type")
            hosts = sorted({urlsplit(r.get("url", "")).hostname for r in item.get("results", []) if r.get("url")})
            clean.append({"type": "web_call", "action": action, "hosts": hosts,
                          "status": item.get("status"), "result_present": bool(item.get("results"))})
        elif kind == "agent_message":
            if item.get("text"):
                clean.append({"type": "reply", "text": item["text"]})
    return clean


def failures(clean: list[dict[str, Any]], case: dict[str, Any], exit_code: int,
             profile: str | None = None) -> list[str]:
    """Évalue la traçabilité technique, sans noter le fond juridique."""
    errors = []
    if exit_code:
        errors.append("process_timeout" if exit_code == 124 else "process_exit_nonzero")
    reads = [path.split("/")[2] for e in clean if e["type"] == "native_read"
             and e["exit_code"] == 0 and e["status"] == "completed"
             for path in e["paths"] if path.endswith("/SKILL.md")]
    segmented = profile == PROFILE or any("chunk" in e for e in clean)
    if segmented:
        expected = [(c["path"],c["start"],c["count"])
                    for name in case["activation_sequence"]
                    for c in entry_chunks(f".agents/skills/{name}/SKILL.md")]
        entries = [e for e in clean if e["type"] == "native_read"
                   and any(p.endswith("/SKILL.md") for p in e["paths"])]
        observed = [(e["chunk"]["path"],e["chunk"]["start"],e["chunk"]["count"])
                    for e in entries if "chunk" in e and e["exit_code"] == 0 and e["status"] == "completed"]
        if observed != expected or len(entries) != len(expected):
            errors.append("native_entry_coverage_mismatch")
        if any(not e.get("chunk", {}).get("content_verified") for e in entries):
            errors.append("native_entry_content_unverified")
    elif reads != case["activation_sequence"]:
        errors.append("native_read_sequence_mismatch")
    if any(e["type"] == "unexpected_command" for e in clean):
        errors.append("unexpected_command")
    for event in clean:
        if segmented or event["type"] != "native_read" or "complete_content_verified" not in event:
            continue  # Les preuves v1 gardent leur portée historique.
        entries = [p for p in event["paths"] if p.endswith("/SKILL.md")]
        if entries and (len(entries) != 1 or any(p not in event["complete_content_verified"] for p in entries)):
            if "native_entry_content_unverified" not in errors:
                errors.append("native_entry_content_unverified")
    calls = [e for e in clean if e["type"] == "mcp_call"]
    if any(e["server"] != "droit-francais" or e["tool"] not in MCP_TOOLS for e in calls):
        errors.append("foreign_mcp_call")
    if case["mcp_mode"] == "required" and not any(e["succeeded"] for e in calls):
        errors.append("plugin_mcp_call_missing")
    if case["mcp_mode"] == "disabled" and calls:
        errors.append("plugin_mcp_call_unexpected")
    web = [e for e in clean if e["type"] == "web_call"]
    if case["web_mode"] == "disabled" and web:
        errors.append("web_call_unexpected")
    if case["web_mode"] == "official_source":
        pages = [e for e in web if e["action"] in ("open_page", "find_in_page")]
        allowed = set(case["official_source_hosts"])
        if not any(e["result_present"] and set(e["hosts"]) & allowed for e in pages):
            errors.append("official_source_call_missing")
        if any(set(e["hosts"]) - allowed for e in pages):
            errors.append("non_official_web_source")
    if not any(e["type"] == "reply" for e in clean) or not any(e["type"] == "turn_completed" for e in clean):
        errors.append("result_error_or_absent")
    return errors


def execute(case: dict[str, Any], cli: str, model: str, timeout: int) -> tuple[list[dict[str, Any]], int]:
    if timeout <= 0:
        raise ValueError("Le délai doit être positif")
    with tempfile.TemporaryDirectory(prefix="ct-codex-campagne-") as directory:
        workspace = Path(directory)
        shutil.copytree(ROOT / "skills", workspace / ".agents/skills")
        try:
            completed = subprocess.run(command(case, cli, model), cwd=workspace, input=prompt(case),
                                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
            raw, code = completed.stdout, completed.returncode
        except subprocess.TimeoutExpired as error:
            raw, code = error.stdout or "", 124
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8", errors="replace")
        events = []
        for line in raw.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict):
                events.append(event)
        return sanitize(events), code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stop-on-failure", action="store_true")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout doit être positif")
    cases = load_cases()
    selected = [c for c in cases if not args.case_ids or c["id"] in args.case_ids]
    if args.case_ids and len(selected) != len(set(args.case_ids)):
        parser.error("Cas inconnu ou dupliqué")
    destinations = [args.output_dir / (c["id"] + ".json") for c in selected]
    if any(p.exists() for p in destinations):
        parser.error("Une preuve existe déjà : choisir un nouveau dossier pour un nouvel essai")
    runtime = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted((ROOT / "skills").rglob("*")) if p.is_file()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = 0
    for case, destination in zip(selected, destinations):
        print(f"[EN COURS] {case['id']}", flush=True)
        clean, code = execute(case, args.codex, args.model, args.timeout)
        errors = failures(clean, case, code, PROFILE)
        evidence = {"profile": PROFILE, "case_id": case["id"], "model_requested": args.model,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "runtime_sha256": runtime, "case_sha256": hashlib.sha256(json.dumps(case, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                    "host": subprocess.run([args.codex, "--version"], capture_output=True, text=True).stdout.strip(),
                    "process_exit": code, "technical_status": "failed" if errors else "passed", "failures": errors,
                    "human_legal_validation": False, "marketplace_installation_tested": False, "events": clean}
        destination.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"[{evidence['technical_status'].upper()}] {case['id']} : {errors}", flush=True)
        if errors:
            result = 1
            if args.stop_on_failure:
                break
    return result


if __name__ == "__main__":
    raise SystemExit(main())
