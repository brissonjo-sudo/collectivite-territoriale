"""Recopie les fichiers d'exécution des skills depuis des commits Git figés.

La liste des dépôts, commits, versions et chemins vient exclusivement de
upstream.json. Aucune modification du contenu des skills n'est effectuée.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_ID = re.compile(r"^[0-9a-f]{40}$")
VERSION_TITLE = re.compile(r"(?m)^# Skill\s*:\s*[^\n]*\(v(\d+\.\d+\.\d+)\)")


def run_git(
    *args: str, cwd: Path | None = None, input_data: bytes | None = None
) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=cwd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, input=input_data, check=False,
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
    tree = run_git(
        "ls-tree", "-r", "-z", spec["commit"], "--", *spec["paths"],
        cwd=repository,
    )
    excluded = set(spec.get("exclude", []))
    entries: list[tuple[str, str]] = []
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_name = record.split(b"\t", 1)
        mode, kind, raw_oid = metadata.decode("ascii").split()
        name = safe_relative(raw_name.decode("utf-8"))
        if name in excluded:
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError(f"Type de fichier non pris en charge : {name}")
        entries.append((name, raw_oid))
    # git archive transforme certains CRLF selon la configuration du poste.
    # Lire les blobs bruts garantit une copie identique sur Windows et Linux.
    request = b"".join(oid.encode("ascii") + b"\n" for _, oid in entries)
    response = run_git("cat-file", "--batch", cwd=repository, input_data=request)
    files: dict[str, bytes] = {}
    offset = 0
    for name, oid in entries:
        end_header = response.index(b"\n", offset)
        raw_id, kind, raw_size = response[offset:end_header].split()
        if raw_id.decode("ascii") != oid or kind != b"blob":
            raise ValueError(f"Objet Git inattendu : {name}")
        size = int(raw_size)
        start = end_header + 1
        files[name] = response[start:start + size]
        offset = start + size + 1
    if offset != len(response):
        raise ValueError("Réponse Git incomplète ou surnuméraire")
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
                "clone", "--quiet", "--no-checkout",
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
