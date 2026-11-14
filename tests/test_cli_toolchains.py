"""ADR 0013 : propriétés CLI sur fixtures en mémoire ; aucune mesure ni preuve de release."""
from pathlib import Path
import contextlib
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cli_toolchains as cli
import human_resolution as human
import measurement_common as common
import run_codex_smoke as smoke
import qualify_distribution as qualifier

SOURCE = ROOT / 'tests/evidence/2026-10-18-candidat-1-3-0/campagne/plugin-mcp-indisponible/reponse/session.json'
COMMIT = '08f92936dd0ae09775a2d2293bae315cdf20847d'
# CLI réelle : CT_CODEX_CLI d'abord, puis la copie figée du harnais de mesure 1.5.0
# (seul chemin personnel admis dans le dépôt, repli explicite décidé le 07/11/2026).
HARNESS_CLI = Path('E:/Claude code/Projects/harnais-mesure-150/cli/codex-cli-0.164.0-alpha.11.1/codex.exe')
ACTUAL_CLI = next((Path(candidate) for candidate in (os.environ.get('CT_CODEX_CLI'), HARNESS_CLI)
                   if candidate and Path(candidate).is_file()), None)


class CliToolchainsTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix='t43-L17-synthetique-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.pins = cli.toolchains()
        self.campaign = json.loads(SOURCE.read_bytes())['origin']
        # Contrefactuel uniquement en mémoire ; pas une session de mesure réelle.
        self.smoke = {**copy.deepcopy(self.campaign), 'test_only_synthetic_origin': True,
            'cli_version': self.pins['smoke_cli']['version'], 'cli_sha256': self.pins['smoke_cli']['sha256'],
            'cli_phase': 'smoke_cli', 'cli_toolchain': copy.deepcopy(self.pins['smoke_cli'])}

    def prove(self, campaign=None, reviews=None, smoke_receipt=None, declared=None) -> dict:
        return cli.prove_toolchains([self.campaign if campaign is None else campaign],
            [self.campaign if reviews is None else reviews], [self.smoke if smoke_receipt is None else smoke_receipt],
            self.pins if declared is None else declared)

    def memory_checked(self, body: dict, phase: str = 'smoke_cli') -> dict:
        path = self.root / 'fixture-synthetique-jamais-ecrite.json'
        raw = (json.dumps(common.seal(body), ensure_ascii=False, indent=2) + '\n').encode()
        original = Path.read_bytes
        with patch.object(Path, 'read_bytes', lambda p: raw if p == path else original(p)):
            return common.checked(path, COMMIT, {body['origin']['kind']}, phase)

    def test_0162_campagne_et_0163_smoke_epingles_acceptes_propriete_CLI_seule(self) -> None:
        result = self.prove()
        self.assertEqual(result, self.pins)
        self.assertEqual(result['campaign_cli']['version'], 'codex-cli 0.162.0-alpha.17.2')
        self.assertEqual(result['smoke_cli']['version'], 'codex-cli 0.163.0-alpha.10.2')
        self.assertFalse((self.root / 'tests/evidence/release-1.3.0.json').exists())
        self.assertTrue(qualifier.distribution_errors(ROOT, {'fixture': True, **result}))

    def test_smoke_sans_CLI_epinglee_refuse(self) -> None:
        declared = copy.deepcopy(self.pins)
        del declared['smoke_cli']
        with self.assertRaisesRegex(ValueError, 'Deux toolchains'):
            self.prove(declared=declared)
        with self.assertRaisesRegex(ValueError, 'Smoke sans CLI épinglée'):
            self.memory_checked({'plugin_commit': COMMIT, 'origin': {'kind': 'real_smoke', 'synthetic': False, 'dry_run': False}})

    def test_verrou_smoke_absent_refuse_sans_fallback(self) -> None:
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/measurement-cli.json').write_bytes((ROOT / 'scripts/measurement-cli.json').read_bytes())
        with self.assertRaisesRegex(ValueError, 'absente ou non épinglée'):
            cli.toolchains(self.root)

    def test_version_ou_SHA_de_verrou_absent_refuse(self) -> None:
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/measurement-cli.json').write_bytes((ROOT / 'scripts/measurement-cli.json').read_bytes())
        for key in ('version', 'sha256'):
            value = copy.deepcopy(self.pins['smoke_cli']); del value[key]
            (self.root / 'scripts/smoke-cli.json').write_text(json.dumps({'smoke_cli': value}), encoding='utf-8')
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'absente ou non épinglée'):
                cli.toolchains(self.root)

    def test_recu_smoke_autre_SHA_ou_version_refuse(self) -> None:
        for key, value in [('cli_sha256', self.pins['campaign_cli']['sha256']), ('cli_version', 'codex-cli autre')]:
            bad = copy.deepcopy(self.smoke); bad[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Reçu CLI différent'):
                self.prove(smoke_receipt=bad)

    def test_relecture_sous_autre_CLI_que_campagne_refusee(self) -> None:
        with self.assertRaisesRegex(ValueError, 'campaign_cli'):
            self.prove(reviews=self.smoke)

    def test_recu_dune_autre_phase_refuse_meme_SHA(self) -> None:
        bad = copy.deepcopy(self.smoke); bad['cli_phase'] = 'campaign_cli'
        with self.assertRaisesRegex(ValueError, 'smoke_cli'):
            self.prove(smoke_receipt=bad)

    def test_recu_smoke_sans_compagnons_ou_identite_complete_refuse(self) -> None:
        for key in ('cli_phase', 'cli_toolchain'):
            bad = copy.deepcopy(self.smoke); del bad[key]
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Reçu CLI différent'):
                self.prove(smoke_receipt=bad)
        bad = copy.deepcopy(self.smoke); bad['cli_toolchain']['companions_sha256'].pop('codex-command-runner.exe')
        with self.assertRaisesRegex(ValueError, 'Reçu CLI différent'):
            self.prove(smoke_receipt=bad)

    def test_checked_smoke_refuse_recu_ancien_CLI(self) -> None:
        body = {'plugin_commit': COMMIT, 'model_requested': 'fixture-non-mesuree', 'origin': self.campaign}
        with self.assertRaisesRegex(ValueError, 'Reçu CLI réel incomplet'):
            self.memory_checked(body)

    def test_checked_smoke_suit_le_pin_smoke_courant_en_H1_et_H2(self) -> None:
        # Pré-vol du 07/11/2026 : un reçu smoke H2 (commit non lié) était comparé au pin 0.163.
        for state, context in self.binding_states():
            with self.subTest(etat=state), context:
                pin = cli.phase_pin('smoke_cli')
                receipt = {**copy.deepcopy(self.campaign), 'cli_version': pin['version'], 'cli_sha256': pin['sha256'],
                           'cli_phase': 'smoke_cli', 'cli_toolchain': pin}
                body = {'plugin_commit': COMMIT, 'model_requested': 'fixture-non-mesuree', 'origin': receipt}
                self.assertEqual(self.memory_checked(body)['origin'], receipt)
                other = cli._pin(cli.CAMPAIGN_140_CLI if state == 'H2' else cli.CAMPAIGN_150_CLI, True)
                bad = {**receipt, 'cli_version': other['version'], 'cli_sha256': other['sha256'], 'cli_toolchain': other}
                with self.assertRaisesRegex(ValueError, 'Reçu CLI réel incomplet'):
                    self.memory_checked({**body, 'origin': bad})

    def test_checked_campagne_refuse_recu_smoke(self) -> None:
        body = {'plugin_commit': COMMIT, 'model_requested': 'fixture-non-mesuree', 'origin': self.smoke}
        with self.assertRaisesRegex(ValueError, 'Reçu CLI réel incomplet'):
            self.memory_checked(body, 'campaign_cli')

    def test_ancien_recu_campagne_admis_sans_recriture(self) -> None:
        before = SOURCE.read_bytes()
        self.assertEqual(common.checked(SOURCE, COMMIT, {'real_cli'})['origin'], self.campaign)
        self.assertEqual(SOURCE.read_bytes(), before)

    def test_phase_inconnue_refusee(self) -> None:
        with self.assertRaisesRegex(ValueError, 'Phase CLI inconnue'):
            cli.phase_pin('auto')

    def test_compagnon_absent_ou_altere_refuse_avant_processus(self) -> None:
        package = self.root / 'codex.exe'; package.write_bytes(b'fixture-binaire-non-executable')
        expected = copy.deepcopy(self.pins['smoke_cli']); expected['sha256'] = cli.sha(package)
        expected['companions_sha256'] = {n: common.digest(n.encode()) for n in cli.COMPANIONS}
        for missing in sorted(cli.COMPANIONS):
            for name in cli.COMPANIONS:
                companion = package.with_name(name)
                if companion.exists():
                    companion.unlink()
                if name != missing:
                    companion.write_bytes(name.encode())
            with patch.object(cli, 'phase_pin', return_value=expected), patch.object(common.subprocess, 'run') as process:
                with self.assertRaisesRegex(ValueError, 'Compagnon smoke absent ou altéré'):
                    common.verify_codex_cli(package, 'smoke_cli')
                process.assert_not_called()
        for name in cli.COMPANIONS:
            package.with_name(name).write_bytes(b'fixture-compagnon-altere')
        with patch.object(cli, 'phase_pin', return_value=expected), self.assertRaisesRegex(ValueError, 'Compagnon smoke'):
            common.verify_codex_cli(package, 'smoke_cli')

    def binding_states(self):
        """H1 réel, puis H2 simulé : smoke lié à la CLI de la mesure de la version courante (ADR 0031, 0034)."""
        # La liaison simulée est celle de la version du plugin, que phase_pin lit dans le manifeste.
        version = json.loads((ROOT / '.codex-plugin/plugin.json').read_bytes())['version']
        binding = {'1.5.0': 'MEASUREMENT_150_V4', '1.5.1': 'MEASUREMENT_151_V4', '1.5.2': 'MEASUREMENT_152_V4'}[version]
        # H1 explicite : le test reste valable une fois le dépôt réel lié en H2.
        yield 'H1', patch.object(cli, binding, None)
        bound = {'campaign_cli': cli._pin(cli.CAMPAIGN_150_CLI, True), 'case_contract_sha256': cli.CYCLE_V4[1]}
        h2 = contextlib.ExitStack()
        h2.enter_context(patch.object(cli, binding, 'f' * 40))
        h2.enter_context(patch.object(cli, 'measurement_contract',
                                      lambda root, commit: bound if commit == 'f' * 40 else None))
        yield 'H2', h2

    @unittest.skipIf(sys.platform != 'win32', 'Binaire Windows local epingle et compagnons requis')
    @unittest.skipUnless(ACTUAL_CLI, 'Aucune CLI Codex locale : definir CT_CODEX_CLI ou installer la copie figee du harnais')
    def test_package_reel_smoke_verifie_sans_le_lancer(self) -> None:
        verified = []
        for state, context in self.binding_states():
            with self.subTest(etat=state), context, patch.object(common.subprocess, 'run') as process:
                expected = cli.phase_pin('smoke_cli')
                if state == 'H1':
                    self.assertEqual(expected, self.pins['smoke_cli'])
                else:
                    self.assertEqual(expected, cli._pin(cli.CAMPAIGN_150_CLI, True))
                if cli.sha(ACTUAL_CLI) == expected['sha256']:
                    self.assertEqual(common.verify_codex_cli(ACTUAL_CLI, 'smoke_cli'), expected)
                    verified.append(state)
                else:
                    with self.assertRaisesRegex(ValueError, 'CLI différente du binaire de mesure épinglé'):
                        common.verify_codex_cli(ACTUAL_CLI, 'smoke_cli')
                process.assert_not_called()
        self.assertTrue(verified, 'La CLI locale ne correspond au pin smoke ni en H1 ni en H2')

    @unittest.skipIf(sys.platform != 'win32', 'Binaire Windows local epingle et compagnons requis')
    @unittest.skipUnless(ACTUAL_CLI, 'Aucune CLI Codex locale : definir CT_CODEX_CLI ou installer la copie figee du harnais')
    def test_recu_emis_lie_la_phase_et_les_compagnons_sans_modele(self) -> None:
        synthetic = subprocess.CompletedProcess([], 0,
            '{"type":"thread.started","thread_id":"00000000-0000-0000-0000-000000000123"}\n{"type":"turn.completed"}\n', '')
        emitted = []
        for state, context in self.binding_states():
            with context:
                expected = cli.phase_pin('smoke_cli')
                if cli.sha(ACTUAL_CLI) != expected['sha256']:
                    continue
                with self.subTest(etat=state), patch.object(common.subprocess, 'run', return_value=synthetic) as process:
                    _, code, receipt = common.run_cli([str(ACTUAL_CLI), 'exec'], 'FIXTURE SANS MODELE', self.root, 1,
                                                      cli_phase='smoke_cli')
                    self.assertEqual(code, 0)
                    self.assertEqual(process.call_count, 1)  # Appel simulé, aucun processus réel.
                    self.assertEqual(receipt['cli_phase'], 'smoke_cli')
                    self.assertEqual(receipt['cli_toolchain'], expected)
                    emitted.append(state)
        self.assertTrue(emitted, 'La CLI locale ne correspond au pin smoke ni en H1 ni en H2')

    def test_transition_naccepte_pas_derive_du_lecteur(self) -> None:
        measured = json.loads(SOURCE.read_bytes())
        target = copy.deepcopy(measured)  # Mutation du protocole à runtime historique identique.
        target['toolchain_sha256']['scripts/measurement_common.py'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Protocole ou outillage'):
            human.compatible(ROOT, measured, target)


if __name__ == '__main__':
    unittest.main()
