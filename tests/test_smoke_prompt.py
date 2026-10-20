"""L29 : consigne exacte et refus des doublons, sans processus ni modèle."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_codex_smoke as smoke
import cli_toolchains as cli

PREFIX = (
    "Utilise les seuls skills pertinents du plugin installé, choisis spontanément leurs noms. "
    "Si STOP s'applique, il doit précéder toute annonce et tout outil. "
    "Lis toute entrée ou référence du cache uniquement par segments contigus avec "
    "Get-Content -LiteralPath 'chemin' -Encoding utf8 | Select-Object -Skip M -First N, "
    "avec N = 85 et M = 0 puis M + N. Un segment qui renvoie moins de N lignes marque la fin du fichier : "
    "ne lis jamais au-delà ; sinon, lis seulement le segment suivant. "
    "Ne fais aucune lecture intégrale et ne relis jamais une ligne, même si la restitution est signalée tronquée. "
    "Si une restitution reste incomplète, signale la limite et n'affirme rien des lignes non reçues, sans arrêter la réponse. "
    "Chaque entrée SKILL.md sélectionnée doit être lue jusqu'à sa fin, marquée par le premier segment de moins de 85 lignes. "
    "Une restitution perçue comme tronquée ne permet ni de relire ni d'interrompre la série : "
    "poursuis avec le segment suivant (M + 85), puis signale la limite dans la réponse. "
    "Aucune autre commande ni accès aux profils. Utilise le MCP juridique installé, sans web. "
)


class SmokePromptTests(unittest.TestCase):
    def test_texte_exact_deux_cas_sans_activation_nommee(self):
        for case in smoke.CASES:
            expected = PREFIX + ("Récupère effectivement une source officielle avec le MCP installé, sans inventer d'identifiant. "
                                 if case == 'mcp-installe' else '') + smoke.source_case(ROOT, case)['prompt']
            self.assertEqual(smoke.smoke_prompt(ROOT, case), expected)
        implicit = smoke.smoke_prompt(ROOT, 'activation-implicite')
        for name in ('dcp-fpt', 'recherche-juridique', 'dsi-fpt', 'dpo-ct', 'dpm-fpt', 'dirfi-fpt', 'drh-fpt'):
            self.assertNotIn(name, implicit)

    def test_doublon_integral_et_chevauchement_toujours_refuses(self):
        full = {'path': 'skills/recherche-juridique/SKILL.md', 'start': 0,
                'count': 1162, 'line_count': 1162, 'content_verified': True}
        self.assertTrue(smoke.complete_entry([full], 'recherche-juridique'))
        self.assertFalse(smoke.complete_entry([full, copy.deepcopy(full)], 'recherche-juridique'))
        segments = [{**full, 'start': start, 'count': min(90, 1162-start)} for start in range(0, 1162, 90)]
        self.assertTrue(smoke.complete_entry(segments, 'recherche-juridique'))
        for variant in ([full] + segments, segments + [full], segments[:-1],
                        [segments[0], segments[0]] + segments[1:]):
            self.assertFalse(smoke.complete_entry(variant, 'recherche-juridique'))
        incomplete = copy.deepcopy(segments); incomplete[0]['content_verified'] = False
        self.assertFalse(smoke.complete_entry(incomplete, 'recherche-juridique'))

    def transition(self):
        manifest = json.loads((ROOT / cli.TRANSITION_D).read_bytes())
        measured = {'plugin_commit': cli.MEASUREMENT_D, 'toolchain_sha256': manifest['source_files_sha256']}
        target = {'toolchain_sha256': {name: cli.sha(ROOT / name) for name in cli.MIGRATION_D}}
        return manifest, measured, target

    def test_transition_d_accepte_uniquement_le_runner_exact_epingle(self):
        _, measured, target = self.transition()
        self.assertEqual(cli.compatibility_files(ROOT, measured, target), cli.MIGRATION_D)
        for field in ('source', 'target'):
            old, new = copy.deepcopy(measured), copy.deepcopy(target)
            (old if field == 'source' else new)['toolchain_sha256']['scripts/run_codex_smoke.py'] = '0'*64
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'transition d refusée'):
                cli.compatibility_files(ROOT, old, new)

    def test_transition_d_refuse_un_chemin_supplementaire(self):
        manifest, measured, target = self.transition()
        manifest['source_files_sha256']['scripts/qualify_distribution.py'] = '0'*64
        manifest['target_files_sha256']['scripts/qualify_distribution.py'] = '0'*64
        raw = json.dumps(manifest).encode()
        original = Path.read_bytes
        with patch.object(Path, 'read_bytes', lambda p: raw if p == ROOT / cli.TRANSITION_D else original(p)):
            with self.assertRaisesRegex(ValueError, 'transition d refusée'):
                cli.compatibility_files(ROOT, measured, target)


if __name__ == '__main__':
    unittest.main()
