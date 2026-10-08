"""Réexport postexécution borné : comparaison brute et erreurs natives typées."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import extraire_campagne_native_dev7_20261008 as original
from verifier_paquets_dev7_r3_20261008 import verify

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "qualification-coactivation-dev7-cli-r3"
CASES = ("plugin-mcp-indisponible", "plugin-dsi-technique", "plugin-dsi-source-indisponible")
FROZEN = ("campagne_native_dev7_20261008.py", "socle_campagne_native_dev7_20261008.py",
          "tests_campagne_native_dev7_20261008.py", "extraire_campagne_native_dev7_20261008.py",
          "tests_extraire_campagne_native_dev7_20261008.py")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def final_text(records: list[dict]) -> str:
    """Récupère la finale native, sans utiliser le texte déjà expurgé."""
    candidates = []
    for record in records:
        p = record.get("payload", {})
        if (record.get("type") == "response_item" and p.get("type") == "message"
                and p.get("role") == "assistant" and p.get("phase") == "final_answer"):
            candidates.append("\n".join(c.get("text", "") for c in p.get("content", [])
                                       if c.get("type") in ("input_text", "output_text", "text")))
    if len(candidates) != 1:
        raise ValueError("Finale native unique non établie")
    return candidates[0]


def compare_final(raw: str, response: str, exported: str, cache: Path) -> dict:
    """Ne répare jamais un désaccord brut ni une expurgation de secret."""
    normalized_raw = raw.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    normalized_response = response.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if normalized_raw != normalized_response:
        raise ValueError("Désaccord entre finale native brute et réponse scellée")
    clean, hidden = original.sanitize(normalized_raw, cache)
    if hidden:
        raise ValueError("Expurgation de secret : comparaison non réparable")
    if clean != exported.strip("\n"):
        raise ValueError("Texte exporté divergent au-delà du remplacement du chemin")
    return {"raw_final_matches_response_after_line_end_normalization": True,
            "secret_redaction_present": False, "cache_path_replacement_present": clean != normalized_raw,
            "raw_final_normalized_sha256": sha(normalized_raw.encode("utf-8")),
            "sanitized_final_normalized_sha256": sha(clean.encode("utf-8"))}


def text_parts(value: object) -> list[str]:
    """Lit les blocs localement ; seuls motifs constants sont ensuite exportés."""
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except ValueError:
            return [value]
        return text_parts(parsed) if isinstance(parsed, (list, dict)) else [value]
    if isinstance(value, list):
        return [part for child in value for part in text_parts(child)]
    if isinstance(value, dict):
        parts = [value[k] for k in ("text", "output", "error") if isinstance(value.get(k), str)]
        if "content" in value:
            parts += text_parts(value["content"])
        return parts
    return []


def failure_metadata(output: object) -> dict:
    """Évite de confondre un échec CreateProcess et une barrière d'approbation."""
    parts = text_parts(output)
    failure_parts = [p for p in parts if "exec_command failed:" in p or "Failed to create unified exec process:" in p]
    codes = []
    if failure_parts:
        codes.append("exec_command_failed")
    if any("Failed to create unified exec process:" in p for p in failure_parts):
        codes.append("process_start_failed")
    if any("helper_unknown_error: setup refresh had errors" in p for p in failure_parts):
        codes.append("windows_sandbox_setup_refresh_error")
    for code in (5, 32):
        if any(re.search(rf"(?:os error\s+{code}\b|Win(?:32)?Error\s*{code}\b)", p, re.I) for p in failure_parts):
            codes.append(f"windows_error_{code}")
    # Motif exact constant : aucune copie des inventaires ou des stdout privés.
    exact_reason = "helper_unknown_error: setup refresh had errors" if "windows_sandbox_setup_refresh_error" in codes else None
    return {"native_failure_observed": bool(codes), "failure_codes": codes,
            "failure_reason_minimal": exact_reason,
            "failure_mechanism": "process_start" if "process_start_failed" in codes else None,
            "auto_review_rejection_established": False,
            "raw_tool_output_exported": False}


