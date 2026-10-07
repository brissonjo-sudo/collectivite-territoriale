"""Ne pas publier une identité locale ni dénaturer une source officielle."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import redact_native_evidence as redactor


class RedactionTests(unittest.TestCase):
    def test_chemin_personnel_relatif_et_reponse_source_empreintee(self):
        original = "Voir [méthode](C:/Users/CANARI/AppData/Local/Temp/ct-codex-campagne-x/.agents/skills/recherche-juridique/SKILL.md). Source https://www.legifrance.gouv.fr/"
        data = {"events":[{"type":"reply","text":original}]}
        bindings = redactor.redact(data)
        self.assertNotIn("CANARI",json.dumps(data))
        self.assertIn("(.agents/skills/recherche-juridique/SKILL.md)",data["events"][0]["text"])
        self.assertIn("https://www.legifrance.gouv.fr/",data["events"][0]["text"])
        self.assertEqual(bindings[0]["original_reply_sha256"],hashlib.sha256(original.encode()).hexdigest())
        self.assertEqual(bindings[0]["public_reply_sha256"],hashlib.sha256(data["events"][0]["text"].encode()).hexdigest())
        self.assertEqual(redactor.redact(data),[])
