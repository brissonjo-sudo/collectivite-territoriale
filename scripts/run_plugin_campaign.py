"""Exécute les cas comportementaux du plugin dans des sessions Claude fraîches.

Le lanceur ne conserve jamais le flux JSONL brut : les blocs de raisonnement,
signatures et sorties de débogage sont éliminés en mémoire. La sortie produite
reste un brouillon technique à relire avant toute promotion en preuve de
release.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "collectivite-territoriale"
LEGAL_MCP_PREFIX = "mcp__droit-francais__"
FOREIGN_MCP_PREFIX = "mcp__claude_ai_"
MCP_TOOLS = (
    "search",
    "fetch",
    "search_articles",
    "get_article",
    "search_case_law",
    "get_decision",
)


def load_cases() -> list[dict[str, Any]]:
    """Charge le contrat des scénarios comportementaux."""

    return json.loads(
        (ROOT / "tests/cas-plugin.json").read_text(encoding="utf-8")
    )


def qualified_skill(name: str) -> str:
    """Retourne le nom qualifié attendu dans une trace Claude Code."""

    return f"{PLUGIN_NAME}:{name}"


def build_prompt(case: dict[str, Any]) -> str:
    """Construit une instruction d'orchestration explicite et bornée."""

    sequence = [qualified_skill(name) for name in case["activation_sequence"]]
    ordered = " puis ".join(f"`{name}`" for name in sequence)
    mcp_rule = (
        "Utilise au moins un outil du serveur MCP local `droit-francais` et "
        "n'utilise aucun connecteur juridique global."
        if case["mcp_mode"] == "required"
        else "Le MCP est volontairement désactivé : applique la voie dégradée."
    )
    web_rule = (
        "Les articles 33 et 34 du RGPD doivent être vérifiés avec WebFetch "
        "sur EUR-Lex ou, si EUR-Lex ne restitue pas le texte, sur la page "
        "officielle de la CNIL. N'affirme pas le délai comme vérifié si ces "
        "récupérations échouent."
        if case["web_mode"] == "official_source"
        else "N'utilise ni WebFetch ni WebSearch."
    )
    return (
        "Contrat de campagne : avant de répondre, active exactement une fois, "
        f"dans cet ordre, {ordered}. {mcp_rule} {web_rule} "
        "Ne remplace jamais une activation Skill par une simple mention textuelle. "
        "Read est disponible pour consulter les références et profils demandés "
        "par les skills, uniquement sous le dossier skills du plugin local. "
        "Produis ensuite une réponse unique et finale à la demande suivante.\n\n"
        f"{case['prompt']}"
    )


def allowed_tools(case: dict[str, Any]) -> str:
    """Construit la liste fermée des outils autorisés sans interaction."""

    tools = ["Skill", "Read(./skills/**)"]
    if case["web_mode"] == "official_source":
        tools.append("WebFetch")
    if case["mcp_mode"] == "required":
        tools.extend(f"{LEGAL_MCP_PREFIX}{name}" for name in MCP_TOOLS)
    return ",".join(tools)


def builtin_tools(case: dict[str, Any]) -> str:
    """Limite les outils intégrés, indépendamment des permissions implicites."""

    tools = ["Skill", "Read"]
    if case["web_mode"] == "official_source":
        tools.append("WebFetch")
    return ",".join(tools)


def build_command(case: dict[str, Any], claude: str) -> list[str]:
    """Construit la commande Claude Code sans interprétation par un shell."""

    mcp_config = (
        str(ROOT / ".mcp.json")
        if case["mcp_mode"] == "required"
        else '{"mcpServers":{}}'
    )
    return [
        claude,
        "-p",
        "--model",
        "claude-sonnet-4-6",
        "--plugin-dir",
        str(ROOT),
        "--mcp-config",
        mcp_config,
        "--strict-mcp-config",
        "--restricted",
        "--tools",
        builtin_tools(case),
        "--setting-sources",
        "project,local",
        "--no-session-persistence",
        "--no-chrome",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-prompts",
        "none",
        "--allowedTools",
        allowed_tools(case),
        "--max-budget-usd",
        str(case["max_budget_usd"]),
        "--prompt-suggestions",
        "false",
        build_prompt(case),
    ]


