"""Rejets de l'auditeur indépendant : aucun modèle, réseau ou pièce modifiée."""
import json
import tempfile
import unittest
from pathlib import Path
import audit_natif_codex_dev5_r2 as audit
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign

class AuditTests(unittest.TestCase):
    def read_fixture(self, path, body, exit_value=0):
        call = {'payload': {'type': 'custom_tool_call', 'name': 'exec', 'call_id': 'read', 'input': campaign.script(path)}}
        output = {'timestamp': '2026-10-07T19:00:00Z', 'payload': {'type': 'custom_tool_call_output', 'call_id': 'read',
                  'output': [{'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': json.dumps({'exit_code': exit_value})},
                             {'type': 'text', 'text': body}]}}
        return [call, output], call

    def test_read_exact_terminal_presentation(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fragment.txt'
            text = 'Donnée\r\nSuite\n'
            path.write_bytes(text.encode('utf-8'))
            for suffix in ('', '\n', '\r\n'):
                native, call = self.read_fixture(path, text + suffix)
                self.assertEqual(audit.read(native, call)[1], text)

    def test_read_injection_or_change_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fragment.txt'
            path.write_bytes(b'ABC\n')
            for body in ('AXC\n', 'ABC\n\r\n\r\n', 'ABC\nInjecte', 'ABC\n\r', 'ABC\ntokens truncated'):
                native, call = self.read_fixture(path, body)
                with self.assertRaises(base.binder.BindingError):
                    audit.read(native, call)

    def test_read_false_exit_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fragment.txt'
            path.write_bytes(b'A')
            for code in (False, None, '0', 1):
                native, call = self.read_fixture(path, 'A', code)
                with self.assertRaises(base.binder.BindingError):
                    audit.read(native, call)

    def test_read_more_than_eight_thousand_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fragment.txt'
            path.write_bytes(b'A' * 8001)
            native, call = self.read_fixture(path, 'A' * 8001)
            with self.assertRaises(base.binder.BindingError):
                audit.read(native, call)

    def test_read_duplicate_or_prior_return_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fragment.txt'
            path.write_bytes(b'A')
            native, call = self.read_fixture(path, 'A')
            for events in ([native[1], native[0]], native + [native[1]], [native[0]]):
                with self.assertRaises(base.binder.BindingError):
                    audit.read(events, call)

    def patch_fixture(self, target, content='Exact'):
        patch = '*** Begin Patch\n*** Add File: ' + target.resolve().as_posix() + '\n+' + content + '\n*** End Patch'
        call = {'payload': {'type': 'custom_tool_call', 'call_id': 'write', 'input': 'text(await tools.apply_patch(' + json.dumps(patch) + '));'}}
        output = {'payload': {'type': 'custom_tool_call_output', 'call_id': 'write',
                  'output': [{'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': '{}'}]}}
        return [call, output], call

    def test_patch_literal_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'response.md'
            target.write_bytes(b'Exact\n')
            native, call = self.patch_fixture(target)
            self.assertEqual(audit.exact_patch(native, call, target), 'Exact\n')

    def test_patch_changed_answer_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'response.md'
            target.write_bytes(b'Altered\n')
            native, call = self.patch_fixture(target)
            with self.assertRaises(base.binder.BindingError):
                audit.exact_patch(native, call, target)

    def test_patch_wrong_destination_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'response.md'
            target.write_bytes(b'Exact\n')
            native, call = self.patch_fixture(Path(temporary) / 'other.md')
            with self.assertRaises(base.binder.BindingError):
                audit.exact_patch(native, call, target)

if __name__ == '__main__':
    unittest.main()
