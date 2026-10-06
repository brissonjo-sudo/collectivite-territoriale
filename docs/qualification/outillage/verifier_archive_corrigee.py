"""Rejoue hors ligne les contrôles de gel et les preuves natives, sans Git."""
from __future__ import annotations

import hashlib
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import lie_jugements_corriges as binder

ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return binder._json(path.read_text(encoding='utf-8-sig'))


def patch_document(script: str, expected: str):
    patch = binder._arguments(script, 'apply_patch')
    if not isinstance(patch, str):
        raise ValueError('Patch non littéral')
    lines = patch.splitlines()
    if (len(lines) < 4 or lines[0] != '*** Begin Patch' or lines[-1] != '*** End Patch'
            or lines[1].replace('\\', '/').casefold() != ('*** Add File: ' + expected).casefold()
            or any(not line.startswith('+') for line in lines[2:-1])):
        raise ValueError('Patch hors destination déclarée')
    return '\n'.join(line[1:] for line in lines[2:-1]) + '\n'


def compare_declared(proof, checked, required=()):
    """Confronte les déclarations aux valeurs dérivées, sans coercition JSON."""
    for field in required:
        if field not in proof:
            raise ValueError('Champ de liaison absent : ' + field)
    for field, value in checked.items():
        if field in proof and binder._canonical(proof[field]) != binder._canonical(value):
            raise ValueError('Champ de liaison divergent : ' + field)


def unique_metadata(events):
    """Une trace conserve une unique identité, placée en tête."""
    if (not events or events[0].get('type') != 'session_meta'
            or sum(event.get('type') == 'session_meta' for event in events) != 1):
        raise ValueError('Métadonnées de session absentes ou dupliquées')


def check_session_filename(proof, field, session_id):
    """Confronte une provenance de fichier déclarée à son identité native."""
    if field in proof:
        value = proof[field]
        if (not isinstance(value, str) or '/' in value or '\\' in value
                or not value.endswith('-' + session_id + '.jsonl')):
            raise ValueError('Fichier de session déclaré divergent : ' + field)


def check_identity(events, parent, proof, exported_at):
    unique_metadata(events)
    unique_metadata(parent)
    meta = events[0]['payload']
    if parent[0].get('type') != 'session_meta' or parent[0]['payload']['id'] != proof['parent_thread_id']:
        raise ValueError('Trace parent différente')
    spawn = meta['source']['subagent']['thread_spawn']
    if meta['id'] != proof['session_id'] or spawn['agent_path'] != proof['agent'] or spawn['parent_thread_id'] != proof['parent_thread_id']:
        raise ValueError('Identité native divergente')
    calls = [event for event in parent if event.get('payload', {}).get('type') == 'function_call'
             and event['payload'].get('name') == 'spawn_agent'
             and binder._json(event['payload']['arguments']).get('task_name') == proof['agent'].rsplit('/', 1)[-1]]
    if len(calls) != 1:
        raise ValueError('Spawn absent ou ambigu')
    call = calls[0]
    arguments = binder._json(call['payload']['arguments'])
    if arguments.get('fork_turns') != 'none':
        raise ValueError('Historique hérité')
    returns = [event for event in parent if event.get('payload', {}).get('type') == 'function_call_output'
               and event['payload'].get('call_id') == call['payload']['call_id']]
    if len(returns) != 1 or binder._json(returns[0]['payload']['output']).get('task_name') != proof['agent']:
        raise ValueError('Retour du spawn divergent')
    if not binder._time(exported_at) <= binder._time(call['timestamp']) <= binder._time(meta['timestamp']) <= binder._time(returns[0]['timestamp']):
        raise ValueError('Contexte réutilisé ou chronologie divergente')
    starts = [event for event in events if event.get('payload', {}).get('type') == 'task_started']
    ends = [event for event in events if event.get('payload', {}).get('type') == 'task_complete']
    contexts = [event for event in events if event['type'] == 'turn_context']
    if len(starts) != 1 or len(ends) != 1 or not contexts:
        raise ValueError('Tâche achevée unique absente')
    turn = starts[0]['payload']['turn_id']
    if ends[0]['payload']['turn_id'] != turn or any(event['payload']['turn_id'] != turn for event in contexts):
        raise ValueError('Contexte de tâche divergent')
    models = sorted({event['payload']['model'] for event in contexts})
    if len(models) != 1 or not isinstance(models[0], str) or not models[0]:
        raise ValueError('Modèle natif absent ou ambigu')
    if models != proof['models']:
        raise ValueError('Modèle natif divergent')
    start, end = events.index(starts[0]), events.index(ends[0])
    if start >= end or meta['id'] == proof['parent_thread_id']:
        raise ValueError('Ordre ou identité de tâche divergent')
    checked = {'agent': spawn['agent_path'], 'session_id': meta['id'],
        'parent_thread_id': spawn['parent_thread_id'], 'turn_id': turn, 'models': models,
        'fork_turns': 'none', 'completed': True, 'spawn_call_id': call['payload']['call_id'],
        'spawn_timestamp': call['timestamp'],
        'spawn_evidence': {'task_name': spawn['agent_path'], 'fork_turns': 'none',
            'call_id': call['payload']['call_id'], 'returned_task_name': spawn['agent_path']}}
    compare_declared(proof, checked, ('turn_id', 'spawn_call_id', 'spawn_timestamp',
        'fork_turns', 'completed'))
    check_session_filename(proof, 'native_session_file', meta['id'])
    check_session_filename(proof, 'parent_session_file', spawn['parent_thread_id'])
    return start, end