def message_tool_calls(
    event: dict[str, Any],
) -> list[tuple[str, dict[str, Any], str]]:
    """Extrait uniquement les noms et entrées des appels d'outils."""

    message = event.get("message") or {}
    calls: list[tuple[str, dict[str, Any], str]] = []
    for block in message.get("content") or []:
        if block.get("type") != "tool_use":
            continue
        calls.append(
            (
                block.get("name", ""),
                block.get("input") or {},
                block.get("id", ""),
            )
        )
    return calls


def sanitize(events: list[dict[str, Any]], case: dict[str, Any]) -> list[dict[str, Any]]:
    """Réduit le flux à la preuve utile, sans raisonnement ni signature."""

    clean: list[dict[str, Any]] = []
    calls_by_id: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("type") == "system" and event.get("subtype") == "init":
            skills = [
                name
                for name in event.get("skills", [])
                if name.startswith(f"{PLUGIN_NAME}:")
            ]
            clean.append(
                {
                    "type": "init",
                    "host": f"Claude Code {event.get('claude_code_version', 'inconnu')}",
                    "model": event.get("model"),
                    "available_skills": skills,
                    "standalone_recherche_juridique_loaded": (
                        "recherche-juridique" in event.get("skills", [])
                    ),
                    "mcp_servers": event.get("mcp_servers", []),
                    "mcp_mode": case["mcp_mode"],
                    "strict_mcp_config": True,
                }
            )
        for name, inputs, tool_use_id in message_tool_calls(event):
            if name == "Skill":
                record = {
                    "type": "skill_activation",
                    "skill": inputs.get("skill"),
                }
            elif name == "Read":
                try:
                    relative = Path(inputs.get("file_path", "")).resolve().relative_to(
                        (ROOT / "skills").resolve()
                    )
                    record = {
                        "type": "plugin_file_read",
                        "path": relative.as_posix(),
                        "succeeded": None,
                    }
                except (ValueError, OSError):
                    record = {"type": "unexpected_tool_call", "tool": "Read outside plugin skills"}
            elif name.startswith(LEGAL_MCP_PREFIX):
                record = {
                    "type": "plugin_mcp_call",
                    "tool": name,
                    "succeeded": None,
                }
            elif name.startswith(FOREIGN_MCP_PREFIX):
                record = {"type": "foreign_mcp_call", "tool": name}
            elif name == "WebFetch":
                record = {
                    "type": "official_source_call",
                    "tool": name,
                    "host": urlparse(inputs.get("url", "")).hostname,
                    "source_path": urlparse(inputs.get("url", "")).path,
                    "succeeded": None,
                }
            else:
                record = {"type": "unexpected_tool_call", "tool": name}
            clean.append(record)
            if tool_use_id:
                calls_by_id[tool_use_id] = record

        message = event.get("message") or {}
        for block in message.get("content") or []:
            if block.get("type") != "tool_result":
                continue
            record = calls_by_id.get(block.get("tool_use_id", ""))
            if record is not None and "succeeded" in record:
                record["succeeded"] = not bool(block.get("is_error"))
        if event.get("type") == "result":
            clean.append(
                {
                    "type": "result",
                    "subtype": event.get("subtype"),
                    "is_error": event.get("is_error"),
                    "cost_usd": event.get("total_cost_usd"),
                    "result": event.get("result", ""),
                    "errors": event.get("errors", []),
                }
            )
    return clean


