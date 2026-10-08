"""Contre-épreuves de distribution : la revue différée n'efface pas les échecs."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from qualify_distribution import distribution_errors, fingerprint, load


class DistributionQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        for relative in ("skills", "tests/evidence/2026-10-07-codex-natif-v5",
                         "tests/evidence/2026-10-08-candidat-013"):
            shutil.copytree(ROOT / relative, self.root / relative)
        for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
                         ".mcp.json", "assets/icon.png", "upstream.json",
                         "tests/cas-plugin.json", "scripts/run_codex_campaign.py",
                         "docs/adr/0007-distribution-open-source-et-deploiement.md",
                         "docs/deploiement-collectivite.md"):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.evidence = copy.deepcopy(load(ROOT, "tests/evidence/release-1.2.0.json"))

    def write_proof(self, name: str, proof: dict) -> None:
        binding = self.evidence["distribution"]["proofs"][name]
        target = self.root / binding["evidence_path"]
        target.write_text(json.dumps(proof, ensure_ascii=False), encoding="utf-8", newline="\n")
        binding["sha256"] = fingerprint(target)

    def test_distribution_possible_sans_inventer_validation_humaine(self) -> None:
        self.assertEqual(distribution_errors(self.root, self.evidence), [])
        self.assertFalse(self.evidence["review"]["human_legal_validation"])
        self.assertFalse(self.evidence["deployment"]["ready"])
        self.assertFalse(self.evidence["release_ready"])
        self.assertTrue(all(not r["human_invariants_reviewed"] for r in self.evidence["runs"]))

    def test_deploiement_sans_avis_reste_refuse(self) -> None:
        self.evidence["deployment"]["ready"] = self.evidence["release_ready"] = True
        self.assertIn("Déploiement déclaré prêt sans avis humain",
                      distribution_errors(self.root, self.evidence))

    def test_changement_runtime_invalide_les_preuves(self) -> None:
        entry = self.root / "skills/dcp-fpt/SKILL.md"
        entry.write_bytes(entry.read_bytes() + b"\nChangement de runtime\n")
        self.assertIn("Runtime différent du plugin installé",
                      distribution_errors(self.root, self.evidence))

    def test_changement_configuration_impose_nouveau_smoke(self) -> None:
        path = self.root / ".mcp.json"
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertIn("Configuration différente du smoke : .mcp.json",
                      distribution_errors(self.root, self.evidence))

    def test_preuve_modifiee_ne_passe_pas_par_simple_statut(self) -> None:
        path = self.root / self.evidence["distribution"]["proofs"]["native_campaign"]["evidence_path"]
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertIn("Preuve modifiée : native_campaign",
                      distribution_errors(self.root, self.evidence))

    def test_campagne_incomplete_reste_bloquante(self) -> None:
        proof = load(self.root, self.evidence["native_campaign"]["evidence_path"])
        proof["runs"].pop()
        self.write_proof("native_campaign", proof)
        self.assertIn("Campagne incomplète ou doublonnée",
                      distribution_errors(self.root, self.evidence))

    def test_echec_technique_reste_bloquant(self) -> None:
        proof = load(self.root, self.evidence["native_campaign"]["evidence_path"])
        proof["runs"][0]["technical_status"] = "failed"
        self.write_proof("native_campaign", proof)
        errors = distribution_errors(self.root, self.evidence)
        self.assertIn("Échec technique : " + proof["runs"][0]["case_id"], errors)

    def test_seuil_dcp_non_atteint_reste_bloquant(self) -> None:
        path = self.evidence["skill_measurements"]["dcp-fpt"]["evidence_path"]
        proof = load(self.root, path)
        proof["summary"]["threshold_passed"] = False
        self.write_proof("dcp_measurement", proof)
        self.assertIn("Seuil DCP non atteint", distribution_errors(self.root, self.evidence))

    def test_smoke_sans_stop_reste_bloquant(self) -> None:
        proof = load(self.root, self.evidence["codex_smoke"]["evidence_path"])
        proof["runs"][0]["stop_first"] = False
        self.write_proof("codex_smoke", proof)
        self.assertIn("STOP absent du smoke", distribution_errors(self.root, self.evidence))

    def test_violation_textuelle_reste_bloquante(self) -> None:
        binding = self.evidence["distribution"]["proofs"]["assistant_review"]
        proof = load(self.root, binding["evidence_path"])
        proof["runs"][0]["violations_textuelles"] = 1
        self.write_proof("assistant_review", proof)
        self.assertIn("Violation textuelle : " + proof["runs"][0]["case_id"],
                      distribution_errors(self.root, self.evidence))

    def test_note_differee_reste_requise(self) -> None:
        (self.root / self.evidence["deployment"]["note_path"]).unlink()
        self.assertIn("Note praticien différée absente",
                      distribution_errors(self.root, self.evidence))
