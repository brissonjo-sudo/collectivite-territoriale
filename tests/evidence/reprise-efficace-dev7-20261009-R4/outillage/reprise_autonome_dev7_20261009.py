"""Reprise ponctuelle hors application, sans relance ni modification de configuration.

L'import ne démarre rien. --armer attend la fermeture gracieuse de Codex puis
exécute une seule campagne. ANNULER arrête l'attente et empêche le prochain
répondant ; il n'interrompt pas un répondant déjà commencé (240 s maximum).
Le dossier contient des états publics assainis ; les RPC restent dans les
dossiers privés du harnais. Aucun juge ni publication ne sont créés ici.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib
import json
import os
from pathlib import Path
import time
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
CONTROL = ROOT / "controle-reprise-efficace-dev7-20261009.json"
LOCK = ROOT / ".reprise-autonome-dev7.private.lock"
MAX_LOG_BYTES = 64 * 1024
MAX_CAMPAIGN_SECONDS = 95 * 60
CASE_MARGIN_SECONDS = 300
WAITABLE = "Runtime CUA Node encore actif ; aucune terminaison automatique"
REQUIRED_TOOLS = {
    "reprise_autonome_dev7_20261009.py",
    "tests_reprise_autonome_dev7_20261009.py",
    "campagne_native_complete_dev7_20261009_r4.py",
    "protocole-native-dev7-complet-20261009-r4.json",
    "normaliseur_native_complete_dev7_20261009_r2.py",
}


class WorkerError(ValueError):
    """Arrêt sans réparation automatique ni répétition de tentative."""


class Cancelled(WorkerError):
    """Annulation avant le prochain lancement."""


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def frozen_tools(control: Path = CONTROL, root: Path = ROOT) -> dict[str, str]:
    """Le contrôle contient seulement des noms de fichiers ROOT et leurs SHA."""
    value = json.loads(control.read_bytes())
    tools = value.get("tools_sha256")
    if not isinstance(tools, dict) or not REQUIRED_TOOLS.issubset(tools):
        raise WorkerError("Gel d'outillage incomplet")
    for name, expected in tools.items():
        if not isinstance(name, str) or Path(name).name != name \
                or not isinstance(expected, str) or len(expected) != 64 \
                or digest((root / name).read_bytes()) != expected:
            raise WorkerError("Outillage différent du gel")
    return tools


def state_destination(folder: Path, root: Path = ROOT) -> Path:
    folder = folder.resolve()
    if folder.parent != root.resolve() or not folder.name.startswith("reprise-autonome-dev7-"):
        raise WorkerError("Dossier d'état hors du périmètre autorisé")
    return folder


@contextmanager
def unique_worker(lock: Path = LOCK):
    """Verrou Windows libéré par l'OS même après arrêt brutal du worker."""
    import msvcrt
    with lock.open("a+b") as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise WorkerError("Un worker de reprise est déjà actif") from error
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


MESSAGES = {
    "waiting": "En attente de la fermeture gracieuse de Codex.",
    "preflight": "Contrôle natif des profils de sources, sans modèle.",
    "prepared": "Campagne préparée ; aucun répondant encore lancé.",
    "running": "Exécution séquentielle ; une seule tentative par cas.",
    "blocked": "Arrêt sur blocage ; aucune relance automatique.",
    "packets_ready": "Les seize paquets sont prêts pour les juges indépendants.",
    "expired": "Délai d'attente ou de campagne atteint ; aucune relance.",
}


class Status:
    def __init__(self, folder: Path, now: Callable[[], str]):
        self.folder = folder
        self.now = now

    def update(self, state: str, **fields: Any) -> dict[str, Any]:
        value = {"updated_at": self.now(), "state": state, "message": MESSAGES[state],
                 "automatic_retry": False, "judges_created": False, "release_ready": False, **fields}
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        temporary = self.folder / "etat.tmp"
        temporary.write_bytes(raw)
        os.replace(temporary, self.folder / "etat.json")
        self.log(MESSAGES[state])
        return value

    def log(self, text: str) -> None:
        path = self.folder / "journal.txt"
        size = path.stat().st_size if path.exists() else 0
        raw = (self.now() + " " + text + "\n").encode("utf-8")
        if size + len(raw) <= MAX_LOG_BYTES:
            with path.open("ab") as stream:
                stream.write(raw)


