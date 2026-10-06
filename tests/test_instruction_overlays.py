"""Contrôle des corrections locales reproductibles, sans réponse attendue injectée."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from instruction_overlays import apply_overlays, validate_overlays


class InstructionOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "overlays").mkdir()
        self.base = b"---\nname: test\n---\n## Start\nbody\n"
        self.content = b"## Correction\nverified method\n"
        (self.root / "overlays/test.md").write_bytes(self.content)
        self.spec = {
            "target": "SKILL.md", "source": "overlays/test.md",
            "base_sha256": hashlib.sha256(self.base).hexdigest(),
            "source_sha256": hashlib.sha256(self.content).hexdigest(),
            "anchor": "## Start",
        }

    def test_insertion_exacte_sans_modifier_la_base(self) -> None:
        original = {"SKILL.md": self.base, "LICENSE": b"license"}
        result = apply_overlays(self.root, original, [self.spec])
        self.assertEqual(result["SKILL.md"], self.base.replace(b"## Start", self.content + b"\n## Start"))
        self.assertEqual(original["SKILL.md"], self.base)
        self.assertEqual(result["LICENSE"], b"license")

    def test_refuse_une_derivation_amont(self) -> None:
        with self.assertRaisesRegex(ValueError, "amont divergente"):
            apply_overlays(self.root, {"SKILL.md": self.base + b"changed"}, [self.spec])

    def test_refuse_une_correction_modifiee(self) -> None:
        (self.root / "overlays/test.md").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "locale divergente"):
            apply_overlays(self.root, {"SKILL.md": self.base}, [self.spec])

    def test_refuse_chemins_dangereux_et_cibles_dupliquees(self) -> None:
        for path in ("../test.md", "/test.md", "C:/test.md", "overlays/../test.md", "overlays/./test.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_overlays([{**self.spec, "source": path}])
        with self.assertRaisesRegex(ValueError, "dupliquée"):
            validate_overlays([self.spec, self.spec])

    def test_refuse_liens_symboliques(self) -> None:
        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaisesRegex(ValueError, "symbolique"):
                apply_overlays(self.root, {"SKILL.md": self.base}, [self.spec])

    def test_refuse_ancre_absente_ou_ambigue(self) -> None:
        for base in (b"no anchor", b"## Start\n## Start\n"):
            spec = {**self.spec, "base_sha256": hashlib.sha256(base).hexdigest()}
            with self.assertRaisesRegex(ValueError, "ancre"):
                apply_overlays(self.root, {"SKILL.md": base}, [spec])

    def test_refuse_cible_absente(self) -> None:
        with self.assertRaisesRegex(ValueError, "cible absente"):
            apply_overlays(self.root, {}, [self.spec])

    def description_fixture(self) -> tuple[bytes, bytes, bytes, dict]:
        """Construit de vrais octets YAML et une description de découverte bornée."""
        old = b"description: >-\n  Expert territorial.\n  Activer sur question du domaine.\n"
        new = b"description: >-\n  Expert territorial. Commencer par STOP si garde applicable.\n  Verifier les sources avant qualification juridique.\n"
        base = (b"---\nname: test\n" + old
                + b"metadata:\n  version: 1.0\n  depends: [source]\n---\n## Start\nbody\n")
        source = "overlays/discovery.md"
        (self.root / source).write_bytes(new)
        spec = {"operation": "replace-description", "target": "SKILL.md", "source": source,
                "base_sha256": hashlib.sha256(base).hexdigest(),
                "source_sha256": hashlib.sha256(new).hexdigest(), "anchor": old.decode()}
        return base, old, new, spec

    def test_remplacement_description_seule_octets_nom_metadata_corps_preserves(self) -> None:
        base, old, new, spec = self.description_fixture()
        files = {"SKILL.md": base, "LICENSE": b"license"}
        result = apply_overlays(self.root, files, [spec])
        self.assertEqual(base.replace(old, new, 1), result["SKILL.md"])
        self.assertEqual(base, files["SKILL.md"])
        self.assertEqual(b"license", result["LICENSE"])

    def test_deux_operations_ordonnee_hash_intermediaire_obligatoire(self) -> None:
        base, old, new, replacement = self.description_fixture()
        insertion = {**self.spec, "base_sha256": hashlib.sha256(base).hexdigest()}
        intermediate = apply_overlays(self.root, {"SKILL.md": base}, [insertion])["SKILL.md"]
        after_insert = {**replacement, "base_sha256": hashlib.sha256(intermediate).hexdigest()}
        expected = intermediate.replace(old, new, 1)
        self.assertEqual(expected, apply_overlays(self.root, {"SKILL.md": base},
                                                 [insertion, after_insert])["SKILL.md"])
        replaced = apply_overlays(self.root, {"SKILL.md": base}, [replacement])["SKILL.md"]
        after_replace = {**insertion, "base_sha256": hashlib.sha256(replaced).hexdigest()}
        self.assertEqual(expected, apply_overlays(self.root, {"SKILL.md": base},
                                                 [replacement, after_replace])["SKILL.md"])
        with self.assertRaisesRegex(ValueError, "amont divergente"):
            apply_overlays(self.root, {"SKILL.md": base}, [insertion, replacement])

    def test_description_refuse_autre_champ_et_yaml_complexe(self) -> None:
        base, _, _, spec = self.description_fixture()
        invalid = (
            b"description: >-\n  text\nname: renamed\n",
            b"description: >-\n  text\nmetadata:\n  version: 9\n",
            b"description: {text: value}\n",
            b"description: >- &alias\n  text\n",
            b"description: !tag >-\n  text\n",
            b"description: >-\n  text\n    indented nesting\n",
            b"---\ndescription: >-\n  text\n---\n",
        )
        for content in invalid:
            with self.subTest(content=content):
                (self.root / spec["source"]).write_bytes(content)
                current = {**spec, "source_sha256": hashlib.sha256(content).hexdigest()}
                with self.assertRaisesRegex(ValueError, "description folded simple"):
                    apply_overlays(self.root, {"SKILL.md": base}, [current])

    def test_description_refuse_ancre_dans_corps(self) -> None:
        _, old, _, spec = self.description_fixture()
        base = b"---\nname: test\n---\n## Start\n" + old
        current = {**spec, "base_sha256": hashlib.sha256(base).hexdigest()}
        with self.assertRaisesRegex(ValueError, "description absente"):
            apply_overlays(self.root, {"SKILL.md": base}, [current])

    def test_description_refuse_ancre_partielle_du_bloc_complexe_amont(self) -> None:
        base, old, _, spec = self.description_fixture()
        base = base.replace(old, old + b"    complex continuation\n")
        current = {**spec, "base_sha256": hashlib.sha256(base).hexdigest()}
        with self.assertRaisesRegex(ValueError, "champ description complet"):
            apply_overlays(self.root, {"SKILL.md": base}, [current])

    def test_description_refuse_ancre_de_description_dupliquee(self) -> None:
        base, old, _, spec = self.description_fixture()
        base += old
        current = {**spec, "base_sha256": hashlib.sha256(base).hexdigest()}
        with self.assertRaisesRegex(ValueError, "ancre absente ou ambiguë"):
            apply_overlays(self.root, {"SKILL.md": base}, [current])

    def test_description_refuse_derives_hash_base_et_source(self) -> None:
        base, _, _, spec = self.description_fixture()
        with self.assertRaisesRegex(ValueError, "amont divergente"):
            apply_overlays(self.root, {"SKILL.md": base + b"modified"}, [spec])
        (self.root / spec["source"]).write_bytes(b"description: >-\n  modified\n")
        with self.assertRaisesRegex(ValueError, "locale divergente"):
            apply_overlays(self.root, {"SKILL.md": base}, [spec])

    def test_refuse_operation_inconnue_autre_cible_autres_champs(self) -> None:
        _, _, _, spec = self.description_fixture()
        for mutation in (
            {"operation": "replace-name"}, {"target": "references/route.md"},
            {"source": "overlays/discovery.yaml"}, {"rename": "other"},
        ):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_overlays([{**spec, **mutation}])
        with self.assertRaisesRegex(ValueError, "dupliquée"):
            validate_overlays([spec, spec])

    def test_insert_before_explicite_conserve_comportement_historique(self) -> None:
        self.assertEqual(apply_overlays(self.root, {"SKILL.md": self.base}, [self.spec]),
                         apply_overlays(self.root, {"SKILL.md": self.base},
                                        [{**self.spec, "operation": "insert-before"}]))

    def test_insertion_ne_peut_pas_contourner_la_limite_frontmatter(self) -> None:
        current = {**self.spec, "anchor": "name: test"}
        with self.assertRaisesRegex(ValueError, "modifier le frontmatter"):
            apply_overlays(self.root, {"SKILL.md": self.base}, [current])


if __name__ == "__main__":
    unittest.main()
