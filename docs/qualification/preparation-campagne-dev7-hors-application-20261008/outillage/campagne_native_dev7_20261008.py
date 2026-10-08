"""Préparation/install officielle puis exécution bornée, à invoquer séparément.

Le coordinateur reste seul autorisé à invoquer prepare/run après lecture réussie.
L'import et les fixtures n'exécutent ni CLI, ni setup, ni installation.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import re
import subprocess
import time
from typing import Any

import socle_campagne_native_dev7_20261008 as s

DEFAULT_RUN = s.ROOT / "qualification-coactivation-dev7-cli-r3"


@contextmanager
def sequential_run(run: Path):
    """Verrou OS Windows libéré à la sortie, même après interruption du processus."""
    import msvcrt
    with (run / "execution.lock").open("a+b") as stream:
        stream.seek(0)
        if not stream.read(1):
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise s.GateError("Autre répondant déjà actif dans ce run") from error
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def cli_call(cli: Path, run: Path, stem: str, args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[bytes]:
    env, _ = s.environment()
    result = subprocess.run([str(cli), "--no-daemon", "--cd", str(run / "workspace"), *s.overrides(), *args],
                            env=env, capture_output=True, timeout=timeout)
    (run / (stem + ".stdout.local")).write_bytes(result.stdout)
    (run / (stem + ".stderr.local")).write_bytes(result.stderr)
    s.require(result.returncode == 0, "Commande officielle échouée : " + stem + " ; sortie privée conservée")
    return result


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [t for child in value for t in strings(child)]
    if isinstance(value, dict):
        return [t for child in value.values() for t in strings(child)]
    return []


def catalogue_evidence(raw: bytes, cache: Path, files: dict[str, str]) -> dict[str, Any]:
    text = "\n".join(strings(json.loads(raw)))
    # Le catalogue natif peut publier des racines rN et des chemins abrégés.
    # Une mention libre du cache ou d'un skill ne prouve pas sa découverte.
    roots: dict[str, Path] = {}
    for alias, folder in re.findall(r"(?m)^- `(?P<alias>r\d+)` = `(?P<folder>[^`\r\n]+)`\s*$", text):
        resolved = Path(folder).resolve()
        s.require(alias not in roots or roots[alias] == resolved, "Racine native ambiguë : " + alias)
        roots[alias] = resolved
    resolved_paths: set[str] = set()
    for reference in re.findall(r"\(file: ([^\r\n)]+)\)", text):
        reference = reference.replace("\\", "/")
        alias_path = re.fullmatch(r"(r\d+)/(.*)", reference)
        if alias_path:
            alias, relative = alias_path.groups()
            s.require(alias in roots, "Racine native absente : " + alias)
            s.require(relative and not any(part in ("", ".", "..") for part in relative.split("/")),
                      "Chemin de skill abrégé non conforme")
            resolved = (roots[alias] / relative).resolve()
            s.require(resolved.is_relative_to(roots[alias]), "Chemin de skill hors racine native")
        else:
            s.require(Path(reference).is_absolute(), "Chemin natif ni absolu ni alias connu")
            resolved = Path(reference).resolve()
        resolved_paths.add(resolved.as_posix().casefold())
    expected = sorted(name for name in files if name.startswith("skills/") and name.endswith("/SKILL.md"))
    s.require(len(expected) == 6, "Catalogue source différent des six skills attendus")
    for name in expected:
        s.require((cache / name).resolve().as_posix().casefold() in resolved_paths,
                  "Skill dev.7 absent du catalogue natif : " + name)
    obsolete_root = s.DEV6.resolve().as_posix().casefold() + "/"
    s.require(not any(path.startswith(obsolete_root) and path.endswith("/skill.md") for path in resolved_paths),
              "Skill dev.6 encore présent dans le catalogue natif")
    return {"native_catalogue_sha256": s.sha(raw), "six_candidate_paths_observed": expected,
            "candidate_aliases_resolved": sorted(alias for alias, folder in roots.items()
                if folder == (cache / "skills").resolve()), "dev6_skill_references_absent": True,
            "global_discovery_completely_isolated": False, "foreign_discovery_possible": True,
            "actual_global_mcp_exposure": "unknown", "native_skill_activation_proven": False,
            "raw_context_local_only": True}


def prepare(cli: Path, receipt_dir: Path, run: Path) -> dict[str, Any]:
    """Action future explicite : vérifie gate puis copie Git/install local officielle.

    Aucune écriture n'a lieu avant les contrôles de lecture et source. Un échec
    conserve le dossier partiel et interdit son remplacement automatique.
    """
    run = s.root_path(run)
    s.require(not run.exists(), "Run déjà présent ; aucun remplacement/reprise automatique")
    s.require(cli.is_file() and s.sha(cli.read_bytes()) == s.CLI_SHA, "CLI différente de l'exécutable autorisé")
    before_dev6 = s.inventory(s.DEV6)
    s.require(len(before_dev6) == 214, "Cache dev.6 incomplet")
    receipts = s.validate_receipts(receipt_dir, before_dev6["skills/dsi-fpt/SKILL.md"])
    s.validate_config()
    proposal = s.read(s.PROPOSAL)
    blobs, frozen = s.source_blobs(proposal)
    cases = s.validate_cases(proposal)
    tools = {name: s.sha((s.ROOT / name).read_bytes()) for name in s.MODULES}
    env, identities = s.environment()
    version = subprocess.check_output([str(cli), "--version"], env=env, timeout=20).decode("utf-8").strip()
    s.require(version == "codex-cli 0.162.0-alpha.2", "Version CLI inattendue")
    auth = subprocess.run([str(cli), "login", "status"], env=env, capture_output=True, timeout=30)
    s.require(auth.returncode == 0, "Connexion isolée non confirmée ; aucun secret lu")
    run.mkdir()
    (run / "workspace").mkdir()
    (run / "workspace/README.md").write_bytes(b"# Scenarios fictifs de qualification\nAucune infrastructure reelle.\n")
    (run / "protocole.json").write_bytes(s.PROPOSAL.read_bytes())
    (run / "rubric-original.md").write_bytes(Path(proposal["rubric_path"]).read_bytes())
    (run / "suite-originale.json").write_bytes(Path(proposal["suite_path"]).read_bytes())
    (run / "outils-figes").mkdir()
    for name in tools:
        (run / "outils-figes" / name).write_bytes((s.ROOT / name).read_bytes())
    (run / "judge-inputs").mkdir()
    (run / "marketplace/.agents/plugins").mkdir(parents=True)
    copy = run / "marketplace/plugin-dev7"
    for name, raw in blobs.items():
        path = copy / name
        s.require(path.resolve().is_relative_to(copy.resolve()), "Chemin source hors copie")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    s.write_new(run / "marketplace/.agents/plugins/marketplace.json", {"name": s.MARKET, "plugins": [{
        "name": "collectivite-territoriale", "source": {"source": "local", "path": "./plugin-dev7"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"}, "category": "Productivity"}]})
    s.write_new(run / "preparation-start.json", {"created_at": s.now(), "source_commit": s.COMMIT,
                "source_tree": s.TREE, "receipt_directory": str(receipt_dir.resolve()), "receipt_sha256": receipts,
                "source_files": {name: s.sha(raw) for name, raw in blobs.items()}, "tools_sha256": tools,
                "dev6_files_before": before_dev6, "model_inference": False, "auth_secrets_read": False})
    # Officiel uniquement ; aucune suppression, copie auth ou écriture config manuelle.
    cli_call(cli, run, "marketplace-add", ["plugin", "marketplace", "add", str(run / "marketplace"), "--json"])
    installation = json.loads(cli_call(cli, run, "plugin-add", ["plugin", "add", s.PLUGIN_ID, "--json"]).stdout)
    cache = Path(installation["installedPath"]).resolve()
    s.require(cache.is_relative_to((s.STATE / "plugins/cache" ).resolve()) and cache != s.DEV6.resolve()
              and s.MARKET in cache.parts, "Installation hors cache distinct dev.7")
    files = s.inventory(cache)
    s.require(files == {name: s.sha(raw) for name, raw in blobs.items()}, "Octets installés différents du Git gelé")
    s.require(s.inventory(s.DEV6) == before_dev6, "Cache dev.6 modifié")
    config_sha = s.validate_config()
    native = cli_call(cli, run, "catalogue-natif", ["debug", "prompt-input"])
    catalogue = catalogue_evidence(native.stdout, cache, files)
    s.require(s.inventory(s.DEV6) == before_dev6 and s.inventory(cache) == files,
              "Cache modifié durant la découverte")
    s.require(s.validate_config() == config_sha, "Config modifiée durant la découverte")
    entries = []
    for case in cases:
        identifier = case["case_id"]
        folder = run / identifier
        folder.mkdir()
        prompt = case["native_prompt"].encode("utf-8")
        (folder / "prompt.txt").write_bytes(prompt)
        # Le paquet juge reste en dehors de workspace, donc hors prompt répondant.
        s.write_new(run / "judge-inputs" / (identifier + ".json"), case)
        allowed = identifier in s.ALLOWED
        entries.append({"id": identifier, "prompt_sha256": s.sha(prompt), "execution_allowed": allowed,
                        "preflight_status": "eligible_no_sources" if allowed else "blocked_primary_mcp_web_unavailable",
                        "judge_input_sha256": s.sha((run / "judge-inputs" / (identifier + ".json")).read_bytes())})
    manifest = {"created_at": s.now(), "status": "prepared_not_measured", "host": "Codex CLI",
        "runtime_source_commit": s.COMMIT, "runtime_source_tree": s.TREE, "plugin_version": "1.2.0-dev.7",
        "installed_path": str(cache), "installed_files": files, "installed_file_count": len(files),
        "frozen_file_count": len(frozen["files"]), "runtime_file_count": 166,
        "dev6_files_preserved": before_dev6, "config_sha256": config_sha, "cli": str(cli.resolve()),
        "cli_sha256": s.CLI_SHA, "cli_version": version, "protocol_sha256": s.sha(s.PROPOSAL.read_bytes()),
        "proposal_source_path": str(s.PROPOSAL), "gel_sha256": proposal["candidate_gel_sha256"],
        "suite_sha256": proposal["suite_sha256"], "rubric_sha256": proposal["rubric_sha256"],
        "harness_sha256": tools[Path(__file__).name], "tools_sha256": tools,
        "extractor_sha256": tools["extraire_campagne_native_dev7_20261008.py"],
        "extractor_tests_sha256": tools["tests_extraire_campagne_native_dev7_20261008.py"],
        "receipt_directory": str(receipt_dir.resolve()), "receipt_sha256": receipts,
        "effective_cli_overrides": s.overrides(), "environment_identity_names_removed": identities,
        "auth_status_exit_code": 0, "auth_status": "credentials_present_local",
        "upstream_authentication_verified": False, "model_override": None, "attempts_per_case": 1,
        "timeout_seconds": 240, "sandbox": "read-only", "approval_policy": "never", "windows_backend": "elevated",
        "mcp_configured_disabled": True, "web_configured_disabled": True, "catalogue": catalogue,
        "case_count": 16, "atomic_count": 124, "execution_allowed_count": 3, "preflight_blocked_count": 13,
        "cases": entries, "historical_scores_reused": False, "release_ready": False,
        "raw_rollout_and_stderr_local_only": True}
    s.write_new(run / "manifest.json", manifest)
    return {"prepared": True, "model_inference": False, "manifest_sha256": s.sha((run / "manifest.json").read_bytes()),
            "cases": 16, "allowed": 3, "blocked": 13}


def verify(run: Path, manifest: dict[str, Any]) -> None:
    s.require(manifest["runtime_source_commit"] == s.COMMIT and manifest["plugin_version"] == "1.2.0-dev.7",
              "Candidat différent")
    s.require(s.sha((run / "protocole.json").read_bytes()) == manifest["protocol_sha256"]
              == s.sha(s.PROPOSAL.read_bytes()), "Protocole modifié")
    for name, digest in manifest["tools_sha256"].items():
        s.require(s.sha((s.ROOT / name).read_bytes()) == digest
                  == s.sha((run / "outils-figes" / name).read_bytes()), "Outil modifié : " + name)
    s.require(s.sha(Path(manifest["cli"]).read_bytes()) == manifest["cli_sha256"] == s.CLI_SHA, "CLI modifiée")
    s.require(s.inventory(Path(manifest["installed_path"])) == manifest["installed_files"], "Cache dev.7 modifié")
    s.require(s.inventory(s.DEV6) == manifest["dev6_files_preserved"], "Cache dev.6 modifié")
    s.require(s.validate_config() == manifest["config_sha256"], "Configuration modifiée")
    actual_receipts = s.validate_receipts(Path(manifest["receipt_directory"]),
                                        manifest["dev6_files_preserved"]["skills/dsi-fpt/SKILL.md"])
    s.require(actual_receipts == manifest["receipt_sha256"], "Reçus sandbox modifiés")
    s.source_blobs(s.read(run / "protocole.json"))
    s.require(manifest["effective_cli_overrides"] == s.overrides() and manifest["model_override"] is None,
              "Permissions ou modèle modifiés")


def native_rollout(thread_id: str | None, folder: Path) -> tuple[str | None, str | None, str | None]:
    if not thread_id:
        return None, None, "thread_id_absent"
    paths = list((s.STATE / "sessions").rglob("*" + thread_id + ".jsonl"))
    if len(paths) != 1:
        return None, None, "native_rollout_missing_or_ambiguous"
    raw = paths[0].read_bytes()
    first = json.loads(raw.splitlines()[0])
    if first.get("type") != "session_meta" or first.get("payload", {}).get("id") != thread_id:
        return None, None, "native_rollout_identity_mismatch"
    destination = folder / "native-rollout.local.jsonl"
    with destination.open("xb") as stream:
        stream.write(raw)
    return str(destination), s.sha(raw), None


def execute(run: Path, identifier: str) -> dict[str, Any]:
    run = s.root_path(run)
    s.require(identifier in s.ALLOWED, "Treize cas nominaux restent bloqués : sources indisponibles")
    with sequential_run(run):
        return execute_locked(run, identifier)


def execute_locked(run: Path, identifier: str) -> dict[str, Any]:
    manifest = s.read(run / "manifest.json")
    verify(run, manifest)
    case = next(c for c in manifest["cases"] if c["id"] == identifier)
    s.require(case["execution_allowed"] is True, "Précontrôle du cas bloqué")
    folder = run / identifier
    s.require(not (folder / "start.json").exists(), "Tentative déjà scellée ; aucune reprise/remplacement")
    prompt = (folder / "prompt.txt").read_bytes()
    s.require(s.sha(prompt) == case["prompt_sha256"], "Prompt modifié")
    s.require(s.sha((run / "judge-inputs" / (identifier + ".json")).read_bytes()) == case["judge_input_sha256"],
              "Entrée juge modifiée")
    env, identities = s.environment()
    argv = [manifest["cli"], "--no-daemon", "--cd", str(run / "workspace"), *s.overrides(),
            "--sandbox", "read-only", "--ask-for-approval", "never", "exec", "--skip-git-repo-check",
            "--json", "--color", "never", "--output-last-message", str(folder / "response.md"), "-"]
    s.write_new(folder / "start.json", {"started_at": s.now(), "argv": argv, "attempt": 1,
                "prompt_sha256": s.sha(prompt), "manifest_sha256": s.sha((run / "manifest.json").read_bytes()),
                "environment_identity_names_removed": identities, "model_override": None})
    start = time.monotonic()
    timed_out = False
    launch_error = None
    exit_code = None
    with (folder / "stdout.jsonl").open("xb") as out, (folder / "stderr.txt").open("xb") as err:
        try:
            process = subprocess.Popen(argv, cwd=run / "workspace", env=env, stdin=subprocess.PIPE, stdout=out, stderr=err)
            try:
                process.communicate(input=prompt, timeout=240)
            except subprocess.TimeoutExpired:
                timed_out = True
                process.kill()
                process.communicate(timeout=10)
            exit_code = process.returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            launch_error = type(error).__name__
    unchanged = True
    try:
        verify(run, manifest)
    except (s.GateError, OSError, ValueError):
        unchanged = False
    events = []
    invalid = 0
    for line in (folder / "stdout.jsonl").read_bytes().splitlines():
        try:
            events.append(json.loads(line))
        except (ValueError, UnicodeError):
            invalid += 1
    identities = [e.get("thread_id") for e in events if e.get("type") == "thread.started"]
    thread_id = identities[0] if len(identities) == 1 else None
    try:
        native_path, native_hash, native_error = native_rollout(thread_id, folder)
    except (ValueError, OSError, IndexError):
        native_path, native_hash, native_error = None, None, "native_capture_failed"
    record = {"completed_at": s.now(), "exit_code": exit_code, "timed_out": timed_out, "launch_error": launch_error,
        "elapsed_seconds": round(time.monotonic() - start, 3), "attempt": 1, "event_count": len(events),
        "invalid_jsonl_lines": invalid, "thread_id": thread_id, "candidate_cache_config_unchanged": unchanged,
        "stdout_sha256": s.sha((folder / "stdout.jsonl").read_bytes()),
        "stderr_sha256": s.sha((folder / "stderr.txt").read_bytes()),
        "response_sha256": s.sha((folder / "response.md").read_bytes()) if (folder / "response.md").exists() else None,
        "native_rollout_path": native_path, "native_rollout_sha256": native_hash, "native_capture_error": native_error,
        "usage": [e.get("usage") for e in events if e.get("type") == "turn.completed"],
        "upstream_authentication_verified": exit_code == 0 and any(e.get("type") == "turn.completed" for e in events),
        "strict_activation_verified": None, "release_ready": False}
    s.write_new(folder / "execution.json", record)
    return {"case_id": identifier, **record}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run"])
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--sandbox-receipt-dir", type=Path)
    parser.add_argument("--case")
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            s.require(args.cli is not None and args.sandbox_receipt_dir is not None, "CLI et reçus sandbox requis")
            result = prepare(args.cli, args.sandbox_receipt_dir, args.run)
        else:
            s.require(args.case is not None, "Identifiant du cas requis")
            result = execute(args.run, args.case)
        print(json.dumps(result, ensure_ascii=False))
    except (s.GateError, OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as error:
        print(json.dumps({"blocked": True, "error_type": type(error).__name__,
                          "reason": str(error)[:600], "automatic_retry": False}, ensure_ascii=False))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