def replay_judge(directory: Path, packet: Path, judgment: Path, parent: Path,
                 proof_path: Path, origin: str, exported_at: str):
    proof = load(proof_path)
    trace = proof_path.with_name('trace-juge.jsonl')
    if proof['trace_sha256'] != digest(trace) or proof['judgment_sha256'] != digest(judgment):
        raise ValueError('Liaison du juge altérée')
    original_packet = origin + '/' + packet.relative_to(ROOT).as_posix()
    original_judgment = origin + '/' + judgment.relative_to(ROOT).as_posix()
    old_read, old_patch, old_arguments = binder._read_command, binder.parse_patch, binder._arguments
    # Le déplacement est explicite. Aucun chemin des traces n'est ouvert.
    def original_read(_):
        spelling = original_packet if proof.get('exact_read_path_format') == 'absolute_posix' else original_packet.replace('/', '\\')
        return "Get-Content -LiteralPath '" + spelling.replace("'", "''") + "' -Raw"
    binder._read_command = original_read
    def read_arguments(script, tool):
        pragma = '// @exec: {"max_output_tokens": 55000}\n'
        if tool == 'exec_command' and script.startswith(pragma):
            script = script[len(pragma):]
        return old_arguments(script, tool)
    binder._arguments = read_arguments
    binder.parse_patch = lambda script, _: binder._json(patch_document(script, original_judgment))
    try:
        native_events, parent_events = binder._events(trace), binder._events(parent)
        unique_metadata(native_events)
        unique_metadata(parent_events)
        if 'raw_adapter_sha256' in proof or 'raw_projection' in proof:
            import lie_jugements_corriges_bruts as raw_binder
            if (proof.get('raw_projection') != raw_binder.PROJECTION
                    or proof.get('raw_adapter_sha256') != digest(ROOT / 'lie_jugements_corriges_bruts.py')
                    or proof.get('exact_read_path_format') != 'absolute_posix'):
                raise ValueError('Adaptateur brut absent ou divergent')
            checked, _ = raw_binder.native_proof(native_events, parent_events,
                proof['agent'], proof['parent_thread_id'], packet, judgment, exported_at)
        else:
            checked, _ = binder.native_proof(native_events, parent_events,
                proof['agent'], proof['parent_thread_id'], packet, judgment, exported_at)
    finally:
        binder._read_command, binder.parse_patch, binder._arguments = old_read, old_patch, old_arguments
    # Le nom de fichier est une provenance déclarée ; native_proof le laisse nul.
    checked.pop('native_session_file', None)
    checked.update(trace_sha256=digest(trace), packet_sha256=digest(packet),
        judgment_sha256=digest(judgment))
    packet_value = load(packet)
    checked['case_id'] = packet_value['case_id']
    response_sha = packet_value.get('response_sha256', packet_value.get('trace_sha256'))
    if response_sha is not None:
        checked['response_sha256'] = response_sha
    if 'native_proof_module_sha256' in proof:
        checked['native_proof_module_sha256'] = digest(Path(binder.__file__))
    if 'portable_adapter_sha256' in proof:
        checked['portable_adapter_sha256'] = digest(ROOT / 'lie_jugements_corriges_portables.py')
    if (directory / 'response.md').is_file():
        checked['response_sha256'] = digest(directory / 'response.md')
    compare_declared(proof, checked, ('session_id', 'models', 'turn_id', 'spawn_call_id',
        'spawn_timestamp', 'read_call_ids', 'write_call_ids', 'completed', 'fork_turns'))
    check_session_filename(proof, 'native_session_file', checked['session_id'])
    check_session_filename(proof, 'parent_session_file', checked['parent_thread_id'])
    return proof['session_id']


