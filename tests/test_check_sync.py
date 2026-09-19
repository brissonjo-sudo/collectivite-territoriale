"""Contrôle de non-régression du détecteur de dérive des copies."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_sync import check  # noqa: E402
from sync_skills import archive_files, load_upstreams  # noqa: E402


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

    def test_accepte_une_racine_source_et_un_fichier_additionnel(self) -> None:
        spec = self._base_spec()
        spec.update(
            source_root="skill/",
            local_directory="droit-francais-skill",
            additional_files=[{"source": "LICENSE", "target": "LICENSE"}],
        )
        loaded = self._load_single(spec)
        self.assertEqual(loaded["test-skill"]["source_root"], "skill/")

    def test_refuse_les_chemins_dangereux(self) -> None:
        invalid_specs = []
        for field, value in (
            ("source_root", "../skill/"),
            ("source_root", "/skill/"),
            ("local_directory", "../droit-francais-skill"),
        ):
            spec = self._base_spec()
            spec[field] = value
            invalid_specs.append(spec)
        spec = self._base_spec()
        spec["additional_files"] = [{"source": "../LICENSE", "target": "LICENSE"}]
        invalid_specs.append(spec)
        for spec in invalid_specs:
            with self.subTest(spec=spec):
                with self.assertRaises(ValueError):
                    self._load_single(spec)

    def test_refuse_une_destination_additionnelle_dupliquee(self) -> None:
        spec = self._base_spec()
        spec["additional_files"] = [
            {"source": "LICENSE", "target": "LICENSE"},
            {"source": "NOTICE", "target": "LICENSE"},
        ]
        with self.assertRaisesRegex(ValueError, "dupliquée"):
            self._load_single(spec)

    def test_aplatit_la_racine_source_et_copie_la_licence(self) -> None:
        spec = self._base_spec()
        spec.update(
            source_root="skill/",
            additional_files=[{"source": "LICENSE", "target": "LICENSE"}],
        )
        skill = b"# Skill : test (v1.0.0)\n"
        license_text = b"licence"
        oid_skill = "1" * 40
        oid_license = "2" * 40
        tree = (
            f"100644 blob {oid_license}\tLICENSE\0"
            f"100644 blob {oid_skill}\tskill/SKILL.md\0"
        ).encode()
        batch = (
            f"{oid_license} blob {len(license_text)}\n".encode()
            + license_text + b"\n"
            + f"{oid_skill} blob {len(skill)}\n".encode()
            + skill + b"\n"
        )
        with patch("sync_skills.run_git", side_effect=[b"", tree, batch]):
            files = archive_files(Path("repo"), spec)
        self.assertEqual(files, {"LICENSE": license_text, "SKILL.md": skill})

    def test_refuse_collision_fichier_additionnel_et_runtime(self) -> None:
        spec = self._base_spec()
        spec.update(
            source_root="skill/",
            additional_files=[{"source": "LICENSE", "target": "SKILL.md"}],
        )
        oid_skill = "1" * 40
        oid_license = "2" * 40
        tree = (
            f"100644 blob {oid_license}\tLICENSE\0"
            f"100644 blob {oid_skill}\tskill/SKILL.md\0"
        ).encode()
        with patch("sync_skills.run_git", side_effect=[b"", tree]):
            with self.assertRaisesRegex(ValueError, "Collision"):
                archive_files(Path("repo"), spec)

    def test_refuse_un_fichier_additionnel_absent(self) -> None:
        spec = self._base_spec()
        spec["additional_files"] = [{"source": "LICENSE", "target": "LICENSE"}]
        oid_skill = "1" * 40
        tree = f"100644 blob {oid_skill}\tSKILL.md\0".encode()
        with patch("sync_skills.run_git", side_effect=[b"", tree]):
            with self.assertRaisesRegex(ValueError, "additionnel absent"):
                archive_files(Path("repo"), spec)

    def test_refuse_un_lien_symbolique_amont(self) -> None:
        spec = self._base_spec()
        oid_skill = "1" * 40
        tree = f"120000 blob {oid_skill}\tSKILL.md\0".encode()
        with patch("sync_skills.run_git", side_effect=[b"", tree]):
            with self.assertRaisesRegex(ValueError, "Type de fichier"):
                archive_files(Path("repo"), spec)

    @staticmethod
    def _base_spec() -> dict:
        return {
            "repository": "https://github.com/brissonjo-sudo/test-skill.git",
            "commit": "0" * 40,
            "version": "1.0.0",
            "paths": ["SKILL.md"],
        }

    @staticmethod
    def _load_single(spec: dict) -> dict[str, dict]:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "upstream.json").write_text(
                json.dumps({"format_version": 1, "skills": {"test-skill": spec}}),
                encoding="utf-8",
            )
            return load_upstreams(root)


if __name__ == "__main__":
    unittest.main()
