"""Citation v4 : refuse des chemins de ressources de skill dans la réponse."""
from __future__ import annotations

import re
from urllib.parse import unquote

LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
RESOURCE = re.compile(r'(?:SKILL\.md|(?:references|objets)/[^\s`<>]+\.md)', re.I)
PATH = re.compile(r'(?:[A-Z]:/|\.agents/skills/|(?:skills/)?[\w-]+/(?:SKILL\.md|references/|objets/)|(?:references|objets)/[^\s`<>]+\.md)', re.I)


def forbidden_skill_path(text: str) -> bool:
    """Les URL officielles HTTP(S) restent des liens de source autorisés."""
    normalized = unquote(text).replace('\\', '/')
    for match in LINK.finditer(normalized):
        target = match[1].strip('<> ')
        if not re.match(r'https?://', target, re.I) and RESOURCE.search(target):
            return True
    # Retirer les URL HTTP(S) avant l'examen des chemins textuels.
    without_urls = re.sub(r'https?://[^\s<>`]+', '', normalized, flags=re.I)
    return bool(PATH.search(without_urls))