def check_raw_export_adapter(exported):
    """Conserve la provenance d'export distincte de l'adaptateur de liaison corrigé."""
    if 'raw_adapter_sha256' not in exported:
        return
    if (exported.get('raw_projection') != 'raw_output_three_parts_v1'
            or exported['raw_adapter_sha256'] != digest(ROOT / 'lie_jugements_corriges_bruts-export-02c.py')):
        raise ValueError('Adaptateur historique d’export brut divergent')


def question_input(directory: Path, manifest, parent, proof, exported):
    """Vérifie le prompt figé et distingue le texte natif opaque d'une preuve."""
    suite_path, prompt_path = directory.parent / 'suite.json', directory / 'prompt.md'
    if digest(suite_path) != manifest['suite_sha256']:
        raise ValueError('Suite du répondant divergente')
    cases = [case for case in load(suite_path) if case['id'] == directory.name]
    if len(cases) != 1:
        raise ValueError('Question du répondant absente ou ambiguë')
    question = cases[0]['prompt']
    if (prompt_path.read_text(encoding='utf-8') != question + '\n'
            or exported['question_sha256'] != digest(prompt_path)
            or binder._canonical(exported['runtime_sha256']) != binder._canonical(manifest['runtime_sha256'])):
        raise ValueError('Prompt ou inventaire du répondant divergent')
    calls = [event for event in parent if event.get('payload', {}).get('type') == 'function_call'
        and event['payload'].get('name') == 'spawn_agent'
        and event['payload'].get('call_id') == proof['spawn_call_id']]
    if len(calls) != 1:
        raise ValueError('Spawn de question absent ou ambigu')
    message = binder._json(calls[0]['payload']['arguments']).get('message')
    if message is None:
        verified, reason = False, 'Message initial non exporté ; son texte n’est pas attesté.'
    elif not isinstance(message, str) or not message:
        raise ValueError('Message du spawn invalide')
    elif message == question:
        verified, reason = True, 'Question identique, texte natif clair intégral.'
    elif re.fullmatch(r'gAAAA[A-Za-z0-9_=-]+', message):
        verified, reason = False, 'Message du spawn chiffré ; texte de la question non démontré.'
    elif question in message:
        verified, reason = False, 'Question présente dans une enveloppe opératoire non confrontée à un contrat figé.'
    else:
        raise ValueError('Question différente dans le message clair du spawn')
    compare_declared(proof, {'initial_message_verified': verified,
        'question_sha256': digest(prompt_path)})
    return {'case_id': directory.name, 'session_id': proof['session_id'],
        'frozen_prompt_verified': True, 'initial_message_verified': verified,
        'question_file_read_verified': False, 'reason': reason}


