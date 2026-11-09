"""DCP-0 : octets publics réels, mutations locales ; aucun appel de modèle."""
from __future__ import annotations

import json
import contextlib
import io
import subprocess
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
import check_dcp_protocol

PROOF = ROOT / "tests/evidence/2026-10-08-candidat-013/dcp-autonome.json"


class DcpReferenceTests(unittest.TestCase):
    PROOF = PROOF
    CONTRACT = ROOT / "scripts/dcp-protocol-0012.json"
    FROZEN = "87afc049f70b7900bc670b5f683a033724cae136"

    def setUp(self) -> None:
        protocol = self.protocol = json.loads(self.CONTRACT.read_bytes())
        if self.FROZEN:
            for module in (dcp, check_dcp_protocol):
                contract_patch = patch.object(module, "contract", return_value=protocol)
                contract_patch.start()
                self.addCleanup(contract_patch.stop)
        temporary = tempfile.TemporaryDirectory(prefix="t43-DCP0-mutations-locales-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.root = self.directory / "candidat"
        if self.FROZEN:
            # Une référence historique part de son runtime exact au commit figé (blobs bruts,
            # sans conversion) ; le candidat courant doit, lui, la refuser séparément.
            names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", self.FROZEN,
                "skills/dcp-fpt"], cwd=ROOT).decode("utf-8").splitlines()
            for name in names + ["upstream.json"]:
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(subprocess.check_output(["git", "show", self.FROZEN + ":" + name], cwd=ROOT))
        else:
            shutil.copytree(ROOT / "skills/dcp-fpt", self.root / "skills/dcp-fpt")
            shutil.copyfile(ROOT / "upstream.json", self.root / "upstream.json")
        self.path = self.directory / "dcp-autonome.json"
        shutil.copyfile(self.PROOF, self.path)

    def mutate_proof(self, action) -> None:
        value = json.loads(self.path.read_bytes())
        action(value)
        self.path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")

    def test_accepte_reference_historique_sans_commit_plugin_transfere(self) -> None:
        proof = assembly.dcp_input(self.root, self.PROOF)
        self.assertEqual(proof, json.loads(self.PROOF.read_bytes()))
        self.assertEqual(len(proof["summary"]["runtime_sha256"]), 30)
        self.assertNotIn("plugin_commit", proof)
        self.assertEqual(set(p.relative_to(self.root / "skills/dcp-fpt").as_posix()
            for p in (self.root / "skills/dcp-fpt").rglob("*") if p.is_file())
            - set(proof["summary"]["runtime_sha256"]),
            set(self.protocol["reference"]["selection_excluded"]))

    def test_candidat_surcharge_refuse_ancienne_reference(self) -> None:
        with self.assertRaisesRegex(ValueError, "Pin DCP différent"):
            assembly.dcp_input(ROOT, PROOF)

    def test_copie_reference_sur_candidat_surcharge_refusee_avant_ecriture(self) -> None:
        destination = self.directory / "jamais-copiee.json"
        with self.assertRaisesRegex(ValueError, "Pin DCP différent"):
            dcp.copy_reference(ROOT, PROOF, destination)
        self.assertFalse(destination.exists())

    def test_diagnostic_historique_reste_compatible_sans_modele(self) -> None:
        historical_proof = self.root / dcp.contract()["reference"]["evidence_path"]
        historical_proof.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.PROOF, historical_proof)
        stream = io.StringIO()
        with patch.object(check_dcp_protocol, "ROOT", self.root), contextlib.redirect_stdout(stream):
            self.assertEqual(check_dcp_protocol.main(), 0)
        result = json.loads(stream.getvalue())
        self.assertTrue(result["compatible"])
        self.assertFalse(result["model_called"])
        self.assertFalse(result["new_dcp_campaign_required"])
        self.assertEqual(result["decision"], json.loads(self.CONTRACT.read_bytes())["decision"])

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
            shutil.copyfile(self.PROOF, self.path)
            self.mutate_proof(lambda p: p.update(update))
            with self.subTest(update=update), self.assertRaisesRegex(ValueError, "Empreinte du fichier de preuve"):
                dcp.reference(self.root, self.path)

    def test_copie_exacte_scope_reserves_et_avis_inchanges(self) -> None:
        target = self.directory / "copie.json"
        proof = dcp.copy_reference(self.root, self.path, target)
        self.assertEqual(target.read_bytes(), self.PROOF.read_bytes())
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



