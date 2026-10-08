"""Le diagnostic ne peut pas blanchir une autre commande ou une sortie altérée."""
import copy
import json
import sys
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import audit_native_reads as audit
from support_preuves_historiques import files_at


class AuditLecturesTests(unittest.TestCase):
    def setUp(self):
        folder=ROOT/'tests/evidence/2026-10-07-codex-natif-v3'
        self.evidence=json.loads((folder/'plugin-dcp-frontiere-dsi-externe.json').read_text(encoding='utf-8'))
        self.commands=json.loads((folder/'diagnostic-lectures.json').read_text(encoding='utf-8'))[self.evidence['case_id']]
        summary=json.loads((folder/'summary.json').read_text(encoding='utf-8'))
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        frozen=Path(temporary.name)
        for name,content in files_at(ROOT,summary['plugin_commit']).items():
            target=frozen/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
        for module in (audit,audit.campaign):
            context=patch.object(module,'ROOT',frozen)
            context.start()
            self.addCleanup(context.stop)

    def test_selection_autorisee_reconnue_sans_modifier_preuve_initiale(self):
        original=copy.deepcopy(self.evidence)
        verified,errors=audit.audit(self.evidence,self.commands)
        self.assertEqual(errors,[])
        self.assertEqual(len(verified),1)
        self.assertEqual(self.evidence,original)
        self.assertEqual(self.evidence['technical_status'],'failed')

    def test_sortie_differente_reste_un_echec(self):
        for event in self.evidence['events']:
            if event['type']=='unexpected_command':
                event['output_sha256']='0'*64
        verified,errors=audit.audit(self.evidence,self.commands)
        self.assertEqual(verified,[])
        self.assertIn('unexpected_command',errors)

    def test_commande_mixte_ne_peut_pas_etre_reclassee(self):
        for command in self.commands:
            command['command']+='; Write-Output secret'
        verified,errors=audit.audit(self.evidence,self.commands)
        self.assertEqual(verified,[])
        self.assertIn('unexpected_command',errors)
