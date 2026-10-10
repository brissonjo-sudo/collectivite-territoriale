"""Charge Ponytail uniquement si sa release publiée et ses octets sont à jour."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

REPOSITORY = "https://github.com/DietrichGebert/ponytail"
API = "https://api.github.com/repos/DietrichGebert/ponytail/"
SKILL = Path(__file__).resolve().parents[1]


def github_json(route: str) -> dict:
    """Effectue une lecture publique bornée, sans token ni cache de succès."""
    request = Request(API + route, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "collectivite-territoriale-ponytail-version-check",
        "X-GitHub-Api-Version": "2026-03-10",
        "Cache-Control": "no-cache",
    })
    with urlopen(request, timeout=10) as response:
        if not response.geturl().startswith(API) or response.status != 200:
            raise ValueError("Réponse GitHub inattendue")
        payload = response.read(1_000_001)
    if len(payload) > 1_000_000:
        raise ValueError("Réponse GitHub trop volumineuse")
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise ValueError("Réponse GitHub non structurée")
    return value


def checked_rules(skill: Path, fetch: Callable[[str], dict] | None = None) -> tuple[dict, str]:
    """Refuse les fichiers altérés, une ancienne release ou une preuve indisponible."""
    fetch = fetch or github_json
    lock = json.loads((skill / "upstream-lock.json").read_text(encoding="utf-8"))
    tag = lock["release_tag"]
    if (lock["format_version"] != 1 or lock["repository"] != REPOSITORY
            or not isinstance(tag, str) or not re.fullmatch(r"v\d+\.\d+\.\d+", tag)
            or lock["version"] != tag[1:]
            or not re.fullmatch(r"[0-9a-f]{40}", lock["commit"])
            or set(lock["files_sha256"]) != {"rules.md", "LICENSE"}):
        raise ValueError("Provenance locale invalide")
    contents: dict[str, bytes] = {}
    for name, expected in lock["files_sha256"].items():
        path = skill / name
        if path.is_symlink():
            raise ValueError("Lien symbolique interdit")
        contents[name] = path.read_bytes()
        if hashlib.sha256(contents[name]).hexdigest() != expected:
            raise ValueError(f"Fichier installé modifié : {name}")

    release = fetch("releases/latest")
    if release["draft"] is not False or release["prerelease"] is not False:
        raise ValueError("Release stable non confirmée")
    if release["tag_name"] != tag:
        raise ValueError(f"Version obsolète : {tag} ; dernière release {release['tag_name']}")
    reference = fetch("git/ref/tags/" + tag)
    if reference["ref"] != "refs/tags/" + tag:
        raise ValueError("Étiquette amont inattendue")
    obj = reference["object"]
    for _ in range(3):
        if not re.fullmatch(r"[0-9a-f]{40}", obj["sha"]):
            raise ValueError("Objet Git amont invalide")
        if obj["type"] == "commit":
            break
        if obj["type"] != "tag":
            raise ValueError("L'étiquette ne désigne pas un commit")
        obj = fetch("git/tags/" + obj["sha"])["object"]
    if obj["type"] != "commit" or obj["sha"] != lock["commit"]:
        raise ValueError("Commit de la release modifié ou non confirmé")
    result = {"status": "current", "version": lock["version"], "tag": tag,
              "commit": obj["sha"], "checked_at": datetime.now(timezone.utc).isoformat()}
    return result, contents["rules.md"].decode("utf-8")


def main() -> int:
    """N'affiche aucune règle Ponytail si un contrôle échoue."""
    try:
        status, rules = checked_rules(SKILL)
    except Exception as exc:
        # Un contrôle non confirmé ne doit jamais devenir une autorisation implicite.
        reason = str(exc)[:200] if isinstance(exc, ValueError) else type(exc).__name__
        print(f"PONYTAIL BLOQUÉ — contrôle non confirmé ({reason}). "
              "Ne pas utiliser Ponytail ; vérifier la version et la connexion.", file=sys.stderr)
        return 1
    print(json.dumps(status, ensure_ascii=False))
    print(rules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
