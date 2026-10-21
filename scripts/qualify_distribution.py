"""Qualifie la distribution open source, séparément d'un déploiement métier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cli_toolchains import (compatibility_files, contract_file, measurement_contract,
                            prove_toolchains, require_cycle_version, toolchains)
from measurement_common import bound, snapshot
from public_projection import ProjectionView, verify_ci

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(path: Path) -> str:
    """Calcule une empreinte sur les octets, sans conversion des lignes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root: Path, relative: str) -> dict:
    """Lit une pièce JSON située dans le dépôt."""
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Pièce hors dépôt")
    return json.loads(path.read_text(encoding="utf-8"))


def qualification_cases(root: Path, evidence: dict, view: ProjectionView | None = None) -> dict[str, dict]:
    """Choisit v2/v3 par le commit source lié ; la version ne permet aucun repli."""
    def resolve(base: Path, link: dict) -> Path:
        try:
            return view.bound(base, link) if view else bound(base, link)
        except ValueError as exc:
            # Même catégorie d'échec avec ou sans traduction par ProjectionView.
            raise ValueError('Preuve liée altérée : ' + str(exc)) from exc

    link = evidence.get("review", {}).get("linked_sources")
    if link is not None:
        index_path = resolve(root, link)
        index = json.loads(index_path.read_bytes())
        contract = measurement_contract(root, index.get("measurement_commit"))
        require_cycle_version(contract, evidence.get('plugin_version'))
        if contract is not None:
            case_link = index.get("case_contract") or {}
            if (index.get("schema") != "ct-human-linked-v1"
                    or case_link.get("sha256") != contract["case_contract_sha256"]):
                raise ValueError("Contrat de cycle " + Path(contract_file(contract)).stem.rsplit('-', 1)[1] + " absent ou divergent")
            path = resolve(index_path.parent, case_link)
            return {c["id"]: c for c in json.loads(path.read_bytes())}
    require_cycle_version(None, evidence.get('plugin_version'))
    return {c["id"]: c for c in load(root, "tests/cas-plugin.json")}


def distribution_errors(root: Path, evidence: dict) -> list[str]:
    """Ajoute la barrière publique ; les contrôles techniques restent tous exécutés."""
    try:
        view = verify_ci(root, evidence) if 'public_projection' in evidence else None
        if (view is None and evidence.get('plugin_version') in {'1.3.0', '1.4.0'}
                and evidence.get('review', {}).get('linked_sources')):
            raise ValueError('Projection publique absente')
    except (KeyError, TypeError, ValueError, OSError) as exc:
        return ['Projection publique refusée : ' + str(exc)]
    return _distribution_errors(root, evidence, view)


def smoke_contract_errors(root: Path, evidence: dict, native: dict, reviews: dict,
                          smoke: dict, view: ProjectionView | None = None) -> list[str]:
    """Rejoue les liaisons du smoke et les deux verrous, y compris en projection CI."""
    errors: list[str] = []
    current = snapshot(root)
    for key in ('case_file_sha256', 'upstream_sha256'):
        if smoke.get(key) != current[key]:
            errors.append('Empreinte différente du smoke : ' + key)
    try:
        # Même périmètre que human_resolution.compatible ; aucune transition ajoutée.
        permitted = {'scripts/assemble_release_evidence.py', 'scripts/human_resolution.py'}
        permitted |= compatibility_files(root, smoke, current)
        old, target = smoke['toolchain_sha256'], current['toolchain_sha256']
        if any(old.get(name) != target.get(name) for name in set(old) | set(target)
               if name not in permitted):
            errors.append('Protocole ou outillage du smoke différent')
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append('Transition du smoke refusée : ' + str(exc))
    try:
        resolve = view.bound if view else bound
        measurement_commit = None
        link = evidence.get('review', {}).get('linked_sources')
        if link is not None:
            index = json.loads(resolve(root, link).read_bytes())
            measurement_commit = index.get('measurement_commit')
        declared = {phase: evidence[phase] for phase in ('campaign_cli', 'smoke_cli')}
        if declared != toolchains(root, measurement_commit) or smoke['smoke_cli'] != declared['smoke_cli']:
            raise ValueError('Verrous CLI différents de la distribution ou du smoke')
        campaign_receipts = [load(root, run['evidence_path'])['origin'] for run in native['runs']]
        review_receipts = [load(root, run['evidence_path'])['origin'] for run in reviews['runs']]
        directory = (root / evidence['distribution']['proofs']['codex_smoke']['evidence_path']).parent
        smoke_receipts = [json.loads(resolve(directory, run['proof']).read_bytes())['origin']
                          for run in smoke['runs']]
        prove_toolchains(campaign_receipts, review_receipts, smoke_receipts, declared,
                         measurement_commit=measurement_commit, root=root)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append('Toolchains de distribution refusées : ' + str(exc))
    return errors


