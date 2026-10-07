"""Exporte et lie les seules réponses r7 achevées à des juges natifs frais."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import lie_jugements_corriges as binder
import lie_jugements_corriges_bruts as raw

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / 'Collectivite-corrections-pr5'
RUN = CANDIDATE / 'tests/evidence/coactivation-corrigee/campagne-r7'
SESSION_DIRECTORIES = tuple(Path('C:/Users/Krn/.codex/sessions/2026/10') / day for day in ('06', '07'))
SELF_AGENT = '/root/outillage_preuves_r7'


def execution_scope(events: list[dict[str, Any]]) -> tuple[str, str | None]:
    """Ne transforme jamais un refus ou une erreur de transport en verdict métier."""
    results = [event for event in events if event.get('type') == 'result']
    assessments = [event for event in events if event.get('type') == 'technical_assessment']
    if len(results) != 1 or len(assessments) != 1 or events[-1] != assessments[0]:
        raise ValueError('Résultat ou bilan final absent ou ambigu')
    result, assessment = results[0], assessments[0]
    exit_code = assessment.get('process_exit')
    if type(exit_code) is not int:
        raise ValueError('Code de sortie invalide')
    if result.get('is_error') is False and exit_code == 0 and result.get('subtype') == 'success':
        return 'completed_response', None
    message = result.get('result')
    if (result.get('is_error') is True and exit_code != 0 and assessment.get('status') == 'failed'
            and isinstance(message, str) and message.strip()):
        message = message.strip()
        scope = ('quota_interrupted' if re.fullmatch(
            r"You've hit your session limit · resets [^\r\n]+", message) else 'execution_failed')
        return scope, message
    raise ValueError('Exécution incomplète dont la cause n’est pas attestée')


def native_inventory(directories: tuple[Path, ...] = SESSION_DIRECTORIES) -> dict[str, tuple[Path, dict[str, Any]]]:
    """Découvre les identités dans les métadonnées, pas dans le nom présumé du fichier."""
    sessions: dict[str, tuple[Path, dict[str, Any]]] = {}
    for directory in directories:
        for path in directory.glob('*.jsonl'):
            with path.open(encoding='utf-8') as stream:
                event = json.loads(stream.readline())
            if event.get('type') != 'session_meta' or not isinstance(event.get('payload'), dict):
                raise ValueError('Métadonnée native absente : ' + str(path))
            meta = event['payload']
            identity = meta.get('id')
            if not isinstance(identity, str) or not identity:
                raise ValueError('Identité native absente')
            if identity in sessions:
                raise ValueError('Identité native dupliquée : ' + identity)
            sessions[identity] = path, meta
    return sessions


def agent_path(meta: dict[str, Any]) -> str | None:
    """Les sources de sessions racine sont parfois une chaîne."""
    source = meta.get('source')
    if not isinstance(source, dict):
        return None
    return source.get('subagent', {}).get('thread_spawn', {}).get('agent_path')


def discover_parent(sessions: dict[str, tuple[Path, dict[str, Any]]]) -> tuple[str, Path]:
    """Établit le parent courant à partir de la propre session native de l’outillage."""
    own = [meta for _, meta in sessions.values() if agent_path(meta) == SELF_AGENT]
    if len(own) != 1:
        raise ValueError('Session propre absente ou ambiguë')
    parent_id = own[0]['source']['subagent']['thread_spawn'].get('parent_thread_id')
    if parent_id not in sessions or parent_id == own[0]['id']:
        raise ValueError('Parent natif absent ou divergent')
    path, parent = sessions[parent_id]
    if agent_path(parent) is not None:
        raise ValueError('Le parent attendu doit être la racine')
    return parent_id, path


def export_finished() -> dict[str, Any]:
    """Les refus et erreurs restent conservés sans paquet comportemental."""
    exported, skipped = [], []
    for case in binder._json((CANDIDATE / 'tests/cas-coactivation-v2.json').read_text(encoding='utf-8')):
        name = case['id']
        response = RUN / (name + '.jsonl')
        if not response.is_file():
            continue
        events = binder._events(response)
        if not events or events[-1].get('type') != 'technical_assessment':
            continue
        scope, _ = execution_scope(events)
        destination = RUN / 'juges' / name
        if scope != 'completed_response':
            if destination.exists():
                raise ValueError('Paquet de juge présent sur exécution interrompue : ' + name)
            skipped.append({'case_id': name, 'execution_scope': scope})
            continue
        manifest = destination / (name + '.export.json')
        if manifest.exists():
            value = binder._json(manifest.read_text(encoding='utf-8'))
            for suffix, field in (('packet.json', 'packet_sha256'), ('prompt.md', 'prompt_sha256')):
                if binder._sha(destination / (name + '.' + suffix)) != value[field]:
                    raise ValueError('Export préexistant divergent : ' + name)
            if (value.get('compact_packet') is not True
                    or value.get('raw_adapter_sha256') != binder._sha(Path(raw.__file__))):
                raise ValueError('Adaptateur préexistant divergent : ' + name)
            continue
        exported.append(raw.export_packet(CANDIDATE, response, destination))
    return {'run': 'r7', 'new_exports': len(exported), 'unjudged_executions': skipped}


def bind_finished() -> dict[str, Any]:
    """Lie chaque numéro de juge à l’ordre inchangé des seize cas."""
    sessions = native_inventory()
    parent_id, parent_path = discover_parent(sessions)
    natives: dict[str, Path] = {}
    for path, meta in sessions.values():
        agent = agent_path(meta)
        if isinstance(agent, str) and re.fullmatch(r'/root/juge_corrige_r7_(0[1-9]|1[0-6])', agent):
            if agent in natives:
                raise ValueError('Session de juge dupliquée : ' + agent)
            natives[agent] = path
    results = []
    cases = binder._json((CANDIDATE / 'tests/cas-coactivation-v2.json').read_text(encoding='utf-8'))
    for number, case in enumerate(cases, 1):
        name = case['id']
        directory = RUN / 'juges' / name
        judgment = directory / (name + '.jugement.json')
        target = RUN / (name + '.jugement.json')
        proof_path = directory / 'liaison/execution-juge.json'
        if proof_path.exists():
            if not judgment.is_file() or not target.is_file() or judgment.read_bytes() != target.read_bytes():
                raise ValueError('Copie de jugement liée absente ou divergente : ' + name)
            continue
        if not judgment.is_file():
            continue
        agent = f'/root/juge_corrige_r7_{number:02d}'
        native = natives.get(agent)
        if native is None or not any(event.get('payload', {}).get('type') == 'task_complete'
                for event in binder._events(native)):
            continue
        if target.exists():
            raise ValueError('Copie de jugement déjà présente sans liaison : ' + name)
        scope, _ = execution_scope(binder._events(RUN / (name + '.jsonl')))
        if scope != 'completed_response':
            raise ValueError('Jugement sur exécution interrompue : ' + name)
        proof = raw.bind_judgment(CANDIDATE, RUN / (name + '.jsonl'),
            directory / (name + '.packet.json'), judgment, native, parent_path,
            agent, parent_id, directory / 'liaison')
        with target.open('xb') as stream:
            stream.write(judgment.read_bytes())
        results.append({'case_id': name, 'assessment': proof['assessment'], 'identity_checked': True})
    return {'run': 'r7', 'parent_thread_id': parent_id, 'new_bindings': results}


def retain_parent(expected_count: int) -> dict[str, Any]:
    """Conserve uniquement les spawns retenus ; aucun message initial opaque n’est publié."""
    parent_id, parent_path = discover_parent(native_inventory())
    parent = binder._events(parent_path)
    proofs = list((RUN / 'juges').glob('*/liaison/execution-juge.json'))
    if not 1 <= expected_count <= 16 or len(proofs) != expected_count:
        raise ValueError('Nombre déclaré de juges liés non établi')
    values = [binder._json(path.read_text(encoding='utf-8')) for path in proofs]
    agents = {value['agent'] for value in values}
    if len(agents) != expected_count or any(value['parent_thread_id'] != parent_id for value in values):
        raise ValueError('Identités de juges réutilisées ou parent divergent')
    meta = parent[0]
    retained = [{'timestamp': meta['timestamp'], 'type': 'session_meta',
        'payload': {key: meta['payload'][key] for key in ('id', 'timestamp')}}]
    for agent in sorted(agents):
        calls = [event for event in parent if event.get('payload', {}).get('type') == 'function_call'
            and event['payload'].get('name') == 'spawn_agent'
            and binder._json(event['payload']['arguments']).get('task_name') == agent.rsplit('/', 1)[-1]]
        if len(calls) != 1 or binder._json(calls[0]['payload']['arguments']).get('fork_turns') != 'none':
            raise ValueError('Spawn frais absent ou ambigu')
        call = calls[0]
        outputs = [event for event in parent if event.get('payload', {}).get('type') == 'function_call_output'
            and event['payload'].get('call_id') == call['payload']['call_id']]
        if len(outputs) != 1 or binder._json(outputs[0]['payload']['output']).get('task_name') != agent:
            raise ValueError('Retour de spawn non lié')
        for event in (call, outputs[0]):
            payload = {key: value for key, value in event['payload'].items()
                if key in ('type', 'name', 'call_id', 'arguments', 'output')}
            if 'arguments' in payload:
                original = binder._json(payload['arguments'])
                visible = {key: value for key, value in original.items()
                    if key in ('task_name', 'fork_turns', 'model', 'reasoning_effort')}
                payload['arguments'] = json.dumps(visible, ensure_ascii=False)
                payload['initial_message_verified'] = False
                payload['initial_message_sha256'] = hashlib.sha256(original.get('message', '').encode()).hexdigest()
            retained.append({'timestamp': event['timestamp'], 'type': event['type'], 'payload': payload})
    binder._write(RUN / 'juges/trace-parent-filtre.jsonl',
        ''.join(json.dumps(event, ensure_ascii=False) + '\n' for event in retained))
    return {'retained_judges': len(agents), 'native_events': len(retained), 'parent_thread_id': parent_id}


def main() -> None:
    """Aucune génération de rapport, aucun appel Claude et aucune mutation runtime."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('export', 'bind', 'parent'))
    parser.add_argument('--expected-count', type=int, default=16)
    args = parser.parse_args()
    actions = {'export': export_finished, 'bind': bind_finished,
        'parent': lambda: retain_parent(args.expected_count)}
    print(json.dumps(actions[args.action](), ensure_ascii=False))


if __name__ == '__main__':
    main()
