"""Contrôles et empreintes de campagne ; aucune action à l'import."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib
from typing import Any

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Collectivite-corrections-pr5"
STATE = ROOT / "smoke-dev6-isole-20261007-211629-4dc9cd90/codex-state"
DEV6 = STATE / "plugins/cache/smoke-dev6/collectivite-territoriale/1.2.0-dev.6"
PROPOSAL = ROOT / "proposition-protocole-campagne-dev7-20261008.json"
COMMIT = "fb186b4951b95adabf05904f8a34995720588be3"
TREE = "367440f629417bd33b6a52a0f4af261bae4a971f"
CLI_SHA = "3553cd6e7df5a093d8cb8301cd8088a57e0971aba71ddbe0e67f7f44a15cdf68"
ALLOWED = frozenset({"plugin-mcp-indisponible", "plugin-dsi-technique", "plugin-dsi-source-indisponible"})
MARKET = "campagne-dev7-20261008-r3"
PLUGIN_ID = "collectivite-territoriale@" + MARKET
MODULES = ("campagne_native_dev7_20261008.py", "socle_campagne_native_dev7_20261008.py",
           "tests_campagne_native_dev7_20261008.py", "extraire_campagne_native_dev7_20261008.py",
           "tests_extraire_campagne_native_dev7_20261008.py")


class GateError(ValueError):
    """Un précontrôle interdit l'action ; aucune réparation implicite."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def write_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def root_path(path: Path) -> Path:
    resolved = path.resolve()
    require(resolved.is_relative_to(ROOT), "Chemin hors de la racine autorisée")
    require(resolved != ROOT and not resolved.is_relative_to(STATE), "Destination protégée")
    return resolved


def environment(source: dict[str, str] | None = None) -> tuple[dict[str, str], list[str]]:
    """Ne conserve ni identités parentes CODEX ni secrets hérités ; ne lit aucun auth."""
    source = dict(os.environ) if source is None else source
    removed = sorted(k for k in source if k.upper().startswith("CODEX"))
    env = {k: v for k, v in source.items() if not k.upper().startswith("CODEX")
           and not re.search(r"TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|AUTHORIZATION", k, re.I)}
    env.update(CODEX_HOME=str(STATE), CODEX_SQLITE_HOME=str(STATE))
    return env, removed


def inventory(folder: Path) -> dict[str, str]:
    require(folder.is_dir(), "Répertoire installé absent")
    return {p.relative_to(folder).as_posix(): sha(p.read_bytes()) for p in folder.rglob("*") if p.is_file()}


def validate_receipts(folder: Path, dev6_skill_sha: str) -> dict[str, str]:
    """Le booléen déclaré ne suffit pas : contrôle du reçu brut et du setup associé."""
    folder = root_path(folder)
    setup = read(folder / "setup-result.json")
    require(setup.get("success") is True and setup.get("cache_unchanged") is True,
            "Setup Windows non réussi ou cache altéré")
    require(setup.get("persisted_windows_sandbox") == "elevated"
            and setup.get("persisted_sandbox_mode") == "read-only"
            and setup.get("persisted_web_search") == "disabled", "Permissions du setup non conformes")
    lecture = read(folder / "lecture-result.json")
    result = lecture.get("response", {}).get("result", {})
    require(lecture.get("success") is True and result.get("exitCode") == 0,
            "Lecture synthétique non réussie")
    lines = [line.strip() for line in result.get("stdout", "").splitlines() if line.strip()]
    require("LECTURE_SANDBOX_ISOLE_20261008" in lines, "Contenu synthétique exact absent")
    require(dev6_skill_sha.lower() in [line.lower() for line in lines]
            and lecture.get("expected_skill_sha256") == dev6_skill_sha, "SHA reçu différent du skill dev.6")
    require(lecture.get("model_inference") is False and lecture.get("auth_secrets_read") is False,
            "Sonde de lecture hors périmètre")
    require(lecture.get("request", {}).get("sandboxPolicy", {}).get("type") == "readOnly",
            "Sonde non faite en lecture seule")
    return {name: sha((folder / name).read_bytes())
            for name in ("inspection.json", "setup-result.json", "lecture-result.json")}


def validate_config() -> str:
    raw = (STATE / "config.toml").read_bytes()
    value = tomllib.loads(raw.decode("utf-8"))
    require(value.get("windows", {}).get("sandbox") == "elevated", "Backend Windows non configuré")
    require(value.get("sandbox_mode") == "read-only" and value.get("web_search") == "disabled",
            "Configuration sandbox/Web non conforme")
    return sha(raw)


def overrides() -> list[str]:
    """Syntaxe TOML des overrides CLI ; aucun enable/remove de plugin inventé."""
    values = ['windows.sandbox="elevated"', 'sandbox_mode="read-only"', 'approval_policy="never"',
              'web_search="disabled"', 'plugins.collectivite-territoriale@smoke-dev6.enabled=false',
              'plugins.collectivite-territoriale@campagne-dev7-20261008.enabled=false',
              f'plugins.{PLUGIN_ID}.enabled=true',
              'plugins.collectivite-territoriale@smoke-dev6.mcp_servers.droit-francais.enabled=false',
              'plugins.collectivite-territoriale@campagne-dev7-20261008.mcp_servers.droit-francais.enabled=false',
              f'plugins.{PLUGIN_ID}.mcp_servers.droit-francais.enabled=false']
    return [part for value in values for part in ("-c", value)]