def _distribution_errors(root: Path, evidence: dict, view: ProjectionView | None = None) -> list[str]:
    """Recalcule les conditions techniques ; aucun avis humain n'est inventé."""
    errors: list[str] = []
    fingerprint = view.fingerprint if view else globals()['fingerprint']

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    try:
        distribution = evidence["distribution"]
        require(distribution["scope"] == "open_source", "Périmètre de distribution absent")
        require(distribution["ready"] is True, "Distribution non déclarée prête")
        require(not distribution["blockers"], "Blocages techniques de distribution")
        require((root / distribution["decision_path"]).is_file(), "Décision de périmètre absente")
        # Le champ historique garde son sens de qualification métier complète.
        require(evidence["deployment"]["ready"] == evidence["release_ready"],
                "Qualification métier incohérente")
        if evidence["review"]["human_legal_validation"] is not True:
            require(evidence["deployment"]["ready"] is False,
                    "Déploiement déclaré prêt sans avis humain")
            require(bool(evidence["deployment"]["blockers"]), "Réserves métier perdues")
            require((root / evidence["deployment"]["note_path"]).is_file(),
                    "Note praticien différée absente")

        manifest = load(root, ".codex-plugin/plugin.json")
        upstream = load(root, "upstream.json")["skills"]
        require(evidence["plugin_version"] == manifest["version"], "Version non mesurée")
        require(evidence["upstream_commits"] == {n: s["commit"] for n, s in upstream.items()},
                "Commits amont divergents")

        proofs: dict[str, dict] = {}
        for name, binding in distribution["proofs"].items():
            relative = binding["evidence_path"]
            proofs[name] = load(root, relative)
            require(fingerprint(root / relative) == binding["sha256"],
                    f"Preuve modifiée : {name}")
        native, smoke = proofs["native_campaign"], proofs["codex_smoke"]
        dcp, reviews = proofs["dcp_measurement"], proofs["assistant_review"]
        baseline = evidence["plugin_commit"]
        for name in ("native_campaign", "codex_smoke"):
            require(evidence[name]["status"] == "passed"
                    and evidence[name]["plugin_commit"] == baseline
                    and evidence[name]["evidence_path"]
                    == distribution["proofs"][name]["evidence_path"],
                    f"Synthèse de qualification divergente : {name}")
        measurement = evidence["skill_measurements"]["dcp-fpt"]
        require(measurement["status"] == "passed"
                and measurement["upstream_commit"] == upstream["dcp-fpt"]["commit"]
                and measurement["evidence_path"]
                == distribution["proofs"]["dcp_measurement"]["evidence_path"],
                "Synthèse de mesure DCP divergente")
        for name, proof in (("campagne", native), ("smoke", smoke), ("relecture", reviews)):
            require(proof["plugin_commit"] == baseline, f"Baseline divergente : {name}")

        runtime = {p.relative_to(root).as_posix(): fingerprint(p)
                   for p in (root / "skills").rglob("*") if p.is_file()}
        require(not any(p.is_symlink() for p in (root / "skills").rglob("*")),
                "Lien symbolique dans le runtime")
        require(runtime == smoke["runtime_sha256"], "Runtime différent du plugin installé")
        configuration = {".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
                         ".mcp.json", "assets/icon.png"}
        require(set(smoke["plugin_configuration_sha256"]) == configuration,
                "Configuration installée incomplète")
        for name in configuration:
            require(fingerprint(root / name) == smoke["plugin_configuration_sha256"][name],
                    f"Configuration différente du smoke : {name}")
        runner = fingerprint(root / "scripts/run_codex_campaign.py")
        require(native["runner_sha256"] == runner, "Protocole de campagne modifié")
        errors.extend(smoke_contract_errors(root, evidence, native, reviews, smoke, view))

        cases = qualification_cases(root, evidence, view)
        runs = {r["case_id"]: r for r in native["runs"]}
        recorded = {r["case_id"]: r for r in evidence["runs"]}
        require(len(runs) == len(native["runs"]) == len(cases)
                and set(runs) == set(cases) == set(recorded), "Campagne incomplète ou doublonnée")
        require(native["technical_passed_count"] == native["case_count"] == len(cases),
                "Nombre de réussites techniques incomplet")
        for case_id, run in runs.items():
            proof = load(root, run["evidence_path"])
            require(fingerprint(root / run["evidence_path"]) == run["evidence_sha256"],
                    f"Réponse modifiée : {case_id}")
            require(run["technical_status"] == proof["technical_status"] == "passed"
                    and not run["failures"] and not proof["failures"]
                    and proof["process_exit"] == 0, f"Échec technique : {case_id}")
            require(recorded[case_id]["technical_status"] == "passed"
                    and recorded[case_id]["plugin_commit"] == baseline
                    and recorded[case_id]["evidence_path"] == run["evidence_path"],
                    f"Synthèse divergente : {case_id}")
            require(proof["runtime_sha256"] == runtime and proof["runner_sha256"] == runner,
                    f"Runtime ou protocole divergent : {case_id}")
            case_hash = hashlib.sha256(json.dumps(cases[case_id], sort_keys=True,
                                                  ensure_ascii=False).encode()).hexdigest()
            require(proof["case_sha256"] == case_hash, f"Scénario modifié : {case_id}")

        review_runs = {r["case_id"]: r for r in reviews["runs"]}
        require(set(review_runs) == set(cases) and len(reviews["runs"]) == len(cases),
                "Relecture automatisée incomplète")
        for case_id, run in review_runs.items():
            proof = load(root, run["evidence_path"])
            require(fingerprint(root / run["evidence_path"]) == run["evidence_sha256"]
                    and proof["evidence_sha256"] == runs[case_id]["evidence_sha256"],
                    f"Relecture non liée à la réponse : {case_id}")
            require(run["violations_textuelles"] == 0
                    and {i["invariant"] for i in proof["report"]["invariants"]}
                    == set(cases[case_id]["invariants"])
                    and all(i["statut"] in {"respecte", "non_verifiable"}
                            for i in proof["report"]["invariants"]),
                    f"Violation textuelle : {case_id}")

        require(smoke["credentials_copied"] is False and smoke["user_config_unchanged"] is True,
                "Configuration utilisateur ou secrets affectés")
        require(len(smoke["visible_skills"]) == len(upstream), "Skills installés incomplets")
        smoke_runs = {r["case_id"]: r for r in smoke["runs"]}
        require(set(smoke_runs) == {"activation-implicite", "mcp-installe"}, "Smoke incomplet")
        for run in smoke_runs.values():
            require(run["process_exit"] == 0 and run["candidate_entry_read"] is True
                    and run["installed_mcp_success"] is True, "Smoke installé en échec")
        require(smoke_runs["activation-implicite"]["stop_first"] is True, "STOP absent du smoke")
        require(dcp["upstream_runtime_commit"] == upstream["dcp-fpt"]["commit"],
                "Mesure DCP d'un autre candidat")
        require(dcp["summary"]["threshold_passed"] is True
                and dcp["summary"]["case_count"] == 28
                and not dcp["summary"]["critical_failures"], "Seuil DCP non atteint")
        expected_dcp = {n.removeprefix("skills/dcp-fpt/"): h for n, h in runtime.items()
                        if n.startswith("skills/dcp-fpt/") and n != "skills/dcp-fpt/LICENSE"}
        require(dcp["summary"]["runtime_sha256"] == expected_dcp, "Octets DCP non mesurés")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append(f"Qualification incomplète ou illisible : {exc}")
    return errors


def current_distribution_errors(root: Path) -> list[str]:
    """Refuse explicitement l'absence de mesure ; jamais de fallback de version."""
    version = load(root, ".codex-plugin/plugin.json")["version"]
    relative = f"tests/evidence/release-{version}.json"
    if not (root / relative).is_file():
        return [f"Preuve courante absente : release-{version}.json"]
    return distribution_errors(root, load(root, relative))


def main() -> int:
    """Contrôle le candidat courant sans appel réseau ni publication."""
    errors = current_distribution_errors(ROOT)
    for error in errors:
        print(f"[ERREUR] {error}")
    if not errors:
        print("[OK] Distribution open source techniquement qualifiée ; avis métier distinct")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
