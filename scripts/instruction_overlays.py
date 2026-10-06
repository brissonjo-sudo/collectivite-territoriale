"""Applique des corrections bornées, déclarées et liées à des empreintes figées."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath

HASH = re.compile(r"^[0-9a-f]{64}$")
DESCRIPTION_FIELD = re.compile(rb"description: >-\r?\n(?:  [^\s\r\n][^\r\n]*\r?\n)+")
FRONTMATTER = re.compile(rb"\A---\r?\n(.*?)^---\r?\n", re.MULTILINE | re.DOTALL)


def description_field(content: bytes) -> bytes:
    """Accepte uniquement un champ description folded simple, complet et UTF-8."""
    content.decode("utf-8")
    if DESCRIPTION_FIELD.fullmatch(content) is None:
        raise ValueError("Surcharge : seul le champ description folded simple est autorisé")
    return content


def replace_description(base: bytes, anchor: bytes, content: bytes) -> bytes:
    """Remplace le seul champ description du frontmatter, sans autre modification."""
    description_field(anchor)
    description_field(content)
    frontmatter = FRONTMATTER.match(base)
    if frontmatter is None:
        raise ValueError("Surcharge : frontmatter absent ou invalide")
    old_fields = list(re.finditer(rb"^description[ \t]*:", frontmatter[1], re.MULTILINE))
    if len(old_fields) != 1:
        raise ValueError("Surcharge : description absente ou ambiguë dans le frontmatter")
    field_start = frontmatter.start(1) + old_fields[0].start()
    header_end = base.index(b"\n", field_start) + 1
    next_field = re.search(rb"^[^\s]", base[header_end:frontmatter.end(1)], re.MULTILINE)
    field_end = header_end + next_field.start() if next_field else frontmatter.end(1)
    complete_field = base[field_start:field_end]
    if complete_field != anchor:
        raise ValueError("Surcharge : ancre différente du champ description complet du frontmatter")
    description_field(complete_field)
    return base[:field_start] + content + base[field_end:]


def validate_overlays(overlays: list[dict]) -> None:
    """Refuse les chemins dangereux et les opérations non bornées ou dupliquées."""
    if not isinstance(overlays, list):
        raise ValueError("Surcharges : liste attendue")
    targets: set[tuple[str, str]] = set()
    for overlay in overlays:
        required = {"target", "source", "base_sha256", "source_sha256", "anchor"}
        if not isinstance(overlay, dict) or set(overlay) not in (required, required | {"operation"}):
            raise ValueError("Surcharge : contrat invalide")
        operation = overlay.get("operation", "insert-before")
        if operation not in ("insert-before", "replace-description"):
            raise ValueError("Surcharge : opération inconnue")
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
        identity = (overlay["target"], operation)
        if identity in targets:
            raise ValueError("Surcharge : cible dupliquée")
        targets.add(identity)
        if operation == "replace-description":
            if overlay["target"] != "SKILL.md" or not overlay["source"].endswith(".md"):
                raise ValueError("Surcharge : description limitée à SKILL.md et à une source Markdown")
        if any(not isinstance(overlay[key], str) or not HASH.fullmatch(overlay[key])
               for key in ("base_sha256", "source_sha256")):
            raise ValueError("Surcharge : empreinte invalide")
        if not isinstance(overlay["anchor"], str) or not overlay["anchor"]:
            raise ValueError("Surcharge : ancre vide")
        if operation == "replace-description":
            description_field(overlay["anchor"].encode("utf-8"))


def apply_overlays(root: Path, files: dict[str, bytes], overlays: list[dict]) -> dict[str, bytes]:
    """Applique les opérations dans l'ordre, avec empreinte d'entrée à chaque étape."""
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
        if overlay.get("operation", "insert-before") == "replace-description":
            result[target] = replace_description(base, anchor, content)
        else:
            frontmatter = FRONTMATTER.match(base)
            if frontmatter and base.index(anchor) < frontmatter.end():
                raise ValueError("Surcharge : insert-before ne peut pas modifier le frontmatter")
            # Une insertion sans changement du frontmatter ni des autres octets amont.
            result[target] = base.replace(anchor, content.rstrip(b"\n") + b"\n\n" + anchor, 1)
    return result
