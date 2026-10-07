"""Contrôles r2 bornés, sans modèle, réseau ou mutation du candidat."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign

class R2Tests(unittest.TestCase):
    def test_all_runtime_octets_exact(self):
        manifest = base.binder._json((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(manifest['runtime_descriptors']), 166)
        for original, record in manifest['runtime_descriptors'].items():
            text = ''.join(campaign.exact_text(Path(part['path'])) for part in record['fragments'])
            self.assertEqual(text.encode('utf-8'), Path(original).read_bytes())
            self.assertEqual(hashlib.sha256(text.encode('utf-8')).hexdigest(), record['source_sha256'])
            self.assertTrue(all(part['characters'] <= 8000 for part in record['fragments']))
            self.assertLessEqual(len(campaign.exact_text(Path(record['index_path']))), 8000)

    def test_16_questions_unchanged_and_exports_before_work(self):
        cases = base.binder._json((campaign.RUN / 'suite.json').read_text(encoding='utf-8'))
        self.assertEqual(len(cases), 16)
        self.assertEqual(sum(len(case['invariant_objects']) for case in cases), 124)
        for case in cases:
            directory = campaign.RUN / case['id']
            entry = base.binder._json(campaign.exact_text(directory / 'input.json'))
            self.assertEqual(entry['question'], case['prompt'])
            index = base.binder._json(campaign.exact_text(directory / 'input.index.json'))
            joined = ''.join(campaign.exact_text(Path(part['path'])) for part in index['fragments'])
            self.assertEqual(joined.encode('utf-8'), (directory / 'input.json').read_bytes())
            export = base.binder._json(campaign.exact_text(directory / 'responder.export.json'))
            self.assertEqual(export['input_sha256'], base.binder._sha(directory / 'input.json'))
            self.assertEqual(export['adapter_sha256'], base.binder._sha(Path(campaign.__file__)))

    def fixture(self, path, body, exit_value=0):
        call = {'payload': {'type': 'custom_tool_call', 'name': 'exec', 'call_id': 'read',
                'input': campaign.script(path)}}
        output = {'timestamp': '2026-10-07T19:00:00Z', 'payload': {'type': 'custom_tool_call_output', 'call_id': 'read',
                  'output': [{'type': 'text', 'text': 'Script completed\n'},
                             {'type': 'text', 'text': json.dumps({'exit_code': exit_value})},
                             {'type': 'text', 'text': body}]}}
        return [call, output], call

    def test_exact_lf_crlf_suffix_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'part.txt'
            text = 'Donnée complète\r\nDeuxième ligne\n'
            path.write_bytes(text.encode('utf-8'))
            for suffix in ('', '\n', '\r\n'):
                events, call = self.fixture(path, text + suffix)
                _, received, _, _ = campaign.real_read(events, call)
                self.assertEqual(received, text)
            for suffix in ('\r\n\r\n', '\r', 'ajout', '\nInjecté'):
                events, call = self.fixture(path, text + suffix)
                with self.assertRaises(base.binder.BindingError):
                    campaign.real_read(events, call)

    def test_changed_middle_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'part.txt'
            path.write_bytes(b'ABC\n')
            events, call = self.fixture(path, 'AXC\n')
            with self.assertRaises(base.binder.BindingError):
                campaign.real_read(events, call)

    def test_false_exit_not_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'part.txt'
            path.write_bytes(b'ABC\n')
            for exit_value in (False, '0', None, 1):
                events, call = self.fixture(path, 'ABC\n', exit_value)
                with self.assertRaises(base.binder.BindingError):
                    campaign.real_read(events, call)

    def test_over_limit_rejected_even_complete(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'part.txt'
            text = 'X' * 8001
            path.write_bytes(text.encode('utf-8'))
            events, call = self.fixture(path, text)
            with self.assertRaises(base.binder.BindingError):
                campaign.real_read(events, call)

    def test_response_not_transferred(self):
        self.assertFalse(any(campaign.RUN.glob('*/response.md'))) if not any(campaign.RUN.glob('*/liaison/execution-repondant.json')) else None
        manifest = base.binder._json(campaign.exact_text(campaign.RUN / 'manifest.json'))
        self.assertFalse(manifest['historical_scores_reused'])
        self.assertFalse(manifest['actual_plugin_activation_verified'])
        self.assertFalse(manifest['release_ready'])

if __name__ == '__main__':
    unittest.main()
