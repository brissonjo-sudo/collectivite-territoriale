"""Adaptation distincte du filtre web littéral, sans inventer des arguments natifs.

Accepte uniquement site:<hôte exact autorisé> ancré, sans autre filtre site,
opérateur OR, URL, autre hôte ou syntaxe d'injection. Les domaines dérivés sont
utilisés seulement pour le contrôle interne ; l'appel original reste conservé.
Un appel hors scope devient un échec technique observable, jamais du primaire.
"""
from __future__ import annotations
import argparse
import copy
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import preuves_codex_dev5 as base
import preuves_codex_dev5_web as web
import campagne_codex_dev5_r2 as campaign

BASE_PREPARE = web.prepare
BASE_PARSE = web.BASE_SOURCE_CALL
BASE_EVIDENCE = web.evidence
BASE_SAFE_URL = web.safe_web_url
BASE_LINKS = base.modules()[0].validate_source_links
BASE_WRITE = base.write
ORIGINALS = {}
FILTERS = {}
PARSED = {}
CASE = None

def literal_site_host(query, approved):
    if not isinstance(query, str):
        raise base.binder.BindingError('literal_site_query_not_string')
    match = re.fullmatch(r'site:([a-z0-9.-]+) ([^\r\n]+)', query)
    if not match or match[1] not in approved:
        raise base.binder.BindingError('literal_site_host_not_exact_approved')
    tail = match[2]
    if (len(re.findall(r'(?i)\bsite\s*:', query)) != 1 or re.search(r'(?i)\bOR\b|-\s*site\s*:', tail)
            or re.search(r'https?://|\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b', tail)
            or re.search(r'[\r\n;`$|]|&&', tail)):
        raise base.binder.BindingError('literal_site_query_ambiguous_or_injected')
    return match[1]

def query_for_validation(query, approved):
    internal = copy.deepcopy(query)
    if 'domains' in query:
        domains = query['domains']
        if not isinstance(domains, list) or not domains or any(domain not in approved for domain in domains):
            raise base.binder.BindingError('explicit_domains_not_approved')
        return internal, {'basis': 'explicit_domains', 'hosts': list(domains)}
    host = literal_site_host(query.get('q'), approved)
    internal['domains'] = [host]
    return internal, {'basis': 'literal_site', 'hosts': [host], 'derived_for_internal_validation_only': True}

def safe_url(url, sources):
    existing = BASE_SAFE_URL(url, sources)
    if existing:
        return existing
    # Chemin public CNIL précisément rencontré ; aucune exception générique.
    try:
        parsed = urlsplit(url)
        if (parsed.scheme == 'https' and parsed.hostname == 'www.cnil.fr' and not parsed.username and not parsed.password
                and parsed.port in (None, 443) and parsed.path == '/fr/violations-de-donnees-personnelles-les-regles-suivre'):
            return urlunsplit(('https', parsed.hostname, parsed.path, '', ''))
    except (ValueError, TypeError):
        pass
    return None

