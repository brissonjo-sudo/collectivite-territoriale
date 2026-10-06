"""Fixtures synthétiques de liaison : aucun jugement de campagne produit ici."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import lie_jugements_corriges as binder


class BindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.packet = self.root / 'synthetic.packet.json'
        self.judgment = self.root / 'synthetic.jugement.json'
        self.packet_value = {'case_id': 'synthetic', 'trace_sha256': 'a' * 64, 'trace': []}
        self.value = {'case_id': 'synthetic', 'trace_sha256': 'a' * 64, 'verdict': 'bloque',
                      'invariants': {'only': {'status': None, 'basis': 'missing',
                                               'evidence_refs': [], 'rationale': 'Fixture synthétique.'}}}
        self.packet.write_text(json.dumps(self.packet_value), encoding='utf-8')
        self.judgment.write_text(json.dumps(self.value), encoding='utf-8')
        self.agent, self.parent_id = '/root/juge_fixture', 'parent-fixture'
        self.exported_at = '2026-10-06T20:00:00Z'
        spawn = {'agent_path': self.agent, 'parent_thread_id': self.parent_id, 'depth': 1}
        self.native = [
            self.event('20:00:02', 'session_meta', {'id': 'judge-fixture', 'timestamp': '2026-10-06T20:00:02Z',
                       'source': {'subagent': {'thread_spawn': spawn}}}),
            self.event('20:00:03', 'event_msg', {'type': 'task_started', 'turn_id': 'turn-fixture'}),
            self.event('20:00:04', 'turn_context', {'turn_id': 'turn-fixture', 'model': 'model-fixture'}),
            self.call('20:00:05', 'read', self.read_script()),
            self.output('20:00:06', 'read', {'exit_code': 0, 'output': json.dumps(self.packet_value)}),
            self.call('20:00:07', 'write', self.patch_script()),
            self.output('20:00:08', 'write', {}),
            self.event('20:00:09', 'event_msg', {'type': 'task_complete', 'turn_id': 'turn-fixture'})]
        self.parent = [
            self.event('19:00:00', 'session_meta', {'id': self.parent_id}),
            self.event('20:00:01', 'response_item', {'type': 'function_call', 'name': 'spawn_agent',
                'call_id': 'spawn', 'arguments': json.dumps({'task_name': 'juge_fixture', 'fork_turns': 'none'})}),
            self.event('20:00:03', 'response_item', {'type': 'function_call_output', 'call_id': 'spawn',
                'output': json.dumps({'task_name': self.agent})})]

    def event(self, time: str, kind: str, payload: dict) -> dict:
        return {'timestamp': '2026-10-06T' + time + 'Z', 'type': kind, 'payload': payload}

    def call(self, time: str, identifier: str, script: str) -> dict:
        return self.event(time, 'response_item', {'type': 'custom_tool_call', 'name': 'exec',
                                                'call_id': identifier, 'input': script})

    def output(self, time: str, identifier: str, value: dict) -> dict:
        return self.event(time, 'response_item', {'type': 'custom_tool_call_output', 'call_id': identifier,
            'output': [{'type': 'text', 'text': 'Script completed\nOutput:\n'},
                       {'type': 'text', 'text': json.dumps(value)}]})

    def read_script(self) -> str:
        args = {'cmd': f"Get-Content -LiteralPath '{self.packet.resolve()}' -Raw", 'max_output_tokens': 55000}
        return 'text(await tools.exec_command(' + json.dumps(args) + '));'

    def patch_script(self, value: dict | None = None, path: Path | None = None) -> str:
        lines = json.dumps(self.value if value is None else value, indent=2).splitlines()
        patch = '\n'.join(['*** Begin Patch', '*** Add File: ' + str((path or self.judgment).resolve()),
                           *('+' + line for line in lines), '*** End Patch'])
        return 'text(await tools.apply_patch(' + json.dumps(patch) + '));'

    def proof(self, native: list | None = None, parent: list | None = None) -> tuple:
        return binder.native_proof(self.native if native is None else native,
                                   self.parent if parent is None else parent,
                                   self.agent, self.parent_id, self.packet, self.judgment, self.exported_at)

    def test_proof_derives_native_identity_and_full_json(self) -> None:
        proof, trace = self.proof()
        self.assertEqual(proof['session_id'], 'judge-fixture')
        self.assertEqual(proof['read_call_ids'], ['read'])
        self.assertEqual(proof['write_call_ids'], ['write'])
        self.assertTrue(proof['judge_identity_checked'])
        self.assertEqual(trace[0]['payload']['source']['subagent']['thread_spawn']['agent_path'], self.agent)

    def test_modified_atomic_rationale_is_refused(self) -> None:
        changed = copy.deepcopy(self.value)
        changed['invariants']['only']['rationale'] = 'Autre justification.'
        self.judgment.write_text(json.dumps(changed), encoding='utf-8')
        with self.assertRaisesRegex(binder.BindingError, 'JSON final'):
            self.proof()

    def test_bool_is_not_coerced_to_integer(self) -> None:
        changed = copy.deepcopy(self.value)
        changed['invariants']['only']['status'] = True
        self.native[5] = self.call('20:00:07', 'write', self.patch_script(changed))
        changed['invariants']['only']['status'] = 1
        self.judgment.write_text(json.dumps(changed), encoding='utf-8')
        with self.assertRaises(binder.BindingError):
            self.proof()

    def test_inherited_history_is_refused(self) -> None:
        self.parent[1]['payload']['arguments'] = json.dumps({'task_name': 'juge_fixture', 'fork_turns': 'all'})
        with self.assertRaisesRegex(binder.BindingError, 'sans historique'):
            self.proof()

    def test_old_session_is_refused(self) -> None:
        self.native[0]['payload']['timestamp'] = '2026-10-06T19:59:59Z'
        with self.assertRaisesRegex(binder.BindingError, 'session réutilisée'):
            self.proof()

    def test_second_task_is_refused(self) -> None:
        self.native.append(self.event('20:01:00', 'event_msg', {'type': 'task_started', 'turn_id': 'other'}))
        with self.assertRaisesRegex(binder.BindingError, 'unique exécution'):
            self.proof()

    def test_incomplete_task_is_refused(self) -> None:
        with self.assertRaisesRegex(binder.BindingError, 'unique exécution'):
            self.proof(self.native[:-1])

    def test_truncated_packet_read_is_refused(self) -> None:
        self.native[4] = self.output('20:00:06', 'read', {'exit_code': 0, 'output': '{"case_id":"synthetic"}'})
        with self.assertRaisesRegex(binder.BindingError, 'Lecture hors paquet'):
            self.proof()

    def test_failed_patch_is_refused(self) -> None:
        self.native[6] = self.output('20:00:08', 'write', {'error': 'failed'})
        with self.assertRaisesRegex(binder.BindingError, 'échouée'):
            self.proof()

    def test_second_successful_write_is_refused(self) -> None:
        self.native[7:7] = [self.call('20:00:08', 'write2', self.patch_script()),
                            self.output('20:00:08', 'write2', {})]
        with self.assertRaisesRegex(binder.BindingError, 'uniques'):
            self.proof()

    def test_extra_code_is_not_executed_and_is_refused(self) -> None:
        self.native[5]['payload']['input'] += 'text(await tools.exec_command({"cmd":"evil"}));'
        with self.assertRaises((binder.BindingError, json.JSONDecodeError)):
            self.proof()

    def test_dynamic_patch_argument_is_refused(self) -> None:
        with self.assertRaises((binder.BindingError, json.JSONDecodeError)):
            binder.parse_patch('text(await tools.apply_patch(patchVariable));', self.judgment)

    def test_wrong_destination_is_refused(self) -> None:
        self.native[5]['payload']['input'] = self.patch_script(path=self.root / 'other.json')
        with self.assertRaisesRegex(binder.BindingError, 'destination différente'):
            self.proof()

    def test_duplicate_json_keys_are_refused(self) -> None:
        with self.assertRaisesRegex(binder.BindingError, 'dupliquée'):
            binder._json('{"status":true,"status":false}')

    def test_foreign_tool_is_refused(self) -> None:
        self.native[3]['payload']['name'] = 'web_search'
        with self.assertRaisesRegex(binder.BindingError, 'extérieur'):
            self.proof()

    def test_spawn_output_for_other_agent_is_refused(self) -> None:
        self.parent[2]['payload']['output'] = json.dumps({'task_name': '/root/other'})
        with self.assertRaisesRegex(binder.BindingError, 'spawn non lié'):
            self.proof()

    def test_write_after_task_complete_is_refused(self) -> None:
        self.native.insert(5, self.native.pop())
        with self.assertRaisesRegex(binder.BindingError, 'extérieur à l’exécution'):
            self.proof()

    def test_duplicate_session_metadata_is_refused(self) -> None:
        self.native.append(copy.deepcopy(self.native[0]))
        with self.assertRaisesRegex(binder.BindingError, 'Métadonnées'):
            self.proof()

    def test_duplicate_tool_output_is_refused(self) -> None:
        self.native.insert(7, copy.deepcopy(self.native[6]))
        with self.assertRaisesRegex(binder.BindingError, 'absent ou ambigu'):
            self.proof()

    def test_foreign_parent_session_is_refused(self) -> None:
        self.parent[0]['payload']['id'] = 'other-parent'
        with self.assertRaisesRegex(binder.BindingError, 'parent différente'):
            self.proof()

    def test_read_command_escapes_literal_apostrophes(self) -> None:
        path = self.root / "dossier d'essai" / 'packet.json'
        self.assertEqual(binder._read_command(path),
                         "Get-Content -LiteralPath '" + str(path.resolve()).replace("'", "''") + "' -Raw")


if __name__ == '__main__':
    unittest.main()
