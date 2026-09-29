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
    return (
        "Contrat de campagne : avant de répondre, active exactement une fois, "
        f"dans cet ordre, {ordered}. {mcp_rule} "
        "Ne remplace jamais une activation Skill par une simple mention textuelle. "
        "Produis ensuite une réponse unique et finale à la demande suivante.\n\n"
        f"{case['prompt']}"
    )


def allowed_tools(case: dict[str, Any]) -> str:
    """Construit la liste fermée des outils autorisés sans interaction."""

    tools = ["Skill"]
    if case["mcp_mode"] == "required":
        tools.extend(f"{LEGAL_MCP_PREFIX}{name}" for name in MCP_TOOLS)
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


def message_tool_names(event: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Extrait uniquement les noms et entrées des appels d'outils."""

    message = event.get("message") or {}
    calls: list[tuple[str, dict[str, Any]]] = []
    for block in message.get("content") or []:
        if block.get("type") != "tool_use":
            continue
        calls.append((block.get("name", ""), block.get("input") or {}))
    return calls


def sanitize(events: list[dict[str, Any]], case: dict[str, Any]) -> list[dict[str, Any]]:
    """Réduit le flux à la preuve utile, sans raisonnement ni signature."""

    clean: list[dict[str, Any]] = []
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
        for name, inputs in message_tool_names(event):
            if name == "Skill":
                clean.append(
                    {
                        "type": "skill_activation",
                        "skill": inputs.get("skill"),
                    }
                )
            elif name.startswith(LEGAL_MCP_PREFIX):
                clean.append({"type": "plugin_mcp_call", "tool": name})
            elif name.startswith(FOREIGN_MCP_PREFIX):
                clean.append({"type": "foreign_mcp_call", "tool": name})
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
        event for event in clean if event["type"] == "plugin_mcp_call"
    ]
    foreign_calls = [
        event for event in clean if event["type"] == "foreign_mcp_call"
    ]
    if foreign_calls:
        failures.append("foreign_mcp_call")
    if case["mcp_mode"] == "required" and not plugin_calls:
        failures.append("plugin_mcp_call_missing")
    if case["mcp_mode"] == "disabled" and plugin_calls:
        failures.append("plugin_mcp_call_unexpected")

    result = next((event for event in clean if event["type"] == "result"), None)
    if result is None or result.get("is_error"):
        failures.append("result_error_or_absent")
    return failures


def execute(case: dict[str, Any], claude: str) -> tuple[list[dict[str, Any]], int]:
    """Exécute un cas et conserve son flux brut seulement en mémoire."""

    environment = os.environ.copy()
    environment["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"
    completed = subprocess.run(
        build_command(case, claude),
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    events: list[dict[str, Any]] = []
    for line in completed.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return sanitize(events, case), completed.returncode


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
    args = parser.parse_args()

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
        clean, process_exit = execute(case, args.claude)
        failures = technical_failures(clean, case)
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
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
