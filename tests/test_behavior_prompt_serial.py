"""B8 : consigne exacte, sans changement du validateur ni du smoke."""
from pathlib import Path
import ast
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_codex_campaign as campaign

H1_A = 'db1308a990b42814844e73288831818a2a5d9c4c'
PHRASE = "Lis une seule entrée à la fois : termine tous ses segments avant d'ouvrir une autre entrée, sans lectures en parallèle."


class BehaviorPromptSerialTests(unittest.TestCase):
    def check_mode(self, mode):
        cases = json.loads((ROOT / 'scripts/cas-plugin-cycle-v3.json').read_bytes())
        case = next(case for case in cases if case.get('schema_version') == 2 and case['activation_mode'] == mode)
        raw = subprocess.check_output(['git', '-c', 'safe.directory=' + str(ROOT), 'show', H1_A + ':scripts/run_codex_campaign.py'], cwd=ROOT).decode('utf-8')
        node = next(node for node in ast.parse(raw).body if isinstance(node, ast.FunctionDef) and node.name == 'behavior_prompt')
        namespace = dict(campaign.__dict__)
        exec(compile(ast.get_source_segment(raw, node), '<prompt-historique-H1a>', 'exec'), namespace)
        original = namespace['behavior_prompt'](case)
        current = campaign.behavior_prompt(case)
        self.assertEqual(current.count(PHRASE), 1)
        anchor = 'Une entrée sélectionnée doit être lue entièrement par ses segments contigus, un appel par segment, max_output_tokens=8000 ; '
        self.assertIn(anchor + PHRASE + ' ', current)
        self.assertEqual(current.replace(PHRASE + ' ', '', 1), original)

    def test_cas_force_texte_exact_et_aucun_autre_changement(self):
        self.check_mode('forced')

    def test_cas_spontane_texte_exact_et_aucun_autre_changement(self):
        self.check_mode('spontaneous')


if __name__ == '__main__':
    unittest.main()
