"""Fixtures synthétiques de projection : aucune campagne ou qualification réelle."""
from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import public_projection as public


class PublicProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix='projection-fixture-')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.raw, self.output = self.root / 'originaux', self.root / 'public'
        pieces = self.raw / public.PIECES
        pieces.mkdir(parents=True)
        self.thread = '00000000-0000-0000-0000-000000000321'
        self.reply = 'Verdict réservé. Source C:/Users/fixture/cache/.agents/skills/rj/SKILL.md ; home C:/Users/fixture/doc.txt.'
        session = {'fixture': True, 'origin': {'thread_id': self.thread}, 'reply': self.reply,
                   'judgment': 'respecte', 'usage': {'input_tokens': 37}, 'conversation_id': self.thread}
        (pieces / 'session.json').write_bytes((json.dumps(session, ensure_ascii=False, indent=2) + '\r\n').encode())
        self.sheet = (self.reply + '\r\nJugement inchangé.\r\n').encode()
        (pieces / 'fiche.md').write_bytes(self.sheet)
        (pieces / 'resume.json').write_bytes(b'{"fixture": true, "passed": 1}\r\n')
        self.opinion = (json.dumps({'fixture': True, 'verdict': 'reserve',
            'fiche_relecture_sha256': public.digest(self.sheet),
            'resume_campagne_sha256': public.digest((pieces / 'resume.json').read_bytes())}, indent=2) + '\r\n').encode()
        (pieces / 'avis.json').write_bytes(self.opinion)
        self.relative = 'tests/evidence/release-1.3.0.json'
        public.write_json(self.raw / self.relative, {'fixture': True, 'plugin_version': '1.3.0',
                                                    'release_evidence': False})

    def publish(self) -> dict:
        path = public.publish(self.raw, self.output, self.relative)
        return json.loads(path.read_bytes())

    def rebound(self, evidence: dict) -> dict:
        """Recalcule les liens d'une attaque de fixture pour éprouver le contrôle de fond."""
        table_path = self.output / public.TABLE
        table = json.loads(table_path.read_bytes())
        files = public.read_pieces(self.output)
        for name, raw in files.items():
            table['pieces'][name].update(projection_sha256=public.digest(raw), projection_octets=len(raw))
        table['links'] = public.graph(files, table['pieces'])
        table_path.write_text(json.dumps(table), encoding='utf-8')
        report_path = self.output / public.REPORT
        report = json.loads(report_path.read_bytes())
        report['table_sha256'] = public.digest(table_path.read_bytes())
        report_path.write_text(json.dumps(report), encoding='utf-8')
        evidence = copy.deepcopy(evidence)
        evidence['public_projection']['table']['sha256'] = public.digest(table_path.read_bytes())
        evidence['public_projection']['local_verification']['sha256'] = public.digest(report_path.read_bytes())
        return evidence

    def test_projection_deterministe_et_octets_hors_substitutions_identiques(self) -> None:
        evidence = self.publish()
        other = self.root / 'public-bis'
        public.publish(self.raw, other, self.relative)
        for path in self.output.rglob('*'):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (other / path.relative_to(self.output)).read_bytes())
        self.assertEqual((self.output / public.PIECES / 'avis.json').read_bytes(), self.opinion)
        expected_sheet = self.sheet.replace(b'C:/Users/fixture/cache/.agents/skills', b'<INSTALL>/.agents/skills').replace(b'C:/Users/fixture', b'<HOME>')
        self.assertEqual((self.output / public.PIECES / 'fiche.md').read_bytes(), expected_sheet)
        session = json.loads((self.output / public.PIECES / 'session.json').read_bytes())
        self.assertEqual(session['origin']['thread_id'], public.digest(self.thread.encode()))
        self.assertEqual(session['usage'], {'input_tokens': 37})
        self.assertEqual(session['judgment'], 'respecte')
        self.assertTrue((self.output / public.PIECES / 'session.json').read_bytes().endswith(b'\r\n'))
        public.verify_ci(self.output, evidence)

    def test_avis_lie_aux_originaux_et_a_la_projection_sans_reecriture(self) -> None:
        evidence = self.publish()
        view = public.verify_ci(self.output, evidence)
        self.assertEqual(view.fingerprint(self.output / public.PIECES / 'fiche.md'), public.digest(self.sheet))
        table = json.loads((self.output / public.TABLE).read_bytes())
        self.assertTrue(any(link['source'].endswith('/avis.json') and link['target'].endswith('/fiche.md')
                            and link['original_sha256'] == public.digest(self.sheet) for link in table['links']))

    def test_home_residuel_refuse_meme_liens_recalcules(self) -> None:
        evidence = self.publish()
        path = self.output / public.PIECES / 'fiche.md'
        path.write_bytes(path.read_bytes() + b'C:/Users/fixture/leak.txt')
        with self.assertRaisesRegex(ValueError, 'home résiduel'):
            public.verify_ci(self.output, self.rebound(evidence))

    def test_thread_residuel_refuse_meme_liens_recalcules(self) -> None:
        evidence = self.publish()
        path = self.output / public.PIECES / 'session.json'
        value = json.loads(path.read_bytes())
        value['origin']['thread_id'] = 'conversation-originale-de-fixture'
        path.write_text(json.dumps(value), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Identifiant de session résiduel'):
            public.verify_ci(self.output, self.rebound(evidence))

    def test_secret_residuel_refuse_meme_liens_recalcules(self) -> None:
        evidence = self.publish()
        path = self.output / public.PIECES / 'session.json'
        value = json.loads(path.read_bytes())
        value['access_token'] = 'valeur-de-fixture-sans-secret-reel'
        path.write_text(json.dumps(value), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Credential résiduel'):
            public.verify_ci(self.output, self.rebound(evidence))

    def test_piece_alteree_refusee(self) -> None:
        evidence = self.publish()
        path = self.output / public.PIECES / 'fiche.md'
        path.write_bytes(path.read_bytes() + b'Alteration')
        with self.assertRaisesRegex(ValueError, 'Projection altérée'):
            public.verify_ci(self.output, evidence)

    def test_original_absent_refuse_localement_pas_en_ci(self) -> None:
        evidence = self.publish()
        (self.raw / public.PIECES / 'session.json').unlink()
        with self.assertRaisesRegex(ValueError, 'Original ou projection absent'):
            public.verify_local(self.raw, self.output)
        public.verify_ci(self.output, evidence)

    def test_lien_avis_supprime_refuse_meme_table_reliee(self) -> None:
        evidence = self.publish()
        path = self.output / public.TABLE
        table = json.loads(path.read_bytes())
        table['links'].pop()
        path.write_text(json.dumps(table), encoding='utf-8')
        evidence['public_projection']['table']['sha256'] = public.digest(path.read_bytes())
        with self.assertRaisesRegex(ValueError, 'Liens de projection divergents'):
            public.verify_ci(self.output, evidence)

    def test_original_modifie_refuse_par_rederivation(self) -> None:
        self.publish()
        path = self.raw / public.PIECES / 'fiche.md'
        path.write_bytes(path.read_bytes() + b'Texte nouveau')
        with self.assertRaisesRegex(ValueError, 'Re-dérivation divergente'):
            public.verify_local(self.raw, self.output)

    def test_gzip_projete_deterministe_et_identifiants_prefixes(self) -> None:
        name = public.PIECES + '/session-comprimee.json.gz'
        original = json.dumps({'fixture': True, 'response_session_id': self.thread,
                               'conversation': {'id': self.thread}, 'path': 'C:/Users/fixture/f.txt'}).encode()
        (self.raw / name).write_bytes(gzip.compress(original, mtime=123))
        evidence = self.publish()
        value = json.loads(gzip.decompress((self.output / name).read_bytes()))
        self.assertEqual(value['response_session_id'], public.digest(self.thread.encode()))
        self.assertEqual(value['conversation']['id'], public.digest(self.thread.encode()))
        self.assertEqual(value['path'], '<HOME>/f.txt')
        public.verify_ci(self.output, evidence)
        public.verify_local(self.raw, self.output)

    def test_home_encode_en_unicode_refuse(self) -> None:
        raw = b'{"fixture":true,"path":"C:/\\u0055sers/fixture/f.txt"}'
        self.assertTrue(any('home résiduel' in error for error in public.privacy_errors('fixture.json', raw)))


if __name__ == '__main__':
    unittest.main()
