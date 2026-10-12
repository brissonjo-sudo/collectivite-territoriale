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


class RepriseFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.legacy = self.root / "historique"
        self.legacy.mkdir()
        self.folder = self.root / "r5"
        self.cli = self.root / "codex.exe"
        self.cli.write_bytes(b"CLI synthetique")
        self.tool = self.legacy / "harnais.py"
        self.tool.write_bytes(b"# Harnais synthetique\n")
        reprise.write_new(self.legacy / "proposition.json", {"candidate_gel_path": str(self.legacy / "source/docs/qualification/gel.json")})
        (self.legacy / "manifest.json").write_bytes(b"{}\n")
        self.protocol = {
            "schema_version": "dev7-native-complete-protocol-v4", "protocol_id": "r4", "status": "non_mesure",
            "immutable_tools_sha256": {"harnais.py": reprise.sha(self.tool.read_bytes())},
            "predecessor_tools_sha256": {}, "new_tools": ["harnais.py"],
            "proposal_path": "proposition.json", "proposal_sha256": reprise.sha((self.legacy / "proposition.json").read_bytes()),
            "r3_manifest_path": "manifest.json", "r3_manifest_sha256": reprise.sha((self.legacy / "manifest.json").read_bytes()),
            "installed_path": str(self.legacy / "state/plugins/cache/catalogue/plugin/version"),
            "cli": "ancien-cli-absent", "cli_version": "ancienne-version", "cli_sha256": "0" * 64,
            "candidate_commit": "candidat-fige", "cases": [{"question": "Question fictive", "oracle": "secret-juge"}],
            "permissions": {"sandbox": "read-only", "approval_policy": "never"}, "attempts_per_case": 1}
        self.store_protocol()
        reprise.write_new(self.legacy / "controle-reprise-efficace-dev7-20261009.json", {"tools_sha256": {}})
        (self.legacy / "auth.json").write_bytes(b"SECRET FICTIF A NE PAS COPIER")

    def tearDown(self):
        self.tmp.cleanup()

    def store_protocol(self):
        p = self.legacy / "protocole-native-dev7-complet-20261009-r4.json"
        p.write_bytes((json.dumps(self.protocol) + "\n").encode())

    def init(self):
        with patch.object(reprise.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, b"codex-cli fixture\n", b"")):
            return reprise.initialiser(self.legacy, self.folder, self.cli)

    def test_cli_supprime_refuse_avant_creation(self):
        self.cli.unlink()
        with self.assertRaisesRegex(ValueError, "CLI explicite absent"):
            self.init()
        self.assertFalse(self.folder.exists())

    def test_outillage_modifie_refuse_avant_creation(self):
        self.tool.write_bytes(b"# Modification\n")
        with self.assertRaisesRegex(ValueError, "Outillage historique divergent"):
            self.init()
        self.assertFalse(self.folder.exists())

    def test_gels_contradictoires_refuses(self):
        self.protocol["predecessor_tools_sha256"] = {"harnais.py": "0" * 64}
        self.store_protocol()
        with self.assertRaisesRegex(ValueError, "Gels contradictoires"):
            self.init()

    def test_traversee_de_chemin_refusee(self):
        self.protocol["immutable_tools_sha256"] = {"../codex.exe": reprise.sha(self.cli.read_bytes())}
        self.store_protocol()
        with self.assertRaisesRegex(ValueError, "Outillage historique divergent"):
            self.init()

    def test_reprise_preserve_octets_contrat_et_secrets(self):
        before = {p.relative_to(self.legacy): p.read_bytes() for p in self.legacy.rglob("*") if p.is_file()}
        identity = self.init()
        successor = reprise.read(self.folder / "protocole-native-dev7-complet-20261012-r5.json")
        for key in ("candidate_commit", "cases", "permissions", "attempts_per_case"):
            self.assertEqual(successor[key], self.protocol[key])
        self.assertEqual(identity["state_root"], str(self.legacy / "state"))
        self.assertFalse(identity["model_inference"])
        self.assertFalse((self.folder / "auth.json").exists())
        self.assertEqual(before, {p.relative_to(self.legacy): p.read_bytes() for p in self.legacy.rglob("*") if p.is_file()})

    def test_aucun_remplacement_destination(self):
        self.folder.mkdir()
        (self.folder / "preuve").write_bytes(b"preuve")
        with self.assertRaisesRegex(ValueError, "Destination existante"):
            self.init()
        self.assertEqual((self.folder / "preuve").read_bytes(), b"preuve")

    def test_gel_modifie_bloque_avant_import(self):
        self.init()
        (self.folder / "harnais.py").write_bytes(b"# Mutation\n")
        with patch.object(reprise.importlib, "import_module", side_effect=AssertionError("Import interdit")):
            with self.assertRaisesRegex(ValueError, "Gel R5 divergent"):
                reprise.charger(self.folder)

    def test_changement_contrat_meme_regelé_bloque(self):
        self.init()
        p = self.folder / "protocole-native-dev7-complet-20261012-r5.json"
        changed = copy.deepcopy(reprise.read(p))
        changed["permissions"]["sandbox"] = "danger-full-access"
        p.write_bytes(json.dumps(changed).encode())
        gel = reprise.read(self.folder / "gel-reprise.json")
        gel[p.name] = reprise.sha(p.read_bytes())
        (self.folder / "gel-reprise.json").write_bytes(json.dumps(gel).encode())
        with self.assertRaisesRegex(ValueError, "Contrat de campagne modifié"):
            reprise.charger(self.folder)

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
        self.init()
        alternate = self.root / SCRIPT.name
        alternate.write_bytes(b"# Lanceur modifie\n")
        with patch.object(reprise, "__file__", str(alternate)):
            with self.assertRaisesRegex(ValueError, "lanceur exécuté diffère"):
                reprise.charger(self.folder)

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
