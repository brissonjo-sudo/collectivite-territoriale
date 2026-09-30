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


if __name__ == "__main__":
    unittest.main()
