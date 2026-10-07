"""Audit indépendant en lecture seule : logs natifs, octets, projections et juges.

Ne relance ni répondant, source ou juge. N'exécute aucun script trouvé dans les
traces. Les pièces existantes ne sont jamais réécrites. Un rapport facultatif
est créé exclusivement à un nouveau chemin. Pas de qualification juridique.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign
import preuves_codex_dev5_web as web
import controler_codex_dev5_r2_site_literal as site
import controler_codex_dev5 as guarded
import jugements_codex_dev5_r2 as judges

def require(condition, message):
    if not condition:
        raise base.binder.BindingError(message)

def normalized(value):
    return base.binder._canonical(value)

def identity(native, parent, agent, exported_at):
    require(native[0]['type'] == 'session_meta', 'Métadonnée initiale absente')
    meta = native[0]['payload']
    source = meta.get('source', {}).get('subagent', {}).get('thread_spawn', {})
    require(source.get('agent_path') == agent and source.get('parent_thread_id') == base.PARENT_ID, 'Identité native ou parent divergent')
    require(meta.get('id') != base.PARENT_ID and sum(e['type'] == 'session_meta' for e in native) == 1, 'Métadonnée dupliquée')
    started = [e for e in native if e.get('payload', {}).get('type') == 'task_started']
    ended = [e for e in native if e.get('payload', {}).get('type') == 'task_complete']
    contexts = [e for e in native if e['type'] == 'turn_context']
    require(len(started) == len(ended) == 1 and contexts, 'Tour frais achevé unique absent')
    turn = started[0]['payload'].get('turn_id')
    require(turn and ended[0]['payload'].get('turn_id') == turn and all(e['payload'].get('turn_id') == turn for e in contexts), 'Tour réutilisé')
    models = {e['payload'].get('model') for e in contexts}
    require(len(models) == 1 and isinstance(next(iter(models)), str), 'Modèle natif ambigu')
    start, end = native.index(started[0]), native.index(ended[0])
    require(start < end, 'Fin antérieure au début')
    require(all(start < index < end for index, e in enumerate(native) if e.get('payload', {}).get('type') in ('custom_tool_call', 'function_call')), 'Appel hors tour natif')
    candidates = []
    refused = []
    for event in parent:
        payload = event.get('payload', {})
        if payload.get('type') != 'function_call' or payload.get('name') != 'spawn_agent':
            continue
        arguments = base.binder._json(payload['arguments'])
        if arguments.get('task_name') != agent.rsplit('/', 1)[-1]:
            continue
        outputs = [e for e in parent if e.get('payload', {}).get('type') == 'function_call_output' and e['payload'].get('call_id') == payload['call_id']]
        require(len(outputs) == 1, 'Retour création ambigu')
        output = outputs[0]
        if output['payload'].get('output') == guarded.FAILED_SPAWN:
            refused.append(payload['call_id'])
            continue
        require(base.binder._json(output['payload']['output']).get('task_name') == agent, 'Retour création non lié')
        require(arguments.get('fork_turns') == 'none' and 'model' not in arguments and 'reasoning_effort' not in arguments, 'Historique ou override transmis')
        candidates.append((event, output))
    require(len(candidates) == 1, 'Création réussie unique non établie')
    event, output = candidates[0]
    require(base.binder._time(exported_at) <= base.binder._time(event['timestamp']) <= base.binder._time(meta['timestamp']) <= base.binder._time(output['timestamp']), 'Export ou création hors chronologie')
    return {'thread_id': meta['id'], 'model': next(iter(models)), 'turn_id': turn, 'refused_spawn_call_ids': refused}

def output_for(native, call):
    matches = [e for e in native if e.get('payload', {}).get('call_id') == call['payload']['call_id'] and e['payload'].get('type') in ('custom_tool_call_output', 'function_call_output')]
    require(len(matches) == 1 and native.index(call) < native.index(matches[0]), 'Retour outil absent ou antérieur')
    return matches[0], base.binder._output(matches[0]['payload'])

def read(native, call):
    result, parts = output_for(native, call)
    args = base.raw.raw_arguments(call['payload'].get('input', call['payload'].get('arguments')))
    match = re.fullmatch(r"Get-Content -LiteralPath '([^']+)' -Raw", args['cmd'])
    require(match and args['max_output_tokens'] == 55000 and len(parts) == 3 and parts[0].startswith('Script completed\n'), 'Lecture brute hors protocole')
    code = base.binder._json(parts[1])
    require(isinstance(code, dict) and set(code) == {'exit_code'} and type(code['exit_code']) is int and code['exit_code'] == 0, 'Lecture non réussie')
    path = Path(match[1]).resolve()
    text = path.read_bytes().decode('utf-8')
    require(len(text) <= 8000, 'Lecture dépassant 8000 caractères')
    require(parts[2] in (text, text + '\n', text + '\r\n'), 'Sortie visible tronquée ou modifiée')
    return path, text, result

def exact_patch(native, call, target):
    _, parts = output_for(native, call)
    require(len(parts) == 2 and parts[0].startswith('Script completed\n') and base.binder._json(parts[1]) == {}, 'Patch natif non réussi')
    patch = base.binder._arguments(call['payload'].get('input', call['payload'].get('arguments')), 'apply_patch')
    lines = patch.splitlines()
    require(lines[0] == '*** Begin Patch' and lines[-1] == '*** End Patch', 'Patch enveloppe invalide')
    require(lines[1].replace('\\', '/').casefold() == ('*** Add File: ' + target.resolve().as_posix()).casefold(), 'Destination patch différente')
    require(all(line.startswith('+') for line in lines[2:-1]), 'Patch ambigu')
    text = '\n'.join(line[1:] for line in lines[2:-1]) + '\n'
    require(text.encode('utf-8') == target.read_bytes(), 'Fichier différent du patch écrit')
    return text

def visible(native, sources):
    messages = []
    for event in native:
        payload = event.get('payload', {})
        if payload.get('type') != 'message' or payload.get('role') != 'assistant':
            continue
        text = ''.join(part.get('text', '') for part in payload.get('content', []) if part.get('type') in ('output_text', 'text'))
        if text.strip():
            clean = sources.scrub_visible_text(text)
            messages.append({'type': 'assistant_text', 'text': clean['text'], 'text_redacted': clean['redacted'],
                             'text_truncated': clean['truncated'], 'phase': payload.get('phase'), 'timestamp': event['timestamp']})
    return messages

def without_id(event):
    return {key: value for key, value in event.items() if key != 'event_id'}

def audit_respondent(number, case, manifest, parent):
    identifier = case['id']
    directory = campaign.RUN / identifier
    proof = base.binder._json((directory / 'liaison/execution-repondant.json').read_text(encoding='utf-8'))
    export = base.binder._json((directory / 'responder.export.json').read_text(encoding='utf-8'))
    for path, field in ((directory / 'input.json', 'input_sha256'), (directory / 'input.index.json', 'input_index_sha256'),
                        (campaign.RUN / 'manifest.json', 'manifest_sha256'), (directory / 'respondant.prompt.md', 'prompt_sha256'),
                        (Path(campaign.__file__), 'adapter_sha256')):
        require(base.binder._sha(path) == export[field], 'Export répondant altéré : ' + path.name)
    require(base.binder._sha(directory / 'response.md') == proof['response_sha256'], 'Réponse altérée')
    trace_path = campaign.RUN / (identifier + '.jsonl')
    require(base.binder._sha(trace_path) == proof['trace_sha256'], 'Projection altérée')
    native_path, _ = campaign.BASE_DISCOVER(f'/root/repondant_codex_dev5_r2_{number:02d}')
    native = base.binder._events(native_path)
    identified = identity(native, parent, f'/root/repondant_codex_dev5_r2_{number:02d}', export['created_at'])
    require(identified['thread_id'] == proof['thread_id'] and identified['model'] == proof['model'], 'Receipt identité divergent')
    events = base.binder._events(trace_path)
    assessment, transport, sources = base.modules()
    require(events[0]['model'] == identified['model'] and events[0]['session_id'] == identified['thread_id'] and events[0]['host'] == 'Codex', 'Init modèle non natif')
    require(events[0]['actual_plugin_activation_verified'] is False, 'Fausse activation plugin')
    entry_parts = base.binder._json((directory / 'input.index.json').read_text(encoding='utf-8'))['fragments']
    require(len(entry_parts) == 6, 'Entrée différente de six fragments')
    runtime = {Path(key).resolve(): value for key, value in manifest['runtime_descriptors'].items()}
    indexes = {Path(value['index_path']).resolve(): original for original, value in runtime.items()}
    entry_reads, groups, pending = [], [], None
    runtime_events, source_calls, writes = [], [], []
    for event in native:
        payload = event.get('payload', {})
        if payload.get('type') not in ('custom_tool_call', 'function_call'):
            continue
        require(payload.get('name') == 'exec', 'Outil natif étranger')
        script = payload.get('input', payload.get('arguments'))
        if 'tools.exec_command(' in script:
            path, text, result = read(native, event)
            if len(entry_reads) < 6:
                expected = entry_parts[len(entry_reads)]
                require(path.as_posix() == expected['path'] and base.binder._sha(path) == expected['sha256'], 'Entrée lecture hors ordre')
                entry_reads.append(payload['call_id'])
                continue
            if pending is None:
                require(path in indexes, 'Lecture hors descripteur autorisé')
                original = indexes[path]
                record = runtime[original]
                require(base.binder._sha(path) == record['index_sha256'], 'Descripteur altéré')
                pending = {'original': original, 'record': record, 'index_call_id': payload['call_id'], 'call_ids': []}
                continue
            record = pending['record']
            expected = record['fragments'][len(pending['call_ids'])]
            require(path.as_posix() == expected['path'] and base.binder._sha(path) == expected['sha256'], 'Runtime lecture hors ordre')
            pending['call_ids'].append(payload['call_id'])
            if len(pending['call_ids']) == len(record['fragments']):
                body = ''.join(Path(part['path']).read_bytes().decode('utf-8') for part in record['fragments'])
                require(hashlib.sha256(body.encode('utf-8')).hexdigest() == record['source_sha256'], 'Runtime non intégral')
                original = pending['original']
                relative = original.relative_to(base.CANDIDATE / 'skills').as_posix()
                value = {'type': 'skill_activation' if original.name == 'SKILL.md' else 'plugin_file_read', 'path': relative,
                         'succeeded': True, 'call_ids': list(pending['call_ids']), 'index_call_id': pending['index_call_id'],
                         'activation_kind': 'file_read_fragments', 'actual_plugin_activation_verified': False,
                         'full_runtime_context_verified': True, 'runtime_sha256': record['source_sha256'], 'timestamp': result['timestamp']}
                if original.name == 'SKILL.md':
                    value['skill'] = 'collectivite-territoriale:' + relative.split('/')[0]
                runtime_events.append(value)
                groups.append({'original_path': original.as_posix(), 'index_call_id': pending['index_call_id'], 'call_ids': list(pending['call_ids'])})
                pending = None
            continue
        require(len(entry_reads) == 6 and pending is None, 'Outil pendant lecture incomplète')
        if 'tools.apply_patch(' in script:
            writes.append((event, exact_patch(native, event, directory / 'response.md')))
        elif 'ALL_TOOLS' in script and 'tools.' not in script:
            pass
        else:
            require(not writes, 'Appel source après réponse')
            tool, arguments = base.source_call(script)
            source_calls.append((event, tool, arguments))
    require(len(entry_reads) == 6 and pending is None and len(writes) == 1, 'Répondant incomplet')
    entry = ''.join(Path(part['path']).read_bytes().decode('utf-8') for part in entry_parts)
    require(entry.encode('utf-8') == (directory / 'input.json').read_bytes(), 'Entrée non reconstruite')
    require(base.binder._json(entry)['question'] == case['prompt'], 'Question différente du barème')
    projected_question = next(e for e in events if e['type'] == 'question_read')
    require(projected_question['call_ids'] == entry_reads and projected_question['full_context_verified'] is True, 'Projection entrée sans appels réels')
    stored_runtime = [without_id(e) for e in events if e['type'] in ('skill_activation', 'plugin_file_read')]
    require(normalized(stored_runtime) == normalized(runtime_events), 'Projection runtime différente des lectures natives')
    require([without_id(e) for e in events if e['type'] == 'assistant_text'] == visible(native, sources), 'Textes visibles modifiés')
    require(writes[0][1].rstrip('\r\n') == visible(native, sources)[-1]['text'].rstrip('\r\n'), 'Réponse finale différente du patch')
    if case['web_mode'] == 'official_source':
        web.CAPTURES.clear(); web.READ_PROJECTION.clear()
        site.ORIGINALS.clear(); site.FILTERS.clear(); site.PARSED.clear()
        if proof.get('site_filter_wrapper_sha256'):
            require(proof['site_filter_wrapper_sha256'] == base.binder._sha(Path(site.__file__)), 'Enveloppe site altérée')
            site.prepare(identifier)
        else:
            web.prepare(identifier)
    warnings = []
    source_ids = set()
    for event, tool, arguments in source_calls:
        call_id = event['payload']['call_id']
        source_ids.add(call_id)
        output, parts = output_for(native, event)
        stored = [e for e in events if e.get('call_id') == call_id and e['type'] == 'source_evidence']
        require(len(stored) == 1, 'Source non liée exactement une fois')
        if tool.startswith('mcp__droit_francais__'):
            require(len(parts) == 2 and parts[0].startswith('Script completed\n'), 'Transport source MCP non complet')
            body = base.binder._json(parts[1])
            expected = sources.extract_source_evidence(body, tool=tool.replace('mcp__droit_francais__', 'mcp__droit-francais__', 1), call_id=call_id, retrieved_at=output['timestamp'])
            require(normalized(expected) == normalized(without_id(stored[0])), 'Source MCP différente du retour natif')
        elif tool == 'web__run':
            require(case['web_mode'] == 'official_source', 'Web appelé hors mode officiel')
            capture = web.CAPTURES[call_id]
            require(normalized(capture['actual_arguments']) == normalized(arguments), 'Arguments web natifs altérés')
            expected = site.evidence(capture, sources) if proof.get('site_filter_wrapper_sha256') else web.evidence(capture, sources)
            require(normalized(expected) == normalized(without_id(stored[0])), 'Source web différente du retour natif')
            if re.search(r'(?m)^Warning: truncated output|tokens truncated', parts[-1]):
                warnings.append({'call_id': call_id, 'kind': 'native_web_output_truncation_marker', 'full_web_context_verified': False})
        else:
            raise base.binder.BindingError('Outil source hors scope')
    expected_native = base.safe_source_native(native, source_ids)
    kept_path = directory / 'liaison/trace-repondant.jsonl'
    require(normalized(expected_native) == normalized(base.binder._events(kept_path)), 'Journal natif filtré différent')
    require(base.binder._sha(kept_path) == proof['native_filtered_sha256'], 'Journal filtré altéré')
    final = events[-1]
    require(final['type'] == 'technical_assessment' and final['failures'] == base.codex_failures(events[:-1], case), 'Bilan technique non reproductible')
    require(final['observables'] == transport.observable_checks(events, case), 'STOP/primaires non reproductibles')
    require(proof['full_runtime_context_verified'] is True and proof['full_question_context_verified'] is True, 'Contexte intégral non attesté')
    return {'case_id': identifier, 'thread_id': identified['thread_id'], 'model': identified['model'], 'entry_fragments': 6,
            'runtime_groups': len(groups), 'source_calls': len(source_calls), 'technical_status': final['status'], 'warnings': warnings}

def audit_judge(number, case, parent):
    identifier = case['id']
    candidates = list((campaign.RUN / 'juges-fragments').glob(identifier + '-*/liaison/execution-juge.json'))
    if not candidates:
        return None
    require(len(candidates) == 1, 'Deux jugements retenus pour un cas')
    proof_path = candidates[0]
    directory = proof_path.parent.parent
    proof = base.binder._json(proof_path.read_text(encoding='utf-8'))
    export = base.binder._json((directory / (identifier + '.export.json')).read_text(encoding='utf-8'))
    agent = export['agent']
    require(re.fullmatch(f'/root/juge_codex_dev5_r2_{number:02d}[bc]', agent), 'Mauvais nom de juge')
    native_path, _ = campaign.BASE_DISCOVER(agent)
    native = base.binder._events(native_path)
    identified = identity(native, parent, agent, export['exported_at'])
    require(identified['thread_id'] == proof['thread_id'] and identified['model'] == proof['model'], 'Receipt juge identité divergent')
    for path, field in ((directory / (identifier + '.packet.json'), 'packet_sha256'), (directory / (identifier + '.prompt.md'), 'prompt_sha256'),
                        (campaign.RUN / (identifier + '.jsonl'), 'response_sha256'), (Path(judges.__file__), 'judge_adapter_sha256')):
        require(base.binder._sha(path) == export[field], 'Export juge altéré : ' + path.name)
    actual_calls = [e for e in native if e.get('payload', {}).get('type') in ('custom_tool_call', 'function_call')]
    require(len(actual_calls) == len(export['fragments']) + 1, 'Nombre lectures/patch du juge incorrect')
    texts = []
    for index, part in enumerate(export['fragments']):
        call = actual_calls[index]
        path, text, _ = read(native, call)
        require(path.as_posix() == part['path'] and base.binder._sha(path) == part['sha256'], 'Fragment juge hors ordre ou modifié')
        texts.append(text)
    packet = ''.join(texts)
    require(packet.encode('utf-8') == (directory / (identifier + '.packet.json')).read_bytes(), 'Paquet juge non intégral')
    assessment, _, _ = base.modules()
    rebuilt = assessment.build_judge_packet(case, campaign.RUN / (identifier + '.jsonl'), base.CANDIDATE / 'docs/protocole-coactivation-v2.md')
    require(normalized(rebuilt) == normalized(base.binder._json(packet)), 'Paquet autre que question/barème/trace')
    judgment_path = directory / (identifier + '.jugement.json')
    exact_patch(native, actual_calls[-1], judgment_path)
    require(judgment_path.read_bytes() == (campaign.RUN / (identifier + '.jugement.json')).read_bytes(), 'Copie jugement différente')
    document = base.binder._json(judgment_path.read_text(encoding='utf-8'))
    validated = guarded.validate(case, base.binder._events(campaign.RUN / (identifier + '.jsonl')), document, base.binder._sha(campaign.RUN / (identifier + '.jsonl')))
    require(validated == proof['assessment'], 'Verdict non reproductible')
    require(base.binder._sha(judgment_path) == proof['judgment_sha256'], 'Jugement modifié après liaison')
    kept = directory / 'liaison/trace-juge.jsonl'
    require(normalized(base.filter_native(native)) == normalized(base.binder._events(kept)) and base.binder._sha(kept) == proof['trace_sha256'], 'Trace juge filtrée différente')
    require(proof['full_packet_context_verified'] is True, 'Lecture complète juge non attestée')
    return {'case_id': identifier, 'thread_id': identified['thread_id'], 'model': identified['model'], 'fragments': len(texts), 'assessment': validated}

def audit(require_complete=False):
    campaign.configure()
    manifest = base.binder._json((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
    require(len(manifest['files']) == 211 and len(manifest['runtime_descriptors']) == 166, 'Gel différent de 211/166 fichiers')
    for relative, digest in manifest['files'].items():
        require(base.binder._sha(base.CANDIDATE / relative) == digest, 'Fichier gelé modifié : ' + relative)
    for original, record in manifest['runtime_descriptors'].items():
        require(base.binder._sha(Path(record['index_path'])) == record['index_sha256'], 'Index runtime altéré')
        joined = ''.join(Path(part['path']).read_bytes().decode('utf-8') for part in record['fragments'])
        require(joined.encode('utf-8') == Path(original).read_bytes() and hashlib.sha256(joined.encode('utf-8')).hexdigest() == record['source_sha256'], 'Fragments runtime altérés')
        require(all(len(Path(part['path']).read_bytes().decode('utf-8')) <= 8000 for part in record['fragments']), 'Fragment runtime supérieur à 8000')
    cases = base.binder._json((campaign.RUN / 'suite.json').read_text(encoding='utf-8'))
    require(len(cases) == 16 and sum(len(case['invariant_objects']) for case in cases) == 124, 'Suite/barème différent de 16/124')
    require(base.binder._sha(campaign.RUN / 'suite.json') == manifest['suite_sha256'], 'Suite r2 altérée')
    _, parent_path = campaign.BASE_DISCOVER('/root/outillage_codex_dev5')
    parent = base.binder._events(parent_path)
    identities = set()
    responders, judges_result, errors = [], [], []
    for number, case in enumerate(cases, 1):
        if not (campaign.RUN / case['id'] / 'liaison/execution-repondant.json').is_file():
            continue
        try:
            respondent = audit_respondent(number, case, manifest, parent)
            require(respondent['thread_id'] not in identities, 'Identité répondant réutilisée entre cas')
            identities.add(respondent['thread_id'])
            responders.append(respondent)
            judge = audit_judge(number, case, parent)
            if judge:
                require(judge['thread_id'] not in identities, 'Identité juge réutilisée')
                identities.add(judge['thread_id'])
                judges_result.append(judge)
        except (ValueError, KeyError, OSError) as error:
            errors.append({'case_id': case['id'], 'error': str(error)})
    if require_complete and (len(responders) != 16 or len(judges_result) != 16 or len(identities) != 32):
        errors.append({'case_id': None, 'error': 'Audit complet exige 16 répondants, 16 juges et 32 identités retenues.'})
    return {'created_at': datetime.now(timezone.utc).isoformat(), 'run': manifest['run'],
            'audit_script_sha256': base.binder._sha(Path(__file__)), 'status': 'failed' if errors else 'passed',
            'require_complete': require_complete, 'frozen_files_verified': 211, 'runtime_files_verified': 166,
            'respondents_verified': len(responders), 'judges_verified': len(judges_result), 'unique_retained_roles': len(identities),
            'initial_messages_verified': False, 'actual_plugin_activation_verified': False, 'release_ready': False,
            'source_scope': 'Sanitized source projection replayed from real native returns; no new request; no legal certification.',
            'respondents': responders, 'judges': judges_result, 'errors': errors}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.require_complete)
    if args.output:
        base.binder._write(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'passed' else 1)
