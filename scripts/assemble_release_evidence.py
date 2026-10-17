"""Assemble exclusivement des pièces réelles liées ; jamais d'avis humain.

La sortie est un dossier de distribution indépendant du checkout candidat.
L'intégration de ses pièces dans le dépôt reste une décision séparée.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from typing import Any

import run_codex_campaign as campaign
from codex_event_contract import activated_skills, stop_errors
from measurement_common import (CONFIGURATION, binding, bound, candidate, canonical, checked,
                                digest, fingerprint, output_outside, seal, write_new)
from qualify_distribution import distribution_errors
from dcp_reference import reference, copy_reference
from review_codex_campaign import validate_report

ROOT = Path(__file__).resolve().parents[1]


def campaign_inputs(root: Path, commit: str, directory: Path, baseline: dict) -> tuple[dict, dict[str, tuple[Path, dict]]]:
    """Recalcule les contrôles des dix-huit cas, pas seulement leurs statuts."""
    summary_path = directory / "summary.json"
    untrusted = json.loads(summary_path.read_bytes())
    cases = {c["id"]: c for c in json.loads((root / "tests/cas-plugin.json").read_bytes())}
    runs = untrusted.get("runs", [])
    if len(runs) != len(cases) or {r.get("case_id") for r in runs} != set(cases):
        raise ValueError("Un run manque, est ajouté ou dupliqué")
    summary = checked(summary_path, commit, {"real_campaign"})
    if any(summary.get(k) != v for k, v in baseline.items()):
        raise ValueError("Baseline de campagne divergente")
    loaded = {}
    for run in runs:
        path = bound(directory, {"evidence_path": run["evidence_path"], "sha256": run["evidence_sha256"]})
        proof = checked(path, commit, {"real_cli"})
        case = cases[run["case_id"]]
        if any(proof.get(k) != v for k, v in baseline.items()):
            raise ValueError("Runtime ou outillage du run divergent")
        if proof.get("events_sha256") != digest(canonical(proof["events"])):
            raise ValueError("Événements altérés")
        if proof["case_sha256"] != digest(json.dumps(case, sort_keys=True, ensure_ascii=False).encode()):
            raise ValueError("Cas de mesure divergent")
        if (proof.get("model_requested") != "gpt-6.1-sol"
                or proof["origin"]["prompt_sha256"] != digest(campaign.prompt(case).encode())):
            raise ValueError("Modèle ou entrée de campagne divergent")
        if proof["runner_sha256"] != fingerprint(root / "scripts/run_codex_campaign.py"):
            raise ValueError("Lanceur de mesure divergent")
        if (campaign.failures(proof["events"], case, proof["process_exit"], proof["profile"])
                or proof["technical_status"] != "passed" or proof["failures"]
                or run["technical_status"] != "passed" or run["failures"]):
            raise ValueError("Run technique en échec")
        loaded[run["case_id"]] = (path, proof)
    if len({p[1]["origin"]["thread_id"] for p in loaded.values()}) != len(loaded):
        raise ValueError("Conversation réutilisée entre cas")
    if summary["technical_passed_count"] != len(cases) or summary["case_count"] != len(cases):
        raise ValueError("Nombre de réussites de campagne divergent")
    return summary, loaded


def dcp_input(root: Path, path: Path | None) -> dict:
    """DCP-0 : mesure du skill autonome, jamais du runtime plugin."""
    return reference(root, path)


def assemble(root: Path, commit: str, campaign_dir: Path, smoke_path: Path,
             dcp_path: Path | None, review_dir: Path, output: Path) -> Path:
    """N'écrit la preuve release qu'après validation et qualification en staging."""
    if dcp_path is None or not dcp_path.is_file():
        raise ValueError("Mesure DCP absente")
    baseline = candidate(root, commit)
    campaign_data, runs = campaign_inputs(root, commit, campaign_dir, baseline)
    cases = {c["id"]: c for c in json.loads((root / "tests/cas-plugin.json").read_bytes())}
    upstream = json.loads((root / "upstream.json").read_bytes())["skills"]
    dcp = dcp_input(root, dcp_path)
    smoke = checked(smoke_path, commit, {"real_smoke"})
    if any(smoke.get(k) != v for k, v in baseline.items()) or smoke.get("credentials_copied") is not False or smoke.get("user_config_unchanged") is not True:
        raise ValueError("Smoke d'un autre runtime ou configuration utilisateur affectée")
    smoke_runs = smoke.get("runs", [])
    if len(smoke_runs) != 2 or {r["case_id"] for r in smoke_runs} != {"activation-implicite", "mcp-installe"}:
        raise ValueError("Smoke incomplet")
    for item in smoke_runs:
        proof = checked(bound(smoke_path.parent, item["proof"]), commit, {"real_cli"})
        if (proof["process_exit"] != 0 or proof["candidate_entry_read"] is not True
                or proof["installed_mcp_success"] is not True or proof["technical_status"] != "passed"):
            raise ValueError("Smoke en échec")
        if item["case_id"] == "activation-implicite" and (proof["stop_first"] is not True or stop_errors(proof["chronology"])):
            raise ValueError("STOP du smoke non prouvé")
    review = checked(review_dir / "summary.json", commit, {"real_review"})
    if any(review.get(k) != v for k, v in baseline.items()):
        raise ValueError("Baseline de relecture divergente")
    if len(review["runs"]) != len(cases) or {r["case_id"] for r in review["runs"]} != set(cases):
        raise ValueError("Relecture incomplète")
    reviews = {}
    for item in review["runs"]:
        path = bound(review_dir, {"evidence_path": item["evidence_path"], "sha256": item["evidence_sha256"]})
        proof = checked(path, commit, {"real_cli"})
        validate_report(proof["report"], cases[item["case_id"]]["invariants"])
        replies = [e["text"] for e in runs[item["case_id"]][1]["events"] if e["type"] == "reply"]
        if not replies or proof.get("reply_sha256") != digest(replies[-1].encode()):
            raise ValueError("Relecture liée à un autre texte de réponse")
        if proof["evidence_sha256"] != fingerprint(runs[item["case_id"]][0]) or any(i["statut"] == "violation" for i in proof["report"]["invariants"]):
            raise ValueError("Relecture non liée à la réponse ou violation identifiée")
        reviews[item["case_id"]] = (path, proof)
    output = output_outside(root, output)
    # Toutes les entrées sont refusées avant toute écriture si synthétiques ou incomplètes.
    output.mkdir(parents=True)
    wanted = [*CONFIGURATION, "upstream.json", "tests/cas-plugin.json", "scripts/run_codex_campaign.py",
              "docs/adr/0007-distribution-open-source-et-deploiement.md", "docs/deploiement-collectivite.md"]
    wanted += list(baseline["runtime_sha256"])
    for name in wanted:
        target = output / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    pieces = output / "tests/evidence/mesure-courante"; pieces.mkdir(parents=True)
    native_runs, recorded, review_runs = [], [], []
    for case_id, (path, proof) in runs.items():
        destination = pieces / (case_id + ".json"); shutil.copyfile(path, destination)
        relative = destination.relative_to(output).as_posix()
        native_runs.append({"case_id": case_id, "evidence_path": relative,
                            "evidence_sha256": fingerprint(destination), "technical_status": "passed", "failures": []})
        case = cases[case_id]
        activated = activated_skills(proof["events"], campaign.entry_chunks)[0] if case.get("schema_version") == 2 else case["activation_sequence"]
        tools = ["mcp__droit-francais__" + e["tool"] for e in proof["events"] if e["type"] == "mcp_call" and e["succeeded"]]
        recorded.append({"case_id": case_id, "plugin_commit": commit, "evidence_path": relative,
            "technical_status": "passed", "status": "blocked", "activated_skills": activated,
            "invariants": {i: False for i in case["invariants"]}, "human_invariants_reviewed": False,
            "mcp_tools": tools, "mcp_status": "disabled" if case["mcp_mode"] == "disabled" else "passed"})
        review_path, review_proof = reviews[case_id]
        destination = pieces / (case_id + "-review.json"); shutil.copyfile(review_path, destination)
        review_runs.append({"case_id": case_id, "evidence_path": destination.relative_to(output).as_posix(),
                            "evidence_sha256": fingerprint(destination), "violations_textuelles": 0})
    native = {**campaign_data, "runs": native_runs}
    assistant = {**review, "runs": review_runs}
    # Copies exactes des pièces secondaires, jamais des répertoires de profils.
    for category, document, original in (("smoke", smoke, smoke_path), ("dcp", dcp, dcp_path)):
        directory = pieces / category; directory.mkdir()
        if category == "dcp":
            if copy_reference(root, original, directory / original.name) != dcp:
                raise ValueError("Référence DCP divergente avant assemblage")
            continue
        shutil.copyfile(original, directory / original.name)
        links = [r["proof"] for r in document["runs"]]
        for link in links:
            source = bound(original.parent, link)
            destination = directory / link["evidence_path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists() and fingerprint(destination) != fingerprint(source):
                raise ValueError("Collision de pièces secondaires")
            if not destination.exists():
                shutil.copyfile(source, destination)
    # Les synthèses de campagne/relecture sont dérivées ; leurs originales restent liées.
    for category, source in (("native-original", campaign_dir / "summary.json"), ("review-original", review_dir / "summary.json")):
        shutil.copyfile(source, pieces / (category + ".json"))
    extra = {}
    for name, document in (("native_campaign", native), ("codex_smoke", smoke), ("dcp_measurement", dcp), ("assistant_review", assistant)):
        if name in {"codex_smoke", "dcp_measurement"}:
            category, source = ("smoke", smoke_path) if name == "codex_smoke" else ("dcp", dcp_path)
            destination = pieces / category / source.name
            extra[name] = binding(destination, output)
            continue
        destination = pieces / (name + ".json")
        # Les synthèses relocalisées ne réutilisent pas un sceau périmé.
        write_new(destination, seal({k: v for k, v in document.items() if k != "payload_sha256"}))
        extra[name] = binding(destination, output)
    version = json.loads((root / ".codex-plugin/plugin.json").read_bytes())["version"]
    evidence = {"plugin_version": version, "plugin_commit": commit,
        "upstream_commits": {n: s["commit"] for n, s in upstream.items()}, "runs": recorded,
        "review": {"human_legal_validation": False}, "release_ready": False,
        "distribution": {"scope": "open_source", "ready": True, "blockers": [],
            "decision_path": "docs/adr/0007-distribution-open-source-et-deploiement.md", "proofs": extra},
        "deployment": {"ready": False, "blockers": ["Avis praticien non délivré"], "note_path": "docs/deploiement-collectivite.md"},
        "native_campaign": {"status": "passed", "plugin_commit": commit, "evidence_path": extra["native_campaign"]["evidence_path"]},
        "codex_smoke": {"status": "passed", "plugin_commit": commit, "evidence_path": extra["codex_smoke"]["evidence_path"]},
        "skill_measurements": {"dcp-fpt": {"status": "passed", "upstream_commit": upstream["dcp-fpt"]["commit"],
            "evidence_path": extra["dcp_measurement"]["evidence_path"]}}}
    if candidate(root, commit) != baseline:
        raise ValueError("Candidat divergent avant finalisation")
    errors = distribution_errors(output, evidence)
    if errors:
        raise ValueError("Qualificateur inchangé en refus : " + "; ".join(errors))
    destination = output / "tests/evidence" / ("release-" + version + ".json")
    write_new(destination, evidence)
    return destination


def main() -> int:
    """Aucune option pour accepter fixtures, absence de DCP ou avis humain."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-commit", required=True)
    parser.add_argument("--campaign-dir", type=Path, required=True)
    parser.add_argument("--smoke", type=Path, required=True)
    parser.add_argument("--dcp", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = assemble(ROOT, args.plugin_commit, args.campaign_dir.resolve(), args.smoke.resolve(),
                          args.dcp.resolve(), args.review_dir.resolve(), args.output_dir)
        print(json.dumps({"path": str(result), "human_legal_validation": False})); return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "blocked", "reason_type": type(exc).__name__,
                          "reason_sha256": digest(str(exc).encode()), "human_legal_validation": False})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