def technical_failures(clean: list[dict[str, Any]], case: dict[str, Any]) -> list[str]:
    """Contrôle les preuves techniques, hors appréciation métier humaine."""

    failures: list[str] = []
    init = next((event for event in clean if event["type"] == "init"), None)
    if init is None:
        failures.append("init_absent")
    elif init["standalone_recherche_juridique_loaded"]:
        failures.append("standalone_recherche_juridique_loaded")

    activations = [
        event.get("skill")
        for event in clean
        if event["type"] == "skill_activation"
    ]
    expected = [qualified_skill(name) for name in case["activation_sequence"]]
    if activations != expected:
        failures.append("activation_sequence_mismatch")

    plugin_calls = [
        event
        for event in clean
        if event["type"] == "plugin_mcp_call" and event.get("succeeded") is True
    ]
    foreign_calls = [
        event for event in clean if event["type"] == "foreign_mcp_call"
    ]
    if foreign_calls:
        failures.append("foreign_mcp_call")
    if any(event["type"] == "unexpected_tool_call" for event in clean):
        failures.append("unexpected_tool_call")
    if case["mcp_mode"] == "required" and not plugin_calls:
        failures.append("plugin_mcp_call_missing")
    if case["mcp_mode"] == "disabled" and plugin_calls:
        failures.append("plugin_mcp_call_unexpected")
    if case["mcp_mode"] == "disabled" and any(
        event["type"] == "plugin_mcp_call" for event in clean
    ):
        if "plugin_mcp_call_unexpected" not in failures:
            failures.append("plugin_mcp_call_unexpected")

    official_calls = [
        event
        for event in clean
        if event["type"] == "official_source_call"
        and event.get("succeeded") is True
    ]
    if case["web_mode"] == "official_source":
        expected_hosts = set(case["official_source_hosts"])
        if not any(event.get("host") in expected_hosts for event in official_calls):
            failures.append("official_source_call_missing")
        if any(
            event.get("host") not in expected_hosts
            for event in clean if event["type"] == "official_source_call"
        ):
            failures.append("non_official_web_source")
    elif any(event["type"] == "official_source_call" for event in clean):
        failures.append("web_call_unexpected")

    result = next((event for event in clean if event["type"] == "result"), None)
    if result is None or result.get("is_error"):
        failures.append("result_error_or_absent")
    return failures


def execute(case: dict[str, Any], claude: str, timeout: int = 300) -> tuple[list[dict[str, Any]], int]:
    """Exécute un cas et conserve son flux brut seulement en mémoire."""

    environment = os.environ.copy()
    environment["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"
    if timeout <= 0:
        raise ValueError("Le délai d'exécution doit être positif")
    try:
        completed = subprocess.run(
            build_command(case, claude), cwd=ROOT, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False,
            timeout=timeout,
        )
        raw, exit_code = completed.stdout, completed.returncode
    except subprocess.TimeoutExpired as error:
        raw = error.stdout or ""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        exit_code = 124
    events: list[dict[str, Any]] = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return sanitize(events, case), exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--claude", default="claude")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "tests/evidence/.work",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--stop-on-failure", action="store_true")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout doit être positif")

    cases = load_cases()
    selected = [
        case for case in cases if not args.case_ids or case["id"] in args.case_ids
    ]
    if args.case_ids and len(selected) != len(set(args.case_ids)):
        parser.error("Un identifiant de cas est inconnu ou dupliqué")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    for case in selected:
        if args.dry_run:
            print(json.dumps(build_command(case, args.claude), ensure_ascii=False))
            continue
        clean, process_exit = execute(case, args.claude, args.timeout)
        failures = technical_failures(clean, case)
        if process_exit:
            failures.append("process_exit_nonzero")
            if process_exit == 124:
                failures.append("process_timeout")
        summary = {
            "type": "technical_assessment",
            "case_id": case["id"],
            "process_exit": process_exit,
            "status": "passed" if not failures else "failed",
            "failures": failures,
            "requires_human_invariant_review": not failures,
        }
        clean.append(summary)
        destination = args.output_dir / f"{case['id']}.jsonl"
        destination.write_text(
            "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in clean),
            encoding="utf-8",
            newline="\n",
        )
        print(f"[{summary['status'].upper()}] {case['id']} -> {destination}")
        if failures:
            exit_code = 1
            if args.stop_on_failure:
                break
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
