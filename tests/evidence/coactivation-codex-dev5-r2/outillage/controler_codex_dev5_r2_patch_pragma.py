"""Directive de capacité d'un patch littéral, sans changer sa destination ou son contenu."""
from pathlib import Path
import hashlib
import json
import re
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign
import controler_codex_dev5_r2_pragma as pragma

BASE_ARGUMENTS = base.binder._arguments
REGISTERED = {}
RECEIPTS = []

def patch_without_pragma(script):
    match = re.match(r'^// @exec: ([^\r\n]+)\r?\n', script)
    if not match:
        raise base.binder.BindingError('Directive de patch absente')
    value = base.binder._json(match[1])
    if (set(value) != {'max_output_tokens'} or type(value['max_output_tokens']) is not int
            or value['max_output_tokens'] != 55000):
        raise base.binder.BindingError('Directive patch non autorisée')
    body = script[match.end():]
    BASE_ARGUMENTS(body, 'apply_patch')
    return body

def prepare():
    campaign.configure()
    native = base.binder._events(campaign.BASE_DISCOVER('/root/repondant_codex_dev5_r2_13')[0])
    REGISTERED.clear(); RECEIPTS.clear()
    for event in native:
        payload = event.get('payload', {})
        script = payload.get('input', payload.get('arguments', ''))
        if payload.get('name') != 'exec' or 'tools.apply_patch(' not in script:
            continue
        body = patch_without_pragma(script)
        REGISTERED[script] = body
        RECEIPTS.append({'call_id': payload['call_id'], 'max_output_tokens': 55000,
                         'native_script_sha256': hashlib.sha256(script.encode('utf-8')).hexdigest()})
    if len(RECEIPTS) != 1:
        raise base.binder.BindingError('Un seul patch littéral avec directive attendu')

def arguments(script, name):
    if name == 'apply_patch' and script in REGISTERED:
        return BASE_ARGUMENTS(REGISTERED[script], name)
    return BASE_ARGUMENTS(script, name)

def activate():
    prepare()
    base.binder._arguments = arguments

def bind():
    activate()
    previous_write = base.write
    def write(path, value):
        if path.name == 'execution-repondant.json':
            value = dict(value)
            value.update(patch_pragma_wrapper_sha256=base.binder._sha(Path(__file__)),
                         native_patch_pragmas=list(RECEIPTS),
                         patch_pragma_scope='Capacity directive only; one native literal patch, target and bytes unchanged.')
        return previous_write(path, value)
    base.write = write
    return pragma.bind('plugin-spontane-incident-donnees')

if __name__ == '__main__':
    print(json.dumps(bind(), ensure_ascii=False, indent=2))
