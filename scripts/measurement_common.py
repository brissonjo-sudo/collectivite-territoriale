"""Identité du candidat et pièces liées, sans qualification ou avis humain."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any
import uuid

CONFIGURATION = (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".mcp.json", "assets/icon.png")


def digest(data: bytes) -> str:
    """SHA-256 sur les octets exacts."""
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    """Sérialisation réservée aux liens internes des nouvelles pièces."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def fingerprint(path: Path) -> str:
    """Empreinte sans conversion des lignes."""
    return digest(path.read_bytes())


def snapshot(root: Path) -> dict[str, Any]:
    """Inventorie octets distribués, contrat et outillage courant."""
    runtime = {}
    for path in sorted((root / "skills").rglob("*")):
        if path.is_symlink():
            raise ValueError("Lien symbolique dans le runtime")
        if path.is_file():
            runtime[path.relative_to(root).as_posix()] = fingerprint(path)
    return {"runtime_sha256": runtime,
            "plugin_configuration_sha256": {n: fingerprint(root / n) for n in CONFIGURATION},
            "case_file_sha256": fingerprint(root / "tests/cas-plugin.json"),
            "upstream_sha256": fingerprint(root / "upstream.json"),
            "toolchain_sha256": {p.relative_to(root).as_posix(): fingerprint(p)
                                   for p in sorted((root / "scripts").glob("*.py"))}}


def candidate(root: Path, commit: str) -> dict[str, Any]:
    """Refuse SHA abrégé, HEAD différent ou arbre modifié, avant tout modèle."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("plugin_commit exact attendu sur quarante caractères")
    def git(*args: str) -> str:
        return subprocess.check_output(["git", "-c", "safe.directory=" + str(root), *args], cwd=root).decode().strip()
    if git("rev-parse", "HEAD") != commit:
        raise ValueError("plugin_commit différent de HEAD")
    if git("status", "--porcelain=v1", "--untracked-files=all"):
        raise ValueError("Arbre candidat modifié")
    return {"plugin_commit": commit, **snapshot(root)}


def output_outside(root: Path, destination: Path) -> Path:
    """Refuse liens, sorties dans le candidat et écrasements."""
    for ancestor in (destination, *destination.parents):
        if ancestor.exists() and ancestor.is_symlink():
            raise ValueError("Sortie redirigée")
    destination = destination.resolve()
    if destination.is_relative_to(root.resolve()):
        raise ValueError("Sortie dans le candidat interdite")
    if destination.exists():
        raise ValueError("Destination déjà existante")
    return destination


def write_new(path: Path, value: Any) -> None:
    """Écriture exclusive : une tentative ne remplace jamais une autre."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def seal(value: dict[str, Any]) -> dict[str, Any]:
    """Lie tous les champs d'une nouvelle pièce, provenance comprise."""
    if "payload_sha256" in value:
        raise ValueError("Pièce déjà scellée")
    return {**value, "payload_sha256": digest(canonical(value))}


def checked(path: Path, commit: str, kinds: set[str]) -> dict[str, Any]:
    """Refuse pièce synthétique déclarée, provenance absente ou octets altérés.

    Les empreintes établissent l'intégrité, pas une attestation indépendante
    contre un opérateur qui fabriquerait toute la chaîne et ses reçus.
    """
    if path.is_symlink():
        raise ValueError("Lien de preuve refusé")
    value = json.loads(path.read_bytes())
    body = {k: v for k, v in value.items() if k != "payload_sha256"}
    if value.get("payload_sha256") != digest(canonical(body)):
        raise ValueError("Empreinte de pièce divergente : " + path.name)
    if value.get("plugin_commit") != commit:
        raise ValueError("Commit de pièce divergent : " + path.name)
    origin = value.get("origin") or {}
    if origin.get("kind") not in kinds or origin.get("synthetic") is not False or origin.get("dry_run") is not False:
        raise ValueError("Pièce synthétique, dry-run ou provenance absente : " + path.name)
    return value


def binding(path: Path, root: Path) -> dict[str, str]:
    """Lien relatif et empreinte d'une pièce sous un dossier contrôlé."""
    resolved = path.resolve()
    if path.is_symlink() or not resolved.is_relative_to(root.resolve()):
        raise ValueError("Pièce hors du dossier de mesure")
    return {"evidence_path": resolved.relative_to(root.resolve()).as_posix(), "sha256": fingerprint(resolved)}


def bound(root: Path, link: dict[str, str]) -> Path:
    """Relit un lien sans traversée ni changement d'empreinte."""
    path = root / link["evidence_path"]
    for ancestor in (path, *path.parents):
        if ancestor == root.parent:
            break
        if ancestor.is_symlink():
            raise ValueError("Lien symbolique de preuve")
    if not path.resolve().is_relative_to(root.resolve()) or fingerprint(path) != link["sha256"]:
        raise ValueError("Preuve liée altérée ou hors dossier")
    return path


def parse_jsonl(raw: str) -> list[dict[str, Any]]:
    """N'accepte pas de lignes non JSON ignorées silencieusement."""
    result = []
    for line in raw.splitlines():
        if line.strip():
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError("Événement JSONL non objet")
            result.append(item)
    return result


def run_cli(argv: list[str], prompt: str, cwd: Path, timeout: int,
            environment: dict[str, str] | None = None) -> tuple[list[dict], int, dict]:
    """Seul point d'appel réel ; flux bruts et stderr restent en mémoire."""
    if timeout <= 0:
        raise ValueError("Timeout positif requis")
    executable = Path(argv[0]).resolve(strict=True)
    started = time.monotonic()
    try:
        result = subprocess.run(argv, input=prompt, cwd=cwd, env=environment, capture_output=True,
                                text=True, encoding="utf-8", errors="strict", timeout=timeout, check=False)
        raw, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or ""; stderr = exc.stderr or ""; code = 124
        raw = raw.decode("utf-8", "strict") if isinstance(raw, bytes) else raw
        stderr = stderr.decode("utf-8", "strict") if isinstance(stderr, bytes) else stderr
    events = parse_jsonl(raw)
    thread = next((e.get("thread_id") for e in events if e.get("type") == "thread.started"), None)
    try:
        uuid.UUID(thread)
        real = True
    except (ValueError, TypeError, AttributeError):
        real = False
    receipt = {"kind": "real_cli" if real else "incomplete_cli", "synthetic": False, "dry_run": False,
               "thread_id": thread, "cli_sha256": fingerprint(executable), "argv_sha256": digest(canonical(argv)),
               "prompt_sha256": digest(prompt.encode()), "stdout_sha256": digest(raw.encode()),
               "stderr_sha256": digest(stderr.encode()), "process_exit": code,
               "elapsed_seconds": round(time.monotonic() - started, 6)}
    return events, code, receipt
