"""Recalcule les empreintes chaînées des surcouches d'un skill dans upstream.json.

L'amont est lu exactement comme sync_skills.py (mêmes fonctions). Chaque
surcouche reçoit l'empreinte de sa source et celle de la sortie de la
précédente ; l'application garde tous les autres contrôles (ancre, section,
chemins). Sans --write, affiche seulement les changements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path, PurePosixPath

from instruction_overlays import apply_overlays
from sync_skills import ROOT, archive_files, load_upstreams, upstream_repository


def rehash(root: Path, files: dict[str, bytes], overlays: list[dict]) -> list[dict]:
    """Renvoie la chaîne recalculée, en appliquant chaque surcouche une à une."""
    current = dict(files)
    chained: list[dict] = []
    for overlay in overlays:
        if overlay["target"] not in current:
            raise ValueError(f"Surcharge : cible absente du runtime ({overlay['source']})")
        source = root.joinpath(*PurePosixPath(overlay["source"]).parts)
        updated = {
            **overlay,
            "base_sha256": hashlib.sha256(current[overlay["target"]]).hexdigest(),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
        current = apply_overlays(root, current, [updated])
        chained.append(updated)
    return chained


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="Nom du skill déclaré dans upstream.json")
    parser.add_argument("--local-repos", type=Path,
                        help="Dossier des dépôts amont locaux, comme pour sync_skills.py")
    parser.add_argument("--write", action="store_true", help="Écrire upstream.json")
    args = parser.parse_args()
    upstreams = load_upstreams(ROOT)
    if args.skill not in upstreams:
        raise SystemExit(f"Skill inconnu : {args.skill}")
    spec = upstreams[args.skill]
    with tempfile.TemporaryDirectory(prefix="collectivite-rehash-") as temp:
        repository = upstream_repository(args.skill, spec, args.local_repos, Path(temp))
        files = archive_files(repository, spec)
    chained = rehash(ROOT, files, spec.get("instruction_overlays", []))
    for old, new in zip(spec.get("instruction_overlays", []), chained):
        for key in ("base_sha256", "source_sha256"):
            if old[key] != new[key]:
                print(f"{args.skill} {new['source']} {key} : {old[key]} -> {new[key]}")
    if args.write:
        path = ROOT / "upstream.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["skills"][args.skill]["instruction_overlays"] = chained
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