def replay_responder(directory: Path, manifest, parent, origin: str, question_reports=None):
    proof = load(directory / 'liaison/execution-repondant.json')
    trace = directory / 'liaison/trace-repondant.jsonl'
    response = directory / 'response.md'
    if proof['trace_sha256'] != digest(trace) or proof['response_sha256'] != digest(response):
        raise ValueError('Liaison du répondant altérée')
    events = binder._events(trace)
    exported = load(directory / 'responder.export.json')
    start, end = check_identity(events, parent, proof, exported['created_at'])
    question_report = question_input(directory, manifest, parent, proof, exported)
    reads, writes, read_ids, write_ids = [], 0, [], []
    question_reads = []
    call_ids = set()
    prefix = origin + '/' + directory.relative_to(ROOT).as_posix()
    for index, event in enumerate(events):
        payload = event.get('payload', {})
        if payload.get('type') not in ('custom_tool_call', 'function_call'):
            continue
        if payload.get('name') != 'exec' or not start < index < end:
            raise ValueError('Outil du répondant hors protocole')
        identifier = payload.get('call_id')
        if not isinstance(identifier, str) or not identifier or identifier in call_ids:
            raise ValueError('Identifiant d’appel absent ou dupliqué')
        call_ids.add(identifier)
        outputs = [(i, event['payload']) for i, event in enumerate(events)
                   if event.get('payload', {}).get('call_id') == payload['call_id']
                   and event['payload'].get('type') in ('custom_tool_call_output', 'function_call_output')]
        if len(outputs) != 1 or not index < outputs[0][0] < end:
            raise ValueError('Résultat du répondant absent ou ambigu')
        parts = binder._output(outputs[0][1])
        if len(parts) != 2 or not parts[0].startswith('Script completed\n'):
            raise ValueError('Opérations multiples ou échouées')
        script = payload.get('input', payload.get('arguments'))
        result = binder._json(parts[1])
        if 'tools.apply_patch(' in script:
            if patch_document(script, prefix + '/response.md') != response.read_text(encoding='utf-8') or result != {}:
                raise ValueError('Réponse différente du patch natif')
            writes += 1
            write_ids.append(identifier)
        else:
            args = binder._arguments(script, 'exec_command')
            match = re.fullmatch(r"Get-Content -LiteralPath '([^']+)' -Raw", args.get('cmd', ''))
            if not match or set(args) != {'cmd', 'max_output_tokens'}:
                raise ValueError('Lecture du répondant hors grammaire')
            absolute = match[1].replace('\\', '/')
            if absolute.casefold() == (prefix + '/prompt.md').casefold():
                if (reads != ['SKILL.md'] or question_reads or writes
                        or type(result.get('exit_code')) is not int or result['exit_code'] != 0
                        or result.get('output', '').rstrip('\r\n') != (directory / 'prompt.md').read_text(encoding='utf-8').rstrip('\r\n')):
                    raise ValueError('Lecture de question absente, tardive, dupliquée ou tronquée')
                question_reads.append(identifier)
                read_ids.append(identifier)
                continue
            runtime_prefix = prefix + '/runtime/'
            if not absolute.casefold().startswith(runtime_prefix.casefold()):
                raise ValueError('Lecture hors runtime isolé')
            relative = absolute[len(runtime_prefix):]
            if relative not in manifest['runtime_sha256']:
                raise ValueError('Fichier runtime inconnu')
            path = directory / 'runtime' / relative
            if digest(path) != manifest['runtime_sha256'][relative] or type(result.get('exit_code')) is not int or result['exit_code'] != 0 or result.get('output', '').rstrip('\r\n') != path.read_text(encoding='utf-8').rstrip('\r\n'):
                raise ValueError('Lecture runtime divergente ou tronquée')
            reads.append(relative)
            read_ids.append(identifier)
    if not reads or reads[0] != 'SKILL.md' or reads != proof['read_runtime_files'] or writes != 1:
        raise ValueError('Chargement du skill ou écriture unique absente')
    if question_reads:
        question_report['question_file_read_verified'] = True
        question_report['reason'] += ' Lecture native du prompt complet après SKILL.md attestée.'
        compare_declared(proof, {'question_file_read_verified': True,
            'question_sha256': digest(directory / 'prompt.md'), 'question_read_call_id': question_reads[0],
            'runtime_and_single_question_reads_only': True},
            ('question_file_read_verified', 'question_sha256', 'question_read_call_id', 'runtime_and_single_question_reads_only'))
    elif proof.get('question_file_read_verified') is not None:
        compare_declared(proof, {'question_file_read_verified': False})
    compare_declared(proof, {'read_call_ids': read_ids, 'write_call_ids': write_ids,
        'read_runtime_files': reads, 'runtime_only_reads': not bool(question_reads), 'skill_read_first': True,
        'response_patch_comparison': 'exact_text', 'trace_sha256': digest(trace),
        'response_sha256': digest(response), 'source_commit': manifest.get('source_commit'),
        'release_ready': False})
    if question_reports is not None:
        question_reports.append(question_report)
    return proof['session_id']


