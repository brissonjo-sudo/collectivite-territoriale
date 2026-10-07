"""Régression import froid et rejet d'une grammaire non préexportée."""
import json
import subprocess
import sys
import unittest


class ColdImportTests(unittest.TestCase):
    def test_actual_five_native_pairs_reaudit_in_fresh_process(self) -> None:
        code = 'import json; import audit_dev6_PARTIEL_initialisation as a; r=a.audit(False); print(json.dumps({k:r[k] for k in ("status","errors","respondents_verified","judges_verified","unique_retained_roles")}))'
        result = subprocess.run([sys.executable, '-c', code], check=True, capture_output=True, text=True, encoding='utf-8')
        document = json.loads(result.stdout)
        self.assertEqual(document, {'status': 'passed', 'errors': [], 'respondents_verified': 5, 'judges_verified': 5, 'unique_retained_roles': 10})

    def test_invalid_capacity_still_rejected_after_cold_import(self) -> None:
        import audit_dev6_PARTIEL_initialisation as audit
        import grammaire_codex_dev6 as grammar
        valid = '// @exec: {"max_output_tokens":55000}\ntext(await tools.web__run({"open":[{"ref_id":"https://www.cnil.fr"}]}));'
        self.assertEqual(grammar.source(valid)[0], 'web__run')
        for invalid in (valid.replace('55000', '55001'), valid + ' exit();'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                grammar.source(invalid)


if __name__ == '__main__':
    unittest.main()
