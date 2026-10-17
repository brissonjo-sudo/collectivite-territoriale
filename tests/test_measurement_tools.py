"""Contre-épreuves de smoke et d'assemblage, sans processus modèle/installation."""
from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import measurement_common as common
import assemble_release_evidence as assembly
import run_codex_smoke as smoke
import review_codex_campaign as reviewer
import check_dcp_protocol
import run_plugin_campaign as legacy_campaign
from qualify_distribution import current_distribution_errors, distribution_errors

COMMIT = "58495cebd7f49e68d6d4d048208f1172d3e14dbd"


class MeasurementToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="t43-fixtures-synthetiques-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def write(self, name: str, value: dict) -> Path:
        path = self.directory / name
        common.write_new(path, common.seal(value))
        return path

    def test_smoke_dry_run_deux_phases_aucun_processus_ni_ecriture(self) -> None:
        for phase in ("install", "run"):
            destination = self.directory / phase
            argv = ["smoke", "--plugin-commit", COMMIT, "--output-dir", str(destination), "--phase", phase, "--dry-run"]
            stream = io.StringIO()
            with patch.object(sys, "argv", argv), patch.object(smoke.subprocess, "run") as call, \
                 patch.object(smoke.subprocess, "Popen") as popen, contextlib.redirect_stdout(stream):
                self.assertEqual(smoke.main(), 0)
            call.assert_not_called(); popen.assert_not_called()
            data = json.loads(stream.getvalue())
            self.assertTrue(data["dry_run"] and data["synthetic"])
            self.assertEqual(data["model_cases"], ["activation-implicite", "mcp-installe"])
            self.assertFalse(destination.exists())

    def test_smoke_sans_autorisation_refuse_avant_tout_processus(self) -> None:
        argv = ["smoke", "--plugin-commit", COMMIT, "--output-dir", str(self.directory / "no")]
        with patch.object(sys, "argv", argv), patch.object(smoke.subprocess, "run") as call, \
             patch.object(smoke.subprocess, "Popen") as popen, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(smoke.main(), 2)
        call.assert_not_called(); popen.assert_not_called()

    def test_smoke_deux_demandes_distinctes_et_activation_implicite(self) -> None:
        first = smoke.smoke_prompt(ROOT, "activation-implicite")
        second = smoke.smoke_prompt(ROOT, "mcp-installe")
        self.assertNotEqual(first, second)
        self.assertNotIn("dcp-fpt", first)
        self.assertNotIn("recherche-juridique", first)
        self.assertIn("Récupère effectivement une source officielle", second)

    def test_lanceur_Claude_historique_refuse_v2_avant_tout_cas(self) -> None:
        destination = self.directory / "claude-ne-doit-pas-ecrire"
        with patch.object(sys, "argv", ["legacy", "--output-dir", str(destination)]), \
             patch.object(legacy_campaign, "execute") as call, contextlib.redirect_stderr(io.StringIO()), \
             self.assertRaises(SystemExit) as error:
            legacy_campaign.main()
        self.assertEqual(error.exception.code, 2)
        call.assert_not_called()
        self.assertFalse(destination.exists())

    def test_visibilite_ne_se_deduit_pas_des_fichiers(self) -> None:
        installed = self.directory / "plugin"
        (installed / "skills/dsi-fpt").mkdir(parents=True)
        path = installed / "skills/dsi-fpt/SKILL.md"; path.write_text("fixture sans droit\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "non visibles"):
            smoke.verify_visible({"data": []}, installed, {"dsi-fpt"})
        good = {"data": [{"skills": [{"name": "dsi-fpt", "path": str(path), "enabled": True}]}]}
        self.assertEqual(smoke.verify_visible(good, installed, {"dsi-fpt"}), ["collectivite-territoriale:dsi-fpt"])
        good["data"][0]["skills"][0]["path"] = str(self.directory / "ailleurs/SKILL.md")
        with self.assertRaises(ValueError):
            smoke.verify_visible(good, installed, {"dsi-fpt"})

    def test_client_metadonnees_ne_demande_ni_thread_tour_ni_OAuth(self) -> None:
        process = Mock()
        process.stdin = io.StringIO()
        process.stdout = io.StringIO('{"id":1,"result":{}}\n{"id":2,"result":{"data":[]}}\n')
        with patch.object(smoke.subprocess, "Popen", return_value=process):
            self.assertEqual(smoke.visible_skills("cli-factice", {}, self.directory), {"data": []})
        sent = [json.loads(line)["method"] for line in process.stdin.getvalue().splitlines()]
        self.assertEqual(sent, ["initialize", "initialized", "skills/list"])
        process.terminate.assert_called_once()

    def test_demande_interactive_metadonnees_refusee(self) -> None:
        process = Mock()
        process.stdin = io.StringIO()
        process.stdout = io.StringIO('{"id":9,"method":"mcpServer/elicitation/request","params":{}}\n')
        with patch.object(smoke.subprocess, "Popen", return_value=process), self.assertRaises(ValueError):
            smoke.visible_skills("cli-factice", {}, self.directory)
        self.assertNotIn("oauth/login", process.stdin.getvalue())
        process.terminate.assert_called_once()

    def test_lecture_installee_tronquee_ou_hors_cache_refusee(self) -> None:
        installed = self.directory / "cache"
        path = installed / "skills/dcp-fpt/SKILL.md"; path.parent.mkdir(parents=True)
        path.write_text("fixture\nseconde ligne\n", encoding="utf-8", newline="\n")
        event = {"type": "item.completed", "item": {"type": "command_execution", "status": "completed", "exit_code": 0,
            "command": f"Get-Content -LiteralPath '{path}' -Encoding utf8", "aggregated_output": "fixture\nseconde ligne\n"}}
        reads = smoke.read_events([event], installed)
        self.assertTrue(smoke.complete_entry(reads, "dcp-fpt"))
        event["item"]["aggregated_output"] = "fixture"
        with self.assertRaisesRegex(ValueError, "tronquée"):
            smoke.read_events([event], installed)
        event["item"]["command"] += "; Write-Output interdit"
        with self.assertRaisesRegex(ValueError, "hors contrat"):
            smoke.read_events([event], installed)

    def test_fixture_dryrun_et_provenance_absente_refusees(self) -> None:
        for index, origin in enumerate(({"kind": "real_cli", "synthetic": True, "dry_run": False},
             {"kind": "real_cli", "synthetic": False, "dry_run": True}, {},
             {"kind": "synthetic", "synthetic": False, "dry_run": False})):
            path = self.write(f"fixture-{index}.json", {"plugin_commit": COMMIT, "origin": origin})
            with self.subTest(origin=origin), self.assertRaisesRegex(ValueError, "synthétique"):
                common.checked(path, COMMIT, {"real_cli"})

    def test_commit_different_refuse(self) -> None:
        path = self.write("autre-commit.json", {"plugin_commit": COMMIT, "origin": {"kind": "synthetic"}})
        with self.assertRaisesRegex(ValueError, "Commit"):
            common.checked(path, "0" * 40, {"real_cli"})

    def test_fixture_reetiquetee_reelle_sans_recu_refusee(self) -> None:
        path = self.write("pseudo-reelle.json", {"plugin_commit": COMMIT,
            "origin": {"kind": "real_cli", "synthetic": False, "dry_run": False}})
        with self.assertRaisesRegex(ValueError, "Reçu CLI réel incomplet"):
            common.checked(path, COMMIT, {"real_cli"})

    def test_simulateur_non_admis_comme_CLI_reelle(self) -> None:
        path = self.directory / "codex-synthetique.exe"
        path.write_bytes(b"fixture de simulateur, pas une CLI fournisseur")
        with patch.object(common.subprocess, "run") as call, self.assertRaisesRegex(ValueError, "CLI différente"):
            common.run_cli([str(path), "exec"], "fixture", self.directory, 1)
        call.assert_not_called()

    def test_sortie_alteree_octets_et_champs_refusee(self) -> None:
        path = self.write("altere.json", {"plugin_commit": COMMIT, "origin": {"kind": "real_cli", "synthetic": False, "dry_run": False}})
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "Octets"):
            common.checked(path, COMMIT, {"real_cli"})
        data = json.loads(path.read_bytes()); data["plugin_commit"] = "0" * 40
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
        with self.assertRaisesRegex(ValueError, "Empreinte"):
            common.checked(path, "0" * 40, {"real_cli"})

    def test_lien_altere_ou_traversee_refuse(self) -> None:
        source = self.directory / "texte.txt"; source.write_text("fixture", encoding="utf-8")
        link = common.binding(source, self.directory)
        source.write_text("modifie", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "altérée"):
            common.bound(self.directory, link)
        for path in ("../texte.txt", str(source), "C:/fixture", "x:y", "x/../texte.txt"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                common.bound(self.directory, {"evidence_path": path, "sha256": "0"*64})

    def test_run_manquant_refuse_sans_ecrire_de_release(self) -> None:
        cases = json.loads((ROOT / "tests/cas-plugin.json").read_bytes())
        summary = {"plugin_commit": COMMIT, "origin": {"kind": "synthetic"}, "runs": [{"case_id": c["id"]} for c in cases[:-1]]}
        self.write("summary.json", summary)
        with self.assertRaisesRegex(ValueError, "run manque"):
            assembly.campaign_inputs(ROOT, COMMIT, self.directory, {})
        self.assertFalse((self.directory / "tests/evidence/release-1.3.0.json").exists())

    def test_18_runs_synthetiques_ne_deviennent_pas_mesure(self) -> None:
        cases = json.loads((ROOT / "tests/cas-plugin.json").read_bytes())
        self.write("summary.json", {"plugin_commit": COMMIT,
            "origin": {"kind": "real_campaign", "synthetic": True, "dry_run": False},
            "runs": [{"case_id": c["id"]} for c in cases]})
        with self.assertRaisesRegex(ValueError, "synthétique"):
            assembly.campaign_inputs(ROOT, COMMIT, self.directory, {})

    def test_DCP_absent_refuse_avant_assemblage(self) -> None:
        destination = self.directory / "release"
        with self.assertRaisesRegex(ValueError, "DCP absente"):
            assembly.assemble(ROOT, COMMIT, self.directory, self.directory / "smoke.json", None, self.directory, destination)
        self.assertFalse(destination.exists())

    def test_pin_DCP_ne_permet_pas_de_declarer_un_juge_Claude_high(self) -> None:
        path = self.write("dcp.json", {"plugin_commit": COMMIT,
            "origin": {"kind": "real_dcp", "synthetic": False, "dry_run": False}})
        with self.assertRaisesRegex(ValueError, "Protocole DCP bloqué"):
            assembly.dcp_input(path, COMMIT, {}, "129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498")

    def test_diagnostic_DCP_sans_modele_et_sans_substitution(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), patch.object(common.subprocess, "run") as call:
            self.assertEqual(check_dcp_protocol.main(), 2)
        call.assert_not_called()
        result = json.loads(stream.getvalue())
        self.assertFalse(result["compatible"])
        self.assertFalse(result["model_called"])
        self.assertEqual(result["requested_judge"], {"engine": "claude", "model": "claude-opus-5-5", "effort": "high"})

    def test_qualificateur_inchange_refuse_fixture_sans_preuve_assemblee(self) -> None:
        root = self.directory / "fixture-distribution"; (root / ".codex-plugin").mkdir(parents=True)
        (root / ".codex-plugin/plugin.json").write_bytes((ROOT / ".codex-plugin/plugin.json").read_bytes())
        self.assertEqual(current_distribution_errors(root), ["Preuve courante absente : release-1.3.0.json"])
        fake_assembly = {"review": {"human_legal_validation": False}, "release_ready": False,
                         "distribution": {"scope": "open_source", "ready": False, "blockers": ["fixtures sans mesure réelle"]}}
        errors = distribution_errors(root, fake_assembly)
        self.assertIn("Distribution non déclarée prête", errors)
        self.assertTrue(errors)

    def test_relecture_ne_perd_aucun_invariant_et_n_invente_pas_statut(self) -> None:
        good = {"invariants": [{"invariant": "STOP", "statut": "non_verifiable", "motif": "fixture sans trace"}]}
        reviewer.validate_report(good, ["STOP"])
        for mutation in ({"invariants": []}, {"invariants": good["invariants"]*2},
                         {"invariants": [{"invariant": "STOP", "statut": "valide_humain", "motif": "fixture"}]}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                reviewer.validate_report(mutation, ["STOP"])

    def test_sorties_dans_candidat_ou_existantes_refusees(self) -> None:
        with self.assertRaisesRegex(ValueError, "candidat"):
            common.output_outside(ROOT, ROOT / "tests/evidence/interdit-L9")
        with self.assertRaisesRegex(ValueError, "existante"):
            common.output_outside(ROOT, self.directory)


if __name__ == "__main__":
    unittest.main()
