import copy
import json
import unittest
from pathlib import Path
import preuves_codex_dev5 as native
import preuves_codex_dev5_fragments as fragmented

class FragmentTests(unittest.TestCase):
    def setUp(self):
        directory = native.RUN / 'juges-fragments/plugin-garde-fou-apja-b'
        self.manifest = native.binder._json((directory / 'plugin-garde-fou-apja.export.json').read_text(encoding='utf-8'))
        self.fragments = self.manifest['fragments']
        self.events = []
        for index, part in enumerate(self.fragments):
            script = native.raw.read_script({'cmd': native.raw.read_command(Path(part['path'])), 'max_output_tokens': 55000})
            self.events += [{'payload': {'type': 'custom_tool_call', 'name': 'exec', 'input': script, 'call_id': str(index)}},
                            {'payload': {'type': 'custom_tool_call_output', 'call_id': str(index), 'output': [
                                {'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': '{"exit_code":0}'},
                                {'type': 'text', 'text': Path(part['path']).read_text(encoding='utf-8')}]}}]
        self.events += [{'payload': {'type': 'custom_tool_call', 'name': 'exec', 'call_id': 'write',
                                     'input': 'text(await tools.apply_patch("dummy"));'}},
                        {'payload': {'type': 'custom_tool_call_output', 'call_id': 'write', 'output': [
                            {'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': '{}'}]}}]

    def test_full_octets_reconstructed(self):
        text, _ = fragmented.verify_fragment_outputs(self.events, self.fragments)
        packet = native.RUN / 'juges-fragments/plugin-garde-fou-apja-b/plugin-garde-fou-apja.packet.json'
        self.assertEqual(text.encode('utf-8'), packet.read_bytes())
        self.assertEqual(len(json.loads(text)['invariant_objects']), 5)

    def test_missing_fragment(self):
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(self.events[:-4] + self.events[-2:], self.fragments)

    def test_wrong_order(self):
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(self.events[2:4] + self.events[:2] + self.events[4:], self.fragments)

    def test_duplicate_fragment(self):
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(self.events[:2] + self.events, self.fragments)

    def test_truncated_content(self):
        altered = copy.deepcopy(self.events)
        altered[1]['payload']['output'][2]['text'] = altered[1]['payload']['output'][2]['text'][:-1]
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(altered, self.fragments)

    def test_wrong_exit(self):
        altered = copy.deepcopy(self.events)
        altered[1]['payload']['output'][1]['text'] = '{"exit_code":1}'
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(altered, self.fragments)

    def test_double_patch(self):
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(self.events + self.events[-2:], self.fragments)

    def test_read_after_write(self):
        with self.assertRaises(native.binder.BindingError):
            fragmented.verify_fragment_outputs(self.events[-2:] + self.events, self.fragments)

if __name__ == '__main__':
    unittest.main()
