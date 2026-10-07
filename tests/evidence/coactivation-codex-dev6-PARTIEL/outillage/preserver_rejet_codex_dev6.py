"""Préserver le rejet natif 02 sans trace métier ni acteur de remplacement."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import campagne_codex_dev6_r1 as campaign

CASE = 'plugin-garde-fou-apja'
AGENT = '/root/repondant_codex_dev6_r1_02'

def preserve() -> dict:
    campaign.configure()
    base = campaign.base
    directory = campaign.RUN / CASE
    destination = campaign.RUN / 'rejets-protocole' / CASE
    if destination.exists():
        raise base.binder.BindingError('Rejet déjà préservé ; aucun remplacement')
    manifest = base.binder._json((campaign.RUN / 'manifest.json').read_text(encoding='utf-8'))
    export = base.binder._json((directory / 'responder.export.json').read_text(encoding='utf-8'))
    for name, field in (('input.json', 'input_sha256'), ('input.index.json', 'input_index_sha256'), ('respondant.prompt.md', 'prompt_sha256')):
        assert base.binder._sha(directory / name) == export[field]
    assert base.binder._sha(campaign.RUN / 'manifest.json') == export['manifest_sha256']
    for name, digest in manifest['outillage_sha256'].items():
        assert base.binder._sha(campaign.ROOT / name) == digest
    native_path, parent_path = campaign.BASE_DISCOVER(AGENT)
    native = base.binder._events(native_path)
    parent = base.binder._events(parent_path)
    projected_parent, failed_creations = campaign.guarded.successful_parent(parent, AGENT)
    identity, spawn = base.identity(native, projected_parent, AGENT, export['created_at'])
    calls = [event for event in native if event.get('payload', {}).get('type') in ('custom_tool_call', 'function_call')]
    reads = [event for event in calls if 'tools.exec_command(' in str(event['payload'].get('input', event['payload'].get('arguments')))]
    assert reads, 'Aucune lecture native'
    first = reads[0]
    script = first['payload'].get('input', first['payload'].get('arguments'))
    try:
        base.raw.raw_arguments(script)
    except base.binder.BindingError as error:
        rejection = str(error)
    else:
        raise AssertionError('Le premier appel ne présente pas le rejet attendu')
    assert rejection == 'Lecture brute hors grammaire fermée'
    assert script.count('tools.exec_command(') == 6 and all('const r' + str(i) in script for i in range(1, 7))
    sources = base.modules()[2]
    cleaned_script = sources.scrub_visible_text(script)
    assert cleaned_script['text'] == script and not cleaned_script['redacted'] and not cleaned_script['truncated'], 'Argument exact non publiable'
    rejected_argument = {'call_id': first['payload']['call_id'], 'timestamp': first['timestamp'], 'native_tool_name': first['payload']['name'],
                         'native_argument': script, 'native_argument_sha256': hashlib.sha256(script.encode('utf-8')).hexdigest(),
                         'reason': rejection, 'script_executed_by_this_preserver': False}
    source_ids = {event['payload']['call_id'] for event in calls
                  if any(name in str(event['payload'].get('input', event['payload'].get('arguments'))) for name in ('tools.mcp__droit_francais__', 'tools.web__run('))}
    retained = base.safe_source_native(native, source_ids)
    normalizations = []
    def sanitize(value: object, pointer: str) -> object:
        if isinstance(value, str):
            clean = sources.scrub_visible_text(value)
            if clean['redacted'] or clean['truncated']:
                normalizations.append({'pointer': pointer, 'original_sha256': hashlib.sha256(value.encode('utf-8')).hexdigest(),
                                       'redacted': clean['redacted'], 'truncated': clean['truncated']})
            return clean['text']
        if isinstance(value, list):
            return [sanitize(item, pointer + '/' + str(index)) for index, item in enumerate(value)]
        if isinstance(value, dict):
            return {key: sanitize(item, pointer + '/' + key) for key, item in value.items()}
        return value
    sanitized = sanitize(retained, '')
    trace_path = destination / 'trace-native-filtre-assainie.jsonl'
    base.binder._write(trace_path, ''.join(json.dumps(event, ensure_ascii=False) + '\n' for event in sanitized))
    base.write(destination / 'argument-rejete.json', rejected_argument)
    base.write(destination / 'spawn-repondant.json', spawn)
    response = directory / 'response.md'
    proof = {**identity, 'created_at_receipt': datetime.now(timezone.utc).isoformat(), 'case_id': CASE,
             'status': 'rejected_protocol_not_scored', 'reason': rejection, 'rejected_call_id': first['payload']['call_id'],
             'export_before_spawn_verified': True, 'export_sha256': base.binder._sha(directory / 'responder.export.json'),
             'manifest_sha256': export['manifest_sha256'], 'native_session_file': native_path.name, 'parent_session_file': parent_path.name,
             'native_session_sha256_at_preservation': base.binder._sha(native_path),
             'native_filtered_sanitized_sha256': base.binder._sha(trace_path), 'sanitizations': normalizations,
             'exact_argument_file_sha256': base.binder._sha(destination / 'argument-rejete.json'),
             'response_exists': response.is_file(), 'response_sha256': base.binder._sha(response) if response.is_file() else None,
             'response_not_bound_or_scored': True, 'rejected_creation_attempts': failed_creations,
             'preserver_sha256': base.binder._sha(Path(__file__)), 'business_trace_created': False, 'replacement_actor_created': False,
             'source_bodies_excluded': True, 'release_ready': False, 'actual_plugin_activation_verified': False}
    base.write(destination / 'rejet-protocole.json', proof)
    return {key: proof[key] for key in ('case_id', 'status', 'reason', 'thread_id', 'export_before_spawn_verified', 'response_sha256', 'native_filtered_sanitized_sha256', 'business_trace_created', 'replacement_actor_created')}

if __name__ == '__main__':
    print(json.dumps(preserve(), ensure_ascii=False, indent=2))