DCP014_PROOF = ROOT / "tests/evidence/2026-10-20-dcp-014/dcp-autonome.json"


class Dcp014ReferenceTests(DcpReferenceTests):
    """DCP-014 historique (ADR 0016) : même batterie, runtime 0.1.4 restauré au dernier commit actif."""
    PROOF = DCP014_PROOF
    CONTRACT = ROOT / "scripts/dcp-protocol-0014.json"
    FROZEN = "601157da9d9d86d7be1647584c955a3a4984ede3"

    def test_candidat_surcharge_refuse_ancienne_reference(self) -> None:
        for proof in (PROOF, self.PROOF):
            with self.subTest(proof=proof.parent.name), self.assertRaisesRegex(ValueError, "Pin DCP différent"):
                assembly.dcp_input(ROOT, proof)

    def test_sources_publiques_embarquees_identiques_aux_empreintes(self) -> None:
        proof = json.loads(self.PROOF.read_bytes())
        for name, digest in proof["source_files_sha256"].items():
            import hashlib
            storage = proof.get("source_files_storage", {}).get(name)
            if storage:
                import gzip
                compressed = (self.PROOF.parent / storage["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(compressed).hexdigest(), storage["sha256"])
                self.assertEqual(storage["encoding"], "gzip")
                with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
                    raw = stream.read(1024 * 1024)
                    self.assertEqual(stream.read(1), b"")
                self.assertEqual(len(raw), storage["original_size"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), storage["original_sha256"])
            else:
                raw = (self.PROOF.parent / Path(name).name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)

    def test_surcharge_locale_meme_au_pin_exact_refusee(self) -> None:
        path = self.root / "skills/dcp-fpt/SKILL.md"
        path.write_bytes(path.read_bytes() + b"\nlocal overlay\n")
        with self.assertRaisesRegex(ValueError, "Octets DCP mesurés divergents : SKILL.md"):
            dcp.reference(self.root, self.path)


class Dcp017ReferenceTests(Dcp014ReferenceTests):
    """DCP-017 (ADR 0033) : la même batterie de mutations s'applique à la référence courante exacte."""
    PROOF = ROOT / "tests/evidence/2026-11-08-dcp-017/dcp-autonome.json"
    CONTRACT = ROOT / "scripts/dcp-protocol.json"
    FROZEN = None

    def test_candidat_surcharge_refuse_ancienne_reference(self) -> None:
        for proof in (PROOF, DCP014_PROOF):
            with self.subTest(proof=proof.parent.name), self.assertRaisesRegex(ValueError, "Pin DCP différent"):
                assembly.dcp_input(ROOT, proof)
        proof = assembly.dcp_input(ROOT, self.PROOF)
        self.assertEqual(proof["upstream_runtime_commit"], "f3be71f4d8feb7e00faabb69786d3b14c7280908")
        self.assertEqual(proof["source_measured_commit"], "5debffd54a6d76e86c79ab261446f9123e564494")
        self.assertEqual(proof["summary"]["totals"], {"DEMI-RÉUSSITE": 2, "RÉUSSITE": 25, "ÉCHEC": 1})
        self.assertEqual(proof["human_review"]["conformes"], 25)
        self.assertEqual(set(proof["human_review"]["reserves"]), {"cas-06", "cas-08", "cas-18"})
        self.assertFalse(proof["human_review"]["practitioner"])


if __name__ == "__main__":
    unittest.main()
