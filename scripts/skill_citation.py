"""Citation v4 : refuse des chemins de ressources de skill dans la réponse."""
from __future__ import annotations

import re
from urllib.parse import unquote

LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
RESOURCE = re.compile(r'(?:SKILL\.md|(?:references|objets)/[^\s`<>]+|\.agents/skills/)', re.I)
HTTP_URL = re.compile(r'https?://[^\s<>`]+', re.I)
PATH = re.compile(r'(?:[A-Z]:/|\.agents/skills/|(?:skills/)?[\w-]+/(?:SKILL\.md|references/|objets/)|(?:references|objets)/[^\s`<>]+\.md)', re.I)


def forbidden_skill_path(text: str) -> bool:
    """Refuse les cibles de ressources de skill, quel que soit leur hôte."""
    normalized = unquote(text).replace('\\', '/')
    for match in LINK.finditer(normalized):
        target = match[1].strip('<> ')
        if RESOURCE.search(target):
            return True
    # Examiner aussi les URL nues et autoliens avant de les retirer du texte.
    if any(RESOURCE.search(match[0]) for match in HTTP_URL.finditer(normalized)):
        return True
    without_urls = HTTP_URL.sub('', normalized)
    return bool(PATH.search(without_urls))
