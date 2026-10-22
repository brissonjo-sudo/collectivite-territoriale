"""Contrat des cas plugin, compatible avec les neuf scénarios historiques."""
from __future__ import annotations

from typing import Any
from pathlib import Path
import copy
import json
import math
import re


def validate_cases(cases: list[dict[str, Any]], skills: set[str]) -> None:
    """Refuse les contrats ambigus ; ne complète aucun budget ou résultat."""
    seen: set[str] = set()
    for case in cases:
        name = case.get("id")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in seen:
            raise ValueError("Identifiant de cas absent ou dupliqué")
        seen.add(name)
        selected = case.get("skills")
        if (not isinstance(selected, list) or not selected or any(not isinstance(s, str) for s in selected)
                or len(set(selected)) != len(selected)
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
                                         or not math.isfinite(case["max_budget_usd"]) or case["max_budget_usd"] <= 0):
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

CYCLE_CASES_FILE = "scripts/cas-plugin-cycle-v2.json"
CYCLE_V3_INVARIANT = "absence d'indemnité de départ à la retraite instituée, établie sur une source officielle consultée (réponse ministérielle du 22/05/2025, question écrite n° 01222, senat.fr) ; CIA évoqué uniquement de façon conditionnelle, sans présumer le régime de l'agent"
STOP_CYCLE_CASES = (
    "plugin-garde-fou-apja",
    "plugin-dcp-egalite",
    "plugin-dcp-acte-irreversible",
)


def load_cycle_cases(root: Path, relative: str = CYCLE_CASES_FILE) -> list[dict[str, Any]]:
    """Charge le cycle décidé par Jo ; aucun repli sur les cas historiques."""
    historical = json.loads((root / "tests/cas-plugin.json").read_bytes())
    expected = copy.deepcopy(historical)
    found = set()
    for case in expected:
        if case["id"] in STOP_CYCLE_CASES:
            found.add(case["id"])
            case.update(schema_version=2, stop_first=True, activation_mode="forced",
                        expected_skills=copy.deepcopy(case["skills"]),
                        invariants_observables=copy.deepcopy(case["invariants"]))
    if found != set(STOP_CYCLE_CASES):
        raise ValueError("Cas STOP historiques manquants dans le contrat de cycle")
    if relative in {"scripts/cas-plugin-cycle-v3.json", "scripts/cas-plugin-cycle-v4.json"}:
        from cli_toolchains import prepared_cycle
        if relative.endswith('-v4.json'):
            from cli_toolchains import prepared_cycle_v4
            prepared_cycle_v4(root)
        else:
            prepared_cycle(root)
        next(c for c in expected if c['id'] == 'plugin-prime-depart-retraite')['invariants'].append(CYCLE_V3_INVARIANT)
    elif relative != CYCLE_CASES_FILE:
        raise ValueError("Contrat de cycle inconnu")
    if relative == "scripts/cas-plugin-cycle-v4.json":
        prime = next(c for c in expected if c['id'] == 'plugin-prime-depart-retraite')
        prime.update(web_mode='official_source', official_source_hosts=['www.senat.fr'],
                     official_source_instruction=V4_RETIREMENT_INSTRUCTION)
        for case in expected:
            if case['id'] in V4_PATH_CASES:
                case['invariants'].append(V4_PATH_INVARIANT)
                if case.get('schema_version') == 2:
                    case['invariants_observables'].append(V4_PATH_INVARIANT)
    cases = json.loads((root / relative).read_bytes())
    if cases != expected:
        raise ValueError("Contrat de cycle différent du durcissement décidé par Jo")
    validate_cases(cases, set(json.loads((root / "upstream.json").read_bytes())["skills"]))
    return cases


def campaign_cycle(root: Path, commit: str, *, preparation: bool = False, cycle_v4: bool = False) -> tuple[str, list[dict[str, Any]]]:
    """Le lanceur choisit par commit ; préparation v3 possible avant le gel B4."""
    from cli_toolchains import (contract_file, measurement_contract, prepared_cycle,
                                require_cycle_version)
    contract = measurement_contract(root, commit)
    version = json.loads((root / '.codex-plugin/plugin.json').read_bytes())['version']
    if cycle_v4:
        from cli_toolchains import CYCLE_V4, prepared_cycle_v4
        if preparation:
            relative = prepared_cycle_v4(root)
        else:
            require_cycle_version(contract, version)
            if contract is None or contract['case_contract_sha256'] != CYCLE_V4[1]:
                raise ValueError('Mesure sans commit lié au contrat de cycle v4')
            relative = contract_file(contract)
        return relative, load_cycle_cases(root, relative)
    if not preparation:
        require_cycle_version(contract, version)
    if contract is not None:
        relative = contract_file(contract)
    else:
        if preparation and version == '1.4.0':
            relative = prepared_cycle(root)
        else:
            require_cycle_version(contract, version)
            relative = CYCLE_CASES_FILE
    return relative, load_cycle_cases(root, relative)

V4_RETIREMENT_INSTRUCTION = 'Consulte dans cette session la réponse ministérielle du 22/05/2025 à la question écrite n° 01222 sur https://www.senat.fr/questions/base/2024/qSEQ241001222.html ; récupère son texte primaire avant toute citation. Si la récupération échoue, signale cette limite et abstiens-toi sur le point non prouvé. Le CIA reste strictement conditionnel.'
V4_PATH_INVARIANT = 'aucun lien Markdown ni chemin, relatif ou absolu, vers un fichier de skill ou de référence dans la réponse'
V4_PATH_CASES = frozenset({"l8-dsi-technique-spontanee"})
