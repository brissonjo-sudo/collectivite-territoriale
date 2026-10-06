"""Fixtures synthétiques : lecture brute, identité et export sans trace inventée."""
import copy
import json
import unittest
import lie_jugements_corriges as binder
import lie_jugements_corriges_bruts as raw
from test_lie_jugements_corriges import BindingTests


class RawTests(BindingTests):
    def setUp(self):
        super().setUp()
        self.original_read = binder._read_command
        binder._read_command = raw.read_command
        self.addCleanup(setattr, binder, '_read_command', self.original_read)
        self.native[3]['payload']['input'] = raw.read_script({
            'cmd': raw.read_command(self.packet), 'max_output_tokens': 55000})
        self.native[4]['payload']['output'] = [
            {'type': 'text', 'text': 'Script completed\nOutput:\n'},
            {'type': 'text', 'text': '{"exit_code":0}'},
            {'type': 'text', 'text': json.dumps(self.packet_value)}]

    def proof(self, native=None, parent=None):
        return raw.native_proof(self.native if native is None else native,
            self.parent if parent is None else parent, self.agent, self.parent_id,
            self.packet, self.judgment, self.exported_at)

    def test_trace_reelle_conservee(self):
        proof, kept = self.proof()
        read = next(e['payload'] for e in kept if e.get('payload', {}).get('call_id') == 'read'
            and e['payload']['type'] == 'custom_tool_call')
        output = next(e['payload'] for e in kept if e.get('payload', {}).get('call_id') == 'read'
            and e['payload']['type'] == 'custom_tool_call_output')
        self.assertEqual(read['input'], self.native[3]['payload']['input'])
        self.assertEqual(output['output'], self.native[4]['payload']['output'])
        self.assertEqual(proof['raw_projection'], raw.PROJECTION)

    def test_exit_nonzero_et_booleen_refuses(self):
        for code in (1, False):
            with self.subTest(code=code):
                self.native[4]['payload']['output'][1]['text'] = json.dumps({'exit_code': code})
                with self.assertRaises(binder.BindingError):
                    self.proof()

    def test_brut_tronque_refuse(self):
        self.native[4]['payload']['output'][2]['text'] = '{"case_id":"synthetic"}'
        with self.assertRaisesRegex(binder.BindingError, 'tronquée'):
            self.proof()

    def test_script_ajoute_refuse(self):
        self.native[3]['payload']['input'] += ' text("injection");'
        with self.assertRaisesRegex(binder.BindingError, 'grammaire'):
            self.proof()

    def test_retour_ligne_final_accepte_sans_modifier_trace(self):
        self.native[3]['payload']['input'] += '\n'
        _, kept = self.proof()
        read = next(e['payload'] for e in kept if e.get('payload', {}).get('call_id') == 'read'
            and e['payload']['type'] == 'custom_tool_call')
        self.assertEqual(read['input'], self.native[3]['payload']['input'])

    # Cette fixture de base teste le résultat enveloppé ; le protocole brut exige trois parties.
    def test_truncated_packet_read_is_refused(self):
        self.test_brut_tronque_refuse()

    def test_read_command_escapes_literal_apostrophes(self):
        path = self.root / "dossier d'essai" / 'packet.json'
        self.assertEqual(raw.read_command(path),
            "Get-Content -LiteralPath '" + path.resolve().as_posix().replace("'", "''") + "' -Raw")


if __name__ == '__main__':
    unittest.main()
