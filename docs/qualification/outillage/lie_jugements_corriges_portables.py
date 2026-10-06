"""Adaptateur de chemins pour les nouveaux juges, sans modifier le lieur natif."""
from pathlib import Path
import json

import lie_jugements_corriges as binder


def read_command(path: Path) -> str:
    """Utilise une graphie Windows acceptée qui évite les échappements JS."""
    return "Get-Content -LiteralPath '" + path.resolve().as_posix().replace("'", "''") + "' -Raw"


original_native_proof = binder.native_proof
original_arguments = binder._arguments
READ_PRAGMA = '// @exec: {"max_output_tokens": 55000}\n'


def arguments(script, tool):
    """Autorise seulement le plafond de sortie explicite d'une lecture fermée."""
    if tool == 'exec_command' and script.startswith(READ_PRAGMA):
        script = script[len(READ_PRAGMA):]
    return original_arguments(script, tool)


def export_packet(candidate, response, destination):
    """Fige le plafond externe, nécessaire pour lire les grands paquets complets."""
    result = binder.export_packet(candidate, response, destination)
    prompt = Path(result['prompt'])
    text = prompt.read_text(encoding='utf-8')
    if text.count('```javascript\n') != 1:
        raise ValueError('Lecture du protocole absente ou ambiguë')
    prompt.write_text(text.replace('```javascript\n', '```javascript\n' + READ_PRAGMA, 1), encoding='utf-8', newline='\n')
    metadata = Path(result['export'])
    value = binder._json(metadata.read_text(encoding='utf-8'))
    value.update(prompt_sha256=binder._sha(prompt), external_read_output_tokens=55000,
        portable_adapter_sha256=binder._sha(Path(__file__)))
    metadata.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return result


def native_proof(*args, **kwargs):
    """Conserve tous les contrôles et déclare la graphie exacte mesurée."""
    proof, events = original_native_proof(*args, **kwargs)
    proof['exact_read_path_format'] = 'absolute_posix'
    proof['portable_adapter_sha256'] = binder._sha(Path(__file__))
    proof['initial_message_verified'] = False
    return proof, events


binder._read_command = read_command
binder._arguments = arguments
binder.native_proof = native_proof


if __name__ == '__main__':
    raise SystemExit(binder.main())
