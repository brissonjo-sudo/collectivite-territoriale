"""Valide un jugement atomique et sépare comportement, document et transport."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from run_coactivation_v2 import observable_checks, technical_failures


def build_judge_packet(case: dict[str, Any], trace: Path, protocol: Path) -> dict[str, Any]:
    """Fournit une entrée figée à un juge frais, sans runtime ni anciens scores."""
    events = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
    return {'schema_version': 2, 'case_id': case['id'], 'question': case['prompt'],
            'activation_mode': case.get('activation_mode', 'forced'),
            'skills': case['skills'], 'activation_sequence': case['activation_sequence'],
            'mcp_mode': case['mcp_mode'], 'source_evidence_policy': case['source_evidence_policy'],
            'invariant_objects': case['invariant_objects'], 'rubric': protocol.read_text(encoding='utf-8'),
            'trace_sha256': hashlib.sha256(trace.read_bytes()).hexdigest(), 'trace': events}


def validate_judgment(case: dict[str, Any], events: list[dict[str, Any]],
                      judgment: dict[str, Any], trace_sha256: str) -> dict[str, Any]:
    """Refuse le faux succès, les valeurs coercibles et les références fabriquées.

    Ce contrôle valide les pièces utilisées et les barrières mécaniques. Il
    ne remplace pas l'appréciation métier ou juridique du juge indépendant.
    """
    if judgment.get('case_id') != case['id'] or judgment.get('trace_sha256') != trace_sha256:
        raise ValueError('Jugement rattaché au mauvais cas ou à une autre trace')
    required = {item['id']: item for item in case['invariant_objects']}
    values = judgment.get('invariants')
    if not isinstance(values, dict) or set(values) != set(required):
        raise ValueError('Clés de jugement incomplètes ou étrangères')
    references = {event['event_id']: event for event in events if 'event_id' in event}
    if len(references) != sum('event_id' in event for event in events):
        raise ValueError('Références d’événements ambiguës')
    assessments = [event for event in events if event['type'] == 'technical_assessment']
    if len(assessments) != 1:
        raise ValueError('Contrôle technique absent ou ambigu')
    assessment = assessments[0]
    if assessment['case_id'] != case['id']:
        raise ValueError('Contrôle technique d’un autre cas')
    computed = technical_failures(events, case)
    if assessment['status'] == 'passed' and (computed or assessment.get('process_exit') != 0):
        raise ValueError('Succès technique non démontré par la trace')
    if assessment['observables'] != observable_checks(events, case):
        raise ValueError('Observations techniques non conformes à la trace')
    calls = {event.get('call_id'): index for index, event in enumerate(events)
             if event['type'] in ('plugin_mcp_call', 'official_source_call')}
    for index, event in enumerate(events):
        if event['type'] != 'source_evidence':
            continue
        call_index = calls.get(event.get('call_id'))
        if call_index is None or call_index >= index:
            raise ValueError('Preuve documentaire non liée à un appel antérieur')
        if event.get('status') == 'available' and events[call_index].get('succeeded') is not True:
            raise ValueError('Preuve documentaire associée à un appel échoué')
    categories: dict[str, list[bool | None]] = {'comportement': [], 'preuve_source': []}
    for key, result in values.items():
        if not isinstance(result, dict) or set(result) != {'status', 'basis', 'evidence_refs', 'rationale'}:
            raise ValueError('Format de jugement atomique invalide')
        status = result['status']
        if status is not None and type(status) is not bool:
            raise ValueError('Statut non booléen ou non null')
        refs = result['evidence_refs']
        if not isinstance(refs, list) or any(not isinstance(ref, str) or ref not in references for ref in refs):
            raise ValueError('Référence de preuve inconnue')
        if not isinstance(result['rationale'], str) or not result['rationale'].strip():
            raise ValueError('Justification manquante')
        if result['basis'] not in ('observation', 'retrieval', 'abstention', 'missing'):
            raise ValueError('Base de preuve inconnue')
        if status is not None and not refs:
            raise ValueError('Conclusion sans référence de preuve')
        item = required[key]
        if item.get('deterministic_check') == 'stop_first':
            measured = assessment['observables']['stop_first']
            if status is True and measured is not True:
                raise ValueError('STOP tardif ou absent ne peut être validé')
        if item['category'] == 'preuve_source' and status is True:
            if result['basis'] == 'retrieval':
                sources = [references[ref] for ref in refs if references[ref]['type'] == 'source_evidence']
                documents = [doc for source in sources if source.get('status') == 'available'
                             for doc in source.get('documents', []) if doc.get('nature') == 'primary_text'
                             and doc.get('status') == 'available']
                if not documents:
                    raise ValueError('Recherche, résumé, contenu absent ou tronqué ne valent pas texte primaire')
                if all(doc.get('metadata', {}).get('applicable_at_as_of_date') is False for doc in documents):
                    raise ValueError('Source signalée non applicable sans autre preuve primaire')
            elif result['basis'] == 'abstention':
                if not item.get('accepts_abstention'):
                    raise ValueError('Abstention non admise pour cet invariant')
                if not any(references[ref]['type'] == 'assistant_text' for ref in refs):
                    raise ValueError('Abstention sans texte observable')
            else:
                raise ValueError('Validation documentaire fondée sur une simple observation')
        categories[item['category']].append(status)
    behavior = categories['comportement']
    sources = categories['preuve_source']
    behavior_status = 'failed' if False in behavior else ('passed' if all(v is True for v in behavior) else 'incomplete')
    primary = assessment['observables']['primary_content_available']
    documentary_status = ('not_required' if case['source_evidence_policy'] == 'not_required'
                          else ('failed' if False in sources else ('passed' if all(v is True for v in sources) else 'incomplete')))
    if assessment['status'] != 'passed' or False in behavior or False in sources:
        verdict = 'echec'
    elif None in behavior or None in sources or (case['mcp_mode'] == 'required' and not primary):
        verdict = 'bloque'
    else:
        verdict = 'reussite'
    if judgment.get('verdict') != verdict:
        raise ValueError(f'Verdict incompatible avec les invariants et preuves : attendu {verdict}')
    return {'case_id': case['id'], 'verdict': verdict, 'technical_status': assessment['status'],
            'behavior_status': behavior_status, 'documentary_status': documentary_status,
            'primary_content_available': primary, 'release_ready': False}
