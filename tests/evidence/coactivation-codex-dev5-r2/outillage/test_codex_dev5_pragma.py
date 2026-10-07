import unittest
import controler_codex_dev5_r2_pragma as p

class PragmaTests(unittest.TestCase):
    def test_exact_directive_preserves_arguments(self):
        actual = '// @exec: {"max_output_tokens": 55000}\ntext(await tools.mcp__droit_francais__search({"query":"cas"}));'
        self.assertEqual(p.parse(actual), ('mcp__droit_francais__search', {'query': 'cas'}))

    def test_other_capacity_or_bool_rejected(self):
        for value in ('true', '10000', '"55000"'):
            with self.assertRaises(ValueError):
                p.parse('// @exec: {"max_output_tokens": ' + value + '}\ntext(await tools.web__run({}));')

    def test_extra_option_or_multiple_directives_rejected(self):
        for prefix in ('// @exec: {"max_output_tokens":55000,"yield_time_ms":1}\n',
                       '// @exec: {"max_output_tokens":55000}\n// @exec: {}\n'):
            with self.assertRaises(ValueError):
                p.parse(prefix + 'text(await tools.web__run({}));')

    def test_execution_injection_rejected(self):
        with self.assertRaises(ValueError):
            p.parse('// @exec: {"max_output_tokens":55000}\ntext(await tools.web__run({})); await tools.exec_command({});')

if __name__ == '__main__':
    unittest.main()