def source_blobs(proposal: dict[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    require(proposal.get("candidate_commit") == COMMIT and proposal.get("candidate_tree") == TREE,
            "Source proposée différente du candidat autorisé")
    for kind in ("candidate_gel", "suite", "rubric"):
        path = Path(proposal[kind + "_path"])
        require(sha(path.read_bytes()) == proposal[kind + "_sha256"], "Entrée source modifiée : " + kind)
    frozen = read(Path(proposal["candidate_gel_path"]))
    require(frozen["candidate_commit"] == COMMIT and frozen["candidate_tree"] == TREE,
            "Identité du gel incorrecte")
    require(len(frozen["files"]) == 213 and sum(p.startswith("skills/") for p in frozen["files"]) == 166,
            "Inventaire gelé incorrect")
    git = ["git", "-c", "core.longpaths=true", "-c", "safe.directory=" + SOURCE.as_posix()]
    tree = subprocess.check_output([*git, "rev-parse", COMMIT + "^{tree}"], cwd=SOURCE, timeout=20).decode().strip()
    require(tree == TREE, "Arbre Git différent du gel")
    listing = subprocess.check_output([*git, "ls-tree", "-r", "-z", COMMIT], cwd=SOURCE, timeout=20)
    wanted = set(frozen["files"]) | {"assets/icon.png"}
    entries: dict[str, bytes] = {}
    for row in listing.split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        fields = meta.split()
        decoded = name.decode("utf-8")
        if decoded in wanted:
            require(fields[1] == b"blob" and fields[0] != b"120000", "Blob source non régulier")
            entries[decoded] = fields[2]
    require(set(entries) == wanted, "Blob gelé absent du commit autorisé")
    response = subprocess.check_output([*git, "cat-file", "--batch"], cwd=SOURCE,
                                      input=b"\n".join(entries.values()) + b"\n", timeout=30)
    blobs: dict[str, bytes] = {}
    offset = 0
    for name, oid in entries.items():
        end = response.find(b"\n", offset)
        fields = response[offset:end].split()
        require(len(fields) == 3 and fields[0] == oid and fields[1] == b"blob", "Réponse Git invalide")
        size = int(fields[2])
        blobs[name] = response[end + 1:end + 1 + size]
        offset = end + size + 2
        require(response[offset - 1:offset] == b"\n", "Blob Git tronqué")
    require(offset == len(response), "Réponse Git surnuméraire")
    for name, digest in frozen["files"].items():
        require(sha(blobs[name]) == digest, "Source Git divergente : " + name)
    return blobs, frozen


def validate_cases(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    suite = read(Path(proposal["suite_path"]))
    historical = suite["cases"] if isinstance(suite, dict) else suite
    by_id = {c["id"]: c for c in historical}
    cases = proposal["cases"]
    require(len(cases) == len(by_id) == 16 and sum(len(c["judge_only_invariant_objects"]) for c in cases) == 124,
            "Suite 16/124 incorrecte")
    require({c["case_id"] for c in cases} == set(by_id), "Identifiants de cas divergents")
    for case in cases:
        original = by_id[case["case_id"]]
        require(case["historical_question"] == original["prompt"]
                and case["judge_only_invariant_objects"] == original["invariant_objects"], "Question/atomes modifiés")
        require(case["judge_only_oracle"] == {k: original[k] for k in ("skills", "activation_sequence", "activation_sequence_semantics")},
                "Oracle modifié")
        require(case["source_requirements_unchanged"] == {k: original[k] for k in ("mcp_mode", "web_mode", "source_evidence_policy")},
                "Exigences documentaires modifiées")
        canonical = json.dumps(original, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        require(sha(canonical) == case["original_case_canonical_sha256"], "Cas original divergent")
        require(sha(case["native_prompt"].encode("utf-8")) == case["prompt_sha256_utf8"], "Prompt divergent")
        if case["activation_mode"] == "spontaneous":
            require("$collectivite-territoriale:" not in case["native_prompt"]
                    and all(name not in case["native_prompt"] for name in original["skills"]), "Oracle dans prompt spontané")
        else:
            markers = " ".join("$collectivite-territoriale:" + name for name in original["activation_sequence"])
            require(case["native_prompt"].startswith(markers + "\n" + original["prompt"]), "Marqueurs forcés divergents")
        require(case["attempt_limit"] == 1 and case["timeout_seconds"] == 240, "Limites modifiées")
        require((case["case_id"] in ALLOWED) == (case["source_requirements_unchanged"]["mcp_mode"] == "disabled"),
                "Périmètre MCP divergent")
    return cases
