"""Reprise explicite de dev.7 avec un CLI choisi et figé, sans modifier R4.

Les dépendances historiques sont copiées après contrôle de leurs empreintes.
Aucun secret n'est copié. Le profil déjà installé est utilisé et vérifié.
Les commandes init/check/preflight/prepare ne lancent aucun répondant.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import queue
import subprocess
import sys
import time
from typing import Any


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


def initialiser(legacy: Path, destination: Path, cli: Path) -> dict[str, Any]:
    """Crée un successeur R5 après vérification des sources et du CLI explicite."""
    legacy, destination, cli = legacy.resolve(), destination.resolve(), cli.resolve()
    require(not destination.exists(), "Destination existante ; aucun remplacement")
    require(not destination.is_relative_to(legacy), "Les preuves historiques restent hors destination")
    original = legacy / "protocole-native-dev7-complet-20261009-r4.json"
    protocol = read(original)
    control = read(legacy / "controle-reprise-efficace-dev7-20261009.json")
    require(protocol["schema_version"] == "dev7-native-complete-protocol-v4", "Protocole R4 requis")
    required = {**protocol["immutable_tools_sha256"], **protocol["predecessor_tools_sha256"],
                **control["tools_sha256"]}
    # Les recouvrements doivent désigner exactement les mêmes octets.
    for mapping in (protocol["immutable_tools_sha256"], protocol["predecessor_tools_sha256"], control["tools_sha256"]):
        require(all(required[name] == digest for name, digest in mapping.items()), "Gels contradictoires")
    for name, digest in required.items():
        require(Path(name).name == name and sha((legacy / name).read_bytes()) == digest,
                "Outillage historique divergent : " + name)
    extras = {protocol["proposal_path"]: protocol["proposal_sha256"],
              protocol["r3_manifest_path"]: protocol["r3_manifest_sha256"]}
    for name, digest in extras.items():
        target = (legacy / name).resolve()
        require(target.is_relative_to(legacy) and sha(target.read_bytes()) == digest, "Preuve historique divergente")
    require(cli.is_file(), "CLI explicite absent")
    cli_digest = sha(cli.read_bytes())
    version = subprocess.run([str(cli), "--version"], capture_output=True, timeout=20, check=True)
    require(sha(cli.read_bytes()) == cli_digest, "CLI modifié pendant sa détection")
    cli_version = version.stdout.decode("utf-8").strip()
    require(cli_version.startswith("codex-cli "), "Identité CLI inconnue")
    destination.mkdir(parents=True)
    for name in (*required, *extras):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((legacy / name).read_bytes())
    # Le successeur garde les cas, oracles, sources, permissions et limites R4.
    protocol.update(schema_version="dev7-native-complete-protocol-v5",
                    protocol_id="dev7-native-complete-20261012-r5",
                    status="successor_not_measured", cli=str(cli), cli_version=cli_version,
                    cli_sha256=cli_digest)
    own_name = Path(__file__).name
    (destination / own_name).write_bytes(Path(__file__).read_bytes())
    protocol["new_tools"] = list(dict.fromkeys([*protocol["new_tools"], own_name]))
    write_new(destination / "protocole-native-dev7-complet-20261012-r5.json", protocol)
    identity = {"legacy_root": str(legacy), "legacy_protocol_sha256": sha(original.read_bytes()),
                "legacy_control_sha256": sha((legacy / "controle-reprise-efficace-dev7-20261009.json").read_bytes()),
                "source_git_root": str(Path(read(legacy / protocol["proposal_path"])["candidate_gel_path"]).parent.parent.parent),
                "state_root": str(Path(protocol["installed_path"]).parents[4]),
                "previous_cli": read(original)["cli"], "previous_cli_version": read(original)["cli_version"],
                "cli": str(cli), "cli_version": cli_version, "cli_sha256": cli_digest,
                "candidate_commit": protocol["candidate_commit"], "model_override": None,
                "runtime_changed": False, "historical_scores_reused": False,
                "model_inference": False, "release_ready": False}
    write_new(destination / "reprise-identite.json", identity)
    frozen = {p.relative_to(destination).as_posix(): sha(p.read_bytes())
              for p in destination.rglob("*") if p.is_file()}
    write_new(destination / "gel-reprise.json", frozen)
    return identity


def charger(folder: Path) -> Any:
    """Valide le gel R5 et charge les modules R4 sans les modifier sur disque."""
    folder = folder.resolve()
    for name, expected in read(folder / "gel-reprise.json").items():
        target = (folder / name).resolve()
        require(target.is_relative_to(folder) and sha(target.read_bytes()) == expected, "Gel R5 divergent : " + name)
    require(sha(Path(__file__).read_bytes()) == sha((folder / Path(__file__).name).read_bytes()),
            "Le lanceur exécuté diffère du lanceur figé")
    identity = read(folder / "reprise-identite.json")
    legacy = Path(identity["legacy_root"])
    require(sha((legacy / "protocole-native-dev7-complet-20261009-r4.json").read_bytes())
            == identity["legacy_protocol_sha256"], "Protocole historique modifié")
    original = read(legacy / "protocole-native-dev7-complet-20261009-r4.json")
    successor = read(folder / "protocole-native-dev7-complet-20261012-r5.json")
    allowed = {"schema_version", "protocol_id", "status", "cli", "cli_version", "cli_sha256", "new_tools"}
    require({k: v for k, v in successor.items() if k not in allowed}
            == {k: v for k, v in original.items() if k not in allowed}, "Contrat de campagne modifié")
    require(all(successor[key] == identity[key] for key in ("cli", "cli_version", "cli_sha256")),
            "Identité CLI différente de la reprise")
    sys.path.insert(0, str(folder))
    harness = importlib.import_module("campagne_native_complete_dev7_20261009_r4")
    historical = importlib.import_module("socle_campagne_native_dev7_20261008")
    historical.SOURCE = Path(identity["source_git_root"])
    harness.ROOT = folder
    harness.STATE = Path(identity["state_root"])
    harness.PROTOCOL = folder / "protocole-native-dev7-complet-20261012-r5.json"
    harness.DEFAULT_RUN = folder / "campagne"
    original_preflight = harness.preflight
    original_execute = harness.execute_case

    class ClientCompatible(harness.Client):
        """Même RPC et sandbox ; calcul SHA-256 sans autoload de module PowerShell."""
        def request(self, method: str, params: dict[str, Any], timeout: float = 30) -> dict[str, Any]:
            deadline = getattr(harness, "campaign_deadline", None)
            if deadline is not None:
                remaining = deadline - time.monotonic() - 20
                require(remaining > 0, "Budget global atteint avant RPC")
                timeout = min(timeout, remaining)
            if method == "command/exec":
                params = commande_hash_compatible(params, Path(successor["installed_path"]) / "skills/dsi-fpt/SKILL.md")
            return super().request(method, params, timeout)

    def preflight(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return original_preflight(*args, **kwargs, client_factory=ClientCompatible)

    def execute_case(run: Path, identifier: str) -> dict[str, Any]:
        return original_execute(run, identifier, gate=preflight)

    harness.preflight = preflight
    harness.execute_case = execute_case
    return harness


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
    parser.add_argument("action", choices=("init", "check", "preflight", "prepare", "run-all", "export"))
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--legacy", type=Path)
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--case")
    args = parser.parse_args()
    if args.action == "init":
        require(args.legacy is not None and args.cli is not None, "Racine historique et CLI explicites requis")
        result = initialiser(args.legacy, args.folder, args.cli)
    else:
        harness = charger(args.folder)
        protocol, installed = harness.inputs()
        if args.action == "check":
            result = {"inputs_verified": True, "candidate_commit": protocol["candidate_commit"],
                      "case_count": len(protocol["cases"]), "installed_files": len(installed["installed_files"]),
                      "cli_version": protocol["cli_version"], "model_inference": False, "release_ready": False}
        elif args.action == "preflight":
            receipts = harness.preparation_preflights(protocol, installed, harness.preflight)
            result = {"profiles_passed": len(harness.profile_groups(protocol)), "cases_covered": len(receipts),
                      "model_inference": False, "release_ready": False}
        elif args.action == "prepare":
            result = harness.prepare(harness.DEFAULT_RUN, gate=harness.preflight)
        elif args.action == "export":
            require(args.case is not None, "Cas requis")
            result = harness.export_case(harness.DEFAULT_RUN, args.case)
        else:
            result = executer(harness)
    print(json.dumps(result, ensure_ascii=False))
    if result.get("stopped_on_technical_failure"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
