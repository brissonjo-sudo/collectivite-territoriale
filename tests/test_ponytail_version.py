"""Vérifie le chargement conditionnel de Ponytail sans appel réseau en test."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/ponytail"
spec = importlib.util.spec_from_file_location("ponytail_version", SKILL / "scripts/check_version.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class PonytailVersionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.skill = Path(self.workspace.name) / "ponytail"
        shutil.copytree(SKILL, self.skill)
        self.lock = json.loads((self.skill / "upstream-lock.json").read_text(encoding="utf-8"))
        self.release = {"tag_name": self.lock["release_tag"], "draft": False, "prerelease": False}
        self.reference = {"ref": "refs/tags/" + self.lock["release_tag"],
                          "object": {"type": "commit", "sha": self.lock["commit"]}}

    def fetch(self) -> Mock:
        return Mock(side_effect=[self.release, self.reference])

    def test_version_courante_charge_uniquement_les_regles_installees(self) -> None:
        fetch = self.fetch()
        status, rules = guard.checked_rules(self.skill, fetch)
        self.assertEqual(status["status"], "current")
        self.assertEqual(status["version"], self.lock["version"])
        self.assertEqual(rules, (self.skill / "rules.md").read_text(encoding="utf-8"))
        self.assertEqual(fetch.call_args_list[0].args, ("releases/latest",))
        self.assertEqual(fetch.call_count, 2)

    def test_aucun_succes_anterieur_ne_couvre_utilisation_suivante(self) -> None:
        fetch = Mock(side_effect=[self.release, self.reference,
                                  {**self.release, "tag_name": "v999.0.0"}])
        guard.checked_rules(self.skill, fetch)
        with self.assertRaisesRegex(ValueError, "Version obsolète"):
            guard.checked_rules(self.skill, fetch)
        self.assertEqual(fetch.call_count, 3)

    def test_tag_annote_resolu_au_commit_exact(self) -> None:
        tag = {"ref": self.reference["ref"], "object": {"type": "tag", "sha": "a" * 40}}
        fetch = Mock(side_effect=[self.release, tag, {"object": self.reference["object"]}])
        status, _ = guard.checked_rules(self.skill, fetch)
        self.assertEqual(status["commit"], self.lock["commit"])
        self.assertEqual(fetch.call_args_list[-1].args, ("git/tags/" + "a" * 40,))

    def test_version_plus_recente_refusee_avant_chargement(self) -> None:
        fetch = Mock(return_value={**self.release, "tag_name": "v999.0.0"})
        with self.assertRaisesRegex(ValueError, "Version obsolète"):
            guard.checked_rules(self.skill, fetch)
        self.assertEqual(fetch.call_count, 1)

    def test_tag_deplace_refuse_meme_si_version_identique(self) -> None:
        self.reference["object"]["sha"] = "b" * 40
        with self.assertRaisesRegex(ValueError, "Commit de la release"):
            guard.checked_rules(self.skill, self.fetch())

    def test_fichiers_modifies_refuses_avant_reseau(self) -> None:
        for name in ("rules.md", "LICENSE"):
            with self.subTest(file=name):
                path = self.skill / name
                original = path.read_bytes()
                path.write_bytes(original + b"\nmodification\n")
                fetch = self.fetch()
                with self.assertRaisesRegex(ValueError, "Fichier installé modifié"):
                    guard.checked_rules(self.skill, fetch)
                fetch.assert_not_called()
                path.write_bytes(original)

    def test_reponse_incomplete_ou_non_stable_refusee(self) -> None:
        for release in ({}, {**self.release, "draft": True},
                        {**self.release, "prerelease": True},
                        {**self.release, "draft": "false"}):
            with self.subTest(release=release):
                with self.assertRaises((ValueError, KeyError)):
                    guard.checked_rules(self.skill, Mock(return_value=release))

    def test_main_ne_divulgue_aucune_regle_si_verification_impossible(self) -> None:
        errors = [TimeoutError(), URLError("réseau indisponible"),
                  HTTPError("https://api.github.com/", 403, "quota", None, None),
                  HTTPError("https://api.github.com/", 404, "absent", None, None),
                  HTTPError("https://api.github.com/", 429, "limite", None, None),
                  ValueError("Version obsolète"), KeyError("tag_name")]
        for error in errors:
            with self.subTest(error=type(error).__name__), \
                 patch.object(guard, "SKILL", self.skill), \
                 patch.object(guard, "github_json", side_effect=error), \
                 contextlib.redirect_stdout(io.StringIO()) as stdout, \
                 contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(guard.main(), 1)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("PONYTAIL BLOQUÉ", stderr.getvalue())

    def test_main_affiche_regles_apres_succes_uniquement(self) -> None:
        with patch.object(guard, "SKILL", self.skill), \
             patch.object(guard, "github_json", self.fetch()), \
             contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(guard.main(), 0)
        first_line, rules = stdout.getvalue().split("\n", 1)
        self.assertEqual(json.loads(first_line)["status"], "current")
        self.assertEqual(rules.rstrip(), (self.skill / "rules.md").read_text(encoding="utf-8").rstrip())

    def test_ponytail_reste_hors_distribution_metier(self) -> None:
        upstreams = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))["skills"]
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertNotIn("ponytail", upstreams)
        self.assertFalse((ROOT / "skills/ponytail").exists())
        self.assertEqual(manifest["skills"], "./skills/")
