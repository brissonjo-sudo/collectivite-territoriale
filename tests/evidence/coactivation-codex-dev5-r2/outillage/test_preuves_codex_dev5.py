"""Tests négatifs du protocole natif séparé, sans modèles ni appels externes."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import preuves_codex_dev5 as native
import controler_codex_dev5 as guarded

class NativeProofTests(unittest.TestCase):
    def test_source_json(self):
        tool, args = native.source_call('text(await tools.mcp__droit_francais__fetch({"id":"LEGIARTI000006574893"}));')
        self.assertEqual(tool, 'mcp__droit_francais__fetch')
        self.assertEqual(args['id'], 'LEGIARTI000006574893')

    def test_js_property_literal(self):
        _, args = native.source_call('text(await tools.mcp__droit_francais__search({query:"{a:une donnée}",limit:3}));')
        self.assertEqual(args, {'query': '{a:une donnée}', 'limit': 3})

    def test_expression_rejected(self):
        for call in ('text(await tools.mcp__droit_francais__fetch({id:process.env.TOKEN}));',
                     'text(await tools.mcp__droit_francais__fetch({id:foo()}));',
                     'text(await tools.mcp__droit_francais__fetch({"id":"x","id":"y"}));',
                     'text(await tools.mcp__droit_francais__fetch({"id":"x"})); exit();'):
            with self.subTest(call=call), self.assertRaises((ValueError, native.binder.BindingError)):
                native.source_call(call)

    def test_only_failed_spawn_excluded(self):
        call = {'timestamp': '2026-10-07T10:00:00Z', 'payload': {'type': 'function_call', 'name': 'spawn_agent',
                'arguments': '{"task_name":"juge_codex_dev5_02","fork_turns":"none"}', 'call_id': 'call_failed'}}
        output = {'timestamp': '2026-10-07T10:00:01Z', 'payload': {'type': 'function_call_output',
                  'call_id': 'call_failed', 'output': guarded.FAILED_SPAWN}}
        parent = [call, output]
        projected, rejected = guarded.successful_parent(parent, '/root/juge_codex_dev5_02')
        self.assertEqual(projected, [])
        self.assertEqual(len(parent), 2)
        self.assertFalse(rejected[0]['created_session'])

    def test_other_spawn_errors_not_ignored(self):
        call = {'payload': {'type': 'function_call', 'name': 'spawn_agent',
                'arguments': '{"task_name":"juge_codex_dev5_02"}', 'call_id': 'failed'}}
        output = {'payload': {'type': 'function_call_output', 'call_id': 'failed', 'output': 'arbitrary error'}}
        projected, rejected = guarded.successful_parent([call, output], '/root/juge_codex_dev5_02')
        self.assertEqual(projected, [call, output])
        self.assertEqual(rejected, [])

    def test_ambiguous_spawn_results_fail(self):
        call = {'payload': {'type': 'function_call', 'name': 'spawn_agent',
                'arguments': '{"task_name":"juge_codex_dev5_02"}', 'call_id': 'failed'}}
        with self.assertRaises(native.binder.BindingError):
            guarded.successful_parent([call], '/root/juge_codex_dev5_02')

    def test_skill_literal_true_rejected(self):
        case = {'invariant_objects': [{'id': 'atom', 'expectation': 'Activer le rôle via Skill.'}]}
        with self.assertRaises(native.binder.BindingError):
            guarded.skill_literal_guard(case, {'invariants': {'atom': {'status': True}}})
        guarded.skill_literal_guard(case, {'invariants': {'atom': {'status': None}}})

    def test_simple_file_method_not_confused(self):
        case = {'invariant_objects': [{'id': 'atom', 'expectation': 'Appliquer la méthode DRH.'}]}
        guarded.skill_literal_guard(case, {'invariants': {'atom': {'status': True}}})

    def test_read_truncation_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'entrée.md'
            target.write_text('Deux lignes\ncomplètes\n', encoding='utf-8')
            args = {'cmd': "Get-Content -LiteralPath '" + target.as_posix() + "' -Raw", 'max_output_tokens': 55000}
            script = native.raw.read_script(args)
            with self.assertRaises(native.binder.BindingError):
                native.read_call(script, ['Script completed\n', '{"exit_code":0}', 'Deux lignes'])
            self.assertEqual(native.read_call(script, ['Script completed\n', '{"exit_code":0}', 'Deux lignes\ncomplètes\n']), target.resolve())

    def test_patch_destination_and_content(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'response.md'
            target.write_text('STOP\n', encoding='utf-8')
            patch = '*** Begin Patch\n*** Add File: ' + target.as_posix() + '\n+STOP\n*** End Patch'
            script = 'text(await tools.apply_patch(' + json.dumps(patch) + '));'
            self.assertEqual(native.literal_patch(script, target, ['Script completed\n', '{}']), 'STOP\n')
            with self.assertRaises(native.binder.BindingError):
                native.literal_patch(script.replace('+STOP', '+AUTRE'), target, ['Script completed\n', '{}'])

    def test_real_model_retained(self):
        case = native.case_and_number('plugin-garde-fou-apja')[1]
        events = native.binder._events(native.RUN / (case['id'] + '.jsonl'))
        self.assertEqual(events[0]['host'], 'Codex')
        self.assertNotEqual(events[0]['model'], 'claude-sonnet-4-6')
        self.assertNotIn('model_mismatch', native.codex_failures(events, case))
        changed = copy.deepcopy(events)
        changed[0]['model_native_verified'] = False
        self.assertIn('model_mismatch', native.codex_failures(changed, case))
        self.assertIn('codex_model_unverified', native.codex_failures(changed, case))

    def test_fake_primary_ref_rejected(self):
        assessment, _, _ = native.modules()
        with self.assertRaises(ValueError):
            assessment.validate_source_links([{'type': 'source_evidence', 'event_id': 'e1', 'call_id': 'fabricated',
                                               'tool': 'mcp__droit-francais__fetch', 'status': 'available'}])

if __name__ == '__main__':
    unittest.main()
