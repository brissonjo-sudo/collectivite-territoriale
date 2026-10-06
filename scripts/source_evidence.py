"""Extrait une preuve documentaire bornée, sans faire confiance au résultat reçu.

Les extraits restent des données non fiables. Leur présence et leur empreinte
ne prouvent ni la justesse d'une réponse ni la vigueur d'une règle de droit.
Les formats non reconnus, erreurs et contenus hors sources officielles sont
refusés sans conserver leur corps. Aucun accès réseau n'est effectué.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


MAX_EXCERPT_CHARS = 12_000
MAX_DOCUMENTS = 8
MAX_TOTAL_CHARS = 60_000
MAX_INPUT_CHARS = 262_144
MAX_VISIBLE_CHARS = 65_536
MAX_DEPTH = 8
MAX_NODES = 4_096
TRUST = "untrusted_source_data"
MCP_PREFIX = "mcp__droit-francais__"
MCP_TOOLS = frozenset(
    {"search", "fetch", "search_articles", "get_article", "search_case_law", "get_decision"}
)
OFFICIAL_HOSTS = frozenset(
    {
        "legifrance.gouv.fr", "www.legifrance.gouv.fr", "eur-lex.europa.eu",
        "cnil.fr", "www.cnil.fr", "courdecassation.fr", "www.courdecassation.fr",
    }
)
_DATE_FIELDS = frozenset(
    {
        "start_date", "end_date", "version_start_date", "version_end_date",
        "as_of_date", "requested_date", "server_date", "decision_date", "source_update_date",
    }
)
_TEXT_FIELDS = frozenset(
    {
        "number", "legal_status", "source", "date_basis", "caveat", "jurisdiction",
        "chamber", "ecli", "formation", "solution",
    }
)
_BOOL_FIELDS = frozenset({"verified", "applicable_at_as_of_date"})
_SUSPECT = re.compile(
    r"(?i)(?:\bbearer\s+\S+|\b(?:authorization|cookie|set-cookie)\s*[:=]"
    r"|\b(?:api[ _-]?key|access[ _-]?token|refresh[ _-]?token|token|secret|"
    r"password|mot[ _]de[ _]passe|jeton|clé[ _]api)\s*[\"']?\s*[:=]"
    r"|\b(?:sk|ghp|gho|github_pat)[_-][A-Za-z0-9_-]{8,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    r"|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"
    r"|(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])"
    r"|(?<!\w)(?:[0-9a-f]{1,4}:){2,}[0-9a-f:]+(?!\w)"
    r"|(?<![\w/.-])[A-Za-z0-9_+/=-]{40,}(?![\w/.-]))"
)
_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:authorization|(?:set[ _-]?)?cookie|api[ _-]?key|"
    r"access[ _-]?token|refresh[ _-]?token|token|secret|password|"
    r"mot[ _]de[ _]passe|jeton|clé[ _]api|signature)[\"']?[ \t]*[:=]"
    r"(?![ \t]*\*{0,2}[ \t]*(?:\r?\n|$))[^\r\n]*"
)
_PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?"
    r"(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)"
)
_REDACTION = "[DONNÉE MASQUÉE]"
_URL_IN_TEXT = re.compile(r"(?i)https?://[^\s<>\"']+")
_IDENTIFIER = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
_CELEX = re.compile(r"(?:CELEX:)?([0-9]{5}[A-Z][0-9]{4}(?:\([0-9]{2}\))?)\Z", re.I)


def _bounded(value: Any) -> bool:
    """Refuse les structures excessives avant de parcourir les champs utiles."""
    stack = [(value, 0)]
    nodes = chars = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            return False
        if isinstance(item, str):
            chars += len(item)
            if chars > MAX_INPUT_CHARS:
                return False
        elif isinstance(item, dict):
            if len(item) > MAX_NODES:
                return False
            stack.extend((key, depth + 1) for key in item)
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            if len(item) > MAX_NODES:
                return False
            stack.extend((child, depth + 1) for child in item)
        elif item is not None and type(item) not in (bool, int, float):
            return False
    return True


def _safe_url(value: Any) -> str | None:
    if not isinstance(value, str) or not value or len(value) > 2_048:
        return None
    if any(ord(char) < 33 or ord(char) == 127 for char in value):
        return None
    try:
        value.encode("utf-8")
        parsed = urlsplit(value)
        host = parsed.hostname
        if (
            parsed.scheme != "https" or host not in OFFICIAL_HOSTS
            or parsed.username is not None or parsed.password is not None
            or parsed.port not in (None, 443)
        ):
            return None
        path = parsed.path or "/"
        decoded = path
        for _ in range(3):
            next_decoded = unquote(decoded)
            if next_decoded == decoded:
                break
            decoded = next_decoded
        if re.search(r"%[0-9a-f]{2}", decoded, re.I):
            return None
        if "\\" in decoded or _SUSPECT.search(decoded):
            return None
        # Les paramètres libres sont éliminés, y compris les paramètres secrets.
        query: list[tuple[str, str]] = []
        if host == "eur-lex.europa.eu":
            for key, candidate in parse_qsl(parsed.query, max_num_fields=16):
                if key not in ("uri", "CELEX"):
                    continue
                match = _CELEX.fullmatch(candidate)
                if match:
                    normalized = match.group(1).upper()
                    query.append((key, "CELEX:" + normalized if key == "uri" else normalized))
        return urlunsplit(("https", host, path, urlencode(query), ""))
    except (ValueError, UnicodeError):
        return None


def _safe_text(value: Any, limit: int) -> tuple[str | None, bool]:
    if not isinstance(value, str) or not value.strip() or _SUSPECT.search(value):
        return None, False
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        return None, False
    # On retire le champ entier lorsqu'il contient une URL étrangère ou sensible.
    for match in _URL_IN_TEXT.finditer(value):
        raw = match.group().rstrip(".,;:)")
        safe = _safe_url(raw)
        if safe is None or unquote(safe) != raw:
            return None, False
    cleaned = "".join(char for char in value if ord(char) >= 32 or char in "\n\t")
    cleaned = cleaned.strip()
    return cleaned[:limit] or None, len(cleaned) > limit


def _safe_identifier(value: Any) -> str | None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        return None
    # Un identifiant d'appel Claude peut être long : sa forme est contrôlée
    # séparément des extraits, où les chaînes opaques longues sont supprimées.
    if _SUSPECT.search(value) and not re.fullmatch(r"toolu_[A-Za-z0-9_-]{1,100}", value):
        return None
    return value


def _source_identifier(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if re.fullmatch(r"(?:LEGIARTI|LEGITEXT|JURITEXT|JORFTEXT|LEGISCTA)\d{12}", value):
        return value
    if re.fullmatch(r"[0-9a-f]{24}", value, re.I) or _CELEX.fullmatch(value):
        return value
    return None


def scrub_visible_text(value: str) -> dict[str, str | bool]:
    """Borne et masque les secrets détectables des seuls textes visibles.

    Les citations, le Markdown et les mentions STOP ordinaires sont conservés.
    Une affectation sensible supprime la fin de sa ligne, plutôt que conserver
    une valeur ambiguë. Les URL sensibles sont remplacées intégralement. Aucun
    texte rejeté n'est haché. Ce filtre prudent ne détecte pas tous les secrets
    arbitraires non étiquetés ; il ne rend pas fiables les textes conservés.
    """
    if not isinstance(value, str):
        return {"text": "", "redacted": True, "truncated": False}
    truncated = len(value) > MAX_VISIBLE_CHARS
    bounded = value[:MAX_VISIBLE_CHARS]
    redacted = False

    def scrub_plain(text: str) -> str:
        nonlocal redacted
        clean = _PRIVATE_KEY.sub(_REDACTION, text)
        clean = _SECRET_ASSIGNMENT.sub(_REDACTION, clean)
        clean = _SUSPECT.sub(_REDACTION, clean)
        clean = "".join(
            char for char in clean
            if (ord(char) >= 32 or char in "\n\t")
            and not 0xD800 <= ord(char) <= 0xDFFF and ord(char) != 127
        )
        redacted = redacted or clean != text
        return clean

    output: list[str] = []
    position = 0
    for match in _URL_IN_TEXT.finditer(bounded):
        output.append(bounded[position:match.start()])
        raw = match.group()
        url = raw.rstrip(".,;:)")
        suffix = raw[len(url):]
        decoded = url
        for _ in range(3):
            decoded = unquote(decoded)
        try:
            parsed = urlsplit(decoded)
            sensitive = (
                parsed.username is not None or parsed.password is not None
                or _SUSPECT.search(decoded) is not None
                or _SECRET_ASSIGNMENT.search(decoded) is not None
                or any(0xD800 <= ord(char) <= 0xDFFF for char in decoded)
            )
        except ValueError:
            sensitive = True
        if sensitive:
            redacted = True
            output.append(_REDACTION + suffix)
        else:
            output.append(raw)
        position = match.end()
    output.append(bounded[position:])
    # La suppression des affectations couvre la ligne entière, même si elle
    # contient une URL. Découper la ligne avant ce filtre laisserait des valeurs.
    cleaned = scrub_plain("".join(output))
    truncated = truncated or len(cleaned) > MAX_VISIBLE_CHARS
    return {
        "text": cleaned[:MAX_VISIBLE_CHARS],
        "redacted": redacted, "truncated": truncated,
    }


def _utc(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) > 40:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError):
        return None


def _metadata(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {"content_trust": TRUST}
    result: dict[str, Any] = {"content_trust": TRUST}
    for key in sorted(_DATE_FIELDS | _TEXT_FIELDS | _BOOL_FIELDS):
        item = value.get(key)
        if key not in value:
            continue
        if item is None:
            result[key] = None
        elif key in _BOOL_FIELDS and type(item) is bool:
            result[key] = item
        elif key in _DATE_FIELDS:
            if type(item) is int and -2_208_988_800_000 <= item <= 32_503_680_000_000:
                result[key] = item
            elif isinstance(item, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", item):
                try:
                    date.fromisoformat(item)
                    result[key] = item
                except ValueError:
                    pass
        elif key in _TEXT_FIELDS:
            safe, shortened = _safe_text(item, 500)
            if safe is not None:
                result[key] = safe
                if shortened:
                    result["truncated"] = True
    return result


def _hash(value: Any) -> str:
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _text_parts(content: Any) -> list[str] | None:
    if isinstance(content, str):
        return [content] if content.strip() else []
    if isinstance(content, list):
        return [
            item["text"] for item in content
            if isinstance(item, dict) and item.get("type") == "text"
            and isinstance(item.get("text"), str) and item["text"].strip()
        ]
    return None


def _decode(value: Any, depth: int = 0) -> tuple[list[dict[str, Any]], str | None]:
    if depth > 4 or not isinstance(value, dict):
        return [], "unknown_format"
    if value.get("isError") is True or value.get("is_error") is True or "error" in value:
        return [], "tool_error"
    if "structuredContent" in value:
        return _decode(value["structuredContent"], depth + 1)
    if "results" in value:
        if not isinstance(value["results"], list):
            return [], "unknown_format"
        return [value], None
    if "url" in value and any(key in value for key in ("id", "title", "text")):
        return [value], None
    parts = _text_parts(value.get("content"))
    if parts is None:
        return [], "unknown_format"
    if not parts:
        return [], "empty_transport"
    payloads: list[dict[str, Any]] = []
    for part in parts:
        try:
            parsed = json.loads(part)
        except (ValueError, RecursionError):
            return [], "unknown_format"
        if not _bounded(parsed):
            return [], "input_limit"
        extracted, reason = _decode(parsed, depth + 1)
        if reason:
            return [], reason
        payloads.extend(extracted)
    return payloads, None


def _web_parts(value: dict[str, Any], depth: int = 0) -> tuple[list[str], str | None]:
    """Accepte un résumé textuel ou une enveloppe connue, jamais du JSON brut."""
    if depth > 4:
        return [], "unknown_format"
    if value.get("isError") is True or value.get("is_error") is True or "error" in value:
        return [], "tool_error"
    parts = _text_parts(value.get("content"))
    if parts is None:
        return [], "unknown_format"
    if not parts:
        return [], "empty_transport"
    result: list[str] = []
    for part in parts:
        if part.lstrip().startswith(("{", "[")):
            try:
                parsed = json.loads(part)
            except (ValueError, RecursionError):
                return [], "unknown_format"
            if not isinstance(parsed, dict) or not _bounded(parsed):
                return [], "unknown_format"
            nested, reason = _web_parts(parsed, depth + 1)
            if reason:
                return [], reason
            result.extend(nested)
        else:
            result.append(part)
    return result, None


def _is_homepage(url: str) -> bool:
    path = urlsplit(url).path.rstrip("/").lower()
    return path in ("", "/fr", "/en", "/accueil", "/home", "/index.html")


def _document(value: dict[str, Any], *, summary: bool = False) -> dict[str, Any] | None:
    if value.get("isError") is True or value.get("is_error") is True or "error" in value:
        return None
    url = _safe_url(value.get("url"))
    if url is None or _is_homepage(url):
        return None
    excerpt, shortened = _safe_text(value.get("text"), MAX_EXCERPT_CHARS)
    identifier = _source_identifier(value.get("id"))
    title, title_shortened = _safe_text(value.get("title"), 500)
    if summary and excerpt is None:
        return None
    if not summary and excerpt is None and identifier is None and title is None:
        return None
    nature = "tool_summary" if summary else ("primary_text" if excerpt else "search_result")
    metadata = _metadata(value.get("metadata"))
    shortened = shortened or title_shortened or metadata.get("truncated") is True
    doc: dict[str, Any] = {
        "nature": nature, "url": url, "content_trust": TRUST,
        "status": "truncated" if shortened else "available",
        "metadata": metadata,
    }
    if identifier:
        doc["id"] = identifier
    if title:
        doc["title"] = title
    if excerpt:
        doc["excerpt"] = excerpt
    return doc


def extract_source_evidence(
    block: dict[str, Any], *, tool: str, call_id: str,
    source_url: str | None = None, retrieved_at: str,
) -> dict[str, Any]:
    """Réduit un résultat Claude aux seules données publiques autorisées.

    ``call_id`` et ``retrieved_at`` proviennent du harnais, jamais du résultat
    de source. L'heure est normalisée en UTC. Les empreintes portent uniquement
    sur les documents assainis. Une erreur retourne une raison fixe, sans corps.
    Le statut ``available`` décrit la présence de données, pas leur validité
    juridique ; les dates et indicateurs source sont conservés sans inférence.
    """
    stamp = _utc(retrieved_at)
    identifier = _safe_identifier(call_id)
    recognized = tool == "WebFetch" or (
        isinstance(tool, str) and tool.startswith(MCP_PREFIX)
        and tool[len(MCP_PREFIX):] in MCP_TOOLS
    )
    result: dict[str, Any] = {
        "type": "source_evidence", "tool": tool if recognized else "unsupported",
        "call_id": identifier, "retrieved_at": stamp, "content_trust": TRUST,
        "status": "missing", "documents": [], "truncated": False,
    }

    def missing(reason: str) -> dict[str, Any]:
        result["reason"] = reason
        return result

    if not recognized:
        return missing("unsupported_tool")
    if stamp is None or identifier is None:
        return missing("invalid_provenance")
    if not isinstance(block, dict):
        return missing("unknown_format")
    if "tool_use_id" in block and block["tool_use_id"] != call_id:
        return missing("call_id_mismatch")
    if not _bounded(block):
        return missing("input_limit")
    if block.get("is_error") is True or block.get("isError") is True or "error" in block:
        return missing("tool_error")
    candidates: list[dict[str, Any]] = []
    if tool == "WebFetch":
        url = _safe_url(source_url)
        if url is None:
            return missing("unapproved_source_url")
        if _is_homepage(url):
            return missing("homepage")
        parts, reason = _web_parts(block)
        if reason:
            return missing(reason)
        doc = _document({"url": url, "text": "\n".join(parts)}, summary=True)
        if doc:
            candidates.append(doc)
    else:
        payloads, reason = _decode(block)
        if reason:
            return missing(reason)
        for payload in payloads:
            items = payload.get("results") if "results" in payload else [payload]
            for item in items:
                if not isinstance(item, dict):
                    continue
                raw = dict(item)
                if "results" in payload:
                    # Seuls les champs connus de datation/provenance sont hérités.
                    raw["metadata"] = {
                        **(payload.get("provenance") if isinstance(payload.get("provenance"), dict) else {}),
                        **(payload.get("dating") if isinstance(payload.get("dating"), dict) else {}),
                        **{key: item[key] for key in _DATE_FIELDS | _TEXT_FIELDS | _BOOL_FIELDS if key in item},
                        **(item.get("metadata") if isinstance(item.get("metadata"), dict) else {}),
                    }
                if "results" in payload or tool[len(MCP_PREFIX):] in (
                    "search", "search_articles", "search_case_law",
                ):
                    # La nature dépend aussi de l'outil : un document direct
                    # renvoyé par une recherche ne devient pas un texte primaire.
                    raw.pop("text", None)
                doc = _document(raw)
                if doc:
                    candidates.append(doc)
    if not candidates:
        return missing("no_public_source_data")
    documents: list[dict[str, Any]] = []
    # Le budget inclut les métadonnées, les échappements JSON et les empreintes.
    # La réserve couvre l'enveloppe finale et le changement de statut.
    budget = MAX_TOTAL_CHARS - len(json.dumps(result, ensure_ascii=False)) - 200
    total = 0
    shortened = len(candidates) > MAX_DOCUMENTS
    for doc in candidates[:MAX_DOCUMENTS]:
        excerpt = doc.get("excerpt", "")
        remaining = max(0, budget - total)
        size = len(json.dumps(doc, ensure_ascii=False)) + 80
        if size > remaining:
            doc["status"] = "truncated"
            low, high = 0, len(excerpt)
            while low < high:
                middle = (low + high + 1) // 2
                doc["excerpt"] = excerpt[:middle]
                if len(json.dumps(doc, ensure_ascii=False)) + 80 <= remaining:
                    low = middle
                else:
                    high = middle - 1
            doc["excerpt"] = excerpt[:low]
            if len(json.dumps(doc, ensure_ascii=False)) + 80 > remaining:
                shortened = True
                break
        shortened = shortened or doc["status"] == "truncated"
        doc["sha256"] = _hash(doc)
        total += len(json.dumps(doc, ensure_ascii=False)) + 2
        documents.append(doc)
    result.update(
        status="truncated" if shortened else "available",
        documents=documents, truncated=shortened, sha256=_hash(documents),
    )
    return result
