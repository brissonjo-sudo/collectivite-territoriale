import unittest
import grammaire_codex_dev6 as grammar
import configuration_codex_dev6 as config
import tempfile
from pathlib import Path

class GrammarTests(unittest.TestCase):
    def test_source_body_and_arguments_unchanged(self):
        original = 'text(await tools.mcp__droit_francais__search({"query":"un objet"}));'
        self.assertEqual(grammar.source(original), grammar.source('// @exec: {"max_output_tokens":55000}\n' + original))

    def test_patch_body_unchanged(self):
        original = 'text(await tools.apply_patch("*** Begin Patch\\n*** Add File: /a\\n+x\\n*** End Patch"));'
        self.assertEqual(grammar.arguments(original, 'apply_patch'), grammar.arguments('// @exec: {"max_output_tokens":55000}\n' + original, 'apply_patch'))

    def test_reject_capacity_variants(self):
        original = 'text(await tools.mcp__droit_francais__search({"query":"x"}));'
        for value in ('{"max_output_tokens":true}', '{"max_output_tokens":55001}', '{"max_output_tokens":55000,"yield_time_ms":1}', '{"max_output_tokens":"55000"}'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                grammar.source('// @exec: ' + value + '\n' + original)

    def test_no_extra_script_or_tool(self):
        for body in ('text(await tools.exec_command({"cmd":"x"}));', 'text(await tools.mcp__droit_francais__search({"query":"x"})); exit();'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                grammar.source('// @exec: {"max_output_tokens":55000}\n' + body)

    def test_directive_not_for_shell_parser(self):
        with self.assertRaises(ValueError):
            grammar.arguments('// @exec: {"max_output_tokens":55000}\ntext(await tools.exec_command({"cmd":"x"}));', 'exec_command')

    def test_configure_keeps_capacity_grammars(self):
        import campagne_codex_dev6_r1 as campaign
        import preuves_codex_dev6 as native
        import preuves_codex_dev6_web as web
        import controler_codex_dev6_r1_site_literal as site
        for _ in range(3):
            campaign.configure()
            site.activate()
            campaign.configure()
            call = '// @exec: {"max_output_tokens":55000}\ntext(await tools.mcp__droit_francais__search({"query":"test"}));'
            self.assertEqual(native.source_call(call), ('mcp__droit_francais__search', {'query': 'test'}))
            self.assertEqual(web.BASE_SOURCE_CALL(call), ('mcp__droit_francais__search', {'query': 'test'}))
            patch = '// @exec: {"max_output_tokens":55000}\ntext(await tools.apply_patch("un contenu littéral"));'
            self.assertEqual(native.binder._arguments(patch, 'apply_patch'), 'un contenu littéral')

class CandidateInputTests(unittest.TestCase):
    def test_all_six_complete_descriptions(self):
        for path in sorted((config.CANDIDATE / 'skills').glob('*/SKILL.md')):
            lines = path.read_text(encoding='utf-8').split('---', 2)[1].splitlines()
            start = next(i for i, line in enumerate(lines) if line.startswith('description:'))
            first = lines[start].split(':', 1)[1].strip()
            continuation = []
            for line in lines[start + 1:]:
                if line and not line[0].isspace():
                    break
                continuation.append(line.strip())
            expected = ' '.join(([first] if first != '>-' else []) + continuation)
            with self.subTest(skill=path.parent.name):
                self.assertEqual(config.description(path), expected)
                self.assertGreater(len(expected), 350)
                self.assertTrue(expected.endswith('.'))
        research = config.description(config.CANDIDATE / 'skills/recherche-juridique/SKILL.md')
        self.assertIn('questions doctrinales sans citation.', research)
        dsi = config.description(config.CANDIDATE / 'skills/dsi-fpt/SKILL.md')
        self.assertIn('incident ancien ou clos.', dsi)
        self.assertTrue(dsi.endswith('Hors passation.'))

    def test_reject_unhandled_description_shapes(self):
        for declaration in ('description: >-\nname: test', 'description: |\n  ' + 'texte long ' * 5, 'description: >-\n\n  texte long', 'description: >-\n   indentation excessive'):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'SKILL.md'
                path.write_text('---\n' + declaration + '\n---\n', encoding='utf-8')
                with self.subTest(declaration=declaration), self.assertRaises(ValueError):
                    config.description(path)

    def test_frozen_git_blobs_and_new_inputs(self):
        manifest, entries = config.manifest_and_inputs()
        self.assertEqual((len(manifest['files']), manifest['case_count'], manifest['atomic_count']), (213, 16, 124))
        self.assertEqual(len(entries), 16)
        for entry in entries.values():
            self.assertEqual((entry['candidate_commit'], entry['runtime_source_commit']), (config.HEAD, config.SOURCE))
            self.assertEqual(len(entry['allowed_runtime_files']), 166)
            self.assertIn('qualification-coactivation-dev6-codex-r1', entry['response_path'])
            for role in entry.get('runtime_catalogue', []):
                self.assertEqual(config.sha(config.Path(role['runtime_path'])), role['runtime_sha256'])
                self.assertEqual(role['description'], config.description(Path(role['runtime_path'])))
                self.assertGreater(len(role['description']), 350)
        self.assertFalse(manifest['historical_scores_reused'])

if __name__ == '__main__':
    unittest.main()
