import unittest
from unittest.mock import patch
import audit_natif_codex_dev5_r2_final as audit

class FinalPatchActivationTests(unittest.TestCase):
    def test_directive_reactivates_before_literal_validation(self):
        target = audit.original.campaign.RUN / 'plugin-spontane-incident-donnees/response.md'
        script = '// @exec: {"max_output_tokens": 55000}\ntext(await tools.apply_patch("literal"));'
        with patch.object(audit.previous.patch, 'activate') as activate, patch.dict(audit.previous.patch.REGISTERED, {script: 'body'}, clear=True), patch.object(audit, 'BASE_PATCH', return_value='bytes'):
            self.assertEqual(audit.exact_patch([], {'payload': {'input': script}}, target), 'bytes')
            activate.assert_called_once()

    def test_directive_cannot_extend_to_another_destination(self):
        script = '// @exec: {"max_output_tokens": 55000}\ntext(await tools.apply_patch("literal"));'
        with self.assertRaises(ValueError), patch.object(audit.previous.patch, 'activate') as activate:
            audit.exact_patch([], {'payload': {'input': script}}, audit.original.campaign.RUN / 'another/response.md')
        activate.assert_not_called()

if __name__ == '__main__':
    unittest.main()
