"""L39 : replays diagnostiques EOF, aucun modèle ni shell exécuté."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_codex_smoke as smoke


class SmokeEofProbeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='L39-EOF-DIAGNOSTIQUE-')
        self.addCleanup(temporary.cleanup)
        self.installed = Path(temporary.name) / 'installation-fixture'

    def source(self, relative):
        path = self.installed / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / relative).read_bytes())
        return path

    def event(self, path, start, count=85, **changes):
        lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
        body = f"Get-Content -LiteralPath '{path}' -Encoding utf8 | Select-Object -Skip {start} -First {count}"
        item = {'type': 'command_execution', 'status': 'completed', 'exit_code': 0,
            'command': '"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "' + body + '"',
            'aggregated_output': ''.join(lines[start:start+count])}
        item.update(changes)
        return {'type': 'item.completed', 'item': item}

    def segments(self, path, count=85):
        length = len(path.read_text(encoding='utf-8').splitlines())
        return [self.event(path, start, count) for start in range(0, length, count)]

    def test_replay_L38d_reference_79_lignes_puis_sonde_85(self):
        path = self.source('skills/dcp-fpt/references/analyse-situation.md')
        self.assertEqual(len(path.read_text(encoding='utf-8').splitlines()), 79)
        probes = []
        events = [self.event(path, 0), self.event(path, 85)]
        reads = smoke.read_events(events, self.installed, eof_probes=probes)
        self.assertEqual([(r['start'], r['count']) for r in reads], [(0, 79)])
        self.assertEqual(len(probes), 1)
        self.assertEqual(probes[0]['start'], 85)
        self.assertTrue(probes[0]['coverage_verified'])
        self.assertFalse(probes[0]['counts_as_content'])
        self.assertEqual(probes[0]['source_sha256'], reads[0]['source_sha256'])
        self.assertFalse(smoke.complete_entry(reads, 'dcp-fpt'))

    def test_replay_L29b_entree_319_lignes_segments_90_puis_sonde_360(self):
        path = self.source('skills/dcp-fpt/SKILL.md')
        self.assertEqual(len(path.read_text(encoding='utf-8').splitlines()), 319)
        probes = []
        events = self.segments(path, 90) + [self.event(path, 360, 90)]
        reads = smoke.read_events(events, self.installed, eof_probes=probes)
        self.assertEqual([r['count'] for r in reads], [90, 90, 90, 49])
        self.assertTrue(smoke.complete_entry(reads, 'dcp-fpt'))
        self.assertEqual(len(probes), 1)
        self.assertEqual(sum(r['count'] for r in reads), 319)

    def test_sonde_a_la_borne_exacte_et_sortie_blanche_normalisee(self):
        path = self.source('skills/dcp-fpt/references/analyse-situation.md')
        probes = []
        reads = smoke.read_events([self.event(path, 0), self.event(path, 79, aggregated_output=' \r\n\t')],
                                  self.installed, eof_probes=probes)
        self.assertEqual(len(reads), 1)
        self.assertEqual(len(probes), 1)

    def test_sonde_avant_couverture_complete_refusee(self):
        path = self.source('skills/dcp-fpt/SKILL.md')
        events = self.segments(path)
        for previous in ([], events[:-1], events[1:], [events[1], events[0], *events[2:]]):
            with self.subTest(previous=len(previous)), self.assertRaises(ValueError):
                smoke.read_events(previous + [self.event(path, 340)], self.installed)

    def test_lecture_vide_au_milieu_et_sortie_tronquee_refusees(self):
        path = self.source('skills/dcp-fpt/SKILL.md')
        for output in ('', 'sortie tronquée diagnostique'):
            with self.subTest(output=output), self.assertRaisesRegex(ValueError, 'tronquée ou échouée'):
                smoke.read_events([self.event(path, 0), self.event(path, 85, aggregated_output=output)], self.installed)

    def test_sonde_sortie_non_vide_ou_echec_refusee(self):
        path = self.source('skills/dcp-fpt/references/analyse-situation.md')
        for changes in ({'aggregated_output': 'contenu inattendu'}, {'aggregated_output': None},
                        {'exit_code': 1}, {'status': 'failed'}, {'status': 'in_progress'}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'tronquée ou échouée'):
                smoke.read_events([self.event(path, 0), self.event(path, 85, **changes)], self.installed)

    def test_deux_sondes_meme_fichier_refusees_meme_offsets_distincts(self):
        path = self.source('skills/dcp-fpt/references/analyse-situation.md')
        for start in (85, 170):
            with self.subTest(start=start), self.assertRaisesRegex(ValueError, 'Sonde de fin de fichier répétée'):
                smoke.read_events([self.event(path, 0), self.event(path, 85), self.event(path, start)], self.installed)

    def test_sonde_ne_peut_emprunter_couverture_autre_fichier_ou_session(self):
        first = self.source('skills/dcp-fpt/references/analyse-situation.md')
        second = self.source('skills/dcp-fpt/SKILL.md')
        with self.assertRaises(ValueError):
            smoke.read_events([self.event(first, 0), self.event(second, 340)], self.installed)
        smoke.read_events([self.event(first, 0)], self.installed)
        with self.assertRaises(ValueError):
            smoke.read_events([self.event(first, 85)], self.installed)

    def test_une_sonde_par_fichier_distinct_acceptee(self):
        first = self.source('skills/dcp-fpt/references/analyse-situation.md')
        second = self.source('skills/dcp-fpt/SKILL.md')
        probes = []
        reads = smoke.read_events([self.event(first, 0), *self.segments(second),
            self.event(first, 85), self.event(second, 340)], self.installed, eof_probes=probes)
        self.assertEqual(len(probes), 2)
        self.assertEqual(len({p['path'] for p in probes}), 2)
        self.assertTrue(smoke.complete_entry(reads, 'dcp-fpt'))

    def test_doublon_de_contenu_et_chevauchement_refuses_apres_sonde_aussi(self):
        path = self.source('skills/dcp-fpt/SKILL.md')
        segments = self.segments(path)
        variants = [[segments[0], copy.deepcopy(segments[0])],
            [segments[0], self.event(path, 84)], segments + [self.event(path, 340), segments[0]]]
        for events in variants:
            with self.subTest(events=len(events)), self.assertRaisesRegex(ValueError, 'Lecture installée dupliquée'):
                smoke.read_events(events, self.installed)

    def test_commande_hors_contrat_reste_refusee_apres_couverture(self):
        path = self.source('skills/dcp-fpt/references/analyse-situation.md')
        event = self.event(path, 85)
        event['item']['command'] += '; Write-Output hors-contrat'
        with self.assertRaisesRegex(ValueError, 'Commande hors contrat'):
            smoke.read_events([self.event(path, 0), event], self.installed)


if __name__ == '__main__':
    unittest.main()
