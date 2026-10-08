"""Intégrité du correctif et séparation entre essai, mesure et avis humain."""
import hashlib
import json
import subprocess
import sys
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_codex_campaign as campaign
import audit_native_reads as read_audit
from support_preuves_historiques import runtime_at, files_at


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class PreuvesCorrectifTests(unittest.TestCase):
    def test_neuf_cas_et_tous_les_essais_lies_au_protocole_fige(self):
        summary = load("tests/evidence/2026-10-07-codex-natif-v3/summary.json")
        cases = {c["id"]:c for c in campaign.load_cases()}
        self.assertEqual(summary["case_count"], len(cases))
        self.assertEqual({r["case_id"] for r in summary["runs"]}, set(cases))
        self.assertEqual(len(summary["runs"]), len(cases))
        runtime = runtime_at(ROOT, summary["plugin_commit"])
        # Les plans de lecture et sélections restent ceux des octets mesurés.
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        frozen = Path(temporary.name)
        for name, content in files_at(ROOT, summary["plugin_commit"]).items():
            target = frozen / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        for module in (campaign, read_audit):
            context = patch.object(module, "ROOT", frozen)
            context.start()
            self.addCleanup(context.stop)
        runner = subprocess.run(["git","show",summary["plugin_commit"]+":scripts/run_codex_campaign.py"],
            cwd=ROOT,check=True,capture_output=True).stdout
        self.assertEqual(hashlib.sha256(runner).hexdigest(),summary["runner_sha256"])
        validator = subprocess.run(["git","show",summary["verification_commit"]+":scripts/run_codex_campaign.py"],
            cwd=ROOT,check=True,capture_output=True).stdout
        self.assertEqual(hashlib.sha256(validator).hexdigest(),summary["validator_sha256"])
        audit_path = ROOT / summary["audit_evidence_path"]
        self.assertEqual(hashlib.sha256(audit_path.read_bytes()).hexdigest(),summary["audit_evidence_sha256"])
        verification = json.loads(audit_path.read_text(encoding="utf-8"))
        commands = load("tests/evidence/2026-10-07-codex-natif-v3/diagnostic-lectures.json")
        observed = {}
        for attempt in summary["attempts"]:
            path = ROOT / attempt["evidence_path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), attempt["evidence_sha256"])
            evidence = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(evidence["runtime_sha256"], runtime)
            self.assertEqual(evidence["runner_sha256"], summary["runner_sha256"])
            self.assertEqual(evidence["profile"], summary["profile"])
            case = cases[attempt["case_id"]]
            expected = hashlib.sha256(json.dumps(case,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            self.assertEqual(evidence["case_sha256"], expected)
            errors = campaign.failures(evidence["events"], case, evidence["process_exit"], evidence["profile"])
            self.assertEqual(errors,evidence["failures"])
            self.assertEqual(attempt["technical_status"], "failed" if errors else "passed")
            self.assertFalse(evidence["human_legal_validation"])
            observed[attempt["evidence_path"]] = attempt
        for run in summary["runs"]:
            attempt = observed[run["evidence_path"]]
            self.assertEqual(run["evidence_sha256"],attempt["evidence_sha256"])
            self.assertEqual(run["original_technical_status"],attempt["technical_status"])
            evidence = load(run["evidence_path"])
            verified,errors = read_audit.audit(evidence,commands[run["case_id"]])
            record = next(r for r in verification["runs"] if r["case_id"]==run["case_id"])
            self.assertEqual(record["verified_reference_slices"],verified)
            self.assertEqual(record["remaining_failures"],errors)
            self.assertEqual(run["technical_status"], "failed" if errors else "passed")
            self.assertFalse(run["human_invariants_reviewed"])
        self.assertEqual(summary["technical_passed_count"],sum(r["technical_status"]=="passed" for r in summary["runs"]))
        self.assertEqual(summary["initial_technical_passed_count"],sum(a["technical_status"]=="passed" for a in summary["attempts"] if a["attempt"]==1))
        self.assertFalse(summary["human_legal_validation"])
        self.assertFalse(summary["publication_ready"])

    def test_mesure_autonome_historique_sans_transfert_au_candidat(self):
        evidence = load("tests/evidence/2026-10-07-correctif/dcp-autonome.json")
        upstream = load("upstream.json")["skills"]["dcp-fpt"]
        source = load("tests/evidence/2026-10-07-codex-natif-v3/summary.json")["plugin_commit"]
        upstream_old = json.loads(subprocess.run(["git", "show", source+":upstream.json"], cwd=ROOT,
            check=True, capture_output=True).stdout)["skills"]["dcp-fpt"]
        self.assertEqual(evidence["upstream_runtime_commit"],upstream_old["commit"])
        runtime = {name.removeprefix("skills/dcp-fpt/"):digest
            for name, digest in runtime_at(ROOT, source).items()
            if name.startswith("skills/dcp-fpt/") and not name.endswith("/LICENSE")}
        self.assertEqual(evidence["summary"]["runtime_sha256"],runtime)
        serialized = json.dumps(evidence["summary"],ensure_ascii=False,indent=2)+"\n"
        self.assertEqual(hashlib.sha256(serialized.encode()).hexdigest(),evidence["source_summary_sha256"])
        self.assertEqual(evidence["summary"]["case_count"],28)
        self.assertFalse(evidence["summary"]["publication_ready"])
        self.assertFalse(evidence["human_legal_validation"])

    def test_essai_tronque_v2_reste_partiel_et_non_qualifie(self):
        folder = "tests/evidence/2026-10-07-codex-natif-v2/"
        summary = load(folder+"summary-essai.json")
        self.assertEqual(summary["status"],"essai_arrete_restitution_modele_non_attestee")
        self.assertLess(summary["completed_count"],summary["planned_case_count"])
        self.assertEqual(summary["completed_count"],len(summary["runs"]))
        for run in summary["runs"]:
            self.assertEqual(hashlib.sha256((ROOT/(folder+run["case_id"]+".json")).read_bytes()).hexdigest(),run["evidence_sha256"])
        self.assertFalse(summary["human_legal_validation"])
        self.assertFalse(summary["publication_ready"])
