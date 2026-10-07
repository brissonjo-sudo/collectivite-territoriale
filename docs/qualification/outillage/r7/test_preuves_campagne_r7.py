"""Contre-exemples de provenance et d’exécution interrompue pour la mesure r7."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import preuves_campagne_r7 as proofs
import verifier_archive_r7 as archive


def attempt(message: str, *, success: bool = False) -> list[dict]:
    return [{'type': 'result', 'is_error': not success,
        'subtype': 'success' if success else 'error_during_execution', 'result': message},
        {'type': 'technical_assessment', 'process_exit': 0 if success else 1,
        'status': 'passed' if success else 'failed'}]


class ExecutionTests(unittest.TestCase):
    def test_actual_quota_message_kept_without_hardcoded_reset(self):
        message = "You've hit your session limit · resets 10pm (Europe/Paris)"
        self.assertEqual(proofs.execution_scope(attempt(message)), ('quota_interrupted', message))

    def test_nonquota_error_cannot_be_counted_as_completed(self):
        self.assertEqual(proofs.execution_scope(attempt('ECONNRESET retry failed')),
            ('execution_failed', 'ECONNRESET retry failed'))

    def test_completed_answer_containing_quota_words_remains_answer(self):
        self.assertEqual(proofs.execution_scope(attempt(
            "You've hit your session limit · resets demain", success=True)), ('completed_response', None))

    def test_boolean_exit_and_duplicate_results_rejected(self):
        value = attempt('ECONNRESET')
        value[-1]['process_exit'] = True
        with self.assertRaises(ValueError):
            proofs.execution_scope(value)
        value = attempt('ECONNRESET')
        value.insert(0, copy.deepcopy(value[0]))
        with self.assertRaises(ValueError):
            proofs.execution_scope(value)

    def test_partial_and_unattested_error_rejected(self):
        with self.assertRaises(ValueError):
            proofs.execution_scope(attempt('ECONNRESET')[:-1])
        value = attempt('ECONNRESET')
        value[0]['is_error'] = False
        with self.assertRaises(ValueError):
            proofs.execution_scope(value)

    def test_quota_never_exported_to_judge(self):
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp)
            run = candidate / 'run'
            run.mkdir()
            (candidate / 'tests').mkdir()
            (candidate / 'tests/cas-coactivation-v2.json').write_text('[{"id":"quota-case"}]')
            (run / 'quota-case.jsonl').write_text(''.join(json.dumps(event) + '\n'
                for event in attempt("You've hit your session limit · resets 10pm (Europe/Paris)")))
            with patch.object(proofs, 'CANDIDATE', candidate), patch.object(proofs, 'RUN', run), \
                    patch.object(proofs.raw, 'export_packet') as exporter:
                result = proofs.export_finished()
            exporter.assert_not_called()
            self.assertEqual(result['new_exports'], 0)
            self.assertFalse((run / 'juges').exists())


class ProvenanceTests(unittest.TestCase):
    def test_discovery_uses_metadata_even_if_filename_differs(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            meta = {'type': 'session_meta', 'payload': {'id': 'real-id', 'source': 'vscode'}}
            (directory / 'unexpected-name.jsonl').write_text(json.dumps(meta) + '\n')
            sessions = proofs.native_inventory((directory,))
            self.assertEqual(sessions['real-id'][0].name, 'unexpected-name.jsonl')
            (directory / 'duplicate.jsonl').write_text(json.dumps(meta) + '\n')
            with self.assertRaises(ValueError):
                proofs.native_inventory((directory,))

    def test_parent_must_match_self_native_session(self):
        own = {'id': 'own', 'source': {'subagent': {'thread_spawn': {
            'agent_path': proofs.SELF_AGENT, 'parent_thread_id': 'root-real'}}}}
        sessions = {'own': (Path('own.jsonl'), own),
            'root-real': (Path('real.jsonl'), {'id': 'root-real', 'source': 'vscode'})}
        self.assertEqual(proofs.discover_parent(sessions), ('root-real', Path('real.jsonl')))
        del sessions['root-real']
        with self.assertRaises(ValueError):
            proofs.discover_parent(sessions)

    def test_raw_export_requires_current_hash_and_exact_projection(self):
        current = archive.historical.digest(Path(proofs.raw.__file__))
        value = {'raw_adapter_sha256': current, 'raw_projection': proofs.raw.PROJECTION,
            'compact_packet': True, 'external_read_output_tokens': 55000}
        archive.check_current_raw_export(value)
        old = archive.historical.digest(proofs.ROOT / 'lie_jugements_corriges_bruts-export-02c.py')
        self.assertNotEqual(old, current)
        for invalid in (old, 'not-a-sha', '', None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                archive.check_current_raw_export(dict(value, raw_adapter_sha256=invalid))
        with self.assertRaises(ValueError):
            archive.check_current_raw_export(dict(value, raw_projection='synthetic'))

    def test_r6_gate_rejects_without_calling_or_replacing_historical_checker(self):
        original = archive.historical.check_raw_export_adapter
        with patch.object(archive.historical, 'load', return_value={
                'coactivation_run': 'campagne-r6', 'frozen_manifest': 'gel-r6.json'}), \
                patch.object(archive.historical, 'main') as main:
            with self.assertRaises(ValueError):
                archive.main()
        main.assert_not_called()
        self.assertIs(archive.historical.check_raw_export_adapter, original)

    def test_r7_checker_restored_even_when_replay_fails(self):
        original = archive.historical.check_raw_export_adapter
        def fail():
            self.assertIs(archive.historical.check_raw_export_adapter, archive.check_current_raw_export)
            raise ValueError('preuve native altérée')
        with patch.object(archive.historical, 'load', return_value={
                'coactivation_run': 'campagne-r7', 'frozen_manifest': 'gel-r7.json'}), \
                patch.object(archive.historical, 'main', side_effect=fail):
            with self.assertRaisesRegex(ValueError, 'preuve native altérée'):
                archive.main()
        self.assertIs(archive.historical.check_raw_export_adapter, original)


if __name__ == '__main__':
    unittest.main()
