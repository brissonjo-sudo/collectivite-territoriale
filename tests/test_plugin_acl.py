"""ACL L18 : sous-processus simulés, aucune installation, permission ou modèle réel."""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_codex_smoke as smoke
import measurement_common as common

SID = "S-1-5-21-111-222-333-444"
COMMIT = "0b3cd68bdeae135554ca5c663c757f25c14eba01"
RULE = {"rights": 1179817, "inheritance": 3, "propagation": 0, "type": "Allow", "inherited": False}


def state(granted: bool = True) -> dict:
    return {"group_sid": SID, "plugin_rules": [copy.deepcopy(RULE)] if granted else [],
            "home_rules": [], "home_dacl": "D:P(A;;FA;;;SY)"}


class PluginAclTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory(prefix="t43-L18-acl-synthetic-")
        self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name)
        environment = patch.dict(smoke.os.environ, {"SystemRoot": str(self.directory / "synthetic-windows")})
        environment.start(); self.addCleanup(environment.stop)
        self.home = self.directory / "codex-home"
        self.plugin = self.home / "plugins/cache/qualification-l9/collectivite-territoriale/1.3.0"
        self.plugin.mkdir(parents=True)
        patched = patch.object(smoke, "WINDOWS", True)
        patched.start(); self.addCleanup(patched.stop)

    def sequence(self, before=None, after=None, grant_code: int = 0) -> list:
        return [subprocess.CompletedProcess([], 0, json.dumps(state(False) if before is None else before), ""),
                subprocess.CompletedProcess([], grant_code, b"", b""),
                subprocess.CompletedProcess([], 0, json.dumps(state() if after is None else after), "")]

    def grant(self) -> dict:
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence()):
            return smoke.grant_plugin_read(self.plugin, self.home)

    def test_octroi_unique_cible_apres_resolution_groupe_et_acl(self) -> None:
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence()) as process:
            receipt = smoke.grant_plugin_read(self.plugin, self.home)
        self.assertEqual(process.call_count, 3)
        argv = process.call_args_list[1].args[0]
        self.assertEqual(argv, [str(Path(smoke.os.environ["SystemRoot"]) / "System32/icacls.exe"),
                              str(self.plugin.resolve()), "/grant", "*" + SID + ":(OI)(CI)RX"])
        for index in (0, 2):
            query = process.call_args_list[index].args[0][-1]
            self.assertIn("Get-LocalGroup -Name 'CodexSandboxUsers'", query)
            self.assertIn("Get-Acl -LiteralPath", query)
            self.assertNotIn("Set-Acl", query)
            self.assertNotIn("PSMODULEPATH", {key.upper() for key in process.call_args_list[index].kwargs["env"]})
        self.assertTrue(receipt["plugin_acl_verified"])
        self.assertFalse(receipt["home_grant_present"])
        self.assertEqual(receipt["command"], argv)
        self.assertEqual(receipt["target"], str(self.plugin.resolve()))
        self.assertEqual(receipt["process_exit"], 0)

    def test_cibles_hors_plugin_refusees_avant_processus(self) -> None:
        for target in (self.home, self.home / "plugins", self.home / "auth", self.directory,
                       self.plugin.parent, self.plugin / "skills", self.home / "plugins/cache/autre/1.3.0"):
            with self.subTest(target=target), patch.object(smoke.subprocess, "run") as process:
                with self.assertRaisesRegex(ValueError, "hors plugin"):
                    smoke.grant_plugin_read(target, self.home)
                process.assert_not_called()

    def test_redirection_refusee_avant_processus(self) -> None:
        original = getattr(Path, "is_junction", lambda p: False)
        with patch.object(Path, "is_junction", lambda p: p == self.plugin.parent or original(p), create=True), \
                patch.object(smoke.subprocess, "run") as process:
            with self.assertRaisesRegex(ValueError, "redirigée"):
                smoke.grant_plugin_read(self.plugin, self.home)
        process.assert_not_called()

    def test_octroi_home_preexistant_refuse_avant_mutation(self) -> None:
        bad = state(False); bad["home_rules"] = [copy.deepcopy(RULE)]
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence(before=bad)) as process:
            with self.assertRaisesRegex(ValueError, "interdit sur codex-home"):
                smoke.grant_plugin_read(self.plugin, self.home)
        self.assertEqual(process.call_count, 1)

    def test_octroi_home_apres_mutation_refuse(self) -> None:
        bad = state(); bad["home_rules"] = [copy.deepcopy(RULE)]
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence(after=bad)):
            with self.assertRaisesRegex(ValueError, "interdit sur codex-home"):
                smoke.grant_plugin_read(self.plugin, self.home)

    def test_groupe_absent_echec_explicite_aucune_mutation(self) -> None:
        with patch.object(smoke.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "")) as process:
            with self.assertRaisesRegex(ValueError, "Groupe local CodexSandboxUsers absent"):
                smoke.grant_plugin_read(self.plugin, self.home)
        self.assertEqual(process.call_count, 1)

    def test_octroi_echoue_refuse_sans_attestation(self) -> None:
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence(grant_code=5)) as process:
            with self.assertRaisesRegex(ValueError, "Échec de l'octroi"):
                smoke.grant_plugin_read(self.plugin, self.home)
        self.assertEqual(process.call_count, 2)

    def test_octroi_non_present_non_heritable_ou_plus_large_refuse(self) -> None:
        cases = [state(False)]
        for key, value in (("rights", 2032127), ("inheritance", 0), ("propagation", 1),
                           ("inherited", True), ("type", "Deny")):
            bad = state(); bad["plugin_rules"][0][key] = value; cases.append(bad)
        for bad in cases:
            with self.subTest(bad=bad), patch.object(smoke.subprocess, "run", side_effect=self.sequence(after=bad)):
                with self.assertRaisesRegex(ValueError, "non attesté"):
                    smoke.grant_plugin_read(self.plugin, self.home)

    def test_home_dacl_changee_refusee(self) -> None:
        bad = state(); bad["home_dacl"] += "(A;;FA;;;BA)"
        with patch.object(smoke.subprocess, "run", side_effect=self.sequence(after=bad)):
            with self.assertRaisesRegex(ValueError, "ACL codex-home modifié"):
                smoke.grant_plugin_read(self.plugin, self.home)

    def test_aucun_octroi_hors_windows(self) -> None:
        with patch.object(smoke, "WINDOWS", False), patch.object(smoke.subprocess, "run") as process:
            receipt = smoke.grant_plugin_read(self.plugin, self.home)
            smoke.verify_plugin_read({"plugin_acl": receipt}, self.plugin, self.home)
        process.assert_not_called()
        self.assertEqual(receipt, {"platform": "non_windows", "status": "not_applicable", "grant_executed": False})

    def test_run_recu_absent_ou_falsifie_refuse_avant_processus(self) -> None:
        receipt = self.grant()
        cases = [{}, {"plugin_acl": {"status": "not_applicable"}}]
        for key, value in (("target", str(self.home)), ("home_grant_present", True),
                           ("process_exit", 5), ("status", "failed"), ("plugin_acl_verified", False)):
            bad = copy.deepcopy(receipt); bad[key] = value; cases.append({"plugin_acl": bad})
        for bad in cases:
            with self.subTest(bad=bad), patch.object(smoke.subprocess, "run") as process:
                with self.assertRaisesRegex(ValueError, "statut d'installation"):
                    smoke.verify_plugin_read(bad, self.plugin, self.home)
                process.assert_not_called()

    def test_run_relecture_acl_sans_octroi(self) -> None:
        receipt = self.grant()
        with patch.object(smoke.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(state()), "")) as process:
            smoke.verify_plugin_read({"plugin_acl": receipt}, self.plugin, self.home)
        self.assertEqual(process.call_count, 1)
        self.assertNotIn("icacls", process.call_args.args[0][0])

    def test_run_acl_supprimee_ou_home_elargi_refuse(self) -> None:
        receipt = self.grant()
        bad_home = state(); bad_home["home_rules"] = [copy.deepcopy(RULE)]
        for bad in (state(False), bad_home):
            with self.subTest(bad=bad), patch.object(smoke.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(bad), "")):
                with self.assertRaises(ValueError):
                    smoke.verify_plugin_read({"plugin_acl": receipt}, self.plugin, self.home)

    def test_run_commande_sid_ou_dacl_etranger_refuse(self) -> None:
        for key, value in (("command", ["icacls", str(self.home), "/grant", "Everyone:F"]),
                           ("group_sid", SID + "1"), ("home_dacl_sha256", "0"*64)):
            receipt = self.grant(); receipt[key] = value
            with self.subTest(key=key), patch.object(smoke.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(state()), "")):
                with self.assertRaisesRegex(ValueError, "Attestation ACL étrangère"):
                    smoke.verify_plugin_read({"plugin_acl": receipt}, self.plugin, self.home)

    def test_install_consigne_attestation_apres_octets(self) -> None:
        output = self.directory / "installation"
        baseline = {"plugin_commit": COMMIT, "runtime_sha256": {}, "plugin_configuration_sha256": {}}
        actual = {k: baseline[k] for k in ("runtime_sha256", "plugin_configuration_sha256")}
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w"):
            pass
        order = []
        def metadata(argv, environment, workspace):
            if argv[1:3] == ["plugin", "add"]:
                installed = Path(environment["CODEX_HOME"]) / "plugins/cache/qualification-l9/collectivite-territoriale/1.3.0"
                installed.mkdir(parents=True)
                self.plugin = installed; self.home = Path(environment["CODEX_HOME"])
                return {"installedPath": str(installed), "version": "1.3.0"}
            return {}
        def snapshot(installed):
            order.append("bytes_verified"); return actual
        def process(argv, **kwargs):
            if argv[0].lower().endswith("icacls.exe"):
                order.append("grant"); return subprocess.CompletedProcess(argv, 0, b"", b"")
            return subprocess.CompletedProcess(argv, 0, json.dumps(state(granted="grant" in order)), "")
        with patch.object(smoke, "candidate", return_value=baseline), \
                patch.object(smoke, "verify_codex_cli", return_value={"synthetic": True}), \
                patch.object(smoke, "metadata", side_effect=metadata), \
                patch.object(smoke, "main_config_hash", return_value=None), \
                patch.object(smoke, "installed_snapshot", side_effect=snapshot), \
                patch.object(smoke, "fingerprint", return_value="0"*64), \
                patch.object(smoke.subprocess, "check_output", return_value=raw.getvalue()), \
                patch.object(smoke.subprocess, "run", side_effect=process):
            smoke.install(ROOT, COMMIT, "synthetic-cli-not-executable", output)
        prepared = json.loads((output / "prepared.json").read_bytes())
        self.assertLess(order.index("bytes_verified"), order.index("grant"))
        self.assertEqual(prepared["plugin_acl"]["status"], "verified")
        self.assertEqual(prepared["plugin_acl"]["command"][1], str(self.plugin.resolve()))
        self.assertFalse(prepared["model_called"])
        self.assertFalse(prepared["credentials_copied"])

    def test_run_sans_attestation_refuse_avant_login_et_modele(self) -> None:
        env_root = self.directory
        baseline = {"plugin_commit": COMMIT}
        prepared = {**baseline, "environment_path": ".", "installed_path": self.plugin.relative_to(env_root).as_posix(), "cli_sha256": "0"*64}
        with patch.object(smoke, "candidate", return_value=baseline), \
                patch.object(smoke, "checked", return_value=prepared), \
                patch.object(smoke, "verify_codex_cli", return_value={}), \
                patch.object(smoke, "fingerprint", return_value="0"*64), \
                patch.object(smoke.subprocess, "run") as process, patch.object(smoke, "run_cli") as model:
            with self.assertRaisesRegex(ValueError, "statut d'installation"):
                smoke.run(ROOT, COMMIT, "synthetic-cli", self.directory / "mesure", env_root, "no-model", 1)
        process.assert_not_called(); model.assert_not_called()


if __name__ == "__main__":
    unittest.main()
