"""Frontières de portabilité R5 : paramètres absents, divergents ou hérités."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import r5_portable as portable


class PortableParametersTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source-fictive"
        self.source.mkdir()
        self.cli = self.root / "cli-fictif"
        self.cli.write_bytes(b"fixture non executable")
        state = self.root / "etat-futur"
        self.settings = dict(source_root=self.source, candidate_commit="d" * 40,
                             state_root=state, installed_path=state / "cache-futur",
                             cli=self.cli, cli_sha256=portable.sha(self.cli.read_bytes()),
                             cli_version="codex-cli fixture")

    def test_parametres_manquants_refuses_sans_detection_implicite(self):
        for key in self.settings:
            with self.subTest(key=key), patch.object(portable, "verify_source") as source:
                with self.assertRaises(ValueError):
                    portable.parameters(**{**self.settings, key: None})
                source.assert_not_called()

    def test_cli_divergent_refuse_sans_execution(self):
        self.cli.write_bytes(b"mutation")
        with patch.object(portable.subprocess, "run", side_effect=AssertionError("aucun CLI")):
            with self.assertRaisesRegex(ValueError, "Empreinte CLI divergente"):
                portable.parameters(**self.settings)

    def test_etat_ou_cache_historique_refuse_sans_lecture(self):
        self.settings["state_root"].mkdir()
        with self.assertRaisesRegex(ValueError, "État neuf requis"):
            portable.parameters(**self.settings)

    def test_cache_hors_etat_refuse(self):
        self.settings["installed_path"] = self.root / "ailleurs"
        with self.assertRaisesRegex(ValueError, "Cache candidat hors état"):
            portable.parameters(**self.settings)

    def test_candidat_different_de_HEAD_refuse(self):
        with patch.object(portable, "git", return_value=b"autre-candidat\n") as git:
            with self.assertRaisesRegex(ValueError, "Commit candidat différent"):
                portable.verify_source(self.source, "d" * 40)
            self.assertEqual(git.call_count, 1)

    def test_candidat_modifie_refuse(self):
        with patch.object(portable, "git", side_effect=[b"d" * 40 + b"\n", b" M fichier\n"]):
            with self.assertRaisesRegex(ValueError, "Racine source modifiée"):
                portable.verify_source(self.source, "d" * 40)

    def test_identite_et_candidat_explicites_sans_appel_cli(self):
        with patch.object(portable, "git", side_effect=[b"d" * 40 + b"\n", b"", b"e" * 40 + b"\n"]) as git:
            result = portable.parameters(**self.settings)
        self.assertEqual(result["candidate_commit"], "d" * 40)
        self.assertEqual(result["candidate_tree"], "e" * 40)
        self.assertEqual([call.args[1] for call in git.call_args_list], ["rev-parse", "status", "rev-parse"])
        self.assertFalse(self.settings["state_root"].exists())

    def test_bundle_sans_empreinte_refuse_avant_clone(self):
        bundle = self.root / "fixture.bundle"
        bundle.write_bytes(b"pas un bundle")
        manifest = Path(__file__).resolve().parents[1] / "scripts/r5-dependencies.json"
        destination = self.root / "recuperation"
        with patch.object(portable.subprocess, "run", side_effect=AssertionError("aucun clone")):
            with self.assertRaisesRegex(ValueError, "Empreinte bundle"):
                portable.recover(manifest, destination, bundle=bundle)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
