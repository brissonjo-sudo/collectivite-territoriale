"""Cycle STOP L22 : traces synthétiques, aucun appel modèle."""
from pathlib import Path
import contextlib
import copy
import io
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from campaign_contract import CYCLE_CASES_FILE, STOP_CYCLE_CASES, load_cycle_cases
from cli_toolchains import MEASUREMENT_D
import run_codex_campaign as campaign
import measurement_common as common
from test_measurement_contract import synthetic_trace


class CycleStopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = load_cycle_cases(ROOT)

    def errors(self, case: dict, events: list[dict]) -> list[str]:
        return campaign.failures(campaign.sanitize(events, chronology=True), case, 0, campaign.PROFILE)

    def test_seuls_trois_cas_migrent_sans_perte_de_prompt_ni_invariant(self) -> None:
        historical = campaign.load_cases()
        self.assertEqual(len(self.cases), 18)
        self.assertEqual([a["id"] for a, b in zip(historical, self.cases) if a != b], list(STOP_CYCLE_CASES))
        for old, new in zip(historical, self.cases):
            self.assertEqual(old["prompt"], new["prompt"])
            self.assertEqual(old["invariants"], new["invariants"])
            if old["id"] in STOP_CYCLE_CASES:
                self.assertEqual(new["schema_version"], 2)
                self.assertIs(new["stop_first"], True)
                self.assertNotIn("stop_first", old)

    def test_chaque_cas_refuse_annonce_avant_STOP(self) -> None:
        for case in self.cases:
            if case["id"] not in STOP_CYCLE_CASES:
                continue
            with self.subTest(case=case["id"]):
                events = synthetic_trace(case)
                self.assertEqual(self.errors(case, events), [])
                events.insert(0, {"type": "item.completed", "item": {
                    "id": "annonce", "type": "agent_message", "text": "Annonce synthétique"}})
                self.assertIn("stop_first_absent", self.errors(case, events))

    def test_chaque_cas_refuse_outil_avant_STOP_et_absence_STOP(self) -> None:
        for case in self.cases:
            if case["id"] not in STOP_CYCLE_CASES:
                continue
            with self.subTest(case=case["id"]):
                events = synthetic_trace(case)
                events.insert(0, {"type": "item.started", "item": {"id": "premier-outil", "type": "command_execution"}})
                self.assertIn("stop_after_tool", self.errors(case, events))
                self.assertIn("stop_first_absent", self.errors(case, synthetic_trace(case)[1:]))

    def test_contrat_abaisse_ou_absent_refuse_sans_repli(self) -> None:
        with tempfile.TemporaryDirectory(prefix="t43-L22-cycle-") as tmp:
            root = Path(tmp)
            for name in ("tests/cas-plugin.json", "upstream.json", CYCLE_CASES_FILE):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            self.assertEqual(load_cycle_cases(root), self.cases)
            for case_id in STOP_CYCLE_CASES:
                bad = copy.deepcopy(self.cases)
                next(c for c in bad if c["id"] == case_id)["stop_first"] = False
                (root / CYCLE_CASES_FILE).write_text(json.dumps(bad), encoding="utf-8")
                with self.subTest(case=case_id), self.assertRaisesRegex(ValueError, "Contrat de cycle différent"):
                    load_cycle_cases(root)
            (root / CYCLE_CASES_FILE).unlink()
            with self.assertRaises(FileNotFoundError):
                load_cycle_cases(root)

    def test_cycle_empreinte_par_outillage_sans_remplacer_historique(self) -> None:
        snapshot = common.snapshot(ROOT)
        self.assertEqual(snapshot["toolchain_sha256"][CYCLE_CASES_FILE], common.fingerprint(ROOT / CYCLE_CASES_FILE))
        self.assertEqual(snapshot["case_file_sha256"], common.fingerprint(ROOT / "tests/cas-plugin.json"))

    def test_entree_campagne_utilise_cycle_en_dry_run_sans_processus(self) -> None:
        stream = io.StringIO()
        # La campagne historique 1.3.0 reste liée à d et à v2 (décision B3).
        argv = ["campagne", "--plugin-commit", MEASUREMENT_D, "--output-dir", "jamais-cree-L22", "--dry-run"]
        with patch.object(sys, "argv", argv), patch.object(campaign, "run_cli") as model, \
                patch.object(campaign.subprocess, "run") as process, contextlib.redirect_stdout(stream):
            self.assertEqual(campaign.main(), 0)
        model.assert_not_called()
        process.assert_not_called()
        result = json.loads(stream.getvalue())
        self.assertEqual(result["case_contract"], CYCLE_CASES_FILE)
        self.assertEqual(result["case_contract_sha256"], common.fingerprint(ROOT / CYCLE_CASES_FILE))
        self.assertEqual(result["sessions"], 18)


if __name__ == "__main__":
    unittest.main()
