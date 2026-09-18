"""Recopie les fichiers d'exécution des skills depuis des commits Git figés.

La liste des dépôts, commits, versions et chemins vient exclusivement de
upstream.json. Aucune modification du contenu des skills n'est effectuée.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_ID = re.compile(r"^[0-9a-f]{40}$")
VERSION_TITLE = re.compile(r"(?m)^# Skill\s*:\s*[^\n]*\(v(\d+\.\d+\.\d+)\)")


def run_git(*args: str, cwd: Path | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=cwd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"git {' '.join(args[:3])} a échoué : "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return result.stdout


def safe_relative(value: str, *, directory: bool = False) -> str:
    path = PurePosixPath(value.rstrip("/"))
    if (
        not value or "\\" in value or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
        or str(path) != value.rstrip("/")
    ):
        raise ValueError(f"Chemin amont invalide : {value!r}")
    if directory and not value.endswith("/"):
        raise ValueError(f"Répertoire sans barre finale : {value!r}")
    return str(path)


def load_upstreams(root: Path) -> dict[str, dict]:
    data = json.loads((root / "upstream.json").read_text(encoding="utf-8"))
    if data.get("format_version") != 1 or not isinstance(data.get("skills"), dict):
        raise ValueError("Format upstream.json non pris en charge")
    for name, spec in data["skills"].items():
        if not SKILL_NAME.fullmatch(name):
            raise ValueError(f"Nom de skill invalide : {name!r}")
        if not COMMIT_ID.fullmatch(spec["commit"]):
            raise ValueError(f"Commit non figé sur 40 caractères : {name}")
        if not spec["repository"].startswith("https://github.com/brissonjo-sudo/"):
            raise ValueError(f"Dépôt inattendu : {name}")
        if not spec["paths"] or "SKILL.md" not in spec["paths"]:
            raise ValueError(f"Point d'entrée manquant : {name}")
        for path in spec["paths"]:
            safe_relative(path)
        for path in spec.get("exclude", []):
            safe_relative(path)
    return data["skills"]


def archive_files(repository: Path, spec: dict) -> dict[str, bytes]:
    run_git("cat-file", "-e", f"{spec['commit']}^{{commit}}", cwd=repository)
    archive = run_git(
        "archive", "--format=tar", spec["commit"], "--", *spec["paths"],
        cwd=repository,
    )
    excluded = set(spec.get("exclude", []))
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar:
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f"Type de fichier non pris en charge : {member.name}")
            name = safe_relative(member.name)
            if name in excluded:
                continue
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError(f"Fichier illisible : {name}")
            files[name] = stream.read()
    if "SKILL.md" not in files:
        raise ValueError("SKILL.md absent de l'archive amont")
    title = VERSION_TITLE.search(files["SKILL.md"].decode("utf-8"))
    if not title or title.group(1) != spec["version"]:
        raise ValueError(
            f"Version du SKILL.md incohérente : attendue {spec['version']}"
        )
    return files


def snapshots(root: Path, local_repos: Path | None = None) -> dict[str, dict[str, bytes]]:
    upstreams = load_upstreams(root)
    result: dict[str, dict[str, bytes]] = {}
    if local_repos is not None:
        for name, spec in upstreams.items():
            source = local_repos / name
            if not (source / ".git").exists():
                raise ValueError(f"Dépôt local introuvable : {source}")
            result[name] = archive_files(source, spec)
        return result
    with tempfile.TemporaryDirectory(prefix="collectivite-sync-") as temp:
        for name, spec in upstreams.items():
            source = Path(temp) / name
            run_git(
                "clone", "--quiet", "--no-checkout", "--filter=blob:none",
                spec["repository"], str(source),
            )
            result[name] = archive_files(source, spec)
    return result


def synchronize(root: Path, expected: dict[str, dict[str, bytes]]) -> None:
    skills_root = root / "skills"
    if skills_root.is_symlink():
        raise ValueError("Le dossier skills ne peut pas être un lien symbolique")
    skills_root.mkdir(exist_ok=True)
    for name, files in expected.items():
        target = skills_root / name
        if target.is_symlink():
            raise ValueError(f"Le skill {name} ne peut pas être un lien symbolique")
        if target.exists():
            shutil.rmtree(target)
        for relative, content in files.items():
            path = target.joinpath(*PurePosixPath(relative).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print(f"{name} : {len(files)} fichiers synchronisés")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-repos", type=Path,
        help="Dossier contenant les quatre dépôts locaux, pour travailler hors réseau",
    )
    args = parser.parse_args()
    synchronize(ROOT, snapshots(ROOT, args.local_repos))


if __name__ == "__main__":
    main()
