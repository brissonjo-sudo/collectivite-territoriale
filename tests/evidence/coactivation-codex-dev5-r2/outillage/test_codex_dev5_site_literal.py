"""Tests bornés du filtre site littéral, sans nouvelle requête documentaire."""
import copy
import json
import unittest
from pathlib import Path
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign
import controler_codex_dev5_r2_site_literal as site

class SiteLiteralTests(unittest.TestCase):
    def setUp(self):
        self.approved = {'eur-lex.europa.eu', 'www.cnil.fr'}

    def test_exact_sites_accepted(self):
        self.assertEqual(site.literal_site_host('site:www.cnil.fr "Article 33" "Article 34"', self.approved), 'www.cnil.fr')
        self.assertEqual(site.literal_site_host('site:eur-lex.europa.eu "02016R0679" "20160504"', self.approved), 'eur-lex.europa.eu')

    def test_derived_domains_do_not_mutate_actual_arguments(self):
        actual = {'q': 'site:www.cnil.fr "Article 33"'}
        original = copy.deepcopy(actual)
        projected, basis = site.query_for_validation(actual, self.approved)
        self.assertEqual(actual, original)
        self.assertNotIn('domains', actual)
        self.assertEqual(projected['domains'], ['www.cnil.fr'])
        self.assertEqual(basis['basis'], 'literal_site')

    def test_alias_and_fake_host_refused(self):
        for query in ('site:cnil.fr Article', 'site:www.cnil.fr.evil.invalid Article', 'site:WWW.CNIL.FR Article'):
            with self.subTest(query=query), self.assertRaises(base.binder.BindingError):
                site.literal_site_host(query, self.approved)

    def test_multiple_sites_refused(self):
        for query in ('site:www.cnil.fr Article site:eur-lex.europa.eu', 'site:www.cnil.fr Article -site:evil.invalid'):
            with self.subTest(query=query), self.assertRaises(base.binder.BindingError):
                site.literal_site_host(query, self.approved)

    def test_or_and_unfiltered_queries_refused(self):
        for query in ('Article 33 CNIL', ' "site:www.cnil.fr" Article', 'site:www.cnil.fr Article OR autre', 'site:www.cnil.fr | autre'):
            with self.subTest(query=query), self.assertRaises(base.binder.BindingError):
                site.literal_site_host(query, self.approved)

    def test_url_other_host_and_injection_refused(self):
        for query in ('site:www.cnil.fr https://evil.invalid', 'site:www.cnil.fr evil.invalid Article',
                      'site:www.cnil.fr Article; commande', 'site:www.cnil.fr $(commande)',
                      'site:www.cnil.fr `commande`', 'site:www.cnil.fr Article\nOR autre'):
            with self.subTest(query=query), self.assertRaises(base.binder.BindingError):
                site.literal_site_host(query, self.approved)

    def test_explicit_domain_validation_still_strict(self):
        _, basis = site.query_for_validation({'q': 'Article', 'domains': ['www.cnil.fr']}, self.approved)
        self.assertEqual(basis['basis'], 'explicit_domains')
        for domains in ([], ['cnil.fr'], ['www.cnil.fr', 'evil.invalid'], 'www.cnil.fr'):
            with self.assertRaises(base.binder.BindingError):
                site.query_for_validation({'q': 'Article', 'domains': domains}, self.approved)

    def test_unknown_unauthorized_source_never_primary(self):
        previous = dict(site.FILTERS)
        try:
            site.FILTERS['bad_call'] = {'scope_valid': False, 'scope_failures': ['outside'], 'query_filters': []}
            capture = {'call_id': 'bad_call', 'timestamp': '2026-10-07T20:00:00Z'}
            result = site.evidence(capture, base.modules()[2])
            self.assertEqual(result['status'], 'missing')
            self.assertEqual(result['documents'], [])
            self.assertEqual(result['reason'], 'native_web_call_outside_authorized_scope')
        finally:
            site.FILTERS.clear()
            site.FILTERS.update(previous)

    def test_actual_case03_original_arguments_conserved(self):
        trace = base.binder._events(campaign.RUN / 'plugin-violation-donnees.jsonl')
        captures = base.binder._events(campaign.RUN / 'plugin-violation-donnees/liaison/capture-web-assainie.jsonl')
        matching = [c for c in captures if c['actual_arguments'].get('search_query')
                    and any(q.get('q', '').startswith('site:') for q in c['actual_arguments']['search_query'])]
        self.assertEqual(len(matching), 1)
        self.assertTrue(all('domains' not in q for q in matching[0]['actual_arguments']['search_query']))
        source = next(e for e in trace if e['type'] == 'source_evidence' and e.get('call_id') == matching[0]['call_id'])
        self.assertEqual([v['basis'] for v in source['domain_filter_validation']['query_filters']], ['literal_site', 'literal_site'])
        self.assertFalse(any(d['nature'] == 'primary_text' for d in source['documents']))

    def test_pdf_remains_unproven_not_invented(self):
        trace = base.binder._events(campaign.RUN / 'plugin-violation-donnees.jsonl')
        pdfs = [d for e in trace if e['type'] == 'source_evidence' for d in e.get('documents', [])
                if '/PDF/' in d.get('url', '')]
        self.assertTrue(pdfs)
        self.assertTrue(all(d['nature'] != 'primary_text' for d in pdfs))

    def test_exception_cnil_path_is_exact(self):
        sources = base.modules()[2]
        url = 'https://www.cnil.fr/fr/violations-de-donnees-personnelles-les-regles-suivre?tracking=1'
        self.assertEqual(site.safe_url(url, sources), url.split('?')[0])
        self.assertIsNone(site.safe_url(url.replace('www.cnil.fr/', 'www.cnil.fr.evil.invalid/'), sources))
        self.assertIsNone(site.safe_url(url.replace('https://', 'https://user:password@'), sources))

    def test_outside_scope_preserves_trace_and_fails_technical(self):
        events = copy.deepcopy(base.binder._events(campaign.RUN / 'plugin-violation-donnees.jsonl'))
        call = next(event for event in events if event['type'] == 'official_source_call')
        old_case, old_filters = site.CASE, dict(site.FILTERS)
        try:
            site.CASE = base.case_and_number('plugin-violation-donnees')[1]
            site.FILTERS[call['call_id']] = {'scope_valid': False, 'scope_failures': ['native_web_reference_outside_authorized_scope'], 'query_filters': []}
            source = next(event for event in events if event['type'] == 'source_evidence' and event['call_id'] == call['call_id'])
            source.update(status='missing', documents=[])
            site.validate_links(events)
            self.assertEqual(events[-1]['status'], 'failed')
            self.assertIn('unexpected_tool_call', events[-1]['failures'])
            self.assertTrue(any(event['type'] == 'assistant_text' for event in events))
            self.assertTrue(any(event.get('full_runtime_context_verified') is True for event in events))
            self.assertFalse(call['succeeded'])
            self.assertEqual(source['documents'], [])
        finally:
            site.CASE = old_case
            site.FILTERS.clear()
            site.FILTERS.update(old_filters)

if __name__ == '__main__':
    unittest.main()
