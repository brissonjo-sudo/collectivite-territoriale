"""Enveloppe séparée pour la directive native de capacité des retours source."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import preuves_codex_dev5 as base
import campagne_codex_dev5_r2 as campaign
import preuves_codex_dev5_web as web
import controler_codex_dev5_r2_site_literal as site
import controler_codex_dev5_r2_mcp_tronque as mcp

BASE_PARSE = base.source_call
PRAGMAS = []

def parse(script):
    if script.startswith('// @exec:'):
        match = re.match(r'^// @exec: ([^\r\n]+)\r?\n', script)
        if not match:
            raise base.binder.BindingError('Directive source mal formée')
        value = base.binder._json(match[1])
        if (not isinstance(value, dict) or set(value) != {'max_output_tokens'}
                or type(value['max_output_tokens']) is not int or value['max_output_tokens'] != 55000):
            raise base.binder.BindingError('Directive source non autorisée')
        return BASE_PARSE(script[match.end():])
    return BASE_PARSE(script)

def collect(native):
    values = []
    for event in native:
        payload = event.get('payload', {})
        script = payload.get('input', payload.get('arguments', ''))
        if payload.get('type') not in ('custom_tool_call', 'function_call') or not isinstance(script, str):
            continue
        if 'tools.mcp__droit_francais__' not in script and 'tools.web__run(' not in script:
            continue
        parse(script)
        if script.startswith('// @exec:'):
            values.append({'call_id': payload['call_id'], 'max_output_tokens': 55000,
                           'native_script_sha256': hashlib.sha256(script.encode('utf-8')).hexdigest()})
    return values

def activate_parser():
    base.source_call = parse
    web.BASE_SOURCE_CALL = parse
    site.BASE_PARSE = parse

def bind(identifier):
    campaign.configure()
    number, case = base.case_and_number(identifier)
    native = base.binder._events(campaign.BASE_DISCOVER(f'/root/repondant_codex_dev5_r2_{number:02d}')[0])
    PRAGMAS[:] = collect(native)
    if not PRAGMAS:
        raise base.binder.BindingError('Aucune directive source réelle à adapter')
    activate_parser()
    if case['web_mode'] == 'official_source':
        site.activate()
    if case['mcp_mode'] == 'required':
        mcp.prepare(identifier)
        if mcp.CAPTURES:
            mcp.BASE_WRITE = base.write
            mcp.activate(identifier)
    previous_write = base.write
    def write(path, value):
        if path.name == 'execution-repondant.json':
            value = dict(value)
            value.update(source_pragma_wrapper_sha256=base.binder._sha(Path(__file__)),
                         native_source_pragmas=list(PRAGMAS),
                         source_pragma_scope='Only max_output_tokens=55000; original native scripts and arguments preserved.')
        return previous_write(path, value)
    base.write = write
    return campaign.respondent(identifier)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    args = parser.parse_args()
    print(json.dumps(bind(args.case), ensure_ascii=False, indent=2))
