"""CLI de d : propriétés sur fixtures en mémoire, aucun modèle ni nouvelle mesure."""
from pathlib import Path
import copy
import json
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import cli_toolchains as cli
import measurement_common as common
import human_resolution as human
from campaign_contract import load_cycle_cases, STOP_CYCLE_CASES

class CampaignDTests(unittest.TestCase):
    def test_pin_d_exact_et_trois_compagnons(self):
        pin=cli.phase_pin('campaign_cli',cli.MEASUREMENT_D)
        self.assertEqual(pin,cli.phase_pin('smoke_cli'))
        self.assertEqual(pin['version'],'codex-cli 0.163.0-alpha.10.2')
        self.assertEqual(pin['sha256'],'f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312')
        self.assertEqual(set(pin['companions_sha256']),cli.COMPANIONS)

    def test_0162_refusee_pour_d_meme_recu_ancien_sans_phase(self):
        old=cli.phase_pin('campaign_cli')
        current=cli.phase_pin('campaign_cli',cli.MEASUREMENT_D)
        origin={'cli_version':old['version'],'cli_sha256':old['sha256']}
        self.assertFalse(cli.receipt_matches(origin,'campaign_cli',current))
        source=ROOT/'tests/evidence/2026-10-18-candidat-1-3-0/campagne/plugin-mcp-indisponible/reponse/session.json'
        value=json.loads(source.read_bytes());value.pop('payload_sha256')
        value.update(plugin_commit=cli.MEASUREMENT_D,test_only_synthetic_fixture=True)
        raw=(json.dumps(common.seal(value),ensure_ascii=False,indent=2)+'\n').encode()
        path=Path('fixture-en-memoire-jamais-ecrite.json')
        original=Path.read_bytes
        with patch.object(Path,'read_bytes',lambda p:raw if p==path else original(p)):
            with self.assertRaisesRegex(ValueError,'Reçu CLI réel incomplet'):
                common.checked(path,cli.MEASUREMENT_D,{'real_cli'})

    def test_recu_d_exige_phase_et_compagnons_exacts(self):
        pin=cli.phase_pin('campaign_cli',cli.MEASUREMENT_D)
        origin={'cli_version':pin['version'],'cli_sha256':pin['sha256'],
            'cli_phase':'campaign_cli','cli_toolchain':copy.deepcopy(pin)}
        self.assertTrue(cli.receipt_matches(origin,'campaign_cli',pin))
        for field in ('cli_phase','cli_toolchain'):
            bad=copy.deepcopy(origin);del bad[field]
            self.assertFalse(cli.receipt_matches(bad,'campaign_cli',pin))
        bad=copy.deepcopy(origin);bad['cli_toolchain']['companions_sha256'].pop('codex-command-runner.exe')
        self.assertFalse(cli.receipt_matches(bad,'campaign_cli',pin))

    def test_empreintes_v1_refusees_pour_les_trois_cas_v2(self):
        historical={c['id']:c for c in json.loads((ROOT/'tests/cas-plugin.json').read_bytes())}
        current={c['id']:c for c in load_cycle_cases(ROOT)}
        for name in STOP_CYCLE_CASES:
            with self.subTest(case=name):
                self.assertTrue(current[name]['stop_first'])
                with self.assertRaisesRegex(ValueError,'Scénario mesuré différent'):
                    human.verify_case_hash({'case_sha256':common.digest(common.canonical(historical[name]))},current[name])
                human.verify_case_hash({'case_sha256':common.digest(common.canonical(current[name]))},current[name])

    def test_contrat_v2_absent_refuse_sans_repli(self):
        with self.assertRaisesRegex(ValueError,'Contrat de cycle v2'):
            human.bundle_cases(ROOT,ROOT,{'measurement_commit':cli.MEASUREMENT_D})

if __name__=='__main__':unittest.main()
