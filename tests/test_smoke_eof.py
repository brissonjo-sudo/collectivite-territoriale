"""L30 : bornes du runtime et lectures diagnostiques, aucun modele ni processus."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_codex_smoke as smoke
from test_smoke_prompt import PREFIX

N=85

class SmokeEofTests(unittest.TestCase):
    def test_tous_les_markdown_non_vides_et_non_multiples_de_N(self):
        files=sorted((ROOT/'skills').rglob('*.md'))
        self.assertTrue(files)
        self.assertEqual(len({p.relative_to(ROOT/'skills').parts[0] for p in files}),7)
        self.assertIn('avec N = '+str(N)+' et M = 0 puis M + N.',PREFIX)
        self.assertLessEqual(N,90)
        for path in files:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertFalse(path.is_symlink())
                count=len(path.read_text(encoding='utf-8').splitlines(keepends=True))
                self.assertGreater(count,0,'Fichier vide : regle de fin incompatible')
                self.assertNotEqual(count%N,0,'Longueur multiple de N : dernier segment court absent')

    def events(self,path):
        lines=path.read_text(encoding='utf-8').splitlines(keepends=True)
        events=[]
        for start in range(0,len(lines),N):
            output=''.join(lines[start:start+N])
            events.append({'type':'item.completed','item':{'type':'command_execution',
                'status':'completed','exit_code':0,
                'command':f"Get-Content -LiteralPath '{path}' -Encoding utf8 | Select-Object -Skip {start} -First {N}",
                'aggregated_output':output}})
        return lines,events

    def test_dernier_segment_court_accepte_pour_tous_les_markdown(self):
        with tempfile.TemporaryDirectory(prefix='L30-LECTURE-DIAGNOSTIQUE-') as tmp:
            installed=Path(tmp)/'fixture-diagnostic-jamais-preuve'
            for source in sorted((ROOT/'skills').rglob('*.md')):
                path=installed/source.relative_to(ROOT)
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(source.read_bytes())
                with self.subTest(path=source.relative_to(ROOT).as_posix()):
                    lines,events=self.events(path)
                    reads=smoke.read_events(events,installed)
                    self.assertEqual([r['start'] for r in reads],list(range(0,len(lines),N)))
                    self.assertEqual(sum(r['count'] for r in reads),len(lines))
                    self.assertTrue(all(r['content_verified'] for r in reads))
                    self.assertGreater(reads[-1]['count'],0)
                    self.assertLess(reads[-1]['count'],N)
                    if path.name=='SKILL.md':
                        self.assertTrue(smoke.complete_entry(reads,path.parent.name))
                        self.assertFalse(smoke.complete_entry(reads+[reads[-1]],path.parent.name))

    def test_lecture_vide_apres_fin_et_sortie_tronquee_toujours_refusees(self):
        with tempfile.TemporaryDirectory(prefix='L30-REFUS-DIAGNOSTIQUE-') as tmp:
            installed=Path(tmp)/'fixture-diagnostic-jamais-preuve'
            path=installed/'skills/dcp-fpt/SKILL.md';path.parent.mkdir(parents=True)
            path.write_bytes((ROOT/'skills/dcp-fpt/SKILL.md').read_bytes())
            lines,events=self.events(path)
            self.assertEqual(len(lines),319)
            self.assertEqual([r['count'] for r in smoke.read_events(events,installed)],[85,85,85,64])
            beyond={'type':'item.completed','item':{'type':'command_execution','status':'completed','exit_code':0,
                'command':f"Get-Content -LiteralPath '{path}' -Encoding utf8 | Select-Object -Skip {len(events)*N} -First {N}",
                'aggregated_output':''}}
            diagnostic=installed.parent/'refus-diagnostic.json'
            with self.assertRaisesRegex(ValueError,'^Lecture installée tronquée ou échouée$'):
                smoke.read_events(events+[beyond],installed,diagnostic_path=diagnostic)
            value=json.loads(diagnostic.read_bytes())
            self.assertTrue(value['diagnostic_only'])
            self.assertEqual(value['output_chars'],0)
            events[-1]['item']['aggregated_output']='sortie tronquee diagnostique'
            with self.assertRaisesRegex(ValueError,'^Lecture installée tronquée ou échouée$'):
                smoke.read_events(events,installed)

if __name__=='__main__':unittest.main()
