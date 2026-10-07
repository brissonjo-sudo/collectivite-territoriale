"""Audit distinct : initialiser la grammaire préexportée avant le filtre web."""
import hashlib
import json
from pathlib import Path
import audit_natif_codex_dev6_final as original
import controler_codex_dev6_r1_site_literal as site
import grammaire_codex_dev6 as grammar


def audit(complete: bool = False) -> dict:
    """Ne changer que la référence de parseur capturée avant configure()."""
    manifest = json.loads((original.campaign.RUN / 'manifest.json').read_bytes())
    assert grammar.fingerprint() == manifest['grammar_sha256']
    previous = site.BASE_PARSE
    try:
        site.BASE_PARSE = grammar.source
        result = original.audit(complete)
    finally:
        site.BASE_PARSE = previous
    result.update(initial_audit_script_sha256=result['audit_script_sha256'],
                  audit_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  initialization_repair={'scope': 'cold-import parser reference only',
                                         'predeclared_grammar_sha256': manifest['grammar_sha256'],
                                         'native_arguments_changed': False, 'judge_results_changed': False,
                                         'grammar_extended_after_measurement': False})
    return result
