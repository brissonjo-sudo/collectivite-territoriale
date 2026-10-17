"""Chronologie visible et activations prouvées par les entrées complètes.

Un texte mentionnant un skill n'est jamais une activation. Le raisonnement
interne n'est ni conservé ni pris pour un message visible.
"""
from __future__ import annotations

import re
from typing import Any, Callable


def timeline(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Conserve les débuts d'outils, y compris avortés, et les textes visibles."""
    result: list[dict[str, Any]] = []
    seen_tools: set[str] = set()
    started: set[str] = set()
    completed: set[str] = set()
    for position, event in enumerate(events):
        kind = event.get("type", "")
        if kind in {"error", "turn.failed"}:
            result.append({"type": "trace_error", "position": position})
        if kind not in {"item.started", "item.updated", "item.completed"}:
            continue
        item = event.get("item") or {}
        item_type = item.get("type")
        if item_type == "agent_message":
            if isinstance(item.get("text"), str) and item["text"].strip():
                result.append({"type": "visible_text", "position": position,
                               "item_id": item.get("id"), "text": item["text"]})
        elif item_type != "reasoning":
            # Tout type futur inconnu est conservativement une action.
            identity = item.get("id") or str(position)
            if identity not in seen_tools:
                result.append({"type": "tool_boundary", "position": position,
                               "item_type": item_type})
                seen_tools.add(identity)
            if item_type not in {"command_execution", "mcp_tool_call", "web_search"}:
                result.append({"type": "trace_error", "position": position})
            if kind == "item.started":
                started.add(identity)
            if kind == "item.completed":
                completed.add(identity)
    if started - completed:
        result.append({"type": "trace_error", "position": len(events)})
    return result


def stop_errors(clean: list[dict[str, Any]]) -> list[str]:
    """Exige STOP comme premier texte visible, complet avant le premier outil."""
    chronology = [e for e in clean if e["type"] in {"visible_text", "tool_boundary"}]
    texts = [e for e in chronology if e["type"] == "visible_text"]
    if not texts:
        return ["stop_first_absent"]
    first = texts[0]
    text = first["text"].lstrip()
    # Un fragment de streaming doit rester un préfixe de STOP jusqu'à complétion.
    normalized = re.sub(r"^(?:\*\*|__)", "", text)
    if not (re.match(r"^STOP\b", normalized) or "STOP".startswith(normalized)):
        return ["stop_first_absent"]
    boundary = next((e["position"] for e in chronology if e["type"] == "tool_boundary"), float("inf"))
    complete = [e for e in texts if e.get("item_id") == first.get("item_id")
                and re.match(r"^\s*(?:\*\*|__)?STOP\b", e["text"])]
    if not complete:
        return ["stop_first_absent"]
    if first["position"] >= boundary or complete[0]["position"] >= boundary:
        return ["stop_after_tool"]
    return []


def activated_skills(clean: list[dict[str, Any]], chunks: Callable[[str], list[dict]]) -> tuple[list[str], list[str]]:
    """Valide chaque segment et n'active un skill qu'après son entrée complète."""
    observed: list[str] = []
    errors: list[str] = []
    pending: list[tuple[str, int, int]] = []
    active: str | None = None
    for event in clean:
        if event["type"] != "native_read":
            continue
        entries = [p for p in event["paths"] if p.endswith("/SKILL.md")]
        if not entries:
            continue
        if len(entries) != 1 or event.get("exit_code") != 0 or event.get("status") != "completed":
            errors.append("activation_read_failed")
            continue
        path = entries[0]
        name = path.split("/")[-2]
        expected = [(c["path"], c["start"], c["count"]) for c in chunks(path)]
        chunk = event.get("chunk")
        if chunk is None or not chunk.get("content_verified"):
            errors.append("activation_entry_unverified")
            continue
        if active is None:
            active, pending = name, expected[:]
        current = (chunk["path"], chunk["start"], chunk["count"])
        if active != name or not pending or pending[0] != current:
            errors.append("activation_entry_order_mismatch")
            continue
        pending.pop(0)
        if not pending:
            if name in observed:
                errors.append("activation_duplicated")
            observed.append(name)
            active = None
    if active is not None:
        errors.append("activation_entry_incomplete")
    return observed, errors


def behavior_errors(clean: list[dict[str, Any]], case: dict[str, Any],
                    chunks: Callable[[str], list[dict]]) -> list[str]:
    """Contrôle les cas v2 ; aucun jugement sur le droit ou le fond métier."""
    observed, errors = activated_skills(clean, chunks)
    if set(observed) != set(case["skills"]):
        errors.append("activation_missing_or_unexpected")
    if case["activation_mode"] == "forced" and observed != case["activation_sequence"]:
        errors.append("activation_sequence_mismatch")
    if any(e["type"] == "trace_error" for e in clean):
        errors.append("trace_error")
    if case["stop_first"]:
        errors.extend(stop_errors(clean))
    return list(dict.fromkeys(errors))
