"""Projection documentaire du rollout natif, sans inférence ni effet à l'import.

Les fonctions ne modifient ni configuration, ni preuve, ni fichier. Les textes
documentaires sont des données non fiables. Leur disponibilité ne certifie
jamais leur pertinence, leur vigueur ou l'applicabilité d'une disposition.
Un retour imprimé par ``functions.exec`` reste relié à l'appel enveloppant ;
il ne crée aucune identité native pour les appels internes non enregistrés.
"""

from __future__ import annotations

import copy
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
MAX_INPUT_CHARS = 262_144
MAX_EXCERPT_CHARS = 12_000
MAX_DOCUMENTS = 8
MAX_TOTAL_CHARS = 60_000
MAX_VISIBLE_CHARS = 65_536
MAX_ARGUMENT_CHARS = 16_384
TRUST = "untrusted_source_data"
OFFICIAL_HOSTS = frozenset(
    {
        "legifrance.gouv.fr",
        "www.legifrance.gouv.fr",
        "eur-lex.europa.eu",
        "cnil.fr",
        "www.cnil.fr",
        "courdecassation.fr",
        "www.courdecassation.fr",
    }
)
MCP_OPERATIONS = frozenset(
    {
        "search",
        "search_articles",
        "search_case_law",
        "fetch",
        "get_article",
        "get_decision",
    }
)
DATE_FIELDS = frozenset(
    {
        "start_date",
        "end_date",
        "version_start_date",
        "version_end_date",
        "as_of_date",
        "requested_date",
        "server_date",
        "decision_date",
        "source_update_date",
    }
)
META_TEXT_FIELDS = frozenset(
    {
        "number",
        "legal_status",
        "source",
        "date_basis",
        "caveat",
        "jurisdiction",
        "chamber",
        "ecli",
        "formation",
        "solution",
    }
)
META_BOOL_FIELDS = frozenset({"verified", "applicable_at_as_of_date"})
SENSITIVE = re.compile(
    r"(?i)(?:\bbearer\s+\S+|\b(?:authorization|cookie|set-cookie)\s*[:=]"
    r"|\b(?:api[ _-]?key|access[ _-]?token|refresh[ _-]?token|password|secret|"
    r"mot[ _]de[ _]passe|jeton|clé[ _]api)\s*[\"']?\s*[:=]"
    r"|\b(?:sk|ghp|gho|github_pat)[_-][A-Za-z0-9_-]{8,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    r"|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"
    r"|(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.]))"
)
CALL_ID = re.compile(r"[A-Za-z0-9_.:-]{1,160}\Z")
TOOL_NAME = re.compile(r"[A-Za-z0-9_.:-]{1,200}\Z")
URL_TEXT = re.compile(r"https?://[^\s<>\"']+", re.I)
TRUNCATION_MARKER = re.compile(
    r"(?:\[\s*(?:output\s+)?truncated\s*\]|Warning:\s*truncated output|"
    r"(?:original|total)\s+(?:token|character)\s+count:\s*\d+|"
    r"(?:output|content|result)\s+(?:was\s+)?truncated)",
    re.I,
)
HOST_ADDENDUM = """Hôte Codex CLI natif dev.7 ; aucune inférence par le normaliseur.
Les événements derived_* sont des projections reliées à une ligne/SHA native.
Une injection complète nom/chemin/SHA dépend du scellement du transport par le harnais.
ReadSKILL seul prouve une réception, jamais l'activation stricte du plugin.
Le premier texte visible inclut commentary ; reasoning et sorties outils sont exclus.
STOP dans la finale ne répare jamais un texte visible antérieur.
Chaque résultat documentaire dépend d'un call_id natif réel, antérieur et unique.
Une sortie functions.exec ne reconstruit jamais l'identité de l'appel interne.
primary_text, search_result, tool_summary, erreur et contenu incomplet restent distincts.
Les métadonnées sont observées ; leur présence ne certifie ni vigueur ni applicabilité.
Retrieval exige un primaire complet utilisable lié ; l'abstention reste atomique.
Une source nominale absente bloque ; aucun score historique n'est transféré.
Les atomes et le barème original restent inchangés ; release_ready=false.
"""


class EvidenceError(ValueError):
    """Une entrée ou une liaison de preuve ne peut être établie."""


