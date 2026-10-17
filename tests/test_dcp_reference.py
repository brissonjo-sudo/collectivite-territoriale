"""DCP-0 : octets publics réels, mutations locales ; aucun appel de modèle."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dcp_reference as dcp
import assemble_release_evidence as assembly

PROOF = ROOT / "tests/evidence/2026-10-08-candidat-013/dcp-autonome.json"


class DcpReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="t43-DCP0-mutations-locales-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.root = self.directory / "candidat"
        shutil.copytree(ROOT / "skills/dcp-fpt", self.root / "skills/dcp-fpt")
        shutil.copyfile(ROOT / "upstream.json", self.root / "upstream.json")
        self.path = self.directory / "dcp-autonome.json"
        shutil.copyfile(PROOF, self.path)

    def mutate_proof(self, action) -> None:
        value = json.loads(self.path.read_bytes())
        action(value)
        self.path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")

    def test_accepte_etat_reel_du_candidat_sans_commit_plugin_transfere(self) -> None:
        proof = assembly.dcp_input(ROOT, PROOF)
        self.assertEqual(proof, json.loads(PROOF.read_bytes()))
        self.assertEqual(len(proof["summary"]["runtime_sha256"]), 30)
        self.assertNotIn("plugin_commit", proof)
        self.assertEqual(set(p.relative_to(ROOT / "skills/dcp-fpt").as_posix()
            for p in (ROOT / "skills/dcp-fpt").rglob("*") if p.is_file())
            - set(proof["summary"]["runtime_sha256"]), {"LICENSE"})

    def test_pin_upstream_different_refuse(self) -> None:
        path = self.root / "upstream.json"
        value = json.loads(path.read_bytes()); value["skills"]["dcp-fpt"]["commit"] = "0" * 40
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Pin DCP différent"):
            dcp.reference(self.root, self.path)

    def test_pin_preuve_different_refuse(self) -> None:
        self.mutate_proof(lambda p: p.update(upstream_runtime_commit="0" * 40))
        with self.assertRaisesRegex(ValueError, "Pin DCP différent"):
            dcp.reference(self.root, self.path)

    def test_un_octet_DCP_modifie_refuse(self) -> None:
        path = self.root / "skills/dcp-fpt/SKILL.md"
        content = path.read_bytes(); path.write_bytes(bytes([content[0] ^ 1]) + content[1:])
        with self.assertRaisesRegex(ValueError, "Octets DCP mesurés divergents : SKILL.md"):
            dcp.reference(self.root, self.path)

    def test_fichier_DCP_manquant_refuse(self) -> None:
        (self.root / "skills/dcp-fpt/agents/openai.yaml").unlink()
        with self.assertRaisesRegex(ValueError, "Octets DCP mesurés divergents : agents/openai.yaml"):
            dcp.reference(self.root, self.path)

    def test_fichier_hors_selection_non_explique_refuse(self) -> None:
        (self.root / "skills/dcp-fpt/supplement.txt").write_bytes(b"mutation locale")
        with self.assertRaisesRegex(ValueError, "Sélection DCP différente"):
            dcp.reference(self.root, self.path)

    def test_preuve_alteree_meme_sans_champ_change_refuse(self) -> None:
        self.path.write_bytes(self.path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "Empreinte du fichier de preuve DCP divergente"):
            dcp.reference(self.root, self.path)

    def test_source_summary_sha256_altere_refuse(self) -> None:
        self.mutate_proof(lambda p: p.update(source_summary_sha256="0" * 64))
        with self.assertRaisesRegex(ValueError, "source_summary_sha256 DCP divergente"):
            dcp.reference(self.root, self.path)

    def test_summary_modifie_refuse(self) -> None:
        self.mutate_proof(lambda p: p["summary"].update(case_count=29))
        with self.assertRaisesRegex(ValueError, "source_summary_sha256 DCP divergente"):
            dcp.reference(self.root, self.path)

    def test_provenance_publique_substituee_refuse(self) -> None:
        self.mutate_proof(lambda p: p.update(source_proof_commit="0" * 40))
        with self.assertRaisesRegex(ValueError, "Provenance publique DCP différente"):
            dcp.reference(self.root, self.path)

    def test_amelioration_scope_ou_avis_humain_refusee(self) -> None:
        for update in ({"scope": "relu par un praticien"}, {"human_legal_validation": True}, {"publication_ready": True}):
            shutil.copyfile(PROOF, self.path)
            self.mutate_proof(lambda p: p.update(update))
            with self.subTest(update=update), self.assertRaisesRegex(ValueError, "Empreinte du fichier de preuve"):
                dcp.reference(self.root, self.path)

    def test_copie_exacte_scope_reserves_et_avis_inchanges(self) -> None:
        target = self.directory / "copie.json"
        proof = dcp.copy_reference(self.root, self.path, target)
        self.assertEqual(target.read_bytes(), PROOF.read_bytes())
        self.assertEqual(proof["scope"], "Seuil automatique de mesure ; relecture juridique et provenance distinctes.")
        self.assertEqual(proof["summary"]["publication_note"], "Relecture praticien et validation du plugin à établir séparément.")
        self.assertFalse(proof["human_legal_validation"])
        self.assertFalse(proof["publication_ready"])
        self.assertFalse(proof["summary"]["publication_ready"])
        self.assertNotIn("plugin_commit", json.loads(target.read_bytes()))

    def test_source_changee_pendant_copie_refusee(self) -> None:
        original = dcp.reference
        def change_after_check(root, path):
            proof = original(root, path)
            if path == self.path:
                self.path.write_bytes(self.path.read_bytes() + b"\n")
            return proof
        with patch.object(dcp, "reference", side_effect=change_after_check), self.assertRaisesRegex(ValueError, "Empreinte du fichier de preuve"):
            dcp.copy_reference(self.root, self.path, self.directory / "copie-alteree.json")


if __name__ == "__main__":
    unittest.main()
