"""ADR 0013 : deux identités CLI fermées, vérifiées selon la fonction du reçu."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COMPANIONS = {'codex-code-mode-host.exe', 'codex-command-runner.exe', 'codex-windows-sandbox-setup.exe'}
MIGRATION = {'scripts/measurement_common.py', 'scripts/run_codex_smoke.py',
             'scripts/cli_toolchains.py', 'scripts/smoke-cli.json', 'scripts/toolchain-transition-0013.json'}
TRANSITION_FILES = (MIGRATION - {'scripts/toolchain-transition-0013.json'}) | {
    'scripts/assemble_release_evidence.py', 'scripts/human_resolution.py'}


def sha(path: Path) -> str:
    """SHA-256 en flux sur les binaires, sans transformation."""
    result = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1024 * 1024):
            result.update(block)
    return result.hexdigest()


def _pin(value: dict, smoke: bool) -> dict:
    if (not isinstance(value, dict) or not isinstance(value.get('version'), str)
            or re.fullmatch(r'codex-cli [^\s]+', value['version']) is None
            or re.fullmatch(r'[0-9a-f]{64}', str(value.get('sha256'))) is None):
        raise ValueError('CLI absente ou non épinglée')
    result = {k: value[k] for k in ('version', 'sha256')}
    if smoke:
        companions = value.get('companions_sha256')
        if (not isinstance(companions, dict) or set(companions) != COMPANIONS
                or any(re.fullmatch(r'[0-9a-f]{64}', str(v)) is None for v in companions.values())):
            raise ValueError('Compagnons smoke absents ou non épinglés')
        result['companions_sha256'] = dict(sorted(companions.items()))
    return result


def toolchains(root: Path = ROOT) -> dict:
    """Les deux verrous sont obligatoires ; aucun remplacement par la CLI du PATH."""
    try:
        campaign = json.loads((root / 'scripts/measurement-cli.json').read_bytes())['codex']
        smoke = json.loads((root / 'scripts/smoke-cli.json').read_bytes())['smoke_cli']
        return {'campaign_cli': _pin(campaign, False), 'smoke_cli': _pin(smoke, True)}
    except (OSError, KeyError, TypeError) as exc:
        raise ValueError('CLI absente ou non épinglée') from exc


def phase_pin(phase: str) -> dict:
    """Phase explicitement nommée, jamais déduite du SHA du reçu."""
    if phase not in {'campaign_cli', 'smoke_cli'}:
        raise ValueError('Phase CLI inconnue')
    return toolchains()[phase]


def verify_package(path: Path, phase: str) -> dict:
    """Vérifie le binaire et, pour smoke, tous les compagnons du même dossier."""
    expected = phase_pin(phase)
    if path.is_symlink() or not path.is_file() or sha(path) != expected['sha256']:
        raise ValueError('CLI différente du binaire de mesure épinglé')
    for name, fingerprint in expected.get('companions_sha256', {}).items():
        companion = path.with_name(name)
        if (companion.is_symlink() or not companion.is_file()
                or sha(companion) != fingerprint):
            raise ValueError('Compagnon smoke absent ou altéré : ' + name)
    return expected


def receipt_matches(origin: dict, phase: str, expected: dict) -> bool:
    """Campagne historique acceptée à son pin exact ; smoke exige son identité complète."""
    if origin.get('cli_sha256') != expected['sha256'] or origin.get('cli_version') != expected['version']:
        return False
    if phase == 'campaign_cli' and 'cli_phase' not in origin and 'cli_toolchain' not in origin:
        return True
    return origin.get('cli_phase') == phase and origin.get('cli_toolchain') == expected


def prove_toolchains(campaign: list[dict], reviews: list[dict], smoke: list[dict], declared: dict) -> dict:
    """Recalcule la propriété des deux CLI ; ne qualifie aucun autre aspect d'un run."""
    expected = toolchains()
    if declared != expected or not campaign or not reviews or not smoke:
        raise ValueError('Deux toolchains épinglées obligatoires et visibles')
    for phase, receipts in [('campaign_cli', campaign), ('campaign_cli', reviews), ('smoke_cli', smoke)]:
        if any(not receipt_matches(r, phase, expected[phase]) for r in receipts):
            raise ValueError('Reçu CLI différent de sa phase : ' + phase)
    return expected


def compatibility_files(root: Path, measured: dict, target: dict) -> set[str]:
    """Transition L14 -> ADR 0013 : liste fermée et hashes exacts, pas d'exemption générale."""
    old, current = measured['toolchain_sha256'], target['toolchain_sha256']
    if not any(old.get(n) != current.get(n) for n in MIGRATION):
        return set()
    try:
        path = root / 'scripts/toolchain-transition-0013.json'
        transition = json.loads(path.read_bytes())
        if (transition['adr'] != 'docs/adr/0013-cli-distinct-smoke.md'
                or measured['plugin_commit'] != transition['measurement_commit']
                or set(transition['target_files_sha256']) != TRANSITION_FILES
                or set(transition['source_files_sha256']) != {'scripts/measurement_common.py', 'scripts/run_codex_smoke.py'}):
            raise ValueError('Transition non autorisée')
        campaign_lock = 'scripts/measurement-cli.json'
        if not (old[campaign_lock] == current[campaign_lock] == transition['campaign_lock_sha256']
                == sha(root / campaign_lock)):
            raise ValueError('Verrou campagne modifié')
        for name, value in transition['source_files_sha256'].items():
            if old.get(name) != value:
                raise ValueError('Outillage source différent')
        for name, value in transition['target_files_sha256'].items():
            if current.get(name) != value or sha(root / name) != value:
                raise ValueError('Transition cible différente')
        if current.get('scripts/toolchain-transition-0013.json') != sha(path):
            raise ValueError('Manifeste de transition différent')
        if any(old.get(n) is not None for n in MIGRATION - {'scripts/measurement_common.py', 'scripts/run_codex_smoke.py'}):
            raise ValueError('Transition déjà présente dans la source')
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise ValueError('Protocole ou outillage mesuré différent : transition ADR 0013 refusée') from exc
    return set(MIGRATION)