def sha(raw: bytes) -> str:
    """Retourne l'empreinte d'octets déjà détenus, sans accès externe."""
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    """Sérialise une projection assainie pour son scellement."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def starts_stop(text: str) -> bool:
    """Tolère seulement les délimiteurs Markdown simples devant STOP."""
    rendered = text.lstrip()
    rendered = re.sub(r"^```(?:text|plaintext)?[ \t]*\r?\n", "", rendered, flags=re.I)
    rendered = re.sub(r"^#{1,6}[ \t]+", "", rendered)
    rendered = re.sub(r"^(?:\*\*|__|\*|_)", "", rendered)
    return bool(re.match(r"STOP\b", rendered))


def _safe_string(value: Any, limit: int) -> tuple[str | None, bool]:
    if not isinstance(value, str) or SENSITIVE.search(value):
        return None, isinstance(value, str) and bool(value)
    if any(
        0xD800 <= ord(c) <= 0xDFFF or (ord(c) < 32 and c not in "\n\r\t") for c in value
    ):
        return None, True
    if len(value) > limit:
        return value[:limit], True
    return value, False


def sanitize(text: str, cache: Path) -> tuple[str, bool]:
    """Omet le champ sensible entier, sans empreinte du secret isolé."""
    clean, incomplete = _safe_string(text, MAX_VISIBLE_CHARS)
    if clean is None:
        return "[CONTENU_SENSIBLE_OMIS]", True
    clean = clean.replace(str(cache), "$INSTALLED_PLUGIN").replace(
        cache.as_posix(), "$INSTALLED_PLUGIN"
    )
    return clean, incomplete


def _identifier(value: Any) -> str | None:
    return (
        value
        if isinstance(value, str)
        and CALL_ID.fullmatch(value)
        and not SENSITIVE.search(value)
        else None
    )


def _timestamp(value: Any) -> str | None:
    """Conserve une date native avec fuseau, sans la reconstruire."""
    clean, hidden = _safe_string(value, 50)
    if not clean or hidden:
        return None
    try:
        parsed = datetime.fromisoformat(clean.replace("Z", "+00:00"))
        return clean if parsed.tzinfo is not None else None
    except ValueError:
        return None


def _tool(value: Any) -> str | None:
    return value if isinstance(value, str) and TOOL_NAME.fullmatch(value) else None


def _bounded(value: Any) -> bool:
    stack = [(value, 0)]
    nodes = chars = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        if nodes > 4096 or depth > 10:
            return False
        if isinstance(item, str):
            chars += len(item)
            if chars > MAX_INPUT_CHARS:
                return False
        elif isinstance(item, dict):
            stack.extend((k, depth + 1) for k in item)
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
        elif item is not None and type(item) not in (bool, int, float):
            return False
    return True


def _parse_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    if len(value) > MAX_INPUT_CHARS:
        return None
    try:
        return json.loads(value)
    except (ValueError, RecursionError):
        return value


def _text_parts(value: Any, depth: int = 0) -> list[str]:
    """Lit les enveloppes fermées ; ne copie pas les inventaires bruts."""
    if depth > 6:
        return []
    if isinstance(value, str):
        parsed = _parse_json(value)
        if isinstance(parsed, (dict, list)):
            return _text_parts(parsed, depth + 1)
        return [value]
    if isinstance(value, list):
        return [part for child in value for part in _text_parts(child, depth + 1)]
    if isinstance(value, dict):
        parts = [
            value[k]
            for k in ("text", "output", "error")
            if isinstance(value.get(k), str)
        ]
        if "content" in value:
            parts += _text_parts(value["content"], depth + 1)
        return parts
    return []


def failure_metadata(output: Any) -> dict[str, Any]:
    """Expose des codes constants, sans erreur brute ou inventaire privé."""
    parts = _text_parts(output)
    failure_parts = [
        p
        for p in parts
        if "exec_command failed:" in p or "Failed to create unified exec process:" in p
    ]
    parsed = _parse_json(output)
    codes: list[str] = []
    if isinstance(parsed, dict):
        if (
            parsed.get("isError") is True
            or parsed.get("is_error") is True
            or "error" in parsed
        ):
            codes.append("tool_error")
        if type(parsed.get("exit_code")) is int and parsed["exit_code"] != 0:
            codes.append("process_exit_nonzero")
    if any("exec_command failed:" in p for p in failure_parts):
        codes.append("exec_command_failed")
    if any("Failed to create unified exec process:" in p for p in failure_parts):
        codes.append("process_start_failed")
    if any(
        "helper_unknown_error: setup refresh had errors" in p for p in failure_parts
    ):
        codes.append("windows_sandbox_setup_refresh_error")
    for code in (5, 32):
        if any(
            re.search(rf"(?:os error\s+{code}\b|Win(?:32)?Error\s*{code}\b)", p, re.I)
            for p in failure_parts
        ):
            codes.append(f"windows_error_{code}")
    blocked = any("blocked by policy" in p.lower() for p in parts)
    if blocked:
        codes.append("policy_block_observed")
    return {
        "native_failure_observed": bool(codes),
        "failure_codes": codes,
        "failure_mechanism": "process_start"
        if "process_start_failed" in codes
        else None,
        "failure_reason_minimal": "helper_unknown_error: setup refresh had errors"
        if "windows_sandbox_setup_refresh_error" in codes
        else None,
        "blocked_by_policy": blocked,
        "auto_review_rejection_established": False,
        "raw_tool_output_exported": False,
    }


def _flags(value: Any, depth: int = 0) -> tuple[bool, bool]:
    if depth > 6:
        return True, False
    if isinstance(value, str):
        return bool(TRUNCATION_MARKER.search(value)), False
    if isinstance(value, list):
        pairs = [_flags(v, depth + 1) for v in value]
    elif isinstance(value, dict):
        truncated = any(
            value.get(k) is True for k in ("truncated", "is_truncated", "incomplete")
        )
        truncated = truncated or any(
            value.get(k) is False for k in ("complete", "is_complete", "text_complete")
        )
        truncated = truncated or value.get("status") in (
            "truncated",
            "incomplete",
            "partial",
            "redacted",
            "omitted",
        )
        summary = (
            isinstance(value.get("summary"), str)
            and bool(value["summary"].strip())
            or isinstance(value.get("tool_summary"), str)
            and bool(value["tool_summary"].strip())
            or value.get("nature", value.get("kind", value.get("type")))
            in (
                "tool_summary",
                "summary",
            )
        )
        pairs = [
            _flags(value[k], depth + 1)
            for k in (
                "content",
                "structuredContent",
                "output",
                "text",
                "excerpt",
                "results",
                "documents",
                "metadata",
            )
            if k in value
        ]
        pairs.append((truncated, summary))
    else:
        pairs = []
    return any(p[0] for p in pairs), any(p[1] for p in pairs)


def _official_url(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) > 2048 or SENSITIVE.search(value):
        return None
    try:
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or parsed.hostname not in OFFICIAL_HOSTS
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port not in (None, 443)
            or any(ord(c) <= 32 for c in value)
        ):
            return None
        decoded = value
        for _ in range(3):
            decoded = unquote(decoded)
        if (
            "\\" in decoded
            or SENSITIVE.search(decoded)
            or re.search(r"%[0-9a-f]{2}", decoded, re.I)
        ):
            return None
        if parsed.path.rstrip("/").lower() in (
            "",
            "/fr",
            "/en",
            "/home",
            "/accueil",
            "/index.html",
        ):
            return None
        # Aucune URL reconstruite : un paramètre inconnu reste non attesté.
        if parsed.query and not (
            parsed.hostname == "eur-lex.europa.eu"
            and re.fullmatch(
                r"(?:uri=CELEX%3A|uri=CELEX:|CELEX=)[0-9A-Z()%]+", parsed.query, re.I
            )
        ):
            return None
        return value if not parsed.fragment else None
    except (ValueError, UnicodeError):
        return None


def _metadata(value: Any) -> tuple[dict[str, Any], bool]:
    result: dict[str, Any] = {"content_trust": TRUST}
    incomplete = False
    if not isinstance(value, dict):
        return result, True
    for key in sorted(DATE_FIELDS | META_TEXT_FIELDS | META_BOOL_FIELDS):
        if key not in value:
            continue
        item = value[key]
        if item is None:
            result[key] = None
        elif key in META_BOOL_FIELDS:
            if type(item) is bool:
                result[key] = item
            else:
                incomplete = True
        elif key in DATE_FIELDS and type(item) is int:
            if -2_208_988_800_000 <= item <= 32_503_680_000_000:
                result[key] = item
            else:
                incomplete = True
        elif (
            key in DATE_FIELDS
            and isinstance(item, str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T[0-9:.+-]+Z?)?", item)
        ):
            try:
                if "T" in item:
                    datetime.fromisoformat(item.replace("Z", "+00:00"))
                else:
                    date.fromisoformat(item)
                result[key] = item
            except ValueError:
                incomplete = True
        elif key in META_TEXT_FIELDS:
            clean, hidden = _safe_string(item, 500)
            if clean is not None:
                result[key] = clean
            incomplete = incomplete or hidden
        else:
            incomplete = True
    return result, incomplete


def _operation(tool: str | None) -> str | None:
    if tool is None:
        return None
    match = re.fullmatch(r"mcp__droit[-_]francais__(\w+)", tool)
    return match[1] if match and match[1] in MCP_OPERATIONS else None


def _decode_documents(
    value: Any, depth: int = 0
) -> tuple[list[dict[str, Any]], str | None]:
    if depth > 5 or not _bounded(value):
        return [], "input_limit_or_depth"
    value = _parse_json(value)
    if not isinstance(value, dict):
        return [], "unknown_format"
    if (
        value.get("isError") is True
        or value.get("is_error") is True
        or "error" in value
    ):
        return [], "tool_error"
    if "structuredContent" in value:
        return _decode_documents(value["structuredContent"], depth + 1)
    if "results" in value:
        if not isinstance(value["results"], list) or not all(
            isinstance(v, dict) for v in value["results"]
        ):
            return [], "unknown_format"
        results = []
        for child in value["results"]:
            # Provenance et datation retournées restent des métadonnées observées.
            metadata = {
                **(
                    value.get("provenance")
                    if isinstance(value.get("provenance"), dict)
                    else {}
                ),
                **(
                    value.get("dating") if isinstance(value.get("dating"), dict) else {}
                ),
                **(
                    child.get("metadata")
                    if isinstance(child.get("metadata"), dict)
                    else {}
                ),
            }
            results.append({**child, "metadata": metadata, "_search_container": True})
        return results, None
    if "url" in value and any(k in value for k in ("id", "title", "text", "excerpt")):
        return [value], None
    if "content" in value:
        parts = _text_parts(value["content"])
        if not parts:
            return [], "empty_transport"
        docs = []
        for part in parts:
            children, reason = _decode_documents(part, depth + 1)
            if reason:
                return [], reason
            docs.extend(children)
        return docs, None
    return [], "unknown_format"


def _document(
    value: dict[str, Any],
    operation: str | None,
    forced_incomplete: bool,
    forced_summary: bool,
) -> dict[str, Any]:
    reasons: list[str] = []
    url = _official_url(value.get("url"))
    if url is None:
        reasons.append("official_provenance_not_established")
    identity, identity_hidden = _safe_string(value.get("id"), 160)
    title, title_hidden = _safe_string(value.get("title"), 500)
    metadata, metadata_incomplete = _metadata(value.get("metadata"))
    if not identity and not title:
        reasons.append("document_identity_missing")
    if identity_hidden or title_hidden or metadata_incomplete:
        reasons.append("identity_or_metadata_incomplete")
    if not any(metadata.get(k) is not None for k in DATE_FIELDS):
        reasons.append("source_dates_missing")
    nature = value.get("nature", value.get("kind", value.get("type")))
    if nature not in (None, "primary_text", "search_result", "tool_summary", "summary"):
        reasons.append("unknown_document_nature")
    is_search = bool(value.get("_search_container")) or operation in (
        "search",
        "search_articles",
        "search_case_law",
    )
    if (
        forced_summary
        or isinstance(value.get("summary"), str)
        and bool(value["summary"].strip())
        or isinstance(value.get("tool_summary"), str)
        and bool(value["tool_summary"].strip())
        or nature in ("tool_summary", "summary")
    ):
        nature = "tool_summary"
    elif is_search or nature == "search_result":
        nature = "search_result"
    else:
        nature = "primary_text"
    text, text_incomplete = _safe_string(
        value.get("text", value.get("excerpt")), MAX_EXCERPT_CHARS
    )
    if nature == "primary_text" and not isinstance(value.get("text"), str):
        reasons.append("excerpt_without_full_primary_text")
    if not text or not text.strip():
        reasons.append(
            "primary_text_missing"
            if nature == "primary_text"
            else "source_text_missing"
        )
    if text is not None:
        # Un lien incorporé sensible/étranger fait omettre tout le champ.
        if any(
            _official_url(m.group().rstrip(".,;:)")) is None
            for m in URL_TEXT.finditer(text)
        ):
            text = None
            text_incomplete = True
    document_truncated, _ = _flags(value)
    if forced_incomplete or document_truncated or text_incomplete:
        reasons.append("document_incomplete")
    if metadata.get("applicable_at_as_of_date") is False:
        reasons.append("source_declared_not_applicable")
    status = "available" if not reasons else "incomplete"
    if url is None:
        status = "missing"
        text = None
        identity = title = None
        metadata = {"content_trust": TRUST}
    result = {
        "nature": nature,
        "status": status,
        "url": url,
        "metadata": metadata,
        "content_trust": TRUST,
        "complete": not reasons,
        "primary_text_available": nature == "primary_text" and bool(text),
        "primary_text_verified": nature == "primary_text" and not reasons,
        "legal_currentness_verified": None,
        "reasons": reasons,
    }
    if identity:
        result["id"] = identity
    if title:
        result["title"] = title
    if text:
        result["excerpt"] = text
    result["sha256"] = sha(canonical(result))
    return result


def _source_evidence(
    output: Any,
    call: dict[str, Any],
    result: dict[str, Any],
    requirements: dict[str, Any],
    linked: bool,
) -> dict[str, Any]:
    operation = _operation(call.get("tool"))
    web = call.get("tool") in ("WebFetch", "web.run", "web__run", "mcp__web__run")
    source = {
        "type": "derived_source_evidence",
        "call_id": result.get("call_id"),
        "call_event_id": call.get("event_id"),
        "result_event_id": result["event_id"],
        "tool": call.get("tool"),
        "native_call_id_verified": linked,
        "retrieved_at": result.get("timestamp"),
        "content_trust": TRUST,
        "status": "missing",
        "documents": [],
        "primary_text_verified": False,
        "legal_currentness_verified": None,
        "raw_output_omitted": True,
    }
    if not linked:
        source["reason"] = "unlinked_or_duplicate_result"
        return source
    if result["failure_observation"]["native_failure_observed"]:
        source["reason"] = "native_tool_failure"
        return source
    if source["retrieved_at"] is None:
        source["reason"] = "native_result_timestamp_missing_or_invalid"
        return source
    if not operation and not web:
        source["reason"] = "unsupported_or_unresolved_wrapper_transport"
        return source
    if (operation and requirements.get("mcp_mode") == "disabled") or (
        web and requirements.get("web_mode") != "official_source"
    ):
        source["reason"] = "source_mode_disallows_tool"
        return source
    docs, reason = _decode_documents(output)
    if reason:
        source["reason"] = reason
        return source
    truncated, summary = _flags(_parse_json(output))
    if web and call.get("tool") == "WebFetch":
        summary = True
    documents = []
    over_limit = len(docs) > MAX_DOCUMENTS
    for candidate in docs[:MAX_DOCUMENTS]:
        doc = _document(candidate, operation, truncated or over_limit, summary)
        if len(canonical(documents + [doc])) > MAX_TOTAL_CHARS:
            over_limit = True
            break
        documents.append(doc)
    if over_limit:
        for doc in documents:
            doc.update(status="incomplete", complete=False, primary_text_verified=False)
            doc["reasons"].append("aggregate_document_limit")
            doc.pop("sha256", None)
            doc["sha256"] = sha(canonical(doc))
    source["documents"] = documents
    source["primary_text_verified"] = any(
        doc["primary_text_verified"] for doc in documents
    )
    source["status"] = (
        "available"
        if documents and all(d["status"] == "available" for d in documents)
        else "incomplete"
        if documents
        else "missing"
    )
    if source["status"] != "available":
        source["primary_text_verified"] = False
    source["truncated"] = truncated or over_limit
    source["sanitized_documents_sha256"] = sha(canonical(documents))
    if not documents:
        source["reason"] = "no_public_source_data"
    return source


def _installed_skills(cache: Path, files: dict[str, str]) -> dict[str, dict[str, Any]]:
    installed = {}
    resolved = cache.resolve()
    for relative, digest in files.items():
        if not relative.endswith("/SKILL.md"):
            continue
        path = (resolved / relative).resolve()
        if not path.is_relative_to(resolved):
            raise EvidenceError("Chemin SKILL hors de la copie installée")
        try:
            raw = path.read_bytes()
            body = raw.decode("utf-8")
        except (OSError, UnicodeError) as error:
            raise EvidenceError("SKILL installé absent ou non UTF-8") from error
        if sha(raw) != digest:
            raise EvidenceError("Empreinte du SKILL installé divergente")
        names = (
            re.findall(r"^name:\s*([^\r\n]+)$", body, re.M)
            if body.startswith("---")
            else []
        )
        name = names[0].strip().strip("\"'") if len(names) == 1 else path.parent.name
        installed[path.as_posix().casefold()] = {
            "relative": relative,
            "sha256": digest,
            "body": body,
            "name": name,
        }
    return installed


def normalize(
    raw: bytes,
    prompt: str,
    thread_id: str,
    cache: Path,
    files: dict[str, str],
    source_requirements: dict[str, Any],
    expected_skills: list[str] | None = None,
) -> dict[str, Any]:
    """Projette les événements natifs sans jugement métier ni écriture.

    ``source_requirements`` reprend les trois modes historiques. Un résultat
    MCP direct doit contenir un document structuré (id/titre, url, text,
    metadata) ou son enveloppe MCP content/structuredContent. Les retours
    d'enveloppes exec sont observés, jamais interprétés comme appels internes.
    ``expected_skills`` sert à comparer l'ensemble observé ; il n'injecte rien.
    """
    if _identifier(thread_id) is None:
        raise EvidenceError("Identité du thread invalide")
    installed = _installed_skills(cache, files)
    events: list[dict[str, Any]] = []
    omitted: list[dict[str, Any]] = []
    issues: list[str] = []
    calls: dict[str, dict[str, Any]] = {}
    results: set[str] = set()
    conflicted_calls: set[str] = set()
    item_ids: dict[tuple[str, str], str] = {}
    prompt_count = session_count = 0
    context_count = 0
    for number, line in enumerate(raw.splitlines(), 1):
        try:
            record = json.loads(line)
        except (ValueError, UnicodeError) as error:
            raise EvidenceError(f"JSONL natif invalide ligne {number}") from error
        if not isinstance(record, dict) or not isinstance(
            record.get("payload", {}), dict
        ):
            raise EvidenceError(f"Enveloppe native invalide ligne {number}")
        payload = record.get("payload", {})
        native = {
            "event_id": f"native-L{number:06d}",
            "native_line": number,
            "native_line_sha256": sha(line),
            "timestamp": _timestamp(record.get("timestamp")),
        }
        kind = record.get("type")
        ptype = payload.get("type")
        identifier = _identifier(payload.get("id"))
        if kind == "response_item" and identifier:
            key = (str(ptype), identifier)
            digest = sha(canonical(payload))
            if key in item_ids and item_ids[key] == digest:
                omitted.append(
                    {**native, "reason": "duplicate_view_of_same_native_item"}
                )
                continue
            if key in item_ids:
                issues.append("conflicting_native_item_id")
            item_ids[key] = digest
        event: dict[str, Any] | None = None
        if kind == "session_meta":
            session_count += 1
            if payload.get("id") != thread_id:
                raise EvidenceError("Identité native différente du thread attendu")
            event = {
                **native,
                "type": "derived_session_identity",
                "thread_id": thread_id,
                "cli_version": _safe_string(payload.get("cli_version"), 100)[0],
                "source": _safe_string(payload.get("source"), 100)[0],
            }
        elif kind == "turn_context":
            context_count += 1
            sandbox = payload.get("sandbox_policy", {})
            sandbox_type = (
                _safe_string(sandbox.get("type"), 100)[0]
                if isinstance(sandbox, dict)
                else None
            )
            event = {
                **native,
                "type": "derived_execution_parameters",
                "model": _safe_string(payload.get("model"), 100)[0],
                "approval_policy": _safe_string(payload.get("approval_policy"), 100)[0],
                "sandbox_type": sandbox_type,
            }
            if event["approval_policy"] != "never" or sandbox_type != "read-only":
                issues.append("native_permissions_not_read_only_never")
        elif kind == "response_item" and ptype == "message":
            content = payload.get("content", [])
            if not isinstance(content, list):
                raise EvidenceError("Contenu de message natif inconnu")
            text = "\n".join(
                c.get("text", "")
                for c in content
                if isinstance(c, dict)
                and c.get("type") in ("input_text", "output_text", "text")
                and isinstance(c.get("text"), str)
            )
            role = payload.get("role")
            if (
                role == "assistant"
                and payload.get("channel") not in ("analysis", "reasoning")
                and text.strip()
            ):
                clean, hidden = sanitize(text, cache)
                if hidden:
                    issues.append("visible_text_redacted_or_truncated")
                event = {
                    **native,
                    "type": "derived_visible_assistant_text",
                    "phase": _safe_string(payload.get("phase"), 100)[0],
                    "channel": _safe_string(payload.get("channel"), 100)[0],
                    "text": clean,
                    "complete": not hidden,
                    "starts_STOP": starts_stop(clean) if not hidden else None,
                }
            elif role == "user" and text == prompt:
                prompt_count += 1
                event = {
                    **native,
                    "type": "derived_submitted_prompt",
                    "prompt_sha256": sha(prompt.encode("utf-8")),
                }
            elif role == "user" and "<skill>" in text:
                wrappers = re.findall(r"<skill>.*?</skill>", text, re.S)
                if not wrappers or text.count("<skill>") != len(wrappers):
                    issues.append("malformed_skill_wrapper")
                for index, wrapper in enumerate(wrappers, 1):
                    names = re.findall(r"<name>(.*?)</name>", wrapper, re.S)
                    paths = re.findall(r"<path>(.*?)</path>", wrapper, re.S)
                    match = None
                    if len(paths) == 1:
                        try:
                            match = installed.get(
                                Path(paths[0]).resolve().as_posix().casefold()
                            )
                        except (ValueError, OSError):
                            pass
                    supplied = names[0] if len(names) == 1 else None
                    full = bool(
                        match
                        and supplied
                        in (match["name"], "collectivite-territoriale:" + match["name"])
                        and match["body"] in wrapper
                    )
                    metadata = record.get("metadata", {})
                    client_authored = (
                        metadata.get("client_authored")
                        if isinstance(metadata, dict)
                        else None
                    )
                    host_authored = (
                        False
                        if client_authored is True
                        else True
                        if client_authored is False
                        else None
                    )
                    if not full:
                        issues.append("skill_injection_partial_foreign_or_unbound")
                    skill = {
                        **native,
                        "event_id": native["event_id"] + f"-skill{index}",
                        "type": "derived_native_skill_injection",
                        "name": _safe_string(supplied, 200)[0],
                        "skill_name": match["name"] if full else None,
                        "path_relative_to_installed_plugin": match["relative"]
                        if match
                        else None,
                        "installed_file_sha256": match["sha256"] if match else None,
                        "full_installed_text_present": full,
                        "native_host_authorship_verified": host_authored,
                        "host_native_activation_verified": full
                        and host_authored is not False,
                        "requires_sealed_native_transport": True,
                        "native_text_block": index,
                        "skill_body_omitted": True,
                    }
                    events.append(skill)
                continue
            elif (
                role == "user" and prompt_count and "<environment_context>" not in text
            ):
                issues.append("unexpected_user_input_after_submitted_prompt")
        elif kind == "response_item" and ptype in ("function_call", "custom_tool_call"):
            call_id = _identifier(payload.get("call_id"))
            tool = _tool(payload.get("name"))
            argument_value = payload.get("input", payload.get("arguments", ""))
            arguments = (
                argument_value
                if isinstance(argument_value, str)
                else json.dumps(argument_value, ensure_ascii=False)
            )
            inventory = "ALL_TOOLS" in arguments or "list_tools" in arguments
            clean, hidden = _safe_string(arguments, MAX_ARGUMENT_CHARS)
            if clean is not None:
                clean = clean.replace(str(cache), "$INSTALLED_PLUGIN").replace(
                    cache.as_posix(), "$INSTALLED_PLUGIN"
                )
            if not call_id or call_id in calls:
                issues.append("missing_or_duplicate_call_id")
                if call_id:
                    conflicted_calls.add(call_id)
            if tool is None:
                issues.append("invalid_native_tool_name")
            if hidden and not inventory:
                issues.append("tool_arguments_redacted_or_truncated")
            event = {
                **native,
                "type": "derived_native_tool_call",
                "call_id": call_id,
                "tool": tool,
                "arguments": clean if not inventory else None,
                "arguments_complete": not hidden and not inventory,
                "tool_inventory_request": inventory,
                "native_payload_type": ptype,
            }
            if call_id and call_id not in calls:
                calls[call_id] = event
        elif kind == "response_item" and ptype in (
            "function_call_output",
            "custom_tool_call_output",
        ):
            call_id = _identifier(payload.get("call_id"))
            call = calls.get(call_id or "", {})
            linked = bool(
                call_id
                and call
                and call_id not in results
                and call_id not in conflicted_calls
            )
            if not linked:
                issues.append("unlinked_or_duplicate_tool_result")
            if call_id:
                results.add(call_id)
            output = payload.get("output")
            truncated, summary = _flags(_parse_json(output))
            failure = failure_metadata(output)
            event = {
                **native,
                "type": "derived_native_tool_result",
                "call_id": call_id,
                "call_event_id": call.get("event_id") if linked else None,
                "native_call_id_verified": linked,
                "raw_output_omitted": True,
                "blocked_by_policy": failure["blocked_by_policy"],
                "failure_observation": failure,
                "truncation_observed": truncated,
                "summary_indicator_observed": summary,
                "primary_text_verified": False,
                "successful_skill_read_verified": None,
                "tool_inventory_output_omitted": bool(
                    call.get("tool_inventory_request")
                ),
            }
            if failure["native_failure_observed"]:
                issues.append("native_tool_failure")
            if (
                linked
                and not failure["native_failure_observed"]
                and not truncated
                and not summary
                and not event["tool_inventory_output_omitted"]
            ):
                received = "\n".join(_text_parts(output))
                matched = [
                    {
                        "path_relative_to_installed_plugin": skill["relative"],
                        "sha256": skill["sha256"],
                    }
                    for skill in installed.values()
                    if skill["body"] in received
                ]
                if matched:
                    event["successful_skill_read_verified"] = True
                    event["full_installed_skill_texts_received"] = matched
            events.append(event)
            if failure["native_failure_observed"]:
                events.append(
                    {
                        **native,
                        "event_id": native["event_id"] + "-failure",
                        "type": "derived_native_process_failure"
                        if "process_start_failed" in failure["failure_codes"]
                        else "derived_native_tool_failure",
                        "call_id": call_id,
                        "call_event_id": event["call_event_id"],
                        "result_event_id": event["event_id"],
                        **failure,
                    }
                )
            if not event["tool_inventory_output_omitted"]:
                source_relevant = bool(_operation(call.get("tool"))) or call.get(
                    "tool"
                ) in ("WebFetch", "web.run", "web__run", "mcp__web__run")
                wrapper = call.get("tool") in (
                    "exec",
                    "functions.exec",
                    "functions__exec",
                )
                if source_relevant or wrapper:
                    source = _source_evidence(
                        output, call, event, source_requirements, linked
                    )
                    source.update(
                        {**native, "event_id": native["event_id"] + "-source"}
                    )
                    events.append(source)
                    event["primary_text_verified"] = source["primary_text_verified"]
                    if source.get("reason") == "source_mode_disallows_tool":
                        issues.append("source_tool_disallowed_by_case")
                    if wrapper:
                        event["wrapper_internal_call_identity_verified"] = False
            continue
        if event is None:
            omitted.append(
                {
                    **native,
                    "reason": "private_context_reasoning_status_or_unknown_record",
                }
            )
        else:
            events.append(event)
    if session_count != 1 or prompt_count != 1:
        raise EvidenceError("Session ou prompt natif absent/dupliqué")
    if not context_count:
        issues.append("native_execution_parameters_missing")
    for call_id in calls.keys() - results:
        issues.append("tool_call_without_result:" + call_id)
    # Un doublon tardif invalide également la première projection documentaire.
    bad_ids = conflicted_calls | {
        e["call_id"]
        for e in events
        if e["type"] == "derived_native_tool_result"
        and not e["native_call_id_verified"]
        and e.get("call_id")
    }
    for event in events:
        if (
            event["type"] == "derived_source_evidence"
            and event.get("call_id") in bad_ids
        ):
            event.update(
                native_call_id_verified=False,
                primary_text_verified=False,
                status="missing",
                reason="ambiguous_native_call_identity",
                documents=[],
            )
            event["sanitized_documents_sha256"] = sha(canonical([]))
        elif (
            event["type"] == "derived_native_tool_result"
            and event.get("call_id") in bad_ids
        ):
            event.update(
                native_call_id_verified=False,
                primary_text_verified=False,
                successful_skill_read_verified=None,
            )
            event.pop("full_installed_skill_texts_received", None)
    visible = [e for e in events if e["type"] == "derived_visible_assistant_text"]
    sources = [e for e in events if e["type"] == "derived_source_evidence"]
    primary = [e["event_id"] for e in sources if e["primary_text_verified"]]
    activations = [
        e
        for e in events
        if e["type"] == "derived_native_skill_injection"
        and e["host_native_activation_verified"]
    ]
    observed_skills = [e["skill_name"] for e in activations]
    return {
        "schema_version": "dev7-native-complete-derived-v1",
        "thread_id": thread_id,
        "native_file_sha256": sha(raw),
        "native_line_count": len(raw.splitlines()),
        "events": events,
        "omitted_records": omitted,
        "technical_issues": sorted(set(issues)),
        "first_visible_event_id": visible[0]["event_id"] if visible else None,
        "first_visible_starts_STOP": visible[0]["starts_STOP"] if visible else None,
        "visible_text_complete": bool(visible) and all(e["complete"] for e in visible),
        "source_requirements": copy.deepcopy(source_requirements),
        "source_primary_verified": bool(primary),
        "primary_source_event_ids": primary,
        "legal_currentness_verified": None,
        "documentary_control": {
            "source_event_count": len(sources),
            "primary_source_event_ids": primary,
            "status": "not_required"
            if source_requirements.get("source_evidence_policy") == "not_required"
            else "available"
            if primary
            else "missing",
        },
        "activation_summary": {
            "observed_skill_names_in_order": observed_skills,
            "expected_skill_names": copy.deepcopy(expected_skills),
            "strict_expected_set_verified": None
            if expected_skills is None
            else set(observed_skills) == set(expected_skills)
            and len(observed_skills) == len(set(observed_skills)),
            "native_activation_event_ids": [e["event_id"] for e in activations],
        },
        "effective_mcp_exposure_verified": None,
        "global_discovery_verified": None,
        "historical_scores_reused": False,
        "release_ready": False,
    }


def judge_packet(
    case: dict[str, Any],
    trace: dict[str, Any],
    rubric: str,
    hostaddendum: str,
    transport_provenance_verified: bool = False,
) -> dict[str, Any]:
    """Lie le cas et la trace sans modifier les atomes ni produire de jugement."""
    identifier = case.get("case_id", case.get("id"))
    question = case.get("historical_question", case.get("prompt"))
    atoms = case.get("judge_only_invariant_objects", case.get("invariant_objects"))
    oracle = case.get("judge_only_oracle")
    if oracle is None:
        oracle = {
            k: case[k]
            for k in ("skills", "activation_sequence", "activation_sequence_semantics")
        }
    requirements = case.get("source_requirements_unchanged")
    if requirements is None:
        requirements = {
            k: case[k] for k in ("mcp_mode", "web_mode", "source_evidence_policy")
        }
    if (
        not isinstance(identifier, str)
        or not isinstance(question, str)
        or not isinstance(atoms, list)
    ):
        raise EvidenceError("Cas juge incomplet")
    atom_ids = [a.get("id") for a in atoms if isinstance(a, dict)]
    if (
        len(atom_ids) != len(atoms)
        or len(set(atom_ids)) != len(atoms)
        or None in atom_ids
    ):
        raise EvidenceError("Atomes absents ou dupliqués")
    prompts = [
        e
        for e in trace.get("events", [])
        if e.get("type") == "derived_submitted_prompt"
    ]
    declared_prompt = case.get("prompt_sha256_utf8")
    if len(prompts) != 1 or prompts[0].get("prompt_sha256") != (
        declared_prompt or sha(question.encode("utf-8"))
    ):
        raise EvidenceError("Prompt du cas non lié à la trace")
    if trace.get("source_requirements") != requirements:
        raise EvidenceError("Modes documentaires de la trace divergents du cas")
    return {
        "schema_version": "dev7-native-complete-judge-packet-v1",
        "case_id": identifier,
        "question": question,
        "oracle": copy.deepcopy(oracle),
        "atoms": copy.deepcopy(atoms),
        "source_requirements": copy.deepcopy(requirements),
        "original_rubric": rubric,
        "host_addendum": hostaddendum,
        "trace_sha256": sha(canonical(trace)),
        "trace": copy.deepcopy(trace),
        "technical_control": {
            "issues": list(trace["technical_issues"]),
            "sealed_native_transport_verified": transport_provenance_verified is True,
            "source_primary_verified": trace["source_primary_verified"],
            "documentary_control": copy.deepcopy(trace["documentary_control"]),
        },
        "historical_scores_reused": False,
        "release_ready": False,
    }


def validate_judgment(
    packet: dict[str, Any], judgment: dict[str, Any]
) -> dict[str, Any]:
    """Vérifie la structure et les liaisons, sans substituer une revue métier.

    Un jugement cohérent peut conclure à l'échec ou au blocage. La validation
    ne démontre ni l'indépendance du juge ni une revue humaine ou juridique.
    """
    if not isinstance(judgment, dict) or set(judgment) != {
        "case_id",
        "trace_sha256",
        "verdict",
        "invariants",
    }:
        raise EvidenceError("Clés du jugement différentes du contrat")
    trace = packet.get("trace")
    if not isinstance(trace, dict) or packet.get("trace_sha256") != sha(
        canonical(trace)
    ):
        raise EvidenceError("Empreinte du paquet de trace divergente")
    if judgment["trace_sha256"] != packet["trace_sha256"] or judgment[
        "case_id"
    ] != packet.get("case_id"):
        raise EvidenceError("Jugement non lié au cas et à sa trace")
    if judgment["verdict"] not in ("reussite", "echec", "bloque"):
        raise EvidenceError("Verdict inconnu")
    atoms = {atom["id"]: atom for atom in packet["atoms"]}
    if len(atoms) != len(packet["atoms"]):
        raise EvidenceError("Atomes du paquet dupliqués")
    values = judgment["invariants"]
    if not isinstance(values, dict) or set(values) != set(atoms):
        raise EvidenceError("Le jugement ne contient pas exactement les atomes")
    events = {e["event_id"]: e for e in trace["events"]}
    if len(events) != len(trace["events"]):
        raise EvidenceError("Identités d'événements dupliquées")

    def usable_primary(event: dict[str, Any]) -> bool:
        if (
            event.get("type") != "derived_source_evidence"
            or event.get("native_call_id_verified") is not True
            or event.get("primary_text_verified") is not True
            or event.get("status") != "available"
        ):
            return False
        call = events.get(event.get("call_event_id"), {})
        result = events.get(event.get("result_event_id"), {})
        if (
            call.get("type") != "derived_native_tool_call"
            or result.get("type") != "derived_native_tool_result"
            or result.get("native_call_id_verified") is not True
            or call.get("call_id") != result.get("call_id")
            or event.get("call_id") != result.get("call_id")
            or type(call.get("native_line")) is not int
            or type(result.get("native_line")) is not int
            or call["native_line"] >= result["native_line"]
            or event.get("native_line") != result["native_line"]
            or event.get("native_line_sha256") != result.get("native_line_sha256")
        ):
            return False
        return any(
            doc.get("nature") == "primary_text"
            and doc.get("status") == "available"
            and doc.get("complete") is True
            and doc.get("primary_text_verified") is True
            and isinstance(doc.get("excerpt"), str)
            and bool(doc["excerpt"].strip())
            and doc.get("metadata", {}).get("applicable_at_as_of_date") is not False
            for doc in event.get("documents", [])
        )

    statuses: list[bool | None] = []
    stop_violation = False
    for atom_id, value in values.items():
        if not isinstance(value, dict) or set(value) != {
            "status",
            "basis",
            "evidence_refs",
            "rationale",
        }:
            raise EvidenceError("Champs d'un atome jugé différents du contrat")
        status = value["status"]
        if status is not None and type(status) is not bool:
            raise EvidenceError("Status exige un booléen strict ou null")
        basis = value["basis"]
        if basis not in ("observation", "retrieval", "abstention", "missing"):
            raise EvidenceError("Base de preuve inconnue")
        refs = value["evidence_refs"]
        if (
            not isinstance(refs, list)
            or not all(isinstance(ref, str) and ref in events for ref in refs)
            or len(set(refs)) != len(refs)
        ):
            raise EvidenceError("Références absentes, inventées ou dupliquées")
        rationale, hidden = _safe_string(value["rationale"], 16_384)
        if not rationale or not rationale.strip() or hidden:
            raise EvidenceError("Justification vide, sensible ou incomplète")
        if status is not None and not refs:
            raise EvidenceError(
                "Un booléen exige une preuve ou contradiction référencée"
            )
        if basis == "missing" and status is not None:
            raise EvidenceError("Une preuve manquante ne produit aucun booléen")
        atom = atoms[atom_id]
        if basis == "abstention":
            if atom.get("accepts_abstention") is not True:
                raise EvidenceError("Abstention interdite par cet atome")
            if not any(
                events[ref].get("type") == "derived_visible_assistant_text"
                and events[ref].get("complete") is True
                for ref in refs
            ):
                raise EvidenceError("Abstention sans texte visible complet référencé")
        if (
            basis == "retrieval"
            and status is True
            and not any(usable_primary(events[ref]) for ref in refs)
        ):
            raise EvidenceError("Retrieval sans primaire utilisable réellement lié")
        if (
            atom.get("category") == "preuve_source"
            and status is True
            and basis not in ("retrieval", "abstention")
        ):
            raise EvidenceError(
                "Un atome documentaire vrai exige retrieval ou abstention autorisée"
            )
        if atom_id.endswith(".stop_premier"):
            if status is True and (
                trace.get("first_visible_starts_STOP") is not True
                or trace.get("first_visible_event_id") not in refs
            ):
                raise EvidenceError(
                    "STOP vrai sans premier texte visible STOP référencé"
                )
            stop_violation = (
                stop_violation or trace.get("first_visible_starts_STOP") is False
            )
        statuses.append(status)
    primary_ids = [e["event_id"] for e in trace["events"] if usable_primary(e)]
    nominal_primary_missing = (
        packet["source_requirements"].get("source_evidence_policy") != "not_required"
        and not primary_ids
    )
    technical_failure = bool(trace.get("technical_issues")) or bool(
        packet.get("technical_control", {}).get("issues")
    )
    if (
        technical_failure
        or stop_violation
        or any(status is False for status in statuses)
    ):
        computed = "echec"
    elif (
        any(status is None for status in statuses)
        or nominal_primary_missing
        or packet.get("technical_control", {}).get("sealed_native_transport_verified")
        is not True
        or trace.get("visible_text_complete") is not True
    ):
        computed = "bloque"
    else:
        computed = "reussite"
    if judgment["verdict"] != computed:
        raise EvidenceError(
            "Verdict incompatible avec les contrôles et statuts atomiques"
        )
    return {
        "case_id": packet["case_id"],
        "trace_sha256": packet["trace_sha256"],
        "structure_and_evidence_links_valid": True,
        "verdict": computed,
        "atom_count": len(atoms),
        "technical_failure_observed": technical_failure,
        "usable_primary_event_ids": primary_ids,
        "nominal_primary_missing": nominal_primary_missing,
        "human_review_attested": False,
        "legal_review_attested": False,
        "historical_scores_reused": False,
        "release_ready": False,
    }
