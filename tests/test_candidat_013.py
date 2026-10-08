"""Les preuves installées et historiques restent liées à leurs octets mesurés."""
import hashlib,json,subprocess,sys,unittest
import tempfile
from unittest.mock import patch
from pathlib import Path
from support_preuves_historiques import runtime_at, files_at

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_codex_campaign as campaign

def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(data):return hashlib.sha256(data).hexdigest()

class Candidat013Tests(unittest.TestCase):
    def test_mesure_dcp_correspond_aux_trente_fichiers_embarques(self):
        proof=load('tests/evidence/2026-10-08-candidat-013/dcp-autonome.json')
        source=load('upstream.json')['skills']['dcp-fpt']['commit']
        self.assertEqual(proof['upstream_runtime_commit'],source)
        runtime={name.removeprefix('skills/dcp-fpt/'):digest
            for name,digest in runtime_at(ROOT,'e26e84bdfbfae697d657b95217e1865df4d84cc2').items()
            if name.startswith('skills/dcp-fpt/') and not name.endswith('/LICENSE')}
        self.assertEqual(proof['summary']['runtime_sha256'],runtime)
        self.assertEqual(proof['summary']['case_count'],28)
        serialized=json.dumps(proof['summary'],ensure_ascii=False,indent=2)+'\n'
        self.assertEqual(sha(serialized.encode()),proof['source_summary_sha256'])
        self.assertTrue(proof['summary']['threshold_passed'])
        self.assertFalse(proof['summary']['publication_ready'])
        self.assertFalse(proof['human_legal_validation'])

    def test_neuf_premieres_reponses_liees_au_runtime_et_au_lanceur(self):
        summary=load('tests/evidence/2026-10-07-codex-natif-v5/summary.json')
        cases={c['id']:c for c in campaign.load_cases()}
        self.assertEqual({r['case_id'] for r in summary['runs']},set(cases))
        self.assertEqual(len(summary['runs']),9)
        self.assertFalse(summary['human_legal_validation'])
        self.assertFalse(summary['publication_ready'])
        runtime=runtime_at(ROOT,summary['plugin_commit'])
        runner=subprocess.run(['git','show',summary['plugin_commit']+':scripts/run_codex_campaign.py'],cwd=ROOT,check=True,capture_output=True).stdout
        self.assertEqual(sha(runner),summary['runner_sha256'])
        with tempfile.TemporaryDirectory() as directory:
            frozen=Path(directory)
            for name,content in files_at(ROOT,summary['plugin_commit']).items():
                target=frozen/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
            with patch.object(campaign,'ROOT',frozen):
                for run in summary['runs']:
                    value=load(run['evidence_path'])
                    self.assertEqual(sha((ROOT/run['evidence_path']).read_bytes()),run['evidence_sha256'])
                    self.assertEqual(value['runtime_sha256'],runtime)
                    self.assertEqual(value['runner_sha256'],summary['runner_sha256'])
                    errors=campaign.failures(value['events'],cases[run['case_id']],value['process_exit'],value['profile'])
                    self.assertEqual(errors,value['failures'])
                    self.assertEqual(run['technical_status'],'failed' if errors else 'passed')

    def test_relectures_separees_ne_valent_pas_avis_humain(self):
        summary=load('tests/evidence/2026-10-08-candidat-013/relecture-assistant.json')
        cases={c['id']:c for c in campaign.load_cases()}
        self.assertEqual({r['case_id'] for r in summary['runs']},set(cases))
        self.assertFalse(summary['human_legal_validation'])
        self.assertFalse(summary['publication_ready'])
        for run in summary['runs']:
            review=load(run['evidence_path'])
            source=ROOT/'tests/evidence/2026-10-07-codex-natif-v5'/(run['case_id']+'.json')
            proof=json.loads(source.read_text(encoding='utf-8'))
            reply=next(e['text'] for e in reversed(proof['events']) if e['type']=='reply')
            self.assertEqual(review['evidence_sha256'],sha(source.read_bytes()))
            self.assertEqual(review['reply_sha256'],sha(reply.encode()))
            self.assertFalse(review['human_legal_validation'])
            self.assertFalse(review['tools_used'])
            self.assertTrue(review['fresh_process'] and review['fresh_workspace'])
            self.assertEqual({r['invariant'] for r in review['report']['invariants']},set(cases[run['case_id']]['invariants']))
            self.assertEqual(sha((ROOT/run['evidence_path']).read_bytes()),run['evidence_sha256'])

    def test_cache_git_installe_correspond_au_commit_mesure(self):
        proof=load('tests/evidence/2026-10-08-candidat-013/installation-codex.json')
        self.assertEqual(proof['runtime_sha256'],runtime_at(ROOT,proof['plugin_commit']))
        self.assertEqual(proof['marketplace_source']['sha'],proof['plugin_commit'])
        for name, digest in proof['plugin_configuration_sha256'].items():
            blob=subprocess.run(['git','show',proof['plugin_commit']+':'+name],cwd=ROOT,check=True,capture_output=True).stdout
            self.assertEqual(sha(blob),digest)
        self.assertEqual(len(proof['visible_skills']),6)
        self.assertFalse(proof['credentials_copied'])
        self.assertTrue(proof['user_config_unchanged'])
        self.assertFalse(proof['native_workspace_skills'])
        self.assertFalse(proof['human_legal_validation'])
        self.assertFalse(proof['publication_ready'])
        self.assertFalse(proof['distributed_catalogue_tested'])
        runs={r['case_id']:r for r in proof['runs']}
        self.assertTrue(runs['activation-implicite']['stop_first'])
        for run in runs.values():
            self.assertEqual(run['process_exit'],0)
            self.assertTrue(run['candidate_entry_read'])
            self.assertTrue(run['installed_mcp_success'])
            reply=next(e['text'] for e in reversed(run['events']) if e['type']=='reply')
            self.assertEqual(sha(reply.encode()),run['final_reply_sha256'])
            self.assertTrue(any(c['server']=='droit-francais' and c['succeeded'] for c in run['mcp_trace']))
        self.assertNotRegex(json.dumps(proof),r'C:[/\\]+Users')

    def test_deux_rejets_historiques_restent_visibles(self):
        folder='tests/evidence/2026-10-07-codex-natif-v4'
        summary=load(folder+'/summary.json')
        self.assertEqual(summary['case_count'],9)
        self.assertEqual(summary['technical_passed_count'],7)
        self.assertFalse(summary['publication_ready'])
        runtime=runtime_at(ROOT,summary['plugin_commit'])
        for run in summary['runs']:
            proof=load(run['evidence_path'])
            self.assertEqual(proof['runtime_sha256'],runtime)
            self.assertEqual(proof['technical_status'],run['technical_status'])
            self.assertEqual(proof['failures'],run['failures'])
            if 'redaction' in proof:
                self.assertEqual(proof['redaction']['original_evidence_sha256'],run['evidence_sha256'])
            else:
                self.assertEqual(sha((ROOT/run['evidence_path']).read_bytes()),run['evidence_sha256'])
