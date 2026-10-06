"""Mesure la suite v2 sans modifier le harnais ni les preuves historiques."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import run_plugin_campaign as legacy
from source_evidence import extract_source_evidence, scrub_visible_text

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / 'tests/cas-coactivation-v2.json'
FROZEN_V2_REQUIRED = (
    'scripts/run_coactivation_v2.py', 'scripts/source_evidence.py',
    'scripts/coactivation_assessment.py', 'scripts/freeze_coactivation_v2.py',
    'scripts/verify_coactivation_v2.py',
    'tests/cas-coactivation-v2.json', 'tests/test_coactivation_v2.py',
    'tests/test_source_evidence.py', 'docs/cas-coactivation-v2.md',
    'docs/protocole-coactivation-v2.md', '.gitattributes',
    'tests/evidence/qualification-dsi/gel-r3.json',
)


def frozen_failures_v2(frozen: dict[str, Any]) -> list[str]:
    """Exige le contrat v2 et ses dépendances en plus du contrôle des octets."""
    if frozen.get('schema_version') != 2 or not isinstance(frozen.get('files'), dict):
        return ['frozen_schema_v2_required']
    prior = json.loads((ROOT / 'tests/evidence/qualification-dsi/gel-r3.json').read_text(encoding='utf-8'))
    missing = (set(FROZEN_V2_REQUIRED) | set(prior['files'])) - set(frozen['files'])
    if missing:
        return ['frozen_v2_inventory_incomplete:' + path for path in sorted(missing)]
    if any(frozen['files'][path] != checksum for path, checksum in prior['files'].items()):
        return ['baseline_runtime_or_harness_changed']
    return legacy.frozen_failures(frozen)


def load_cases() -> list[dict[str, Any]]:
    """Charge une suite atomique et refuse les identités ambiguës."""
    cases = json.loads(SUITE.read_text(encoding='utf-8'))
    if not isinstance(cases, list) or not cases:
        raise ValueError('Suite v2 vide ou invalide')
    identifiers: set[str] = set()
    for case in cases:
        identifier = case['id']
        if not re.fullmatch(r'[a-z0-9-]+', identifier) or identifier in identifiers:
            raise ValueError('Identifiant de cas invalide ou dupliqué')
        identifiers.add(identifier)
        if case.get('schema_version') != 2:
            raise ValueError('Version de contrat non prise en charge')
        items = case['invariant_objects']
        keys = [item['id'] for item in items]
        if not keys or len(set(keys)) != len(keys):
            raise ValueError('Invariants vides ou dupliqués')
        if case.get('activation_mode', 'forced') not in ('forced', 'spontaneous'):
            raise ValueError('Mode d’activation non pris en charge')
        if set(case['skills']) - set(json.loads((ROOT / 'upstream.json').read_text(encoding='utf-8'))['skills']):
            raise ValueError('Skill extérieur au candidat')
        if case['mcp_mode'] not in ('required', 'disabled'):
            raise ValueError('Mode MCP non pris en charge')
        if case['source_evidence_policy'] not in ('required', 'required_or_abstain', 'not_required'):
            raise ValueError('Politique de preuve non prise en charge')
        if any(item['category'] not in ('comportement', 'preuve_source') for item in items):
            raise ValueError('Catégorie d’invariant non prise en charge')
    return cases


def build_prompt(case: dict[str, Any]) -> str:
    """Isole la mesure forcée de la sélection spontanée sans divulguer son oracle."""
    if case.get('activation_mode') != 'spontaneous':
        return legacy.build_prompt(case)
    return (
        'Contrat de campagne : sélectionne les seuls skills nécessaires et active-les '
        'réellement via Skill. Read est disponible uniquement sous skills du plugin local. '
        'Les seuls outils externes disponibles sont ceux autorisés par la session. '
        'Ne remplace pas une activation par une mention. Réponds à la demande suivante.\n\n'
        + case['prompt']
    )


def build_command(case: dict[str, Any], claude: str) -> list[str]:
    """Garde les permissions du harnais r3 et remplace uniquement le contrat de mesure."""
    command = legacy.build_command(case, claude)
    command[-1] = build_prompt(case)
    return command


def sanitize(events: list[dict[str, Any]], case: dict[str, Any], *, captured_at: str) -> list[dict[str, Any]]:
    """Conserve ordre visible, identité des appels et résultat documentaire assaini."""
    clean: list[dict[str, Any]] = []
    calls: dict[str, dict[str, Any]] = {}
    inputs_by_id: dict[str, dict[str, Any]] = {}
    seen_results: set[str] = set()
    for event in events:
        records = legacy.sanitize([event], case)
        raw_calls = iter(legacy.message_tool_calls(event))
        for record in records:
            if record['type'] == 'official_source_call':
                # La preuve assainie porte l'URL utile ; le chemin brut est exclu.
                record.pop('source_path', None)
                if record.get('host') not in case.get('official_source_hosts', []):
                    record['host'] = 'unapproved_source_host'
            if record['type'] in ('assistant_text', 'result'):
                field = 'text' if record['type'] == 'assistant_text' else 'result'
                scrubbed = scrub_visible_text(record.get(field, ''))
                record[field] = scrubbed['text']
                record['text_redacted'] = scrubbed['redacted']
                record['text_truncated'] = scrubbed['truncated']
                if record['type'] == 'result':
                    errors = record.pop('errors', [])
                    record['errors_count'] = len(errors) if isinstance(errors, list) else int(bool(errors))
            if record['type'] in ('skill_activation', 'plugin_file_read', 'plugin_mcp_call',
                                  'official_source_call', 'foreign_mcp_call', 'unexpected_tool_call'):
                name, inputs, call_id = next(raw_calls)
                record['call_id'] = call_id
                if not call_id or call_id in calls:
                    clean.append({'type': 'unexpected_tool_call', 'tool': 'duplicate_or_missing_call_id'})
                else:
                    calls[call_id] = record
                    inputs_by_id[call_id] = {'name': name, 'source_url': inputs.get('url')}
            clean.append(record)
        for block in (event.get('message') or {}).get('content') or []:
            if block.get('type') != 'tool_result':
                continue
            call_id = block.get('tool_use_id', '')
            record = calls.get(call_id)
            if record is None or call_id in seen_results:
                clean.append({'type': 'unexpected_tool_call', 'tool': 'unlinked_or_duplicate_tool_result'})
                continue
            seen_results.add(call_id)
            if 'succeeded' in record:
                record['succeeded'] = not bool(block.get('is_error'))
            if record['type'] in ('plugin_mcp_call', 'official_source_call'):
                details = inputs_by_id[call_id]
                evidence = extract_source_evidence(block, tool=details['name'], call_id=call_id,
                    source_url=details['source_url'], retrieved_at=captured_at)
                clean.append({**evidence, 'type': 'source_evidence',
                              'timestamp_basis': 'capture_apres_processus',
                              'content_trust': 'untrusted_source_data'})
    for index, event in enumerate(clean):
        event['event_id'] = f'e{index + 1}'
    return clean


def technical_failures(clean: list[dict[str, Any]], case: dict[str, Any]) -> list[str]:
    """Vérifie le transport et le routage observé, indépendamment du droit."""
    failures = legacy.technical_failures(clean, case)
    for flag in ('truncated', 'redacted'):
        if any(event.get('text_' + flag) is True for event in clean
               if event['type'] in ('assistant_text', 'result')):
            failures.append('visible_text_' + flag)
    if case.get('activation_mode') == 'spontaneous':
        actual = [e.get('skill') for e in clean if e['type'] == 'skill_activation']
        expected = {legacy.qualified_skill(s) for s in case['skills']}
        if 'activation_sequence_mismatch' in failures:
            failures.remove('activation_sequence_mismatch')
        if set(actual) != expected or len(actual) != len(expected):
            failures.append('activation_set_mismatch')
    init = next((e for e in clean if e['type'] == 'init'), None)
    if init is not None and case['mcp_mode'] == 'required':
        if not any(s.get('name') == 'droit-francais' and s.get('status') == 'connected'
                   for s in init.get('mcp_servers', [])):
            failures.append('mcp_not_connected')
    return failures


def observable_checks(clean: list[dict[str, Any]], case: dict[str, Any]) -> dict[str, Any]:
    """Produit des observations sans attribuer de validation juridique automatique."""
    text = next((e for e in clean if e['type'] == 'assistant_text' and e.get('text', '').strip()), None)
    stop_required = any(item.get('deterministic_check') == 'stop_first' for item in case['invariant_objects'])
    primary = [e['event_id'] for e in clean if e['type'] == 'source_evidence'
               and e.get('status') == 'available' and any(d.get('nature') == 'primary_text'
                   and d.get('status') == 'available' for d in e.get('documents', []))]
    return {'stop_required': stop_required,
            'first_visible_text_ref': text['event_id'] if text else None,
            'stop_first': bool(text and re.match(r'^(?:#{1,6}\s*)?(?:\*\*)?STOP\b', text['text'].lstrip())) if stop_required else None,
            'primary_content_refs': primary, 'primary_content_available': bool(primary),
            'legal_validity': None, 'note': 'Le contenu disponible ne certifie ni pertinence ni vigueur.'}


def execute(case: dict[str, Any], claude: str) -> tuple[list[dict[str, Any]], int, dict[str, str]]:
    """Exécute une session fraîche ; le flux brut reste en mémoire."""
    environment = os.environ.copy()
    environment.update(ENABLE_CLAUDEAI_MCP_SERVERS='false', CLAUDE_CODE_DISABLE_BUNDLED_SKILLS='1',
                       DISABLE_DOCTOR_COMMAND='1')
    started = datetime.now(timezone.utc).isoformat()
    try:
        completed = subprocess.run(build_command(case, claude), cwd=ROOT, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
            errors='replace', check=False, timeout=900)
        output, code = completed.stdout, completed.returncode
    except subprocess.TimeoutExpired:
        # Le flux partiel brut n'est pas écrit, même pour un timeout.
        output, code = '', 124
    finished = datetime.now(timezone.utc).isoformat()
    events = []
    for line in output.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return sanitize(events, case, captured_at=finished), code, {'started_at': started, 'finished_at': finished}


def main(*, frozen_validator: Callable[[dict[str, Any]], list[str]] = frozen_failures_v2,
         candidate_profile: str | None = None) -> int:
    """Mesure seulement un gel explicite et refuse d'écraser une preuve existante."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', dest='case_ids')
    parser.add_argument('--claude', default='claude')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--frozen-manifest', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    cases = load_cases()
    selected = [c for c in cases if not args.case_ids or c['id'] in args.case_ids]
    if args.case_ids and len(selected) != len(set(args.case_ids)):
        parser.error('Identifiant inconnu ou dupliqué')
    if args.dry_run:
        for case in selected:
            print(json.dumps(build_command(case, args.claude), ensure_ascii=False))
        return 0
    if args.frozen_manifest is None:
        parser.error('--frozen-manifest requis')
    frozen = json.loads(args.frozen_manifest.read_text(encoding='utf-8'))
    if failures := frozen_validator(frozen):
        parser.error(' | '.join(failures))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for case in selected:
        path = args.output_dir / (case['id'] + '.jsonl')
        if path.exists():
            parser.error('Trace existante conservée : ' + str(path))
    result = 0
    for case in selected:
        if failures := frozen_validator(frozen):
            parser.error(' | '.join(failures))
        path = args.output_dir / (case['id'] + '.jsonl')
        if path.exists():
            parser.error('Trace existante conservée : ' + str(path))
        clean, code, window = execute(case, args.claude)
        failures = technical_failures(clean, case) + frozen_validator(frozen)
        if code:
            failures.append('process_exit_nonzero')
        assessment = {'type': 'technical_assessment', 'case_id': case['id'], 'process_exit': code,
            'status': 'failed' if failures else 'passed', 'failures': failures,
            'observables': observable_checks(clean, case), 'requires_independent_judgment': True}
        provenance = {'type': 'provenance', 'schema_version': 2, 'candidate_commit': frozen['candidate_commit'],
            'suite_sha256': hashlib.sha256(SUITE.read_bytes()).hexdigest(),
            'case_sha256': hashlib.sha256(json.dumps(case, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
            'prompt_sha256': hashlib.sha256(build_prompt(case).encode()).hexdigest(),
            'frozen_manifest_sha256': hashlib.sha256(args.frozen_manifest.read_bytes()).hexdigest(),
            'activation_mode': case.get('activation_mode', 'forced'), 'capture_window': window}
        if candidate_profile is not None:
            provenance['candidate_profile'] = candidate_profile
        path.write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in [provenance, *clean, assessment]),
                        encoding='utf-8', newline='\n')
        print(json.dumps({'case_id': case['id'], 'technical_status': assessment['status'],
                         'primary_content_available': assessment['observables']['primary_content_available'],
                         'business_status': 'not_judged', 'path': str(path)}, ensure_ascii=False))
        result = max(result, bool(failures))
    return int(result)


if __name__ == '__main__':
    raise SystemExit(main())
