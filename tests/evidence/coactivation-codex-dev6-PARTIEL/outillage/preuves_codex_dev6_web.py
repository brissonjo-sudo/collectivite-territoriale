"""Enveloppe web Codex séparée : retours texte réels, provenance et nature bornées.

Le protocole natif autorise web__run sur les seuls hôtes du cas. La projection
historique WebFetch est adaptée explicitement, jamais présentée comme telle.
Une recherche/find/click ou une page de conseils ne devient pas texte primaire.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import preuves_codex_dev6 as native

BASE_SINGLE_RESULT = native.single_result
BASE_SOURCE_CALL = native.source_call
BASE_WRITE = native.write
BASE_SOURCE_LINKS = native.modules()[0].validate_source_links
CAPTURES = {}
CASE = None
READ_PROJECTION = {}

def safe_web_url(url, sources):
    """Exception bornée pour les chemins publics CNIL trop longs du filtre ancien."""
    existing = sources._safe_url(url)
    if existing:
        return existing
    if not isinstance(url, str) or any(ord(char) < 33 for char in url):
        return None
    try:
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.hostname != 'www.cnil.fr' or parsed.username or parsed.password or parsed.port not in (None, 443):
            return None
        approved_path = re.fullmatch(r'/(?:fr/)?reglement-europeen-protection-donnees(?:/chapitre[1-9][0-9]*)?/?', parsed.path)
        approved_path = approved_path or parsed.path in (
            '/fr/le-cadre-national/la-loi-informatique-et-libertes',
            '/fr/notifier-une-violation-de-donnees-personnelles',
            '/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles')
        return urlunsplit(('https', 'www.cnil.fr', parsed.path, '', '')) if approved_path else None
    except ValueError:
        return None

def blocks(text):
    pattern = re.compile(r'(?m)^([^\n]*) \((https://[^\n]+)\)\ncite(turn[0-9]+(?:view|search)[0-9]+)')
    matches = list(pattern.finditer(text))
    result = []
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.start():stop]
        source = re.search(r'Source:\s*(open|find|click)\(', body)
        total = re.search(r'Total lines:\s*([0-9]+)', body)
        result.append({'title': match[1], 'url': match[2], 'reference_id': match[3],
                       'operation': source[1] if source else 'search_query',
                       'total_lines': int(total[1]) if total else None, 'text': body})
    return result

def normative_document(url):
    parsed = urlsplit(url)
    if parsed.hostname == 'eur-lex.europa.eu':
        return bool(re.search(r'(?:/eli/reg/2016/679/|[?&]uri=CELEX(?::|%3A)(?:0?2016R0679))', url, re.I))
    return parsed.hostname == 'www.cnil.fr' and bool(re.fullmatch(r'/(?:fr/)?reglement-europeen-protection-donnees/chapitre[1-9][0-9]*', parsed.path.rstrip('/')))

def complete_article_excerpts(text):
    """Seulement article 33/34 réellement reçu entre deux titres, sans ligne manquante."""
    rows = [(int(match[1]), match[2]) for match in re.finditer(r'(?m)^L([0-9]+):[ \t]?(.*)$', text)]
    headers = [(index, int(match[1])) for index, (_, value) in enumerate(rows)
               if (match := re.fullmatch(r'\s*(?:#{1,6}\s*)?Article\s+([0-9]+)\s*(?:[-–—].*)?', value, re.I))]
    found = []
    for position, (start, number) in enumerate(headers):
        if number not in (33, 34) or position + 1 == len(headers):
            continue
        stop, next_number = headers[position + 1]
        segment = rows[start:stop]
        if next_number != number + 1 or len(segment) < 4 or any(segment[index + 1][0] != segment[index][0] + 1 for index in range(len(segment) - 1)):
            continue
        excerpt = '\n'.join('L' + str(line) + ': ' + value for line, value in segment)
        if len(excerpt) <= 12000:
            found.append({'number': number, 'excerpt': excerpt, 'first_line': segment[0][0], 'last_line': segment[-1][0]})
    return found

def evidence(capture, sources):
    call_id = capture['call_id']
    documents = []
    for page in capture['pages'][:8]:
        cleaned = sources.scrub_visible_text(page['text'])
        if re.search(r"not a robot|JavaScript is disabled|access denied|captcha", page['text'], re.I):
            documents.append({'nature': 'tool_summary', 'url': page['safe_url'], 'status': 'missing',
                              'reason': 'anti_robot_or_access_denied', 'excerpt': cleaned['text'][:12000],
                              'metadata': {'native_operation': page['operation'], 'native_reference_id': page['reference_id'],
                                           'total_lines': page['total_lines'], 'content_trust': 'untrusted_source_data'}})
            continue
        primary = (complete_article_excerpts(page['text']) if (page['operation'] == 'open'
                   or (page['operation'] == 'find' and page.get('prior_open_verified') is True))
                   and normative_document(page['url']) else [])
        primary = [article for article in primary if not sources.scrub_visible_text(article['excerpt'])['redacted']
                   and not sources.scrub_visible_text(article['excerpt'])['truncated']]
        if primary:
            for article in primary:
                documents.append({'nature': 'primary_text', 'url': page['safe_url'], 'status': 'available',
                                  'excerpt': article['excerpt'], 'metadata': {
                                      'native_operation': page['operation'], 'native_reference_id': page['reference_id'],
                                      'number': str(article['number']), 'first_line': article['first_line'], 'last_line': article['last_line'],
                                      'excerpt_complete_between_consecutive_article_headings': True,
                                      'full_document_received': False, 'excerpt_received_verbatim': True,
                                      'prior_open_verified': page.get('prior_open_verified', False),
                                      'applicable_at_as_of_date': None, 'legal_validity': None,
                                      'content_trust': 'untrusted_source_data'}})
        else:
            shortened = len(cleaned['text']) > 12000 or cleaned['truncated']
            documents.append({'nature': 'search_result' if page['operation'] == 'search_query' else 'tool_summary',
                              'url': page['safe_url'], 'status': 'truncated' if shortened else 'available',
                              'excerpt': cleaned['text'][:12000], 'metadata': {
                                  'native_operation': page['operation'], 'native_reference_id': page['reference_id'],
                                  'total_lines': page['total_lines'], 'redacted': cleaned['redacted'], 'truncated': shortened,
                                  'classification_basis': 'search/find/click or no complete normative article open attested',
                                  'content_trust': 'untrusted_source_data'}})
    if not documents:
        text = sources.scrub_visible_text(capture['text'])
        documents = [{'nature': 'tool_summary', 'status': 'available' if text['text'].strip() else 'missing',
                      'url': capture['effective_urls'][0], 'excerpt': text['text'][:12000],
                      'metadata': {'native_operation': 'unparsed', 'content_trust': 'untrusted_source_data',
                                   'truncated': len(text['text']) > 12000 or text['truncated'], 'redacted': text['redacted']}}]
    return {'type': 'source_evidence', 'tool': 'web__run', 'native_tool': 'web__run', 'call_id': call_id,
            'status': 'available' if any(doc['status'] in ('available', 'truncated') for doc in documents) else 'missing',
            'documents': documents, 'retrieved_at': capture['timestamp'], 'content_trust': 'untrusted_source_data',
            'native_web_adapter_sha256': native.binder._sha(Path(__file__)),
            'web_protocol_adaptation': 'real Codex search/open/find/click; authorized hosts only; no WebFetch claim'}

def prepare(identifier):
    global CASE
    _, CASE = native.case_and_number(identifier)
    if CASE['web_mode'] != 'official_source':
        raise native.binder.BindingError('Enveloppe web réservée aux cas official_source')
    number, _ = native.case_and_number(identifier)
    native_path, _ = native.discover(f'/root/repondant_codex_dev5_{number:02d}')
    events = native.binder._events(native_path)
    _, _, sources = native.modules()
    references = {}
    opened_documents = set()
    approved = set(CASE['official_source_hosts'])
    for event in events:
        payload = event.get('payload', {})
        script = payload.get('input', payload.get('arguments'))
        if payload.get('type') not in ('custom_tool_call', 'function_call') or not isinstance(script, str) or 'tools.web__run(' not in script:
            continue
        tool, args = BASE_SOURCE_CALL(script)
        if tool != 'web__run' or set(args) - {'open', 'find', 'click', 'search_query', 'response_length'}:
            raise native.binder.BindingError('Opération web hors adaptation bornée')
        requested_urls = []
        for operation in ('open', 'find', 'click'):
            for request in args.get(operation, []):
                ref = request.get('ref_id')
                url = ref if isinstance(ref, str) and ref.startswith('https://') else references.get(ref)
                if not url or urlsplit(url).hostname not in approved or safe_web_url(url, sources) is None:
                    raise native.binder.BindingError('Référence web non liée à un hôte autorisé')
                requested_urls.append(url)
        for query in args.get('search_query', []):
            domains = query.get('domains')
            if not isinstance(domains, list) or not domains or any(domain not in approved for domain in domains):
                raise native.binder.BindingError('Recherche web sans filtre exact d’hôtes autorisés')
        output, parts = native.outputs(events, event)
        if len(parts) != 2 or not parts[0].startswith('Script completed\n'):
            raise native.binder.BindingError('Retour web incomplet')
        text = parts[1]
        pages = blocks(text)
        allowed_pages = []
        for page in pages:
            safe_url = safe_web_url(page['url'], sources)
            if not safe_url or urlsplit(page['url']).hostname not in approved:
                continue
            page['safe_url'] = safe_url
            page['prior_open_verified'] = safe_url in opened_documents
            references[page['reference_id']] = page['url']
            allowed_pages.append(page)
        for request in args.get('open', []):
            ref = request.get('ref_id')
            url = ref if isinstance(ref, str) and ref.startswith('https://') else references.get(ref)
            canonical = safe_web_url(url, sources) if url else None
            if canonical and normative_document(url):
                opened_documents.add(canonical)
        effective_urls = [page['safe_url'] for page in allowed_pages] or requested_urls
        if not effective_urls:
            # Empty filtered search is still a real call, no primary text inferred.
            domain = args['search_query'][0]['domains'][0]
            effective_urls = ['https://' + domain + '/']
        capture = {'call_id': payload['call_id'], 'timestamp': output['timestamp'], 'native_tool': tool,
                   'actual_arguments': args, 'pages': allowed_pages, 'effective_urls': effective_urls, 'text': text}
        CAPTURES[payload['call_id']] = capture
        READ_PROJECTION[native.binder._canonical(args)] = {'open': [{'ref_id': url} for url in effective_urls]}

def single_result(parts):
    try:
        return BASE_SINGLE_RESULT(parts)
    except (ValueError, native.binder.BindingError):
        if len(parts) == 2 and parts[0].startswith('Script completed\n') and any(parts[1] == c['text'] for c in CAPTURES.values()):
            return {'native_web_text_result_captured': True}
        raise

def source_call(script):
    tool, args = BASE_SOURCE_CALL(script)
    if tool == 'web__run':
        normalized = READ_PROJECTION.get(native.binder._canonical(args))
        if normalized is None:
            raise native.binder.BindingError('Appel web non capturé ou non autorisé')
        return tool, normalized
    return tool, args

def validate_links(events):
    _, transport, sources = native.modules()
    for index, event in enumerate(events):
        capture = CAPTURES.get(event.get('call_id'))
        if capture is None:
            continue
        if event['type'] == 'official_source_call':
            event.update(native_arguments=capture['actual_arguments'],
                         web_protocol_adaptation='authorized Codex search/open/find/click',
                         succeeded=True, timestamp_basis='actual native call and return',
                         result_timestamp=capture['timestamp'])
        elif event['type'] == 'source_evidence':
            events[index] = {**evidence(capture, sources), 'event_id': event['event_id']}
    final = events[-1]
    if final.get('type') == 'technical_assessment':
        final['observables'] = transport.observable_checks(events, CASE)
        final['failures'] = native.codex_failures(events[:-1], CASE)
        final['status'] = 'failed' if final['failures'] else 'passed'
        final['web_protocol_adaptation'] = 'Codex authorized host operations; original rubric unchanged'
    return BASE_SOURCE_LINKS(events)

def write(path, value):
    if path.name == 'execution-repondant.json':
        _, _, sources = native.modules()
        capture_path = path.parent / 'capture-web-assainie.jsonl'
        values = []
        for capture in CAPTURES.values():
            cleaned = sources.scrub_visible_text(capture['text'])
            values.append({'call_id': capture['call_id'], 'native_tool': capture['native_tool'],
                           'timestamp': capture['timestamp'], 'actual_arguments': capture['actual_arguments'],
                           'text': cleaned['text'], 'text_redacted': cleaned['redacted'], 'text_truncated': cleaned['truncated'],
                           'content_trust': 'untrusted_source_data'})
        native.binder._write(capture_path, ''.join(json.dumps(item, ensure_ascii=False) + '\n' for item in values))
        value = dict(value)
        value.update(native_web_adapter_sha256=native.binder._sha(Path(__file__)),
                     native_web_capture_sha256=native.binder._sha(capture_path), actual_web_calls=len(values),
                     web_protocol_adaptation='native text outputs captured; only official hosts; no summary promoted')
    return BASE_WRITE(path, value)

def activate(identifier):
    prepare(identifier)
    native.single_result = single_result
    native.source_call = source_call
    native.write = write
    native.modules()[0].validate_source_links = validate_links

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    args = parser.parse_args()
    activate(args.case)
    print(json.dumps(native.bind_respondent(args.case), ensure_ascii=False, indent=2))
