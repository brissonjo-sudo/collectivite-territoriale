"""Contre-exemples bloquant les fausses réussites et les liaisons manquantes de r7."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest

import generer_rapport_partiel_r7 as partial


class PartialEvidenceTests(unittest.TestCase):
    def test_completed_response_without_native_binding_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            trace = root / 'nominal.jsonl'
            trace.write_text('{"type":"result","subtype":"success","is_error":false}\n')
            directory = root / 'juges/nominal'
            directory.mkdir(parents=True)
            (directory / 'nominal.jugement.json').write_text('{"verdict":"reussite"}')
            trace.with_suffix('.jugement.json').write_text('{"verdict":"reussite"}')
            with self.assertRaisesRegex(ValueError, 'non liée'):
                partial.require_bound_response(trace, directory)

    def test_divergent_frozen_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp)
            files = {}
            for index in range(211):
                path = candidate / f'file-{index}.txt'
                path.write_bytes(b'frozen')
                files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            frozen = {'files': files, 'runtime_files': 166}
            partial.verify_frozen(frozen, candidate)
            (candidate / 'file-137.txt').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'file-137'):
                partial.verify_frozen(frozen, candidate)

    def test_missing_primary_nominal_never_success(self):
        events = [{'type': 'technical_assessment', 'observables': {'primary_content_available': False}}]
        nominal = {'id': 'nominal', 'mcp_mode': 'required'}
        with self.assertRaisesRegex(ValueError, 'sans primaire'):
            partial.reject_unproved_nominal(nominal, {'verdict': 'reussite'}, events)
        partial.reject_unproved_nominal(nominal, {'verdict': 'echec'}, events)
        # L’absence voulue de MCP ne transforme pas la règle nominale en règle universelle.
        partial.reject_unproved_nominal({'id': 'degraded', 'mcp_mode': 'disabled'},
            {'verdict': 'reussite'}, events)

    def test_absence_cannot_replace_controlled_interruption_receipt(self):
        cases = [{'id': f'case-{number}'} for number in range(1, 17)]
        frozen = {'candidate_commit': 'measured'}
        receipt = {'run': 'r7', 'candidate_commit': 'measured', 'interrupted_case_id': 'case-5',
            'response_captured': False, 'launcher_interrupted': True, 'reason': 'arrêt needs-auth',
            'completed_case_ids': ['case-1', 'case-2', 'case-3', 'case-4', 'case-11', 'case-12'],
            'not_executed_case_ids': ['case-6', 'case-7', 'case-8', 'case-9', 'case-10',
                'case-13', 'case-14', 'case-15', 'case-16']}
        partial.verify_receipt(receipt, frozen, cases)
        receipt.pop('not_executed_case_ids')
        with self.assertRaises(ValueError):
            partial.verify_receipt(receipt, frozen, cases)


if __name__ == '__main__':
    unittest.main()
