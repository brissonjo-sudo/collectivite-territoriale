"""Fixtures négatives de comparaison brute et de typage des erreurs natives."""
import unittest
from pathlib import Path

from corriger_export_dev7_r3_20261008 import compare_final, failure_metadata, final_text


class ExportRepairTests(unittest.TestCase):
    def test_cache_path_replacement_only(self):
        result = compare_final("Lire C:/plugin/SKILL.md\n", "Lire C:/plugin/SKILL.md\r\n",
                               "Lire $INSTALLED_PLUGIN/SKILL.md", Path("C:/plugin"))
        self.assertTrue(result["cache_path_replacement_present"])

    def test_true_raw_mismatch_refused(self):
        with self.assertRaises(ValueError):
            compare_final("STOP", "Autre réponse", "STOP", Path("C:/plugin"))

    def test_secret_redaction_refused(self):
        with self.assertRaises(ValueError):
            compare_final("sk-abcdefghijklmnopq", "sk-abcdefghijklmnopq", "[SECRET_OMIS]", Path("C:/plugin"))

    def test_unexplained_export_difference_refused(self):
        with self.assertRaises(ValueError):
            compare_final("STOP", "STOP", "STOP modifié", Path("C:/plugin"))

    def test_native_array_process_failure(self):
        result = failure_metadata([{"type": "input_text", "text": "Script failed"},
                                   {"type": "input_text", "text": "exec_command failed: CreateProcess Rejected Failed to create unified exec process: helper_unknown_error: setup refresh had errors"}])
        self.assertEqual(result["failure_codes"], ["exec_command_failed", "process_start_failed", "windows_sandbox_setup_refresh_error"])
        self.assertFalse(result["auto_review_rejection_established"])

    def test_unrelated_inventory_does_not_prove_winerror(self):
        result = failure_metadata([{"text": "inventory describes os error 32"},
                                   {"text": "exec_command failed: Failed to create unified exec process: helper_unknown_error: setup refresh had errors"}])
        self.assertNotIn("windows_error_32", result["failure_codes"])

    def test_actual_winerror_is_typed(self):
        result = failure_metadata("exec_command failed: os error 32")
        self.assertIn("windows_error_32", result["failure_codes"])

    def test_success_output_not_failure(self):
        self.assertFalse(failure_metadata({"exit_code": 0, "output": "texte lu"})["native_failure_observed"])

    def test_unique_native_final_required(self):
        with self.assertRaises(ValueError):
            final_text([])


if __name__ == "__main__":
    unittest.main()
