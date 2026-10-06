"""Dérives du gel corrigé : vrais commits Git locaux, sans réseau ni Claude."""
from __future__ import annotations

import copy
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import corrected_candidate as candidate
import run_coactivation_v2 as campaign
import verify_coactivation_v2 as verifier


class CorrectedCandidateTests(unittest.TestCase):
    """Les fichiers déclarés, leurs blobs et l'identité HEAD restent indissociables."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for relative in candidate.FIXED:
            self.write(relative, b'fixture\n')
        self.write('skills/dsi-fpt/SKILL.md', b'Runtime corrige\n')
        self.write('scripts/corrected_candidate.py', b'fixture script\n')
        self.write('tests/cas-coactivation-v2.json', b'[]\n')
        (self.root / 'overlays').mkdir()
        self.write('upstream.json', json.dumps({'skills': {
            'dsi-fpt': {'commit': 'b' * 40, 'version': '0.2.1'}}}).encode())
        self.write(candidate.BASELINE, json.dumps({'candidate_commit': 'a' * 40, 'files': {
            'skills/dsi-fpt/SKILL.md': candidate.checksum(b'Ancien runtime\n')}}).encode())
        self.git('init', '--quiet')
        self.git('config', 'user.name', 'Test local')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'core.autocrlf', 'false')
        self.commit()
        self.frozen = candidate.build_manifest(self.root)

    def write(self, relative: str, data: bytes) -> None:
        """Prépare une pièce de fixture sans toucher aux sources du dépôt."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def git(self, *arguments: str) -> str:
        """Exécute Git dans le dépôt jetable uniquement."""
        return subprocess.check_output(['git', '-c', 'safe.directory=' + self.root.as_posix(),
                                        '-c', 'core.excludesFile=',
                                        *arguments], cwd=self.root, text=True).strip()

    def commit(self) -> None:
        """Crée un vrai commit de fixture, sans remote."""
        self.git('add', '-A')
        self.git('commit', '--quiet', '-m', 'Fixture')

    def failures(self, *, live: bool = False) -> list[str]:
        """Vérifie les octets réels ou également leur identité committée."""
        return candidate.frozen_failures_corrected(self.frozen, root=self.root, require_git=live)

    def test_committed_candidate_valid_live_and_offline(self) -> None:
        self.assertEqual([], self.failures(live=True))
        with patch.object(candidate, 'git_revision', side_effect=AssertionError('Git interdit')):
            self.assertEqual([], self.failures())
        self.assertIs(False, self.frozen['historical_scores_reused'])

    def test_raw_crlf_blob_is_preserved_under_windows_autocrlf(self) -> None:
        relative = '.agents/plugins/marketplace.json'
        raw = b'{\r\n  "fixture": "CRLF"\r\n}\r\n'
        self.write(relative, raw)
        self.commit()
        self.git('config', 'core.autocrlf', 'true')
        self.assertEqual(raw, candidate.git_bytes(self.root, 'HEAD', {relative})[relative])
        self.frozen = candidate.build_manifest(self.root)
        self.assertEqual([], self.failures(live=True))

    def test_batch_rejects_non_regular_git_objects(self) -> None:
        relative = 'skills/dsi-fpt/SKILL.md'
        tree = b'120000 blob ' + b'a' * 40 + b'\t' + relative.encode() + b'\0'
        with (patch.object(candidate.subprocess, 'check_output', return_value=tree),
              self.assertRaisesRegex(ValueError, 'non régulier')):
            candidate.git_bytes(self.root, 'HEAD', {relative})

    def test_batch_rejects_truncated_blob(self) -> None:
        relative = 'skills/dsi-fpt/SKILL.md'
        oid = b'a' * 40
        tree = b'100644 blob ' + oid + b'\t' + relative.encode() + b'\0'
        truncated = oid + b' blob 9\nshort\n'
        with (patch.object(candidate.subprocess, 'check_output', side_effect=[tree, truncated]),
              self.assertRaisesRegex(ValueError, 'Blob Git incomplet')):
            candidate.git_bytes(self.root, 'HEAD', {relative})

    def test_modified_runtime_detected(self) -> None:
        self.write('skills/dsi-fpt/SKILL.md', b'Mutation\n')
        self.assertIn('gel_divergent:skills/dsi-fpt/SKILL.md', self.failures())
        with self.assertRaisesRegex(ValueError, 'Octets locaux'):
            candidate.build_manifest(self.root)

    def test_forged_local_digest_cannot_replace_committed_blob(self) -> None:
        self.write('skills/dsi-fpt/SKILL.md', b'Mutation\n')
        self.frozen['files']['skills/dsi-fpt/SKILL.md'] = candidate.checksum(b'Mutation\n')
        self.assertEqual([], self.failures())
        self.assertEqual(['corrected_committed_bytes_mismatch'], self.failures(live=True))

    def test_unrelated_new_commit_changes_identity(self) -> None:
        self.write('README.md', b'Nouveau commit\n')
        self.commit()
        self.assertEqual(['corrected_head_mismatch'], self.failures(live=True))

    def test_added_runtime_file_invalidates_inventory(self) -> None:
        self.write('skills/dsi-fpt/references/untracked.md', b'Injecte\n')
        self.assertEqual(['corrected_inventory_mismatch'], self.failures())

    def test_added_harness_file_invalidates_inventory(self) -> None:
        self.write('scripts/new_transport.py', b'Injecte\n')
        self.assertEqual(['corrected_inventory_mismatch'], self.failures())

    def test_local_settings_are_not_ambient(self) -> None:
        self.write('.claude/settings.local.json', b'{}\n')
        self.assertEqual(['corrected_inventory_mismatch'], self.failures())

    def test_runtime_count_cannot_be_claimed(self) -> None:
        self.frozen['runtime_files'] += 1
        self.assertEqual(['corrected_runtime_count_mismatch'], self.failures())

    def test_missing_file_is_not_ignored(self) -> None:
        del self.frozen['files']['.mcp.json']
        self.assertEqual(['corrected_inventory_mismatch'], self.failures())

    def test_legacy_manifest_does_not_opt_into_corrected_profile(self) -> None:
        legacy = copy.deepcopy(self.frozen)
        legacy['schema_version'] = 2
        self.assertEqual(['corrected_manifest_schema_required'],
                         candidate.frozen_failures_corrected(legacy, root=self.root))
        self.assertEqual(['frozen_schema_v2_required'], campaign.frozen_failures_v2(self.frozen))

    def test_old_scores_cannot_be_embedded(self) -> None:
        self.frozen['historical_business_score'] = 12
        self.assertEqual(['corrected_manifest_schema_required'], self.failures())

    def test_score_reuse_flag_cannot_be_enabled(self) -> None:
        self.frozen['historical_scores_reused'] = True
        self.assertEqual(['corrected_candidate_identity_invalid'], self.failures())

    def test_unchanged_runtime_requires_legacy_profile(self) -> None:
        self.write('skills/dsi-fpt/SKILL.md', b'Ancien runtime\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'corrected_runtime_change_required'):
            candidate.build_manifest(self.root)

    def test_declared_overlay_hash_is_checked(self) -> None:
        overlay = b'Garde corrigee\n'
        self.write('overlays/dsi-fpt.md', overlay)
        self.write('upstream.json', json.dumps({'skills': {'dsi-fpt': {'commit': 'b' * 40,
            'instruction_overlays': [{'target': 'SKILL.md', 'source': 'overlays/dsi-fpt.md',
                'base_sha256': 'a' * 64, 'source_sha256': candidate.checksum(overlay),
                'anchor': '## Garde'}]}}}).encode())
        self.commit()
        self.frozen = candidate.build_manifest(self.root)
        self.assertEqual([], self.failures())
        self.write('overlays/dsi-fpt.md', b'Alteree\n')
        self.frozen['files']['overlays/dsi-fpt.md'] = candidate.checksum(b'Alteree\n')
        self.assertEqual(['corrected_validation_failed:ValueError'], self.failures())

    def test_undeclared_overlay_is_rejected_at_freeze(self) -> None:
        self.write('overlays/unknown.md', b'Non declaree\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Surcharge absente'):
            candidate.build_manifest(self.root)

    def campaign_arguments(self) -> tuple[list[str], dict, Path, Path]:
        """Prépare une campagne isolée et son cas technique réel, sans appel modèle."""
        case = next(case for case in campaign.load_cases() if case['id'] == 'plugin-dsi-technique')
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps(self.frozen), encoding='utf-8')
        traces = self.root / 'traces'
        arguments = ['runner', '--case', case['id'], '--output-dir', str(traces),
                     '--frozen-manifest', str(manifest)]
        return arguments, case, manifest, traces

    def test_runner_emits_new_profile_and_verifier_requires_it(self) -> None:
        arguments, case, manifest, traces = self.campaign_arguments()
        validate = lambda frozen: candidate.frozen_failures_corrected(frozen, root=self.root)
        measured = [{'type': 'init', 'session_id': 'fixture-session'}]
        checks = {'stop_required': False, 'primary_content_available': False}
        with (patch.object(sys, 'argv', arguments),
              patch.object(campaign, 'execute', return_value=(measured, 0, {})),
              patch.object(campaign, 'technical_failures', return_value=[]),
              patch.object(campaign, 'observable_checks', return_value=checks),
              contextlib.redirect_stdout(io.StringIO())):
            self.assertEqual(0, campaign.main(frozen_validator=validate, candidate_profile=candidate.PROFILE))
        path = traces / (case['id'] + '.jsonl')
        events = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        self.assertEqual(candidate.PROFILE, events[0]['candidate_profile'])
        self.assertNotIn('business_score', events[0])
        verify_arguments = ['verify', '--manifest', str(manifest), '--traces', str(traces)]
        with (patch.object(sys, 'argv', verify_arguments),
              patch.object(verifier, 'technical_failures', return_value=[]),
              patch.object(verifier, 'observable_checks', return_value=checks),
              contextlib.redirect_stdout(io.StringIO())):
            self.assertEqual(0, verifier.main(frozen_validator=validate, candidate_profile=candidate.PROFILE))
        del events[0]['candidate_profile']
        path.write_text(''.join(json.dumps(event) + '\n' for event in events), encoding='utf-8')
        with (patch.object(sys, 'argv', verify_arguments), contextlib.redirect_stderr(io.StringIO()),
              self.assertRaises(SystemExit)):
            verifier.main(frozen_validator=validate, candidate_profile=candidate.PROFILE)

    def test_runner_checks_head_before_each_case(self) -> None:
        arguments, _, _, traces = self.campaign_arguments()
        validate = unittest.mock.Mock(side_effect=[[], ['corrected_head_mismatch']])
        with (patch.object(sys, 'argv', arguments), patch.object(campaign, 'execute') as execute,
              contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit)):
            campaign.main(frozen_validator=validate, candidate_profile=candidate.PROFILE)
        execute.assert_not_called()
        self.assertEqual(2, validate.call_count)
        self.assertEqual([], list(traces.glob('*.jsonl')))

    def test_mutation_during_measurement_cannot_pass(self) -> None:
        arguments, case, _, traces = self.campaign_arguments()
        validate = unittest.mock.Mock(side_effect=[[], [], ['corrected_head_mismatch']])
        with (patch.object(sys, 'argv', arguments),
              patch.object(campaign, 'execute', return_value=([{'type': 'init'}], 0, {})),
              patch.object(campaign, 'technical_failures', return_value=[]),
              patch.object(campaign, 'observable_checks', return_value={'primary_content_available': False}),
              contextlib.redirect_stdout(io.StringIO())):
            self.assertEqual(1, campaign.main(frozen_validator=validate, candidate_profile=candidate.PROFILE))
        path = traces / (case['id'] + '.jsonl')
        events = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        self.assertEqual('failed', events[-1]['status'])
        self.assertEqual(['corrected_head_mismatch'], events[-1]['failures'])
        self.assertEqual(3, validate.call_count)


if __name__ == '__main__':
    unittest.main()