def sanitized_error(error: BaseException) -> dict[str, str]:
    """Aucun texte d'exception/RPC, URL ou identifiant transmis au journal public."""
    known = {"WorkerError", "Cancelled", "GateError", "OSError", "ValueError", "TimeoutError"}
    kind = type(error).__name__
    return {"error_type": kind if kind in known else "ErreurTechnique",
            "error_sha256": digest(str(error).encode("utf-8", errors="replace"))}


def snapshot(c: Any, control: Path, root: Path) -> dict[str, Any]:
    tools = frozen_tools(control, root)
    protocol, installed = c.inputs()
    return {"tools_sha256": tools,
            "control_sha256": digest(control.read_bytes()),
            "persistent_config_sha256": digest((c.STATE / "config.toml").read_bytes()),
            "candidate_commit": protocol["candidate_commit"],
            "installed_inventory_sha256": digest(c.canonical(installed["installed_files"]))}


def run_worker(folder: Path, c: Any, *, waiting_seconds: int = 900,
               control: Path = CONTROL, root: Path = ROOT,
               monotonic: Callable[[], float] = time.monotonic,
               sleep: Callable[[float], None] = time.sleep) -> dict[str, Any]:
    """Appelé seulement sous unique_worker ; dépendances injectables pour les tests."""
    if type(waiting_seconds) is not int or not 1 <= waiting_seconds <= 900:
        raise WorkerError("Attente hors limite 1–900 secondes")
    folder = state_destination(folder, root)
    folder.mkdir(exist_ok=False)
    status = Status(folder, c.now)
    before = None
    final: dict[str, Any] = {}
    executed = 0
    prepared = False
    run = c.DEFAULT_RUN
    receipts_before = {p.name for p in root.glob("precontrole-complet-dev7-*") if p.is_dir()}

    def cancelled() -> None:
        if (folder / "ANNULER").exists():
            raise Cancelled("Annulation demandée avant le prochain répondant")

    try:
        before = snapshot(c, control, root)
        if run.exists():
            raise WorkerError("Campagne déjà préparée ; aucun remplacement ni reprise")
        env, _ = c.environment()
        wait_deadline = monotonic() + waiting_seconds
        status.update("waiting", executed_cases=0)
        while True:
            cancelled()
            if monotonic() >= wait_deadline:
                final = status.update("expired", executed_cases=0, phase="waiting")
                break
            try:
                c.node_gate(env)
                if monotonic() >= wait_deadline:
                    final = status.update("expired", executed_cases=0, phase="waiting")
                break
            except c.GateError as error:
                if str(error) != WAITABLE:
                    raise
            sleep(min(3, max(0, wait_deadline - monotonic())))
        if not final:
            cancelled()
            if snapshot(c, control, root) != before:
                raise WorkerError("Gel ou candidat modifié pendant l'attente")
            campaign_deadline = monotonic() + MAX_CAMPAIGN_SECONDS

            def deadline_client(*args: Any, **kwargs: Any) -> Any:
                client = c.Client(*args, **kwargs)
                original_request = client.request

                def request(method: str, params: Any, timeout: float = 30) -> Any:
                    # Réserve la fermeture de notre seul enfant ; aucun autre PID touché.
                    available = campaign_deadline - monotonic() - 20
                    if available <= 0:
                        raise WorkerError("Délai global atteint avant RPC")
                    return original_request(method, params, timeout=min(timeout, 45, available))

                client.request = request
                return client

            def preparation_gate(*args: Any, **kwargs: Any) -> Any:
                cancelled()
                if monotonic() + 45 >= campaign_deadline:
                    raise WorkerError("Délai global atteint avant précontrôle")
                receipt = c.preflight(*args, **kwargs, client_factory=deadline_client)
                cancelled()
                return receipt

            status.update("preflight", executed_cases=0)
            c.prepare(run, gate=preparation_gate)
            prepared = True
            if snapshot(c, control, root) != before:
                raise WorkerError("Gel ou candidat modifié pendant la préparation")
            status.update("prepared", executed_cases=0)
            protocol, _, _ = c.verify(run)
            if len(protocol["cases"]) != 16:
                raise WorkerError("La campagne requiert exactement seize cas")
            if any((run / "cases" / item["case_id"] / "start.json").exists()
                   for item in protocol["cases"]):
                raise WorkerError("Une tentative a déjà commencé")
            for case in protocol["cases"]:
                cancelled()
                if monotonic() + CASE_MARGIN_SECONDS >= campaign_deadline:
                    final = status.update("expired", executed_cases=executed, phase="campaign")
                    break

                def checked_gate(*args: Any, **kwargs: Any) -> Any:
                    cancelled()
                    if monotonic() + 45 >= campaign_deadline:
                        raise WorkerError("Délai global atteint avant précontrôle")
                    receipt = c.preflight(*args, **kwargs, client_factory=deadline_client)
                    cancelled()
                    if frozen_tools(control, root) != before["tools_sha256"] \
                            or digest(control.read_bytes()) != before["control_sha256"]:
                        raise WorkerError("Gel d'outillage modifié avant le répondant")
                    if monotonic() + 250 >= campaign_deadline:
                        raise WorkerError("Délai global insuffisant pour un nouveau répondant")
                    return receipt

                status.update("running", executed_cases=executed, current_case=case["case_id"])
                outcome = c.execute_case(run, case["case_id"], gate=checked_gate)
                executed += 1
                issues = False
                if outcome.get("native_rollout_sha256"):
                    exported = c.export_case(run, case["case_id"])
                    issues = bool(exported["technical_issues"])
                if issues or outcome.get("timed_out") or outcome.get("capture_overflow") \
                        or outcome.get("exit_code") != 0 \
                        or outcome.get("candidate_cache_config_unchanged") is not True:
                    final = status.update("blocked", executed_cases=executed, phase="respondent",
                                          failure="execution_failed_or_capture_incomplete")
                    break
            if not final:
                final = status.update("packets_ready", executed_cases=executed)
    except Exception as error:
        final = status.update("blocked", executed_cases=executed,
                              cancellation_requested=isinstance(error, Cancelled) or (folder / "ANNULER").exists(),
                              **sanitized_error(error))
    finally:
        if prepared:
            executed = sum(path.is_file() for path in (run / "cases").glob("*/start.json"))
            final["executed_cases"] = executed
        try:
            after = snapshot(c, control, root)
            final["candidate_cache_config_tools_unchanged"] = before is not None and before == after
            if before is None or before != after:
                final = status.update("blocked", executed_cases=executed,
                                      failure="inputs_changed_or_unverifiable",
                                      candidate_cache_config_tools_unchanged=False)
        except Exception as error:
            final = status.update("blocked", executed_cases=executed,
                                  failure="inputs_changed_or_unverifiable",
                                  candidate_cache_config_tools_unchanged=False, **sanitized_error(error))
        final["preflight_receipts"] = sorted(p.name for p in root.glob("precontrole-complet-dev7-*")
                                             if p.is_dir() and p.name not in receipts_before)
        final["run_directory"] = run.name
        final["preexisting_processes_terminated"] = False
        if prepared:
            c.write_new(run / "execution-bilan.json", {"completed_at": c.now(),
                        "executed_cases": executed,
                        "stopped_on_technical_failure": final["state"] != "packets_ready",
                        "stop_reason": final["state"] if final["state"] != "packets_ready" else None,
                        "judges_created": False, "release_ready": False})
        c.write_new(folder / "final.json", final)
    return final


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--armer", action="store_true")
    mode.add_argument("--check-only", action="store_true")
    parser.add_argument("--dossier", type=Path)
    parser.add_argument("--attente-secondes", type=int, default=900)
    args = parser.parse_args()
    frozen_tools()
    c = importlib.import_module("campagne_native_complete_dev7_20261009_r4")
    if args.check_only:
        snapshot(c, CONTROL, ROOT)
        print("Outillage et candidat vérifiés. Aucun précontrôle natif ni modèle lancé.")
        return
    if args.dossier is None:
        parser.error("--dossier est requis avec --armer")
    with unique_worker():
        result = run_worker(args.dossier, c, waiting_seconds=args.attente_secondes)
    print(json.dumps(result, ensure_ascii=False))
    if result["state"] != "packets_ready":
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except (WorkerError, OSError, ValueError) as error:
        print(json.dumps({"state": "blocked", "automatic_retry": False,
                          "release_ready": False, **sanitized_error(error)}, ensure_ascii=False))
        raise SystemExit(2)
