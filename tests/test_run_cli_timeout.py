"""Timeout de run_cli : dernière ligne coupée signalée, cas en échec ; faux processus seul."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import measurement_common as common
import run_codex_campaign as campaign

THREAD = '{"type":"thread.started","thread_id":"00000000-0000-0000-0000-000000000124"}\n'
IDENTITY = {'version': 'codex-cli fixture', 'sha256': '0' * 64}


class ParseJsonlTests(unittest.TestCase):
    def test_lignes_completes_et_vides(self) -> None:
        self.assertEqual(common.parse_jsonl(THREAD + '\n{"type":"turn.completed"}\n'),
                         [{'type': 'thread.started', 'thread_id': '00000000-0000-0000-0000-000000000124'},
                          {'type': 'turn.completed'}])

    def test_ligne_tronquee_ou_non_objet_refusee_hors_timeout(self) -> None:
        with self.assertRaises(ValueError):
            common.parse_jsonl(THREAD + '{"type":"item.comp')
        with self.assertRaisesRegex(ValueError, 'non objet'):
            common.parse_jsonl('[1]\n')


class RunCliTimeoutTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix='faux-processus-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.cli = self.root / 'codex.exe'
        self.cli.write_bytes(b'faux binaire, jamais execute')

    def run_fake(self, **outcome):
        patches = [patch.object(common, 'verify_codex_cli', return_value=IDENTITY)]
        if 'timeout_stdout' in outcome:
            error = subprocess.TimeoutExpired([str(self.cli)], 1, output=outcome['timeout_stdout'], stderr=b'')
            patches.append(patch.object(common.subprocess, 'run', side_effect=error))
        else:
            patches.append(patch.object(common.subprocess, 'run',
                                        return_value=subprocess.CompletedProcess([], 0, outcome['stdout'], '')))
        with patches[0], patches[1] as process:
            result = common.run_cli([str(self.cli), 'exec'], 'FIXTURE SANS MODELE', self.root, 1)
            self.assertEqual(process.call_count, 1)
        return result

    def test_timeout_ligne_coupee_signalee_et_cas_en_echec(self) -> None:
        for cut in (b'{"type":"item.comp', '{"type":"item.completed","text":"é'.encode()[:-1]):
            with self.subTest(fin=cut):
                events, code, receipt = self.run_fake(timeout_stdout=THREAD.encode() + cut)
                self.assertEqual(code, 124)
                self.assertEqual([e['type'] for e in events], ['thread.started'])
                self.assertIs(receipt['truncated_tail'], True)
                self.assertEqual(receipt['kind'], 'real_cli')
                self.assertEqual(receipt['process_exit'], 124)
                case = json.loads((ROOT / 'scripts/cas-plugin-cycle-v4.json').read_bytes())[0]
                self.assertIn('process_timeout', campaign.failures([], case, code, campaign.PROFILE))

    def test_timeout_sans_coupure_non_marque(self) -> None:
        events, code, receipt = self.run_fake(timeout_stdout=THREAD.encode())
        self.assertEqual((len(events), code), (1, 124))
        self.assertNotIn('truncated_tail', receipt)

    def test_timeout_ligne_corrompue_au_milieu_toujours_refusee(self) -> None:
        with self.assertRaises(ValueError):
            self.run_fake(timeout_stdout=b'{"type":"cass\n' + THREAD.encode() + b'{"x":')

    def test_sortie_normale_coupee_refusee_sans_tolerance(self) -> None:
        with self.assertRaises(ValueError):
            self.run_fake(stdout=THREAD + '{"type":"item.comp')


if __name__ == '__main__':
    unittest.main()
