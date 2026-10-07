"""Rejoue les jugements liés de la nouvelle portée Codex sans réécrire les scores."""
from __future__ import annotations
import json
from pathlib import Path
import preuves_codex_dev6 as native
import controler_codex_dev6 as guarded

def generate():
    cases = native.binder._json((native.RUN / 'suite.json').read_text(encoding='utf-8'))
    manifest = native.binder._json((native.RUN / 'manifest.json').read_text(encoding='utf-8'))
    results = []
    identities = set()
    responder_proofs = []
    judge_proofs = []
    atoms = {'true': 0, 'false': 0, 'null': 0}
    for case in cases:
        identifier = case['id']
        answer_proof = native.RUN / identifier / 'liaison/execution-repondant.json'
        if not answer_proof.is_file():
            continue
        responder = native.binder._json(answer_proof.read_text(encoding='utf-8'))
        responder_proofs.append(responder)
        if responder['thread_id'] in identities:
            raise native.binder.BindingError('Identité répondant réutilisée')
        identities.add(responder['thread_id'])
        response = native.RUN / (identifier + '.jsonl')
        if (native.binder._sha(response) != responder['trace_sha256']
                or native.binder._sha(native.RUN / identifier / 'response.md') != responder['response_sha256']
                or native.binder._sha(native.RUN / identifier / 'liaison/trace-repondant.jsonl') != responder['native_filtered_sha256']):
            raise native.binder.BindingError('Pièce répondant modifiée : ' + identifier)
        candidates = list((native.RUN / 'juges-fragments').glob(identifier + '-*/liaison/execution-juge.json'))
        ordinary = native.RUN / 'juges' / identifier / 'liaison/execution-juge.json'
        if ordinary.is_file():
            candidates.append(ordinary)
        if len(candidates) > 1:
            raise native.binder.BindingError('Deux jugements retenus pour un cas')
        if not candidates:
            continue
        proof_path = candidates[0]
        proof = native.binder._json(proof_path.read_text(encoding='utf-8'))
        if proof['thread_id'] in identities:
            raise native.binder.BindingError('Identité du juge réutilisée')
        identities.add(proof['thread_id'])
        judge_proofs.append(proof)
        directory = proof_path.parent.parent
        packet = directory / (identifier + '.packet.json')
        judgment = directory / (identifier + '.jugement.json')
        if (native.binder._sha(packet) != proof['packet_sha256']
                or native.binder._sha(judgment) != proof['judgment_sha256']
                or native.binder._sha(directory / 'liaison/trace-juge.jsonl') != proof['trace_sha256']
                or judgment.read_bytes() != (native.RUN / (identifier + '.jugement.json')).read_bytes()):
            raise native.binder.BindingError('Pièce juge liée modifiée : ' + identifier)
        assessment, _, _ = native.modules()
        expected = assessment.build_judge_packet(case, response, native.CANDIDATE / 'docs/protocole-coactivation-v2.md')
        if native.binder._canonical(expected) != native.binder._canonical(native.binder._json(packet.read_text(encoding='utf-8'))):
            raise native.binder.BindingError('Paquet altéré ou barème différent')
        document = native.binder._json(judgment.read_text(encoding='utf-8'))
        assessment = guarded.validate(case, native.binder._events(response), document, native.binder._sha(response))
        if assessment != proof['assessment']:
            raise native.binder.BindingError('Rejeu différent du jugement lié')
        for item in document['invariants'].values():
            atoms['null' if item['status'] is None else ('true' if item['status'] else 'false')] += 1
        results.append(assessment)
    summary = {'run': manifest['run'], 'host': 'Codex', 'candidate_commit': manifest['candidate_commit'],
               'runtime_source_commit': manifest['runtime_source_commit'], 'case_count': len(cases),
               'atomic_count': manifest['atomic_count'], 'completed_respondents': len(responder_proofs),
               'judged_count': len(results), 'retained_unique_role_count': len(identities),
               'counts': {v: sum(r['verdict'] == v for r in results) for v in ('reussite', 'echec', 'bloque')},
               'atomic_results': atoms, 'scope': 'native Codex fresh roles; candidate runtime file loads',
               'actual_plugin_activation_verified': False, 'codex_plugin_smoke': 'not_established',
               'historical_scores_reused': False, 'release_ready': False,
               'first_two_export_pre_spawn_missing': [p['case_id'] for p in responder_proofs if not p['export_pre_spawn']],
               'source_provenance_limit': 'Raw source bodies omitted from published native log; original extraction attestations and sanitized v2 excerpts retained.',
               'results': results}
    return summary

if __name__ == '__main__':
    print(json.dumps(generate(), ensure_ascii=False, indent=2))
