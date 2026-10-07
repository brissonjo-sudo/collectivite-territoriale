"""Grammaire dev.6 déclarée avant tout export, sans évaluation de scripts."""
import hashlib
import re
from pathlib import Path
import preuves_codex_dev6 as base

BASE_SOURCE = base.source_call
BASE_ARGUMENTS = base.binder._arguments

def strip_capacity(script: str) -> str:
    if not isinstance(script, str):
        raise base.binder.BindingError('Script non textuel')
    if not script.startswith('// @exec:'):
        return script
    match = re.match(r'^// @exec: ([^\r\n]+)\r?\n', script)
    if not match:
        raise base.binder.BindingError('Directive de capacité mal formée')
    value = base.binder._json(match[1])
    if (not isinstance(value, dict) or set(value) != {'max_output_tokens'}
            or type(value['max_output_tokens']) is not int or value['max_output_tokens'] != 55000):
        raise base.binder.BindingError('Seule capacité 55000 autorisée')
    return script[match.end():]

def source(script: str) -> tuple[str, dict]:
    tool, arguments = BASE_SOURCE(strip_capacity(script))
    if tool != 'web__run' and not tool.startswith('mcp__droit_francais__'):
        raise base.binder.BindingError('Directive source hors outils autorisés')
    return tool, arguments

def arguments(script: str, tool: str) -> object:
    if isinstance(script, str) and script.startswith('// @exec:'):
        if tool != 'apply_patch':
            raise base.binder.BindingError('Directive facultative hors patch littéral')
        script = strip_capacity(script)
    return BASE_ARGUMENTS(script, tool)

def activate() -> None:
    base.source_call = source
    base.binder._arguments = arguments
    import preuves_codex_dev6_web as web
    web.BASE_SOURCE_CALL = source

def fingerprint() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
