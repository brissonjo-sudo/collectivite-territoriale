"""Outillage R5 portable : récupération publique et contrôle sans inférence.

Les commandes natives historiques ne sont pas transposées implicitement : leurs
validateurs restent récupérables sans changement, liés au runtime R4 archivé.
Aucun protocole, gel, cache, profil ou état historique n'est une entrée portable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import queue
import subprocess
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_portable


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def write_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def charger(folder: Path, *, manifest_path: Path, contract_path: Path,
            contract_sha256: str, **settings: Any) -> dict[str, Any]:
    """Vérifie l'outillage sans importer le harnais historique à état privé."""
    return r5_portable.check(folder, manifest_path, contract_path, contract_sha256,
                             Path(__file__), **settings)


def commande_hash_compatible(params: dict[str, Any], skill: Path) -> dict[str, Any]:
    """N'adapte que la commande exacte de lecture synthétique SHA-256 de R4."""
    literal = str(skill).replace("'", "''")
    expected = "$ErrorActionPreference='Stop'; (Get-FileHash -LiteralPath '" + literal + "' -Algorithm SHA256).Hash"
    command = params.get("command")
    require(isinstance(command, list) and len(command) == 6 and command[-1] == expected
            and command[1:5] == ["-NoLogo", "-NoProfile", "-NonInteractive", "-Command"]
            and params.get("sandboxPolicy") == {"type": "readOnly"}
            and params.get("timeoutMs") == 20000, "Commande de précontrôle inattendue")
    expression = ("$ErrorActionPreference='Stop'; $hashDsi=[System.Security.Cryptography.SHA256]::Create(); "
                  "try { [System.BitConverter]::ToString($hashDsi.ComputeHash([System.IO.File]::ReadAllBytes('"
                  + literal + "'))).Replace('-','') } finally { $hashDsi.Dispose() }")
    return {**params, "command": [*command[:-1], expression]}


def executer(harness: Any) -> dict[str, Any]:
    """Une seule campagne bornée, sans retry et avec bilan même sur erreur."""
    run = harness.DEFAULT_RUN
    protocol, _, _ = harness.verify(run)
    require(not any((run / "cases" / c["case_id"] / "start.json").exists() for c in protocol["cases"]),
            "Campagne commencée ; aucune relance ni remplacement")
    require(not (run / "campagne-start.json").exists() and not (run / "execution-bilan.json").exists(),
            "Campagne déjà lancée ; aucune reprise")
    harness.write_new(run / "campagne-start.json", {"started_at": harness.now(), "max_seconds": 95 * 60,
                                                  "automatic_retry": False, "release_ready": False})
    started = time.monotonic()
    harness.campaign_deadline = started + 95 * 60
    original_bounded_process = harness.bounded_process

    def bounded_process(*args: Any, **kwargs: Any) -> dict[str, Any]:
        require(harness.campaign_deadline - time.monotonic() >= 260,
                "Budget insuffisant pour une tentative complète")
        return original_bounded_process(*args, **kwargs)

    harness.bounded_process = bounded_process
    outcomes: list[dict[str, Any]] = []
    issues: list[str] = []
    try:
        for case in protocol["cases"]:
            require(harness.campaign_deadline - time.monotonic() >= 300,
                    "Budget global insuffisant avant le prochain cas")
            if (run / "ANNULER").exists():
                issues = ["annulation_avant_prochain_cas"]
                break
            outcome = harness.execute_case(run, case["case_id"])
            outcomes.append(outcome)
            if outcome.get("native_rollout_sha256"):
                issues = harness.export_case(run, case["case_id"])["technical_issues"]
            if outcome.get("timed_out") or outcome.get("capture_overflow") or outcome.get("exit_code") != 0 \
                    or outcome.get("candidate_cache_config_unchanged") is not True:
                issues = issues or ["execution_failed_or_capture_incomplete"]
            print(json.dumps({"case_id": case["case_id"], "executed_cases": len(outcomes),
                              "technical_issues": issues, "release_ready": False}), flush=True)
            if issues:
                break
    except (ValueError, OSError, queue.Empty, subprocess.SubprocessError) as error:
        issues = ["arret_technique_" + type(error).__name__]
        print(json.dumps({"error_type": type(error).__name__, "error_sha256": sha(str(error).encode())}), flush=True)
    finally:
        result = {"completed_at": harness.now(), "executed_cases": len(outcomes),
                  "stopped_on_technical_failure": bool(issues), "stop_reason": issues,
                  "elapsed_seconds": round(time.monotonic() - started, 3), "max_seconds": 95 * 60,
                  "automatic_retry": False, "judges_created": False, "release_ready": False}
        harness.write_new(run / "execution-bilan.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("recover", "check", "init", "preflight", "prepare", "run-all", "export"))
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("r5-dependencies.json"))
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--bundle-sha256")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--contract-sha256")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--candidate-commit")
    parser.add_argument("--state-root", type=Path)
    parser.add_argument("--installed-path", type=Path)
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--cli-sha256")
    parser.add_argument("--cli-version")
    args = parser.parse_args()
    if args.action == "recover":
        result = r5_portable.recover(args.manifest, args.folder, repository=args.repository,
                                     bundle=args.bundle, bundle_sha256=args.bundle_sha256)
    else:
        require(args.action == "check",
                "Action native historique non portable : protocole et bridge du nouveau runtime à arbitrer ; aucun lancement")
        require(args.contract is not None and args.contract_sha256 is not None,
                "Contrat portable et empreinte explicites requis")
        result = charger(args.folder, manifest_path=args.manifest, contract_path=args.contract,
                         contract_sha256=args.contract_sha256,
                         source_root=args.source_root, candidate_commit=args.candidate_commit,
                         state_root=args.state_root, installed_path=args.installed_path,
                         cli=args.cli, cli_sha256=args.cli_sha256, cli_version=args.cli_version)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
