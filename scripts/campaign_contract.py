"""Contrat des cas plugin, compatible avec les neuf scénarios historiques."""
from __future__ import annotations

from typing import Any


def validate_cases(cases: list[dict[str, Any]], skills: set[str]) -> None:
    """Refuse les contrats ambigus ; ne complète aucun budget ou résultat."""
    seen: set[str] = set()
    for case in cases:
        name = case.get("id")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("Identifiant de cas absent ou dupliqué")
        seen.add(name)
        selected = case.get("skills")
        if (not isinstance(selected, list) or not selected or len(set(selected)) != len(selected)
                or not set(selected).issubset(skills)):
            raise ValueError("Skills de cas invalides : " + name)
        if case.get("mcp_mode") not in {"required", "disabled"}:
            raise ValueError("Mode MCP invalide : " + name)
        if case.get("mcp") != ("droit-francais" if case["mcp_mode"] == "required" else None):
            raise ValueError("Serveur MCP incohérent : " + name)
        if case.get("web_mode") not in {"official_source", "disabled"}:
            raise ValueError("Mode web invalide : " + name)
        if case["web_mode"] == "official_source" and not case.get("official_source_hosts"):
            raise ValueError("Domaines officiels absents : " + name)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("Prompt absent : " + name)
        invariants = case.get("invariants")
        if (not isinstance(invariants, list) or not invariants
                or any(not isinstance(i, str) or not i.strip() for i in invariants)
                or len(set(invariants)) != len(invariants)):
            raise ValueError("Invariants absents ou dupliqués : " + name)
        if "max_budget_usd" in case and (type(case["max_budget_usd"]) not in {int, float}
                                         or case["max_budget_usd"] <= 0):
            raise ValueError("Budget invalide : " + name)
        version = case.get("schema_version", 1)
        if version not in {1, 2}:
            raise ValueError("Version de contrat inconnue : " + name)
        if version == 1:
            if case.get("activation_sequence") != selected:
                raise ValueError("Séquence historique divergente : " + name)
            continue
        if type(case.get("stop_first")) is not bool:
            raise ValueError("stop_first doit être explicite : " + name)
        if case.get("activation_mode") not in {"forced", "spontaneous"}:
            raise ValueError("Mode d'activation invalide : " + name)
        if case.get("expected_skills") != selected or case.get("invariants_observables") != invariants:
            raise ValueError("Perte du contrat DSI : " + name)
        expected = selected if case["activation_mode"] == "forced" else []
        if case.get("activation_sequence") != expected:
            raise ValueError("Séquence incompatible avec le mode : " + name)

