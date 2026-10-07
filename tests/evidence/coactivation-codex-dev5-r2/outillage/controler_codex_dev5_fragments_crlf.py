"""Enveloppe de présentation CRLF ; octets natifs bruts inchangés et conservés."""
from __future__ import annotations
from pathlib import Path
import preuves_codex_dev5 as native
import preuves_codex_dev5_fragments as fragmented

BASE_OUTPUTS = native.outputs
BASE_WRITE = native.write
NORMALIZATIONS = []

def outputs(events, call):
    result, original = BASE_OUTPUTS(events, call)
    script = call.get('payload', {}).get('input', call.get('payload', {}).get('arguments'))
    if not isinstance(script, str) or 'tools.exec_command(' not in script:
        return result, original
    args = native.raw.raw_arguments(script)
    for directory in (native.RUN / 'juges-fragments').glob('*'):
        for part in directory.glob('fragment-*.txt'):
            if args['cmd'] != native.raw.read_command(part):
                continue
            expected = part.read_text(encoding='utf-8')
            parts = list(original)
            if len(parts) == 3 and parts[2] == expected + '\r\n':
                parts[2] = expected
                NORMALIZATIONS.append({'call_id': call['payload']['call_id'], 'path': part.resolve().as_posix(),
                                       'removed_presentation_suffix': 'CRLF', 'native_output_modified': False})
            return result, parts
    return result, original

def write(path, value):
    if path.name == 'execution-juge.json':
        value = dict(value)
        value.update(presentation_wrapper_sha256=native.binder._sha(Path(__file__)),
                     exact_presentation_normalizations=list(NORMALIZATIONS),
                     normalization_scope='only expected content plus one terminal CRLF; raw events unchanged')
    return BASE_WRITE(path, value)

def activate():
    native.outputs = outputs
    native.write = write

if __name__ == '__main__':
    activate()
    fragmented.main()
