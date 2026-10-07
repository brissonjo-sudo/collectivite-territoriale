"""Conserve une tentative de patch refusée et impose un échec technique."""
from pathlib import Path
import argparse
import hashlib
import json
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign
import controler_codex_dev5_r2_pragma as pragma

ORIGINAL_EVENTS = base.binder._events
ORIGINAL_SAFE = base.safe_source_native
RAW = []
NATIVE_PATH = None
REJECTED = []
EXPECTED_TARGET = 'C:/Users/Krn/Documents/Codex/Codex/response.md'

def rejected_patch(script, parts):
    patch = base.binder._arguments(script, 'apply_patch')
    if not isinstance(patch, str) or patch != ('*** Begin Patch\n*** Add File: ' + EXPECTED_TARGET + '\n+placeholder\n*** End Patch'):
        raise base.binder.BindingError('Tentative refusée hors exception exactement attestée')
    if (len(parts) != 2 or not parts[0].startswith('Script failed\n')
            or not parts[1].startswith('Script error:\nExit code: 1\n')
            or parts[1].splitlines()[-1] != 'Failed to create parent directories for ' + EXPECTED_TARGET.replace('/', '\\')):
        raise base.binder.BindingError('Refus natif de patch non attesté')

def prepare():
    global RAW, NATIVE_PATH
    campaign.configure()
    NATIVE_PATH = campaign.BASE_DISCOVER('/root/repondant_codex_dev5_r2_14')[0].resolve()
    RAW = ORIGINAL_EVENTS(NATIVE_PATH)
    REJECTED.clear()
    for event in RAW:
        payload = event.get('payload', {})
        script = payload.get('input', payload.get('arguments', ''))
        if payload.get('name') != 'exec' or EXPECTED_TARGET not in script:
            continue
        output, parts = base.outputs(RAW, event)
        rejected_patch(script, parts)
        REJECTED.append({'call_id': payload['call_id'], 'timestamp': event['timestamp'],
                         'result_timestamp': output['timestamp'], 'target': EXPECTED_TARGET,
                         'native_script_sha256': hashlib.sha256(script.encode('utf-8')).hexdigest(),
                         'native_output_sha256': hashlib.sha256(base.binder._canonical(output).encode('utf-8')).hexdigest(),
                         'native_patch_succeeded': False})
    if len(REJECTED) != 1:
        raise base.binder.BindingError('Une seule tentative refusée connue attendue')

def events(path):
    actual = ORIGINAL_EVENTS(path)
    if Path(path).resolve() != NATIVE_PATH:
        return actual
    ids = {item['call_id'] for item in REJECTED}
    return [event for event in actual if event.get('payload', {}).get('call_id') not in ids]

def safe_native(native, source_ids):
    if RAW and native[0]['payload']['id'] == RAW[0]['payload']['id']:
        return ORIGINAL_SAFE(RAW, source_ids)
    return ORIGINAL_SAFE(native, source_ids)

def activate_projection():
    prepare()
    base.binder._events = events
    base.safe_source_native = safe_native

def bind():
    activate_projection()
    previous_links = base.modules()[0].validate_source_links
    previous_write = base.write
    def links(values):
        values.insert(-1, {'type': 'unexpected_tool_call', 'tool': 'apply_patch',
                          'call_id': REJECTED[0]['call_id'], 'reason': 'rejected_write_outside_campaign',
                          'succeeded': False, 'native_attempt_preserved': True})
        for index, event in enumerate(values):
            event['event_id'] = f'e{index + 1}'
        _, transport, _ = base.modules()
        final = values[-1]
        case = base.case_and_number('plugin-spontane-rssi-rh')[1]
        final['failures'] = base.codex_failures(values[:-1], case)
        final['status'] = 'failed'
        final['observables'] = transport.observable_checks(values, case)
        return previous_links(values)
    def write(path, value):
        if path.name == 'execution-repondant.json':
            value = dict(value)
            value.update(rejected_patch_wrapper_sha256=base.binder._sha(Path(__file__)),
                         rejected_native_patch_attempts=list(REJECTED), protocol_compliance=False,
                         rejected_patch_projection_scope='Rejected pair excluded only from successful-write parsing; raw native log retained; technical failure mandatory.')
        return previous_write(path, value)
    base.modules()[0].validate_source_links = links
    base.write = write
    pragma.bind('plugin-spontane-rssi-rh')
    final = ORIGINAL_EVENTS(campaign.RUN / 'plugin-spontane-rssi-rh.jsonl')[-1]
    if final['status'] != 'failed' or 'unexpected_tool_call' not in final['failures']:
        raise base.binder.BindingError('Échec technique de la tentative masqué')
    return {'case_id': 'plugin-spontane-rssi-rh', 'technical_status': 'failed', 'failures': final['failures']}

if __name__ == '__main__':
    print(json.dumps(bind(), ensure_ascii=False, indent=2))
