"""Contrôle de non-régression du détecteur de dérive des copies."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_sync import check  # noqa: E402


class SyncCheckTests(unittest.TestCase):
    def test_detecte_une_copie_modifiee(self) -> None:
        root = Path(__file__).resolve().parents[1]
        expected = {
            skill.name: {
                path.relative_to(skill).as_posix(): path.read_bytes()
                for path in skill.rglob("*") if path.is_file()
            }
            for skill in (root / "skills").iterdir() if skill.is_dir()
        }
        self.assertEqual(check(root, expected), [])
        expected["dpm-fpt"]["SKILL.md"] += b"modification volontaire"
        self.assertIn(
            "Fichier divergent : dpm-fpt/SKILL.md", check(root, expected)
        )


if __name__ == "__main__":
    unittest.main()