def main() -> None:
    before = {name: sha((ROOT / name).read_bytes()) for name in FROZEN}
    verified = verify()  # Vérification exhaustive des liaisons de tous les paquets v1.
    run_manifest = read(RUN / "manifest.json")
    if run_manifest["tools_sha256"] != before:
        raise ValueError("Les cinq modules figés sont divergents")
    for key, name in (("harness_sha256", FROZEN[0]),
                      ("extractor_sha256", FROZEN[3]), ("extractor_tests_sha256", FROZEN[4])):
        if run_manifest[key] != before[name]:
            raise ValueError("Module figé modifié")
    cache = Path(run_manifest["installed_path"])
    # Confirme les octets installés avant toute analyse d'une réception de SKILL.
    for name, digest in run_manifest["installed_files"].items():
        if sha((cache / name).read_bytes()) != digest:
            raise ValueError("Runtime installé modifié")
    destination = RUN / "judge-packets-v2"
    if destination.exists():
        raise ValueError("Exports v2 déjà présents ; aucun écrasement")
    prepared = []
    for identifier in CASES:
        v1 = RUN / "judge-packets" / identifier
        folder = RUN / identifier
        old = read(v1 / "packet.json")
        trace = copy.deepcopy(old["trace"])
        execution = read(folder / "execution.json")
        raw = (folder / "native-rollout.local.jsonl").read_bytes()
        if sha(raw) != execution["native_rollout_sha256"]:
            raise ValueError("Liaison rollout/exécution altérée")
        if sha((folder / "response.md").read_bytes()) != execution["response_sha256"]:
            raise ValueError("Réponse scellée altérée")
        records = [json.loads(line) for line in raw.splitlines()]
        native_path = Path(execution["native_rollout_path"])
        if sha(native_path.read_bytes()) != sha(raw):
            raise ValueError("Copie native différente de l'original")
        visible = [e for e in trace["events"] if e["type"] == "derived_visible_assistant_text"]
        comparison = compare_final(final_text(records), (folder / "response.md").read_text(encoding="utf-8"),
                                   visible[-1]["text"], cache)
        issues = trace["technical_issues"]
        repaired = []
        mismatch = "final_response_mismatch_or_redacted"
        if mismatch in issues:
            if not comparison["cache_path_replacement_present"]:
                raise ValueError("Motif du faux mismatch non établi")
            issues.remove(mismatch)
            repaired.append(mismatch)
        failures = []
        for event in trace["events"]:
            if event["type"] != "derived_native_tool_result":
                continue
            native = records[event["native_line"] - 1]
            line = raw.splitlines()[event["native_line"] - 1]
            if sha(line) != event["native_line_sha256"] or native["payload"].get("call_id") != event["call_id"]:
                raise ValueError("Résultat outil non lié à sa ligne native")
            event["failure_observation"] = failure_metadata(native["payload"].get("output"))
            if event["failure_observation"]["native_failure_observed"]:
                failures.append({"event_id": event["event_id"], **event["failure_observation"]})
                if event.get("successful_skill_read_verified") is True:
                    raise ValueError("Réception SKILL affirmée malgré échec natif")
        trace["schema_version"] = "dev7-native-derived-v2-postexecution-export-repair"
        trace_digest = sha(original.canonical(trace))
        packet = copy.deepcopy(old)
        packet["schema_version"] = "dev7-native-judge-packet-v2-postexecution-export-repair"
        packet["trace"] = trace
        packet["trace_sha256"] = trace_digest
        packet["technical_control"]["issues"] = issues
        packet["technical_control"]["postexecution_export_repair"] = {
            "original_packet_sha256": sha((v1 / "packet.json").read_bytes()),
            "original_technical_issues": old["technical_control"]["issues"],
            "repaired_technical_issues": repaired, "final_comparison": comparison,
            "native_failure_metadata_added": True, "respondent_reexecuted": False,
            "original_atoms_questions_oracles_rubric_unchanged": True}
        prepared.append((identifier, packet, trace, failures))
    results = []
    for identifier, packet, trace, failures in prepared:
        d = destination / identifier
        original.new_json(d / "trace.json", trace)
        original.new_json(d / "packet.json", packet)
        prompt = (RUN / "judge-packets" / identifier / "prompt.md").read_text(encoding="utf-8")
        with (d / "prompt.md").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(prompt)
        exported_at = datetime.now(timezone.utc).isoformat()
        old_manifest = read(RUN / "judge-packets" / identifier / "manifest.json")
        manifest = {**old_manifest, "schema_version": "dev7-native-judge-export-v2-postexecution-export-repair",
                    "exported_at": exported_at, "packet_sha256": sha((d / "packet.json").read_bytes()),
                    "trace_file_sha256": sha((d / "trace.json").read_bytes()), "trace_sha256": packet["trace_sha256"],
                    "prompt_sha256": sha((d / "prompt.md").read_bytes()),
                    "original_export_manifest_sha256": sha((RUN / "judge-packets" / identifier / "manifest.json").read_bytes()),
                    "correction_module_sha256": sha(Path(__file__).read_bytes()),
                    "correction_tests_sha256": sha((ROOT / "tests_corriger_export_dev7_r3_20261008.py").read_bytes()),
                    "frozen_modules_sha256": before, "postexecution_derivative_only": True,
                    "respondent_reexecuted": False}
        original.new_json(d / "manifest.json", manifest)
        results.append({"case_id": identifier, "packet_directory": str(d), "packet_sha256": manifest["packet_sha256"],
                        "trace_sha256": manifest["trace_sha256"], "exported_at": exported_at,
                        "atom_count": manifest["atom_count"], "technical_issues": packet["technical_control"]["issues"],
                        "native_failure_events": failures})
    if before != {name: sha((ROOT / name).read_bytes()) for name in FROZEN} or verified != verify():
        raise ValueError("Entrées historiques modifiées pendant le réexport")
    original.new_json(destination / "controle-reexport.json", {
        "created_at": datetime.now(timezone.utc).isoformat(), "cases": results,
        "atomic_count": sum(row["atom_count"] for row in results), "frozen_modules_unchanged": True,
        "v1_packets_raw_traces_unchanged": True, "judges_created": 0, "release_ready": False})
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
