"""Contre-épreuves de la chaîne et des doublons, sans runtime métier."""
from __future__ import annotations

import hashlib
import itertools
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from instruction_overlays import apply_overlays


class OverlayChainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "overlays").mkdir()
        self.description = b"description: >-\n  Original description.\n"
        self.new_description = b"description: >-\n  New description.\n"
        self.block = b"### Old\nold instruction\n\n"
        self.new_block = b"### Old\nnew instruction\n\n"
        self.base = (b"---\nname: test\n" + self.description
                     + b"metadata:\n  version: 1.0\n---\n# Entry\n"
                     + self.block + b"### Next\nuntouched\n")
        priority = b"## Priority\ncontract\n"
        intermediate = self.base.replace(b"# Entry", priority + b"\n# Entry", 1)
        described = intermediate.replace(self.description, self.new_description, 1)
        self.insertion = self.spec("priority", "insert-before", b"# Entry", priority, self.base)
        self.replacement = self.spec("description", "replace-description", self.description,
                                     self.new_description, intermediate)
        self.section = self.spec("block", "replace-block", self.block, self.new_block, described)
        self.chain = [self.insertion, self.replacement, self.section]
        self.expected = described.replace(self.block, self.new_block, 1)

    @staticmethod
    def sha(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def spec(self, name: str, operation: str, anchor: bytes, content: bytes,
             base: bytes) -> dict:
        source = f"overlays/{name}.md"
        (self.root / source).write_bytes(content)
        return {"target": "SKILL.md", "source": source, "operation": operation,
                "anchor": anchor.decode(), "base_sha256": self.sha(base),
                "source_sha256": self.sha(content)}

    def test_trois_operations_preservent_les_autres_octets_et_l_entree(self) -> None:
        original = {"SKILL.md": self.base, "LICENSE": b"license"}
        result = apply_overlays(self.root, original, self.chain)
        self.assertEqual(result, {"SKILL.md": self.expected, "LICENSE": b"license"})
        self.assertEqual(original, {"SKILL.md": self.base, "LICENSE": b"license"})

    def test_tous_les_ordres_inverses_echouent_sur_l_empreinte_intermediaire(self) -> None:
        for permutation in itertools.permutations(self.chain):
            if list(permutation) == self.chain:
                continue
            with self.subTest(order=[spec["operation"] for spec in permutation]):
                with self.assertRaisesRegex(ValueError, "^Surcharge : empreinte amont divergente$"):
                    apply_overlays(self.root, {"SKILL.md": self.base}, list(permutation))

    def test_deux_remplacements_meme_section_refuses_meme_avec_hashes_valides(self) -> None:
        first = self.spec("first", "replace-block", self.block, self.new_block, self.base)
        intermediate = self.base.replace(self.block, self.new_block, 1)
        second = self.spec("second", "replace-block", self.new_block,
                           b"### Old\nthird instruction\n\n", intermediate)
        with self.assertRaisesRegex(ValueError, "^Surcharge : cible dupliquée$"):
            apply_overlays(self.root, {"SKILL.md": self.base}, [first, second])

    def test_description_ancre_absente_refusee_sans_masquage_par_empreinte(self) -> None:
        replacement = {**self.replacement, "base_sha256": self.sha(self.base),
                       "anchor": "description: >-\n  Absent description.\n"}
        with self.assertRaisesRegex(ValueError, "^Surcharge : ancre absente ou ambiguë$"):
            apply_overlays(self.root, {"SKILL.md": self.base}, [replacement])

    def test_deux_champs_description_refuses_avec_ancre_unique(self) -> None:
        base = self.base.replace(self.description,
                                 self.description + b"description: >-\n  Other field.\n", 1)
        replacement = {**self.replacement, "base_sha256": self.sha(base)}
        with self.assertRaisesRegex(ValueError,
                                    "^Surcharge : description absente ou ambiguë dans le frontmatter$"):
            apply_overlays(self.root, {"SKILL.md": base}, [replacement])


if __name__ == "__main__":
    unittest.main()
