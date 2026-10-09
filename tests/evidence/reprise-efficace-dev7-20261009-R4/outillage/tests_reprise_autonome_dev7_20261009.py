"""Tests de contrôle du worker : aucun modèle, réseau ou fermeture de processus."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import reprise_autonome_dev7_20261009 as w


class Clock:
    def __init__(self):
        self.value = 0.0

    def monotonic(self):
        return self.value

    def sleep(self, seconds):
        self.value += seconds


class FakeHarness:
    GateError = w.WorkerError
    canonical = staticmethod(lambda value: json.dumps(value, sort_keys=True).encode())

    def __init__(self, root):
        self.root = root
        self.STATE = root / "profil-protege"
        self.STATE.mkdir()
        (self.STATE / "config.toml").write_bytes(b"unchanged")
        self.DEFAULT_RUN = root / "qualification-test"
        self.protocol = {"candidate_commit": "frozen", "cases": [
            {"case_id": "cas-" + str(i)} for i in range(16)]}
        self.prepares = 0
        self.gates = 0
        self.preflights = 0
        self.executions = []
        self.exports = []
        self.waits = 0
        self.unknown = False
        self.cancel_folder = None
        self.cancel_on_preflight = False
        self.fail_at = None
        self.drift = False
        self.clock = None
        self.advance = 0

    def now(self):
        return "2026-10-09T12:00:00+00:00"

    def inputs(self):
        return self.protocol, {"installed_files": {"SKILL.md": "fixed"}}

    def environment(self):
        return {}, []

    def node_gate(self, env):
        self.gates += 1
        if self.unknown:
            raise self.GateError("Chemin ou identité d'un processus Node inaccessible")
        if self.gates <= self.waits:
            raise self.GateError(w.WAITABLE)
        return {"process_inventory_verified": True}

    def prepare(self, run, gate):
        self.prepares += 1
        run.mkdir()
        self.write_new(run / "manifest.json", {})
        (run / "cases").mkdir()
        for case in self.protocol["cases"]:
            (run / "cases" / case["case_id"]).mkdir()

    def verify(self, run):
        return self.protocol, {}, {}

    def preflight(self, *args, **kwargs):
        self.preflights += 1
        if self.cancel_on_preflight:
            (self.cancel_folder / "ANNULER").touch()
        return {"ready": True}

    def execute_case(self, run, identifier, gate):
        gate({}, {}, {}, run)
        self.executions.append(identifier)
        self.write_new(run / "cases" / identifier / "start.json", {})
        if self.clock:
            self.clock.value += self.advance
        if self.drift:
            (self.STATE / "config.toml").write_bytes(b"changed")
        return {"native_rollout_sha256": "frozen", "exit_code": 0,
                "candidate_cache_config_unchanged": identifier != self.fail_at}

    def export_case(self, run, identifier):
        self.exports.append(identifier)
        return {"technical_issues": []}

    @staticmethod
    def write_new(path, value):
        with path.open("x", encoding="utf-8") as stream:
            json.dump(value, stream)


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".tests-worker-dev7-", dir=w.ROOT)
        self.root = Path(self.temp.name)
        self.folder = self.root / "reprise-autonome-dev7-test"
        self.control = self.root / "gel.json"
        self.tools = {}
        for name in w.REQUIRED_TOOLS:
            (self.root / name).write_bytes(name.encode())
            self.tools[name] = w.digest(name.encode())
        self.control.write_text(json.dumps({"tools_sha256": self.tools}), encoding="utf-8")
        self.c = FakeHarness(self.root)
        self.clock = Clock()

    def tearDown(self):
        self.temp.cleanup()

    def run_worker(self, **kwargs):
        return w.run_worker(self.folder, self.c, root=self.root, control=self.control,
                            monotonic=self.clock.monotonic, sleep=self.clock.sleep, **kwargs)

    def test_sixteen_cases_once_after_graceful_close(self):
        self.c.waits = 2
        result = self.run_worker()
        self.assertEqual(result["state"], "packets_ready")
        self.assertEqual(self.c.prepares, 1)
        self.assertEqual(len(self.c.executions), 16)
        self.assertEqual(self.c.exports, self.c.executions)
        self.assertEqual(self.c.gates, 3)
        self.assertFalse(result["automatic_retry"])
        self.assertFalse(result["preexisting_processes_terminated"])
        self.assertTrue(result["candidate_cache_config_tools_unchanged"])
        self.assertTrue((self.c.DEFAULT_RUN / "execution-bilan.json").exists())

    def test_no_replacement_or_second_execution(self):
        self.run_worker()
        with self.assertRaises(FileExistsError):
            self.run_worker()
        second = self.root / "reprise-autonome-dev7-second"
        result = w.run_worker(second, self.c, root=self.root, control=self.control)
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.prepares, 1)
        self.assertEqual(len(self.c.executions), 16)

    def test_wait_timeout_launches_nothing(self):
        self.c.waits = 1000
        result = self.run_worker(waiting_seconds=7)
        self.assertEqual(result["state"], "expired")
        self.assertEqual(self.clock.value, 7)
        self.assertEqual(self.c.prepares, 0)
        self.assertEqual(self.c.executions, [])

    def test_unknown_cim_path_blocks_without_retry(self):
        self.c.unknown = True
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.gates, 1)
        self.assertEqual(self.c.prepares, 0)
        self.assertNotIn("Chemin", json.dumps(result))

    def test_cancel_during_wait_starts_nothing(self):
        self.c.waits = 100
        def cancel(seconds):
            self.clock.sleep(seconds)
            (self.folder / "ANNULER").touch()
        result = w.run_worker(self.folder, self.c, root=self.root, control=self.control,
                              monotonic=self.clock.monotonic, sleep=cancel)
        self.assertTrue(result["cancellation_requested"])
        self.assertEqual(self.c.prepares, 0)

    def test_cancel_after_preflight_prevents_model_start(self):
        self.c.cancel_folder = self.folder
        self.c.cancel_on_preflight = True
        result = self.run_worker()
        self.assertTrue(result["cancellation_requested"])
        self.assertEqual(self.c.preflights, 1)
        self.assertEqual(self.c.executions, [])
        self.assertTrue((self.c.DEFAULT_RUN / "execution-bilan.json").exists())

    def test_first_technical_failure_stops_sequence(self):
        self.c.fail_at = "cas-1"
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.executions, ["cas-0", "cas-1"])

    def test_config_drift_never_reports_success(self):
        self.c.drift = True
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertFalse(result["candidate_cache_config_tools_unchanged"])

    def test_global_deadline_prevents_next_case(self):
        self.c.clock = self.clock
        self.c.advance = 5401
        result = self.run_worker()
        self.assertEqual(result["state"], "expired")
        self.assertEqual(len(self.c.executions), 1)

    def test_tool_hash_drift_blocks_before_native_preflight(self):
        (self.root / "reprise_autonome_dev7_20261009.py").write_bytes(b"changed")
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.gates, 0)
        self.assertEqual(self.c.prepares, 0)

    def test_edit_during_wait_blocks_before_preparation(self):
        self.c.waits = 1
        def edit(seconds):
            self.clock.sleep(seconds)
            (self.root / "reprise_autonome_dev7_20261009.py").write_bytes(b"changed")
        result = w.run_worker(self.folder, self.c, root=self.root, control=self.control,
                              monotonic=self.clock.monotonic, sleep=edit)
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.prepares, 0)

    def test_control_metadata_edit_during_wait_also_blocks(self):
        self.c.waits = 1
        def edit(seconds):
            self.clock.sleep(seconds)
            self.control.write_text(json.dumps({"tools_sha256": self.tools, "changed": True}),
                                    encoding="utf-8")
        result = w.run_worker(self.folder, self.c, root=self.root, control=self.control,
                              monotonic=self.clock.monotonic, sleep=edit)
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.prepares, 0)

    def test_edit_during_preparation_prevents_all_respondents(self):
        original = self.c.prepare
        def edit(run, gate):
            original(run, gate)
            (self.root / "reprise_autonome_dev7_20261009.py").write_bytes(b"changed")
        self.c.prepare = edit
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.executions, [])

    def test_edit_after_rpc_prevents_model_start(self):
        original = self.c.preflight
        def edit(*args, **kwargs):
            receipt = original(*args, **kwargs)
            (self.root / "reprise_autonome_dev7_20261009.py").write_bytes(b"changed")
            return receipt
        self.c.preflight = edit
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.executions, [])

    def test_rpc_timeout_respects_remaining_global_budget(self):
        observed = []
        class Client:
            def __init__(self, *args):
                pass

            def request(self, method, params, timeout):
                observed.append(timeout)
                return {}
        self.c.Client = Client
        def preflight(*args, client_factory, **kwargs):
            self.clock.value = w.MAX_CAMPAIGN_SECONDS - 50
            client = client_factory()
            client.request("mcpServerStatus/list", {}, timeout=999)
            return {}
        self.c.preflight = preflight
        result = self.run_worker()
        self.assertEqual(observed, [30])
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(self.c.executions, [])

    def test_inventory_finishing_after_wait_deadline_does_not_prepare(self):
        def slow_gate(env):
            self.clock.value += 15
        self.c.node_gate = slow_gate
        result = self.run_worker(waiting_seconds=7)
        self.assertEqual(result["state"], "expired")
        self.assertEqual(self.c.prepares, 0)

    def test_started_case_is_counted_if_later_storage_fails(self):
        original = self.c.execute_case
        def fail(run, identifier, gate):
            original(run, identifier, gate)
            raise OSError("private response failed")
        self.c.execute_case = fail
        result = self.run_worker()
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(result["executed_cases"], 1)
        bilan = json.loads((self.c.DEFAULT_RUN / "execution-bilan.json").read_bytes())
        self.assertEqual(bilan["executed_cases"], 1)

    def test_incomplete_tool_gel_rejected(self):
        self.control.write_text('{"tools_sha256":{}}', encoding="utf-8")
        with self.assertRaises(w.WorkerError):
            w.frozen_tools(self.control, self.root)

    def test_protected_and_external_folders_rejected(self):
        for folder in (self.c.STATE, self.root.parent / "reprise-autonome-dev7-other",
                       self.root / "DSI-corrections-pr5"):
            with self.assertRaises(w.WorkerError):
                w.state_destination(folder, self.root)

    def test_log_size_is_bounded(self):
        self.folder.mkdir()
        status = w.Status(self.folder, self.c.now)
        for _ in range(100):
            status.log("x" * 1024)
        self.assertLessEqual((self.folder / "journal.txt").stat().st_size, w.MAX_LOG_BYTES)

    def test_atomic_current_state_and_final_no_secret(self):
        self.folder.mkdir()
        status = w.Status(self.folder, self.c.now)
        status.update("waiting")
        status.update("preflight")
        self.assertEqual(json.loads((self.folder / "etat.json").read_bytes())["state"], "preflight")
        self.assertFalse((self.folder / "etat.tmp").exists())
        record = w.sanitized_error(ValueError("https://auth.example/?token=confidentiel"))
        self.assertNotIn("confidentiel", json.dumps(record))
        self.assertNotIn("https", json.dumps(record))

    def test_os_mutex_rejects_second_worker(self):
        with w.unique_worker(self.root / "lock.private"):
            with self.assertRaises(w.WorkerError):
                with w.unique_worker(self.root / "lock.private"):
                    self.fail("deux workers actifs")
        with w.unique_worker(self.root / "lock.private"):
            pass

    def test_wait_limit_is_validated_before_folder_creation(self):
        for seconds in (0, 901, True):
            with self.assertRaises(w.WorkerError):
                self.run_worker(waiting_seconds=seconds)
        self.assertFalse(self.folder.exists())


if __name__ == "__main__":
    unittest.main()