def response_scope(events):
    """Distingue une réponse achevée d'un refus de quota attesté par le harnais."""
    results = [e for e in events if e.get('type') == 'result']
    assessments = [e for e in events if e.get('type') == 'technical_assessment']
    if len(results) != 1 or len(assessments) != 1:
        raise ValueError('Résultat ou bilan de campagne absent ou ambigu')
    result, assessment = results[0], assessments[0]
    exit_code = assessment.get('process_exit')
    if type(exit_code) is not int:
        raise ValueError('Code de sortie de campagne invalide')
    if (result.get('is_error') is True and exit_code != 0
            and assessment.get('status') == 'failed'
            and re.fullmatch(r"You've hit your session limit · resets [^\r\n]+", result.get('result', '').strip())):
        return 'quota_interrupted'
    if result.get('is_error') is False and exit_code == 0 and result.get('subtype') == 'success':
        return 'completed_response'
    raise ValueError('Exécution incomplète dont la cause n’est pas attestée')


def main():
    archive = load(ROOT / 'archive-manifest.json')
    expected = archive['files']
    actual = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob('*')
              if path.is_file() and '__pycache__' not in path.parts and path.name != 'archive-manifest.json'}
    if actual != set(expected):
        raise ValueError('Inventaire de l’archive divergent')
    for relative, sha in expected.items():
        if PurePosixPath(relative).is_absolute() or '..' in PurePosixPath(relative).parts or digest(ROOT / relative) != sha:
            raise ValueError('Octets archivés divergents : ' + relative)
    origin = archive['origin_workspace'].rstrip('/')
    if (not re.fullmatch(r'qualification-dsi-0\.2\.1-native-r\d+', archive['native_run'])
            or not re.fullmatch(r'campagne-r\d+', archive['coactivation_run'])
            or not re.fullmatch(r'gel-r\d+\.json', archive['frozen_manifest'])):
        raise ValueError('Chemin de mesure hors contrat')
    native = ROOT / archive['native_run']
    manifest = load(native / 'manifest.json')
    summary = load(native / 'summary.json')
    source = ROOT / 'DSI-corrections-pr5'
    if (manifest['source_commit'] != archive['dsi_source_commit']
            or summary['source_commit'] != archive['dsi_source_commit']
            or digest(source / 'tests/cas-de-test.json') != manifest['suite_sha256']
            or digest(native / 'suite.json') != manifest['suite_sha256']
            or digest(source / 'tests/bareme-cas-de-test.md') != manifest['rubric_sha256']
            or digest(native / 'bareme.md') != manifest['rubric_sha256']):
        raise ValueError('Source, suite ou barème autonome divergent')
    for relative, sha in manifest['runtime_sha256'].items():
        if digest(source / relative) != sha:
            raise ValueError('Source runtime autonome divergente')
    parent = binder._events(native / 'trace-parent-filtre.jsonl')
    identities = set()
    question_reports = []
    for case in load(native / 'suite.json'):
        directory = native / case['id']
        for relative, sha in manifest['runtime_sha256'].items():
            if digest(directory / 'runtime' / relative) != sha:
                raise ValueError('Runtime autonome divergent')
        packet = load(directory / 'judge.packet.json')
        judgment = load(directory / 'judgment.json')
        expected_packet = {'case_id': case['id'], 'prompt': case['prompt'],
            'response': (directory / 'response.md').read_text(encoding='utf-8'),
            'attendus': case['attendus'], 'rubric': (native / 'bareme.md').read_text(encoding='utf-8'),
            'response_sha256': digest(directory / 'response.md')}
        if binder._canonical(packet) != binder._canonical(expected_packet):
            raise ValueError('Paquet autonome différent du barème figé')
        if packet['response_sha256'] != digest(directory / 'response.md') or judgment['response_sha256'] != packet['response_sha256']:
            raise ValueError('Jugement autonome d’une autre réponse')
        identities.add(replay_responder(directory, manifest, parent, origin, question_reports))
        identities.add(replay_judge(directory, directory / 'judge.packet.json', directory / 'judgment.json',
            native / 'trace-parent-filtre.jsonl', directory / 'liaison/execution-juge.json', origin,
            load(directory / 'judge.export.json')['exported_at']))
    sys.path.insert(0, str(ROOT / 'DSI-corrections-pr5/scripts'))
    suite = importlib.import_module('eval_suite')
    if suite.validate_run(native) != summary['totals'] or len(identities) != 56:
        raise ValueError('Synthèse autonome ou indépendance divergente')
    plugin = ROOT / 'Collectivite-corrections-pr5'
    evidence = plugin / 'tests/evidence/coactivation-corrigee'
    traces = evidence / archive['coactivation_run']
    frozen_path = evidence / archive['frozen_manifest']
    if load(frozen_path)['candidate_commit'] != archive['candidate_commit']:
        raise ValueError('Candidat de coactivation divergent')
    result = subprocess.run([sys.executable, str(plugin / 'scripts/verify_corrected_campaign.py'),
        '--manifest', str(frozen_path), '--traces', str(traces)], cwd=plugin, capture_output=True,
        text=True, encoding='utf-8', check=True)
    verified = json.loads(result.stdout)
    if not verified['full_campaign'] or len(verified['cases']) != 16:
        raise ValueError('Coactivation complète non démontrée')
    coactivation_ids = set()
    interrupted = []
    for record in verified['cases']:
        case = record['case_id']
        directory = traces / 'juges' / case
        packet = directory / (case + '.packet.json')
        judgment = directory / (case + '.jugement.json')
        if response_scope(binder._events(traces / (case + '.jsonl'))) == 'quota_interrupted':
            if judgment.exists() or (traces / (case + '.jugement.json')).exists() or (directory / 'liaison/execution-juge.json').exists():
                raise ValueError('Jugement comportemental déclaré sur un refus de quota')
            interrupted.append(case)
            continue
        if judgment.read_bytes() != (traces / (case + '.jugement.json')).read_bytes():
            raise ValueError('Copie de jugement divergente')
        exported = load(directory / (case + '.export.json'))
        check_raw_export_adapter(exported)
        coactivation_ids.add(replay_judge(directory, packet, judgment, traces / 'juges/trace-parent-filtre.jsonl',
            directory / 'liaison/execution-juge.json', origin, exported['exported_at']))
    if len(coactivation_ids) + len(interrupted) != 16 or identities & coactivation_ids:
        raise ValueError('Juge de coactivation réutilisé')
    if not all(record['question_file_read_verified'] for record in question_reports):
        raise ValueError('Lecture native de chacune des 28 questions non démontrée')
    print(json.dumps({'archive_integrity': 'passed', 'native_cases': 28, 'native_fresh_sessions': 56,
        'coactivation_attempts': 16, 'coactivation_completed_responses': len(coactivation_ids),
        'coactivation_fresh_judges': len(coactivation_ids), 'quota_interrupted_cases': interrupted,
        'behavioral_campaign_complete': not bool(interrupted),
        'judge_identity_checked': True, 'judge_identity_scope': 'Réponses achevées seulement ; aucun jugement déduit des refus de quota.',
        'initial_message_verified': all(record['initial_message_verified'] for record in question_reports),
        'question_file_read_verified': all(record['question_file_read_verified'] for record in question_reports),
        'question_input_verification': question_reports,
        'independence_scope': 'Identités, spawns sans historique, tâche unique et outils capturés contrôlés ; texte de la question native seulement si démontré séparément.',
        'source_scope': 'traces assainies; aucune validation humaine déduite', 'release_ready': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
