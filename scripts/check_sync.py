"""Vérifie que chaque skill embarqué est identique à son commit amont figé."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path, PurePosixPath

from sync_skills import ROOT, snapshots


def check(root: Path, expected: dict[str, dict[str, bytes]]) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if skills_root.is_symlink():
        return ["Le dossier skills ne peut pas être un lien symbolique"]
    entries = list(skills_root.iterdir()) if skills_root.exists() else []
    actual_dirs = {path.name for path in entries if path.is_dir()}
    for path in entries:
        if not path.is_dir():
            errors.append(f"Fichier inattendu dans skills : {path.name}")
    for name in sorted(actual_dirs - expected.keys()):
        errors.append(f"Skill supplémentaire : {name}")
    for name, files in expected.items():
        target = skills_root / name
        if not target.is_dir() or target.is_symlink():
            errors.append(f"Skill absent ou invalide : {name}")
            continue
        actual = {
            path.relative_to(target).as_posix(): path
            for path in target.rglob("*") if path.is_file()
        }
        for relative in sorted(actual.keys() - files.keys()):
            errors.append(f"Fichier supplémentaire : {name}/{relative}")
        for relative, content in files.items():
            path = target.joinpath(*PurePosixPath(relative).parts)
            if relative not in actual:
                errors.append(f"Fichier manquant : {name}/{relative}")
            elif path.is_symlink() or path.read_bytes() != content:
                errors.append(f"Fichier divergent : {name}/{relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-repos", type=Path,
        help="Dossier contenant les quatre dépôts locaux, pour travailler hors réseau",
    )
    args = parser.parse_args()
    expected = snapshots(ROOT, args.local_repos)
    errors = check(ROOT, expected)
    for error in errors:
        print(f"[ERREUR] {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"[OK] {len(expected)} skills conformes à upstream.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
