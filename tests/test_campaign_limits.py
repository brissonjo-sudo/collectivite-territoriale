"""Contre-épreuves des limites du lanceur, sans appel modèle ni réseau."""
import subprocess
import sys
import tempfile
import contextlib
import io
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_plugin_campaign as campaign


class CampaignLimitsTests(unittest.TestCase):
    def test_timeout_ne_fabrique_pas_resultat_et_elimine_raisonnement(self):
        case = campaign.load_cases()[0]
        partial = b'{"type":"assistant","message":{"content":[{"type":"thinking","thinking":"CANARI"}]}}\n'
        with patch.object(campaign.subprocess, "run", side_effect=subprocess.TimeoutExpired("cli", 1, output=partial)) as call:
            clean, exit_code = campaign.execute(case, "cli-factice", timeout=1)
        self.assertEqual(exit_code, 124)
        self.assertEqual(clean, [])
        self.assertEqual(call.call_args.kwargs["timeout"], 1)
        self.assertIn("result_error_or_absent", campaign.technical_failures(clean, case))

    def test_delai_invalide_refuse_avant_tout_appel(self):
        with patch.object(campaign.subprocess, "run") as call:
            with self.assertRaises(ValueError):
                campaign.execute(campaign.load_cases()[0], "cli-factice", timeout=0)
        call.assert_not_called()

    def test_arret_sur_echec_ne_consomme_pas_les_cas_suivants(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ["campagne", "--stop-on-failure", "--output-dir", directory]
            with patch.object(sys, "argv", args), \
                 patch.object(campaign, "load_cases", return_value=campaign.load_cases()[:2]), \
                 patch.object(campaign, "execute", return_value=([], 0)) as call, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(campaign.main(), 1)
            self.assertEqual(call.call_count, 1)
            self.assertEqual(len(list(Path(directory).glob("*.jsonl"))), 1)