def prepare(identifier):
    global CASE
    number, CASE = base.case_and_number(identifier)
    approved = set(CASE['official_source_hosts'])
    native_path, _ = campaign.BASE_DISCOVER(f'/root/repondant_codex_dev5_r2_{number:02d}')
    native = base.binder._events(native_path)
    references = {}
    sources = base.modules()[2]
    for event in native:
        payload = event.get('payload', {})
        script = payload.get('input', payload.get('arguments'))
        if payload.get('type') not in ('custom_tool_call', 'function_call') or not isinstance(script, str) or 'tools.web__run(' not in script:
            continue
        tool, actual = BASE_PARSE(script)
        internal = copy.deepcopy(actual)
        bases = []
        failures = []
        if set(actual) - {'open', 'find', 'click', 'search_query', 'response_length'}:
            failures.append('unsupported_native_web_operation')
        for query in actual.get('search_query', []):
            try:
                projected, basis = query_for_validation(query, approved)
                bases.append(basis)
            except base.binder.BindingError as error:
                failures.append(str(error))
                projected = {'q': 'scope-rejected-not-used-as-proof', 'domains': [sorted(approved)[0]]}
            index = actual.get('search_query', []).index(query)
            internal['search_query'][index] = projected
        for operation in ('open', 'find', 'click'):
            for request in actual.get(operation, []):
                ref = request.get('ref_id')
                url = ref if isinstance(ref, str) and ref.startswith('https://') else references.get(ref)
                if not url or urlsplit(url).hostname not in approved or safe_url(url, sources) is None:
                    failures.append('native_web_reference_outside_authorized_scope')
        output, parts = base.outputs(native, event)
        if len(parts) != 2 or not parts[0].startswith('Script completed\n'):
            raise base.binder.BindingError('Retour natif web incomplet, identité à conserver séparément')
        for page in web.blocks(parts[1]):
            if urlsplit(page['url']).hostname in approved and safe_url(page['url'], sources):
                references[page['reference_id']] = page['url']
        if failures:
            # Analyse seulement : aucune nouvelle requête n'est effectuée.
            internal = {'search_query': [{'q': 'scope-rejected-not-used-as-proof', 'domains': [sorted(approved)[0]]}]}
        call_id = payload['call_id']
        ORIGINALS[call_id] = actual
        FILTERS[call_id] = {'query_filters': bases, 'scope_valid': not failures, 'scope_failures': failures}
        PARSED[script] = (tool, internal)
    previous_parse, previous_safe = web.BASE_SOURCE_CALL, web.safe_web_url
    try:
        web.BASE_SOURCE_CALL = lambda script: PARSED[script] if script in PARSED else BASE_PARSE(script)
        web.safe_web_url = safe_url
        BASE_PREPARE(identifier)
    finally:
        web.BASE_SOURCE_CALL, web.safe_web_url = previous_parse, previous_safe
    for call_id, capture in web.CAPTURES.items():
        capture['actual_arguments'] = ORIGINALS[call_id]
        capture['domain_filter_validation'] = FILTERS[call_id]
        if not FILTERS[call_id]['scope_valid']:
            capture['pages'] = []
        web.READ_PROJECTION[base.binder._canonical(ORIGINALS[call_id])] = {'open': [{'ref_id': url} for url in capture['effective_urls']]}

def evidence(capture, sources):
    validation = FILTERS[capture['call_id']]
    if not validation['scope_valid']:
        result = {'type': 'source_evidence', 'tool': 'web__run', 'native_tool': 'web__run', 'call_id': capture['call_id'],
                  'status': 'missing', 'documents': [], 'reason': 'native_web_call_outside_authorized_scope',
                  'retrieved_at': capture['timestamp'], 'content_trust': 'untrusted_source_data'}
    else:
        result = BASE_EVIDENCE(capture, sources)
    result.update(domain_filter_validation=validation, site_filter_wrapper_sha256=base.binder._sha(Path(__file__)),
                  native_arguments_preserved=True, domains_derived_for_internal_validation_only=True)
    return result

def validate_links(events):
    if CASE is None:
        return BASE_LINKS(events)
    for index in range(len(events) - 1, -1, -1):
        event = events[index]
        validation = FILTERS.get(event.get('call_id'))
        if event.get('type') == 'official_source_call' and validation and not validation['scope_valid']:
            event.update(succeeded=False, native_scope_valid=False, native_scope_failures=validation['scope_failures'])
            events.insert(index + 1, {'type': 'unexpected_tool_call', 'tool': 'web__run', 'call_id': event['call_id'],
                                      'reason': 'native_web_call_outside_authorized_scope',
                                      'native_scope_failures': validation['scope_failures']})
    for index, event in enumerate(events):
        event['event_id'] = f'e{index + 1}'
    if events[-1].get('type') == 'technical_assessment':
        _, transport, _ = base.modules()
        final = events[-1]
        final['failures'] = base.codex_failures(events[:-1], CASE)
        final['status'] = 'failed' if final['failures'] else 'passed'
        final['observables'] = transport.observable_checks(events, CASE)
        final['site_filter_wrapper_sha256'] = base.binder._sha(Path(__file__))
    return BASE_LINKS(events)

def write(path, value):
    if path.name == 'execution-repondant.json':
        value = dict(value)
        value.update(site_filter_wrapper_sha256=base.binder._sha(Path(__file__)),
                     native_web_filter_validation=FILTERS,
                     filter_projection_scope='literal site host derived only internally; actual_arguments unchanged')
    return BASE_WRITE(path, value)

def activate():
    web.prepare = prepare
    web.evidence = evidence
    base.modules()[0].validate_source_links = validate_links
    base.write = write

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    args = parser.parse_args()
    activate()
    result = campaign.respondent(args.case)
    trace = base.binder._events(campaign.RUN / (args.case + '.jsonl'))
    result['technical_failures'] = trace[-1]['failures']
    result['literal_site_adaptation'] = True
    print(json.dumps(result, ensure_ascii=False, indent=2))
