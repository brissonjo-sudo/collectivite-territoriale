"""Contrôles additionnels distincts ; préserve l'adaptateur natif initial gelé.

Une tentative de spawn dont l'erreur native exacte démontre l'absence de
création ne compte pas comme une session fraîche réussie. Elle reste tracée.
Un invariant exigeant littéralement « via Skill » ne peut être vrai en lecture.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import preuves_codex_dev6 as native

BASE_NATIVE_PROOF = native.raw.native_proof
BASE_VALIDATE = native.validate_codex
FAILED_SPAWN = 'collab spawn failed: agent thread limit reached'

def successful_parent(parent, agent):
    filtered = list(parent)
    rejected = []
    for event in parent:
        payload = event.get('payload', {})
        if payload.get('type') != 'function_call' or payload.get('name') != 'spawn_agent':
            continue
        args = native.binder._json(payload['arguments'])
        if args.get('task_name') != agent.rsplit('/', 1)[-1]:
            continue
        outputs = [e for e in parent if e.get('payload', {}).get('type') == 'function_call_output'
                   and e['payload'].get('call_id') == payload.get('call_id')]
        if len(outputs) != 1:
            raise native.binder.BindingError('Sortie de spawn absente ou ambiguë')
        if outputs[0]['payload'].get('output') == FAILED_SPAWN:
            rejected.append({'call_id': payload['call_id'], 'timestamp': event['timestamp'],
                             'result_timestamp': outputs[0]['timestamp'], 'reason': FAILED_SPAWN,
                             'task_name': args['task_name'], 'created_session': False})
            filtered.remove(event)
            filtered.remove(outputs[0])
    return filtered, rejected

def native_proof(events, parent, agent, parent_id, packet, judgment, exported_at):
    filtered, rejected = successful_parent(parent, agent)
    proof, kept = BASE_NATIVE_PROOF(events, filtered, agent, parent_id, packet, judgment, exported_at)
    proof.update(identity_wrapper_sha256=native.binder._sha(Path(__file__)),
                 rejected_creation_attempts=rejected,
                 parent_projection_scope='only explicit failed spawn without creation excluded; retained receipt')
    return proof, kept

def skill_literal_guard(case, judgment):
    for item in case['invariant_objects']:
        wording = ' '.join(str(item.get(key, '')) for key in ('expectation', 'legacy_label', 'observable'))
        if re.search(r'\bvia\s+Skill\b', wording, re.I) and judgment['invariants'][item['id']]['status'] is True:
            raise native.binder.BindingError('Activation native Skill non démontrée : ' + item['id'])

def validate(case, events, judgment, digest):
    skill_literal_guard(case, judgment)
    return BASE_VALIDATE(case, events, judgment, digest)

def activate():
    native.raw.native_proof = native_proof
    native.validate_codex = validate

if __name__ == '__main__':
    activate()
    native.main()
