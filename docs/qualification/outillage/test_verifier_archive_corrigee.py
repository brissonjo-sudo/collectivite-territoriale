"""Rejeux et mutations synthétiques en mémoire, sans modifier les pièces."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import lie_jugements_corriges as binder
import verifier_archive_corrigee as verifier
import lie_jugements_corriges_bruts as raw_binder

RAW_ADAPTER_BYTES = Path(raw_binder.__file__).read_bytes()


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / 'archive-synthetique-virtuelle'
        self.directory = self.root / 'run/cas-01'
        self.origin = 'Y:/origine'
        self.prefix = self.origin + '/run/cas-01'
        self.parent_path = self.root / 'parent.jsonl'
        self.files = {}
        self.addCleanup(patch.stopall)
        patch.object(verifier, 'ROOT', self.root).start()
        patch.object(Path, 'read_text', lambda p, *a, **k: self.files[p].decode('utf-8')).start()
        patch.object(Path, 'read_bytes', lambda p: self.files[p]).start()
        patch.object(Path, 'is_file', lambda p: p in self.files).start()
        self.question = 'Comment cadrer le rôle du DSI ?'
        self.response = 'Réponse synthétique.\n'
        self.put(self.directory / 'prompt.md', self.question + '\n')
        self.put(self.directory / 'runtime/SKILL.md', 'Skill synthétique.\n')
        self.put(self.directory / 'response.md', self.response)
        self.put_json(self.directory.parent / 'suite.json', [{'id': 'cas-01', 'prompt': self.question}])
        self.manifest = {'suite_sha256': verifier.digest(self.directory.parent / 'suite.json'),
            'runtime_sha256': {'SKILL.md': verifier.digest(self.directory / 'runtime/SKILL.md')}}
        self.exported = {'created_at': '2026-10-06T20:00:00Z',
            'runtime_sha256': self.manifest['runtime_sha256'],
            'question_sha256': verifier.digest(self.directory / 'prompt.md')}
        self.put_json(self.directory / 'responder.export.json', self.exported)
        self.packet = {'case_id': 'cas-01', 'response': self.response,
            'response_sha256': verifier.digest(self.directory / 'response.md')}
        self.judgment = {'verdict': 'RÉUSSITE', 'notes': 'Fixture.',
            'response_sha256': self.packet['response_sha256']}
        self.put_json(self.directory / 'judge.packet.json', self.packet)
        self.put_json(self.directory / 'judgment.json', self.judgment)
        self.parent = [self.event(0, 'session_meta', {'id': 'parent', 'timestamp': self.time(0)})]
        self.respondent, self.respondent_proof = self.native('respondant', False)
        self.judge, self.judge_proof = self.native('juge', True)
        self.save()

    def time(self, seconds):
        return f'2026-10-06T20:00:{seconds:02d}Z'

    def event(self, seconds, kind, payload):
        return {'timestamp': self.time(seconds), 'type': kind, 'payload': payload}

    def put(self, path, value):
        self.files[path] = value.encode('utf-8')

    def put_json(self, path, value):
        self.put(path, json.dumps(value, ensure_ascii=False))

    def put_events(self, path, events):
        self.put(path, ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events))

    def native(self, role, judge):
        agent, turn, session = '/root/' + role, 'tour-' + role, 'session-' + role
        self.parent.extend([
            self.event(1, 'response_item', {'type': 'function_call', 'name': 'spawn_agent',
                'call_id': 'spawn-' + role, 'arguments': json.dumps({'task_name': role,
                    'fork_turns': 'none', 'message': self.question})}),
            self.event(3, 'response_item', {'type': 'function_call_output', 'call_id': 'spawn-' + role,
                'output': json.dumps({'task_name': agent})})])
        read_target = '/judge.packet.json' if judge else '/runtime/SKILL.md'
        read_result = json.dumps(self.packet, ensure_ascii=False) if judge else 'Skill synthétique.\n'
        target = '/judgment.json' if judge else '/response.md'
        content = json.dumps(self.judgment, ensure_ascii=False) if judge else self.response.rstrip('\n')
        patch_value = '\n'.join(['*** Begin Patch', '*** Add File: ' + self.prefix + target,
            *('+' + line for line in content.splitlines()), '*** End Patch'])
        def call(seconds, identifier, script):
            return self.event(seconds, 'response_item', {'type': 'custom_tool_call',
                'name': 'exec', 'call_id': identifier, 'input': script})
        def result(seconds, identifier, value):
            return self.event(seconds, 'response_item', {'type': 'custom_tool_call_output',
                'call_id': identifier, 'output': [{'type': 'text', 'text': 'Script completed\n'},
                    {'type': 'text', 'text': json.dumps(value, ensure_ascii=False)}]})
        read_id, write_id = 'read-' + role, 'write-' + role
        events = [self.event(2, 'session_meta', {'id': session, 'timestamp': self.time(2),
            'source': {'subagent': {'thread_spawn': {'agent_path': agent, 'parent_thread_id': 'parent'}}}}),
            self.event(3, 'event_msg', {'type': 'task_started', 'turn_id': turn}),
            self.event(4, 'turn_context', {'turn_id': turn, 'model': 'modele-fixture'}),
            call(5, read_id, 'text(await tools.exec_command(' + json.dumps({'cmd':
                "Get-Content -LiteralPath '" + self.prefix + read_target + "' -Raw",
                'max_output_tokens': 55000}) + '));'),
            result(6, read_id, {'exit_code': 0, 'output': read_result}),
            call(7, write_id, 'text(await tools.apply_patch(' + json.dumps(patch_value) + '));'),
            result(8, write_id, {}), self.event(9, 'event_msg', {'type': 'task_complete', 'turn_id': turn})]
        proof = {'agent': agent, 'session_id': session, 'parent_thread_id': 'parent',
            'turn_id': turn, 'models': ['modele-fixture'], 'completed': True, 'fork_turns': 'none',
            'spawn_call_id': 'spawn-' + role, 'spawn_timestamp': self.time(1),
            'read_call_ids': [read_id], 'write_call_ids': [write_id],
            'response_sha256': verifier.digest(self.directory / 'response.md')}
        if judge:
            proof.update(comparison='full_json', exact_read_path_format='absolute_posix',
                packet_sha256=verifier.digest(self.directory / 'judge.packet.json'),
                judgment_sha256=verifier.digest(self.directory / 'judgment.json'),
                judge_identity_checked=True, spawn_evidence={'task_name': agent, 'fork_turns': 'none',
                    'call_id': 'spawn-' + role, 'returned_task_name': agent})
        else:
            proof.update(read_runtime_files=['SKILL.md'], runtime_only_reads=True, skill_read_first=True,
                response_patch_comparison='exact_text')
        return events, proof

    def save(self):
        self.put_events(self.parent_path, self.parent)
        for role, events, proof in [('repondant', self.respondent, self.respondent_proof),
                                   ('juge', self.judge, self.judge_proof)]:
            trace = self.directory / ('liaison/trace-' + role + '.jsonl')
            self.put_events(trace, events)
            proof['trace_sha256'] = verifier.digest(trace)
            self.put_json(self.directory / ('liaison/execution-' + role + '.json'), proof)

    def replay_respondent(self):
        reports = []
        result = verifier.replay_responder(self.directory, self.manifest, self.parent,
            self.origin, reports)
        return result, reports[0]

    def replay_judge(self):
        return verifier.replay_judge(self.directory, self.directory / 'judge.packet.json',
            self.directory / 'judgment.json', self.parent_path,
            self.directory / 'liaison/execution-juge.json', self.origin, self.exported['created_at'])

    def test_relocalisation_et_question_claire(self):
        self.assertEqual(self.replay_judge(), 'session-juge')
        identity, report = self.replay_respondent()
        self.assertEqual(identity, 'session-respondant')
        self.assertTrue(report['initial_message_verified'])
        self.assertTrue(report['frozen_prompt_verified'])

    def test_metadonnees_dupliquees_refusees_pour_chaque_role_et_parent(self):
        for target in (self.respondent, self.judge, self.parent):
            with self.subTest(target=target[0]['payload']['id']):
                target.append(copy.deepcopy(target[0])); self.save()
                with self.assertRaisesRegex(ValueError, 'Métadonnées'):
                    self.replay_judge() if target is self.judge else self.replay_respondent()
                target.pop(); self.save()

    def test_champs_liaison_juge_alteres_refuses(self):
        mutations = {'spawn_call_id': 'inexistant', 'turn_id': 'autre',
            'read_call_ids': ['autre'], 'write_call_ids': ['autre'],
            'spawn_timestamp': self.time(0), 'packet_sha256': '0' * 64,
            'completed': 1, 'comparison': 'autre', 'judge_identity_checked': False,
            'spawn_evidence': {'call_id': 'autre'}}
        for field, value in mutations.items():
            with self.subTest(field=field):
                old = self.judge_proof[field]; self.judge_proof[field] = value; self.save()
                with self.assertRaisesRegex(ValueError, 'liaison divergent'):
                    self.replay_judge()
                self.judge_proof[field] = old; self.save()

    def test_champs_liaison_repondant_alteres_refuses(self):
        for field in ('spawn_call_id', 'turn_id', 'read_call_ids', 'write_call_ids'):
            with self.subTest(field=field):
                old = self.respondent_proof[field]
                self.respondent_proof[field] = ['autre'] if isinstance(old, list) else 'autre'; self.save()
                with self.assertRaisesRegex(ValueError, 'liaison divergent'):
                    self.replay_respondent()
                self.respondent_proof[field] = old; self.save()

    def test_question_claire_differente_refusee(self):
        args = json.loads(self.parent[1]['payload']['arguments']); args['message'] = 'Autre question.'
        self.parent[1]['payload']['arguments'] = json.dumps(args)
        with self.assertRaisesRegex(ValueError, 'Question différente'):
            self.replay_respondent()

    def test_question_chiffree_non_demontrable_sans_faux_succes(self):
        args = json.loads(self.parent[1]['payload']['arguments']); args['message'] = 'gAAAA_TEST_OPAQUE=='
        self.parent[1]['payload']['arguments'] = json.dumps(args)
        _, report = self.replay_respondent()
        self.assertFalse(report['initial_message_verified'])
        self.assertFalse(report['question_file_read_verified'])
        self.assertTrue(report['frozen_prompt_verified'])
        self.respondent_proof['initial_message_verified'] = True; self.save()
        with self.assertRaisesRegex(ValueError, 'initial_message_verified'):
            self.replay_respondent()

    def test_enveloppe_non_figee_ne_prouve_pas_la_question(self):
        args = json.loads(self.parent[1]['payload']['arguments'])
        args['message'] = 'Lis le runtime. Question : ' + self.question
        self.parent[1]['payload']['arguments'] = json.dumps(args)
        self.assertFalse(self.replay_respondent()[1]['initial_message_verified'])

    def test_provenance_fichier_autre_session_refusee(self):
        self.judge_proof['native_session_file'] = 'rollout-2026-10-06-autre-session.jsonl'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Fichier de session'):
            self.replay_judge()

    def test_prompt_modifie_refuse_meme_avec_nouvelle_empreinte_export(self):
        self.put(self.directory / 'prompt.md', 'Autre question.\n')
        self.exported['question_sha256'] = verifier.digest(self.directory / 'prompt.md')
        self.put_json(self.directory / 'responder.export.json', self.exported)
        with self.assertRaisesRegex(ValueError, 'Prompt'):
            self.replay_respondent()

    def test_code_de_trace_ajoute_refuse_sans_execution(self):
        self.judge[5]['payload']['input'] += 'text(await tools.exec_command({"cmd":"evil"}));'
        self.save()
        with self.assertRaises(ValueError):
            self.replay_judge()

    def add_question_read(self):
        read = copy.deepcopy(self.respondent[3]); result = copy.deepcopy(self.respondent[4])
        read['payload']['call_id'] = 'question-respondant'
        read['payload']['input'] = 'text(await tools.exec_command(' + json.dumps({'cmd':
            "Get-Content -LiteralPath '" + self.prefix + "/prompt.md' -Raw",
            'max_output_tokens': 55000}) + '));'
        result['payload']['call_id'] = 'question-respondant'
        result['payload']['output'][1]['text'] = json.dumps({'exit_code': 0, 'output': self.question + '\n'})
        self.respondent[5:5] = [read, result]
        self.respondent_proof.update(runtime_only_reads=False,
            runtime_and_single_question_reads_only=True, question_file_read_verified=True,
            question_read_call_id='question-respondant',
            question_sha256=verifier.digest(self.directory / 'prompt.md'))
        self.respondent_proof['read_call_ids'].append('question-respondant')
        args = json.loads(self.parent[1]['payload']['arguments']); args.pop('message')
        self.parent[1]['payload']['arguments'] = json.dumps(args)
        self.save()

    def test_question_lue_complete_prouvee_sans_message_initial(self):
        self.add_question_read()
        _, report = self.replay_respondent()
        self.assertTrue(report['question_file_read_verified'])
        self.assertFalse(report['initial_message_verified'])

    def test_question_lue_tronquee_refusee(self):
        self.add_question_read()
        self.respondent[6]['payload']['output'][1]['text'] = json.dumps({'exit_code': 0, 'output': self.question[:5]})
        self.save()
        with self.assertRaisesRegex(ValueError, 'Lecture de question'):
            self.replay_respondent()

    def test_question_lue_dupliquee_refusee(self):
        self.add_question_read()
        extra = copy.deepcopy(self.respondent[5:7])
        for event in extra:
            event['payload']['call_id'] = 'deuxieme-question'
        self.respondent[7:7] = extra; self.save()
        with self.assertRaisesRegex(ValueError, 'Lecture de question'):
            self.replay_respondent()

    def test_question_avant_skill_refusee(self):
        self.add_question_read()
        self.respondent[3:7] = self.respondent[5:7] + self.respondent[3:5]; self.save()
        with self.assertRaisesRegex(ValueError, 'Lecture de question'):
            self.replay_respondent()

    def test_identifiant_lecture_question_falsifie_refuse(self):
        self.add_question_read()
        self.respondent_proof['question_read_call_id'] = 'inexistant'; self.save()
        with self.assertRaisesRegex(ValueError, 'question_read_call_id'):
            self.replay_respondent()

    def test_exit_code_booleen_refuse(self):
        for question in (False, True):
            with self.subTest(question=question):
                if question:
                    self.add_question_read()
                index = 6 if question else 4
                value = json.loads(self.respondent[index]['payload']['output'][1]['text'])
                value['exit_code'] = False
                self.respondent[index]['payload']['output'][1]['text'] = json.dumps(value); self.save()
                with self.assertRaises(ValueError):
                    self.replay_respondent()


class RawArchiveTests(ArchiveTests):
    def setUp(self):
        super().setUp()
        self.files[Path(raw_binder.__file__)] = RAW_ADAPTER_BYTES
        self.files[self.root / 'lie_jugements_corriges_bruts.py'] = RAW_ADAPTER_BYTES
        self.judge[3]['payload']['input'] = raw_binder.read_script({'cmd':
            "Get-Content -LiteralPath '" + self.prefix + "/judge.packet.json' -Raw",
            'max_output_tokens': 55000})
        self.judge[4]['payload']['output'] = [
            {'type': 'text', 'text': 'Script completed\n'},
            {'type': 'text', 'text': '{"exit_code":0}'},
            {'type': 'text', 'text': json.dumps(self.packet, ensure_ascii=False)}]
        self.judge_proof.update(raw_adapter_sha256=verifier.digest(Path(raw_binder.__file__)),
            raw_projection=raw_binder.PROJECTION, initial_message_verified=False)
        self.save()

    def test_adaptateur_brut_altere_refuse(self):
        self.judge_proof['raw_adapter_sha256'] = '0' * 64; self.save()
        with self.assertRaisesRegex(ValueError, 'Adaptateur brut'):
            self.replay_judge()

    def test_sortie_brute_tronquee_refusee(self):
        self.judge[4]['payload']['output'][2]['text'] = '{}'; self.save()
        with self.assertRaisesRegex(ValueError, 'tronquée'):
            self.replay_judge()

    def test_operation_brute_ajoutee_refusee(self):
        self.judge[3]['payload']['input'] += ' text("intrus");'; self.save()
        with self.assertRaisesRegex(ValueError, 'grammaire'):
            self.replay_judge()

    def test_retour_ligne_final_brut_accepte(self):
        self.judge[3]['payload']['input'] += '\n'; self.save()
        self.assertEqual(self.replay_judge(), 'session-juge')

    def test_adaptateur_export_historique_distinct_verifie(self):
        target = self.root / 'lie_jugements_corriges_bruts-export-02c.py'
        self.files[target] = b'adaptateur historique synthetique'
        exported = {'raw_adapter_sha256': verifier.digest(target),
            'raw_projection': 'raw_output_three_parts_v1'}
        verifier.check_raw_export_adapter(exported)
        exported['raw_adapter_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'historique'):
            verifier.check_raw_export_adapter(exported)


class ExecutionScopeTests(unittest.TestCase):
    def events(self, error, exit_code, text="You've hit your session limit · resets 3:30am (Europe/Paris)", status='failed'):
        return [{'type': 'result', 'is_error': error, 'result': text, 'subtype': 'success'},
            {'type': 'technical_assessment', 'process_exit': exit_code, 'status': status}]

    def test_quota_atteste(self):
        self.assertEqual(verifier.response_scope(self.events(True, 1)), 'quota_interrupted')

    def test_texte_quota_dans_reponse_ne_simule_pas_interruption(self):
        self.assertEqual(verifier.response_scope(self.events(False, 0, status='passed')), 'completed_response')

    def test_autre_erreur_non_assimilee_au_quota(self):
        with self.assertRaises(ValueError):
            verifier.response_scope(self.events(True, 1, 'ECONNREFUSED'))

    def test_code_sortie_booleen_refuse(self):
        with self.assertRaises(ValueError):
            verifier.response_scope(self.events(True, True))

    def test_resultat_duplique_refuse(self):
        events = self.events(True, 1); events.insert(0, events[0].copy())
        with self.assertRaises(ValueError):
            verifier.response_scope(events)


if __name__ == '__main__':
    unittest.main()
