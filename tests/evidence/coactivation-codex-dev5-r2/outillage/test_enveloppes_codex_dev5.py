"""Contrôles de présentation et documentaire, sans requête extérieure."""
import copy
import json
import unittest
from pathlib import Path
import preuves_codex_dev5 as native
import preuves_codex_dev5_fragments as fragmented
import controler_codex_dev5_fragments_crlf as presentation
import preuves_codex_dev5_web as web

class PresentationTests(unittest.TestCase):
    def setUp(self):
        directory = native.RUN / 'juges-fragments/plugin-garde-fou-apja-b'
        self.fragments = native.binder._json((directory / 'plugin-garde-fou-apja.export.json').read_text(encoding='utf-8'))['fragments']
        self.events = []
        for index, part in enumerate(self.fragments):
            script = native.raw.read_script({'cmd': native.raw.read_command(Path(part['path'])), 'max_output_tokens': 55000})
            self.events += [{'payload': {'type': 'custom_tool_call', 'name': 'exec', 'input': script, 'call_id': str(index)}},
                            {'payload': {'type': 'custom_tool_call_output', 'call_id': str(index), 'output': [
                                {'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': '{"exit_code":0}'},
                                {'type': 'text', 'text': Path(part['path']).read_text(encoding='utf-8') + '\r\n'}]}}]
        self.events += [{'payload': {'type': 'custom_tool_call', 'name': 'exec', 'call_id': 'write',
                                     'input': 'text(await tools.apply_patch("dummy"));'}},
                        {'payload': {'type': 'custom_tool_call_output', 'call_id': 'write', 'output': [
                            {'type': 'text', 'text': 'Script completed\n'}, {'type': 'text', 'text': '{}'}]}}]

    def verify(self, events):
        old = native.outputs
        try:
            native.outputs = presentation.outputs
            return fragmented.verify_fragment_outputs(events, self.fragments)
        finally:
            native.outputs = old

    def test_crlf_only_normalization_preserves_raw(self):
        saved = copy.deepcopy(self.events)
        text, _ = self.verify(self.events)
        self.assertEqual(self.events, saved)
        original = native.RUN / 'juges-fragments/plugin-garde-fou-apja-b/plugin-garde-fou-apja.packet.json'
        self.assertEqual(text.encode('utf-8'), original.read_bytes())

    def test_double_crlf_rejected(self):
        self.events[1]['payload']['output'][2]['text'] += '\r\n'
        with self.assertRaises(native.binder.BindingError):
            self.verify(self.events)

    def test_suffix_injection_rejected(self):
        self.events[1]['payload']['output'][2]['text'] += 'Faux contenu'
        with self.assertRaises(native.binder.BindingError):
            self.verify(self.events)

    def test_changed_middle_rejected(self):
        text = self.events[1]['payload']['output'][2]['text']
        self.events[1]['payload']['output'][2]['text'] = text[:20] + 'X' + text[21:]
        with self.assertRaises(native.binder.BindingError):
            self.verify(self.events)

    def test_lf_and_exact_are_accepted(self):
        for suffix in ('', '\n'):
            events = copy.deepcopy(self.events)
            for index, part in enumerate(self.fragments):
                events[index * 2 + 1]['payload']['output'][2]['text'] = Path(part['path']).read_text(encoding='utf-8') + suffix
            self.verify(events)

class WebTests(unittest.TestCase):
    def setUp(self):
        self.sources = native.modules()[2]
        self.norm_url = 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra'
        self.body = ('L1: Article 33\nL2: Notification à l’autorité de contrôle.\nL3: Paragraphe un.\nL4: Paragraphe deux.\n'
                     'L5: Article 34\nL6: Communication à la personne concernée.\nL7: Paragraphe un.\nL8: Paragraphe deux.\nL9: Article 35\n')

    def capture(self, operation='find', prior=True, url=None):
        page = {'url': url or self.norm_url, 'safe_url': url or self.norm_url, 'text': self.body,
                'operation': operation, 'reference_id': 'turn12view0', 'total_lines': 2000, 'prior_open_verified': prior}
        return {'call_id': 'call_web', 'pages': [page], 'timestamp': '2026-10-07T17:00:00Z',
                'text': self.body, 'effective_urls': [page['url']]}

    def test_find_complete_normative_excerpt_after_open(self):
        evidence = web.evidence(self.capture(), self.sources)
        self.assertEqual([d['metadata']['number'] for d in evidence['documents']], ['33', '34'])
        self.assertTrue(all(d['nature'] == 'primary_text' for d in evidence['documents']))
        self.assertFalse(evidence['documents'][0]['metadata']['full_document_received'])
        self.assertIsNone(evidence['documents'][0]['metadata']['applicable_at_as_of_date'])

    def test_find_without_prior_open_stays_summary(self):
        evidence = web.evidence(self.capture(prior=False), self.sources)
        self.assertEqual(evidence['documents'][0]['nature'], 'tool_summary')

    def test_search_never_primary(self):
        evidence = web.evidence(self.capture(operation='search_query'), self.sources)
        self.assertEqual(evidence['documents'][0]['nature'], 'search_result')

    def test_guidance_never_primary(self):
        evidence = web.evidence(self.capture(operation='open', url='https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles'), self.sources)
        self.assertEqual(evidence['documents'][0]['nature'], 'tool_summary')

    def test_missing_line_prevents_complete_article(self):
        excerpt = self.body.replace('L3: Paragraphe un.\n', '')
        self.assertEqual([d['number'] for d in web.complete_article_excerpts(excerpt)], [34])

    def test_missing_boundary_prevents_primary(self):
        self.assertEqual(web.complete_article_excerpts(self.body.split('L5:')[0]), [])

    def test_anti_robot_kept_but_missing(self):
        capture = self.capture(operation='open')
        capture['pages'][0]['text'] = 'JavaScript is disabled. We need to verify that you are not a robot.'
        evidence = web.evidence(capture, self.sources)
        self.assertEqual(evidence['status'], 'missing')
        self.assertEqual(evidence['documents'][0]['reason'], 'anti_robot_or_access_denied')

    def test_secret_marker_prevents_primary(self):
        capture = self.capture(operation='open')
        capture['pages'][0]['text'] = self.body.replace('Paragraphe un.', 'access_token=secret_value')
        evidence = web.evidence(capture, self.sources)
        self.assertFalse(any(d['nature'] == 'primary_text' for d in evidence['documents']))

    def test_known_cnil_path_exception_is_bounded(self):
        url = 'https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4?tracking=1'
        self.assertEqual(web.safe_web_url(url, self.sources), url.split('?')[0])
        self.assertIsNone(web.safe_web_url('https://www.cnil.fr/unknown/this-is-a-long-unrecognized-private-path-with-secret-data', self.sources))

    def test_fake_hosts_and_credentials_refused(self):
        self.assertIsNone(web.safe_web_url('https://www.cnil.fr.evil.invalid/fr/reglement-europeen-protection-donnees', self.sources))
        self.assertIsNone(web.safe_web_url('https://login:password@www.cnil.fr/fr/reglement-europeen-protection-donnees', self.sources))

    def test_plaintext_reference_blocks(self):
        text = 'Titre (https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra)\nciteturn12view0 Source: find({"ref_id":"turn11view0"}); Total lines: 2000\n' + self.body
        page = web.blocks(text)[0]
        self.assertEqual(page['operation'], 'find')
        self.assertEqual(page['reference_id'], 'turn12view0')
        self.assertEqual(page['total_lines'], 2000)

if __name__ == '__main__':
    unittest.main()
