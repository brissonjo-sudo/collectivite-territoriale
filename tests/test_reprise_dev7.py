"""Contre-épreuves de reprise, sans réseau, modèle, authentification ni CLI réel."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/reprise_dev7.py"
spec = importlib.util.spec_from_file_location("reprise", SCRIPT)
reprise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reprise)
portable = reprise.r5_portable


class RepriseFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.legacy = self.root / "sources-publiques-fictives"
        self.legacy.mkdir()
        self.folder = self.root / "outils-recuperes"
        self.cli = self.root / "codex.exe"
        self.cli.write_bytes(b"CLI synthetique non executable")
        self.tool = self.legacy / "harnais.py"
        self.tool.write_bytes(b"# Harnais synthetique sans inference\n")
        self.manifest_path = self.root / "dependencies.json"
        self.manifest = {"schema_version": 1, "source_commit": "a" * 40,
                         "entrypoints": ["harnais"], "modules": [{"module": "harnais", "path": "harnais.py",
                         "commit": "a" * 40, "sha256": reprise.sha(self.tool.read_bytes()),
                         "bytes": len(self.tool.read_bytes()), "imports_publics": []}]}
        self.state = self.root / "etat-neuf-non-cree"
        self.settings = {"source_root": self.legacy, "candidate_commit": "b" * 40,
                         "state_root": self.state, "installed_path": self.state / "installation-nouvelle",
                         "cli": self.cli, "cli_sha256": reprise.sha(self.cli.read_bytes()),
                         "cli_version": "codex-cli fixture"}
        self.source_check = patch.object(portable, "verify_source", return_value="c" * 40)
        self.source_check.start()
        self.addCleanup(self.source_check.stop)
        identity = portable.parameters(**self.settings)
        self.protocol = {"schema_version": "r5-portable-contract-v1", "identity": identity,
                         "status": "non_mesure", "historical_scores_reused": False,
                         "public_tools_sha256": {"harnais.py": reprise.sha(self.tool.read_bytes())},
                         "launcher_sha256": reprise.sha(SCRIPT.read_bytes()),
                         "cases": [{"question": "Question fictive", "oracle": "oracle synthetique separe"}],
                         "permissions": {"sandbox": "read-only", "approval_policy": "never"},
                         "attempts_per_case": 1, "timeout_seconds_per_case": 240, "max_seconds": 5700}
        self.contract_path = self.root / "contrat-synthetique.json"
        self.store_protocol()
        # Sentinelle synthétique : le récupérateur ne lit/copiera jamais ce fichier.
        (self.legacy / "auth.json").write_bytes(b"SENTINELLE SYNTHETIQUE NON SECRETE")

    def tearDown(self):
        self.tmp.cleanup()

    def store_protocol(self):
        self.manifest_path.write_text(json.dumps(self.manifest) + "\n", encoding="utf-8")
        self.contract_path.write_text(json.dumps(self.protocol) + "\n", encoding="utf-8")
        self.contract_sha = reprise.sha(self.contract_path.read_bytes())

    def repository_blob(self, repository, *args):
        self.assertEqual(args[:2], ("cat-file", "blob"))
        name = args[2].split(":", 1)[1]
        return (self.legacy / name).read_bytes()

    def fixture_reprise(self):
        # Aucun initialiser/init, gel ou CLI réel : plan pur puis sources fictives publiques.
        with patch.object(portable, "git", side_effect=self.repository_blob):
            identity = portable.plan(self.manifest_path, self.legacy, self.folder,
                                     self.contract_path, self.contract_sha, SCRIPT, **self.settings)
            portable.recover(self.manifest_path, self.folder, repository=self.legacy)
        return identity

    def checked(self):
        return reprise.charger(self.folder, manifest_path=self.manifest_path,
                                contract_path=self.contract_path, contract_sha256=self.contract_sha,
                                **self.settings)

    def test_cli_supprime_refuse_avant_creation(self):
        self.cli.unlink()
        with self.assertRaisesRegex(ValueError, "CLI explicite absent"):
            self.fixture_reprise()
        self.assertFalse(self.folder.exists())

    def test_outillage_modifie_refuse_avant_creation(self):
        self.tool.write_bytes(b"# Modification\n")
        with self.assertRaisesRegex(ValueError, "Outillage historique divergent"):
            self.fixture_reprise()
        self.assertFalse(self.folder.exists())

    def test_gels_contradictoires_refuses(self):
        self.protocol["public_tools_sha256"] = {"harnais.py": "0" * 64}
        self.store_protocol()
        with self.assertRaisesRegex(ValueError, "Gels contradictoires"):
            self.fixture_reprise()
        self.assertFalse(self.folder.exists())

    def test_traversee_de_chemin_refusee(self):
        self.manifest["modules"][0]["path"] = "../harnais.py"
        self.store_protocol()
        with self.assertRaisesRegex(ValueError, "Outillage historique divergent"):
            self.fixture_reprise()
        self.assertFalse(self.folder.exists())

    def test_reprise_preserve_octets_contrat_et_secrets(self):
        before = {p.relative_to(self.legacy): p.read_bytes() for p in self.legacy.rglob("*") if p.is_file()}
        contract_before = self.contract_path.read_bytes()
        identity = self.fixture_reprise()
        for key in ("candidate_commit", "candidate_tree", "state_root", "installed_path"):
            self.assertEqual(identity[key], self.protocol["identity"][key])
        self.assertNotEqual(identity["candidate_commit"], self.manifest["source_commit"])
        self.assertFalse(identity["model_inference"])
        self.assertFalse(identity["historical_scores_reused"])
        self.assertEqual(contract_before, self.contract_path.read_bytes())
        self.assertEqual({p.name for p in self.folder.iterdir()}, {"harnais.py"})
        self.assertFalse(self.state.exists())
        self.assertEqual(before, {p.relative_to(self.legacy): p.read_bytes() for p in self.legacy.rglob("*") if p.is_file()})

    def test_aucun_remplacement_destination(self):
        self.folder.mkdir()
        (self.folder / "preuve").write_bytes(b"preuve")
        with self.assertRaisesRegex(ValueError, "Destination existante"):
            self.fixture_reprise()
        self.assertEqual((self.folder / "preuve").read_bytes(), b"preuve")

    def test_gel_modifie_bloque_avant_import(self):
        self.fixture_reprise()
        (self.folder / "harnais.py").write_bytes(b"# Mutation\n")
        with patch("importlib.import_module", side_effect=AssertionError("Import interdit")):
            with self.assertRaisesRegex(ValueError, "Gel R5 divergent"):
                self.checked()

    def test_changement_contrat_meme_regelé_bloque(self):
        self.fixture_reprise()
        changed = copy.deepcopy(self.protocol)
        changed["permissions"]["sandbox"] = "danger-full-access"
        self.contract_path.write_text(json.dumps(changed), encoding="utf-8")
        self.contract_sha = reprise.sha(self.contract_path.read_bytes())
        with self.assertRaisesRegex(ValueError, "Contrat de campagne modifié"):
            self.checked()

    def test_adaptation_hash_preserve_sandbox_et_literal(self):
        skill = self.root / "dossier ' cite" / "SKILL.md"
        literal = str(skill).replace("'", "''")
        params = {"command": ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
                  "$ErrorActionPreference='Stop'; (Get-FileHash -LiteralPath '" + literal + "' -Algorithm SHA256).Hash"],
                  "sandboxPolicy": {"type": "readOnly"}, "timeoutMs": 20000, "cwd": str(self.root)}
        changed = reprise.commande_hash_compatible(params, skill)
        self.assertEqual(changed["sandboxPolicy"], params["sandboxPolicy"])
        self.assertEqual(changed["command"][:-1], params["command"][:-1])
        self.assertIn("ReadAllBytes('" + literal + "')", changed["command"][-1])
        self.assertIn("SHA256", changed["command"][-1])
        self.assertIn("Get-FileHash", params["command"][-1])
        changed["sandboxPolicy"] = {"type": "dangerFullAccess"}
        with self.assertRaisesRegex(ValueError, "Commande de précontrôle inattendue"):
            reprise.commande_hash_compatible(changed, skill)

    def test_adaptation_refuse_toute_autre_commande(self):
        params = {"command": ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", "commande differente"],
                  "sandboxPolicy": {"type": "readOnly"}, "timeoutMs": 20000}
        with self.assertRaisesRegex(ValueError, "Commande de précontrôle inattendue"):
            reprise.commande_hash_compatible(params, self.root / "SKILL.md")

    def test_lanceur_different_du_gel_refuse(self):
        self.fixture_reprise()
        alternate = self.root / SCRIPT.name
        alternate.write_bytes(b"# Lanceur modifie\n")
        with patch.object(reprise, "__file__", str(alternate)):
            with self.assertRaisesRegex(ValueError, "lanceur exécuté diffère"):
                self.checked()

    def fake_harness(self, issues):
        self.folder.mkdir()
        cases = [{"case_id": "cas-fictif-1"}, {"case_id": "cas-fictif-2"}]
        self.executed = []

        def execute(run, identifier):
            self.executed.append(identifier)
            return {"native_rollout_sha256": "fixture", "exit_code": 0, "timed_out": False,
                    "capture_overflow": [], "candidate_cache_config_unchanged": True}

        return SimpleNamespace(DEFAULT_RUN=self.folder, verify=lambda run: ({"cases": cases}, {}, {}),
                               bounded_process=lambda: None, execute_case=execute,
                               export_case=lambda run, identifier: {"technical_issues": issues},
                               now=lambda: "date-fictive", write_new=reprise.write_new)

    def test_campagne_arrete_au_premier_echec(self):
        result = reprise.executer(self.fake_harness(["echec_technique_fictif"]))
        self.assertEqual(self.executed, ["cas-fictif-1"])
        self.assertTrue(result["stopped_on_technical_failure"])
        self.assertFalse(result["automatic_retry"])
        self.assertTrue((self.folder / "execution-bilan.json").is_file())

    def test_campagne_ne_repart_pas_apres_un_lancement(self):
        harness = self.fake_harness([])
        reprise.write_new(self.folder / "campagne-start.json", {})
        with self.assertRaisesRegex(ValueError, "Campagne déjà lancée"):
            reprise.executer(harness)
        self.assertEqual(self.executed, [])

    def test_budget_expire_avant_repondant(self):
        harness = self.fake_harness([])
        with patch.object(reprise.time, "monotonic", side_effect=[0, 5701, 5701]):
            result = reprise.executer(harness)
        self.assertEqual(self.executed, [])
        self.assertTrue(result["stopped_on_technical_failure"])
        self.assertEqual(result["max_seconds"], 5700)

    def test_annulation_avant_repondant(self):
        harness = self.fake_harness([])
        (self.folder / "ANNULER").write_bytes(b"")
        result = reprise.executer(harness)
        self.assertEqual(self.executed, [])
        self.assertEqual(result["stop_reason"], ["annulation_avant_prochain_cas"])


if __name__ == "__main__":
    unittest.main()
