import unittest
import controler_codex_dev5_r2_patch_pragma as p
import controler_codex_dev5_r2_ecriture_refusee as r

class PatchTests(unittest.TestCase):
    def test_directive_does_not_change_patch(self):
        body = 'text(await tools.apply_patch("*** Begin Patch\\n*** Add File: C:/test\\n+texte\\n*** End Patch"));'
        self.assertEqual(p.patch_without_pragma('// @exec: {"max_output_tokens":55000}\n' + body), body)

    def test_patch_directive_and_injection_rejected(self):
        for script in ('// @exec: {"max_output_tokens":true}\ntext(await tools.apply_patch("x"));',
                       '// @exec: {"max_output_tokens":55000}\ntext(await tools.apply_patch("x")); await tools.web__run({});'):
            with self.assertRaises(ValueError):
                p.patch_without_pragma(script)

    def test_failed_patch_exactly_attested(self):
        script = 'text(await tools.apply_patch("*** Begin Patch\\n*** Add File: ' + r.EXPECTED_TARGET + '\\n+placeholder\\n*** End Patch"));'
        parts = ['Script failed\nWall time 1 seconds\nOutput:\n',
                 'Script error:\nExit code: 1\nWall time: 1 seconds\nOutput:\nFailed to create parent directories for ' + r.EXPECTED_TARGET.replace('/', '\\') + '\n']
        r.rejected_patch(script, parts)
        with self.assertRaises(ValueError):
            r.rejected_patch(script, ['Script completed\n', '{}'])
        with self.assertRaises(ValueError):
            r.rejected_patch(script.replace('placeholder', 'autre'), parts)

if __name__ == '__main__':
    unittest.main()
