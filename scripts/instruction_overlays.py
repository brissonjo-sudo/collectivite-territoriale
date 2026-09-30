"""Applique des insertions locales déclarées et liées à des empreintes figées."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath

HASH = re.compile(r"^[0-9a-f]{64}$")


def validate_overlays(overlays: list[dict]) -> None:
    """Refuse les chemins dangereux, empreintes absentes et cibles dupliquées."""
    if not isinstance(overlays, list):
        raise ValueError("Surcharges : liste attendue")
    targets: set[str] = set()
    for overlay in overlays:
        if not isinstance(overlay, dict) or set(overlay) != {
            "target", "source", "base_sha256", "source_sha256", "anchor"
        }:
            raise ValueError("Surcharge : contrat invalide")
        for field in ("target", "source"):
            value = overlay[field]
            if not isinstance(value, str):
                raise ValueError("Surcharge : chemin non textuel")
            path = PurePosixPath(value)
            if (not value or path.is_absolute() or "\\" in value or ":" in value
                    or str(path) != value or ".." in path.parts):
                raise ValueError("Surcharge : chemin dangereux")
        if not overlay["source"].startswith("overlays/"):
            raise ValueError("Surcharge : source hors overlays")
        if overlay["target"] in targets:
            raise ValueError("Surcharge : cible dupliquée")
        targets.add(overlay["target"])
        if any(not isinstance(overlay[key], str) or not HASH.fullmatch(overlay[key])
               for key in ("base_sha256", "source_sha256")):
            raise ValueError("Surcharge : empreinte invalide")
        if not isinstance(overlay["anchor"], str) or not overlay["anchor"]:
            raise ValueError("Surcharge : ancre vide")


def apply_overlays(root: Path, files: dict[str, bytes], overlays: list[dict]) -> dict[str, bytes]:
    """Insère chaque correction une fois ; toute dérive impose une revue explicite."""
    validate_overlays(overlays)
    result = dict(files)
    for overlay in overlays:
        target = overlay["target"]
        if target not in result:
            raise ValueError("Surcharge : cible absente du runtime")
        base = result[target]
        if hashlib.sha256(base).hexdigest() != overlay["base_sha256"]:
            raise ValueError("Surcharge : empreinte amont divergente")
        source = root.joinpath(*PurePosixPath(overlay["source"]).parts)
        if source.is_symlink() or any(parent.is_symlink() for parent in source.parents if parent != root.parent):
            raise ValueError("Surcharge : lien symbolique interdit")
        if not source.resolve().is_relative_to((root / "overlays").resolve()):
            raise ValueError("Surcharge : source hors overlays")
        content = source.read_bytes()
        if hashlib.sha256(content).hexdigest() != overlay["source_sha256"]:
            raise ValueError("Surcharge : empreinte locale divergente")
        anchor = overlay["anchor"].encode("utf-8")
        if base.count(anchor) != 1:
            raise ValueError("Surcharge : ancre absente ou ambiguë")
        # Une insertion sans changement du frontmatter ni des autres octets amont.
        result[target] = base.replace(anchor, content.rstrip(b"\n") + b"\n\n" + anchor, 1)
    return result
