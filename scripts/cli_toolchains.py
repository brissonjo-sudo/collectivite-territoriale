"""ADR 0013 : deux identités CLI fermées, vérifiées selon la fonction du reçu."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
COMPANIONS = {'codex-code-mode-host.exe', 'codex-command-runner.exe', 'codex-windows-sandbox-setup.exe'}
MIGRATION = {'scripts/measurement_common.py', 'scripts/run_codex_smoke.py',
             'scripts/cli_toolchains.py', 'scripts/smoke-cli.json', 'scripts/toolchain-transition-0013.json'}
TRANSITION_FILES = (MIGRATION - {'scripts/toolchain-transition-0013.json'}) | {
    'scripts/assemble_release_evidence.py', 'scripts/human_resolution.py'}
MEASUREMENT_D = '13b4e1e537e5a8097a004ee913abcc9d079114a7'
# À renseigner en H2 avec le seul commit H1 effectivement mesuré ; None refuse v3.
MEASUREMENT_140: str | None = None
MEASUREMENT_140_V4: str | None = None
CYCLE_V4 = ('scripts/cas-plugin-cycle-v4.json', 'be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24')
TRANSITION_140_V4 = 'scripts/toolchain-transition-0028.json'
MIGRATION_140_V4 = {'scripts/cli_toolchains.py', 'scripts/measurement-cli.json', TRANSITION_140_V4}
ADR_140_V4 = 'docs/adr/0028-contrat-v4-et-tentative-d.md'
CYCLE_CONTRACTS = {
    '1.3.0': ('scripts/cas-plugin-cycle-v2.json',
              '65593a1c46bd31b403c5b83344f14951cbc3455f456eefcde2c6853fa68a9478'),
    '1.4.0': ('scripts/cas-plugin-cycle-v3.json',
              'deb0d39efc93a24b16444922dbafddbb6570801a67e21ca23d612343ba471e89'),
}
TRANSITION_D = 'scripts/toolchain-transition-0017.json'
MIGRATION_D = {'scripts/measurement-cli.json', 'scripts/cli_toolchains.py',
    'scripts/measurement_common.py', 'scripts/human_resolution.py',
    'scripts/assemble_release_evidence.py', 'scripts/run_codex_smoke.py',
    'scripts/qualify_distribution.py', 'scripts/public_projection.py', TRANSITION_D, 'CHANGELOG.md',
    '.gitattributes'}
TRANSITION_140 = 'scripts/toolchain-transition-0026.json'
MIGRATION_140 = {'scripts/cli_toolchains.py', 'scripts/measurement-cli.json', TRANSITION_140}
ADR_140 = 'docs/adr/0026-transition-fermee-1-4-0.md'
CAMPAIGN_140_CLI = {
    'version': 'codex-cli 0.163.0-alpha.10.2',
    'sha256': 'f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312',
    'companions_sha256': {
        'codex-code-mode-host.exe': '3b6a9179a4da17fa5fc6948219cd61486dc3b534c683838076d8c61bd311c68e',
        'codex-command-runner.exe': 'ce80b56a2f37f808815fde33cceb97ac858ceecde296425ad3860f0f37fb4877',
        'codex-windows-sandbox-setup.exe': 'c4da812016cbfb92d9a62791f78460c59e9662faadb0a2720d3aa5d0535b80bd',
    },
}


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


def measurement_contract(root: Path, commit: str | None) -> dict | None:
    """Contrat choisi par un commit explicitement autorisé, jamais par un reçu."""
    if MEASUREMENT_140_V4 is not None and commit == MEASUREMENT_140_V4:
        prepared_cycle_v4(root)
        value = json.loads((root / 'scripts/measurement-cli.json').read_bytes()).get('campaign_measurements', {}).get(commit)
        if value != {'campaign_cli': CAMPAIGN_140_CLI, 'case_contract_sha256': CYCLE_V4[1]}:
            raise ValueError('Mesure v4 sans contrat CLI/cas épinglé')
        return {'campaign_cli': _pin(value['campaign_cli'], True), 'case_contract_sha256': CYCLE_V4[1]}
    if commit == MEASUREMENT_D:
        version = '1.3.0'
    elif MEASUREMENT_140 is not None and commit == MEASUREMENT_140:
        version = '1.4.0'
        prepared_cycle(root)
    else:
        return None
    value = json.loads((root / 'scripts/measurement-cli.json').read_bytes()).get('campaign_measurements', {}).get(commit)
    if (not isinstance(value, dict) or set(value) != {'campaign_cli', 'case_contract_sha256'}
            or value['case_contract_sha256'] != CYCLE_CONTRACTS[version][1]):
        raise ValueError('Mesure sans contrat CLI/cas épinglé : ' + version)
    if version == '1.4.0' and value['campaign_cli'] != CAMPAIGN_140_CLI:
        raise ValueError('CLI de mesure 1.4.0 différente du verrou exact')
    return {'campaign_cli': _pin(value['campaign_cli'], True),
            'case_contract_sha256': value['case_contract_sha256']}


def prepared_cycle(root: Path) -> str:
    """V3 préparé à empreinte fermée, y compris avant la liaison du gel."""
    value = json.loads((root / 'scripts/measurement-cli.json').read_bytes()).get('prepared_cycles', {}).get('1.4.0')
    name, fingerprint = CYCLE_CONTRACTS['1.4.0']
    if (value != {'case_contract_file': name, 'case_contract_sha256': fingerprint,
                 'measurement_commit': MEASUREMENT_140} or sha(root / name) != fingerprint):
        raise ValueError('Contrat de cycle v3 absent ou divergent')
    return name


def contract_file(contract: dict) -> str:
    """Aucun chemin ni hash fourni par une preuve ne choisit un contrat."""
    for name, fingerprint in (*CYCLE_CONTRACTS.values(), CYCLE_V4):
        if contract['case_contract_sha256'] == fingerprint:
            return name
    raise ValueError('Contrat de cycle inconnu')


def require_cycle_version(contract: dict | None, version: str) -> None:
    """Une mesure 1.4.0 exige le commit v3 lié ; 1.3.0 conserve v2."""
    if contract is not None and contract.get('case_contract_sha256') == CYCLE_V4[1]:
        if version != '1.4.0':
            raise ValueError('Contrat de cycle v4 réservé à la mesure 1.4.0')
        return
    if version == '1.4.0' and (contract is None
            or contract['case_contract_sha256'] != CYCLE_CONTRACTS[version][1]):
        raise ValueError('Mesure 1.4.0 sans commit lié au contrat de cycle v3')
    if contract is not None and contract_file(contract) == CYCLE_CONTRACTS['1.4.0'][0] and version != '1.4.0':
        raise ValueError('Contrat de cycle v3 réservé à la mesure 1.4.0')
    if contract is not None and contract_file(contract) == CYCLE_CONTRACTS['1.3.0'][0] and version != '1.3.0':
        raise ValueError('Contrat de cycle v2 réservé à la mesure 1.3.0')


def toolchains(root: Path = ROOT, measurement_commit: str | None = None) -> dict:
    """Les deux verrous sont obligatoires ; aucun remplacement par la CLI du PATH."""
    try:
        campaign = json.loads((root / 'scripts/measurement-cli.json').read_bytes())['codex']
        smoke = json.loads((root / 'scripts/smoke-cli.json').read_bytes())['smoke_cli']
        contract = measurement_contract(root, measurement_commit)
        return {'campaign_cli': contract['campaign_cli'] if contract else _pin(campaign, False),
                'smoke_cli': _pin(smoke, True)}
    except (OSError, KeyError, TypeError) as exc:
        raise ValueError('CLI absente ou non épinglée') from exc


def phase_pin(phase: str, measurement_commit: str | None = None) -> dict:
    """Phase explicitement nommée, jamais déduite du SHA du reçu."""
    if phase not in {'campaign_cli', 'smoke_cli'}:
        raise ValueError('Phase CLI inconnue')
    return toolchains(measurement_commit=measurement_commit)[phase]


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
    if (phase == 'campaign_cli' and not expected.get('companions_sha256')
            and 'cli_phase' not in origin and 'cli_toolchain' not in origin):
        return True
    return origin.get('cli_phase') == phase and origin.get('cli_toolchain') == expected


def prove_toolchains(campaign: list[dict], reviews: list[dict], smoke: list[dict], declared: dict,
                     measurement_commit: str | None = None, *, root: Path = ROOT) -> dict:
    """Recalcule la propriété des deux CLI ; ne qualifie aucun autre aspect d'un run."""
    expected = toolchains(root, measurement_commit=measurement_commit)
    if declared != expected or not campaign or not reviews or not smoke:
        raise ValueError('Deux toolchains épinglées obligatoires et visibles')
    for phase, receipts in [('campaign_cli', campaign), ('campaign_cli', reviews), ('smoke_cli', smoke)]:
        if any(not receipt_matches(r, phase, expected[phase]) for r in receipts):
            raise ValueError('Reçu CLI différent de sa phase : ' + phase)
    return expected


def transition_140_files(root: Path, measured: dict, target: dict) -> set[str]:
    """H1→H2 fermé sur trois chemins et les seules données de liaison décidées."""
    try:
        commit = MEASUREMENT_140
        if (not isinstance(commit, str) or re.fullmatch(r'[0-9a-f]{40}', commit) is None
                or commit == MEASUREMENT_D or measured.get('plugin_commit') != commit):
            raise ValueError('SHA H1 non autorisé')
        old, current = measured['toolchain_sha256'], target['toolchain_sha256']
        if not isinstance(old, dict) or not isinstance(current, dict):
            raise ValueError('Inventaire de transition 1.4.0 invalide')
        transition = json.loads((root / TRANSITION_140).read_bytes())
        names = MIGRATION_140 - {TRANSITION_140}
        if (not isinstance(transition, dict)
                or set(transition) != {'adr', 'measurement_commit', 'case_contract_sha256', 'campaign_cli',
                                'source_files_sha256', 'target_files_sha256'}
                or transition['adr'] != ADR_140 or transition['measurement_commit'] != commit
                or transition['case_contract_sha256'] != CYCLE_CONTRACTS['1.4.0'][1]
                or transition['campaign_cli'] != CAMPAIGN_140_CLI
                or not isinstance(transition['source_files_sha256'], dict)
                or not isinstance(transition['target_files_sha256'], dict)
                or set(transition['source_files_sha256']) != names
                or set(transition['target_files_sha256']) != names
                or any(re.fullmatch(r'[0-9a-f]{64}', str(value)) is None
                       for key in ('source_files_sha256', 'target_files_sha256')
                       for value in transition[key].values())
                or current.get(TRANSITION_140) != sha(root / TRANSITION_140)):
            raise ValueError('Manifeste 1.4.0 non fermé ou divergent')
        if any(old.get(name) != current.get(name) for name in set(old) | set(current)
               if name not in MIGRATION_140):
            raise ValueError('Fichier supplémentaire dans la transition 1.4.0')

        def source(name: str) -> bytes:
            return subprocess.check_output(['git', '-c', 'safe.directory=' + str(root),
                'show', commit + ':' + name], cwd=root, stderr=subprocess.PIPE)

        source_bytes = {name: source(name) for name in names}
        for name in names:
            source_hash = hashlib.sha256(source_bytes[name]).hexdigest()
            if (old.get(name) != source_hash or source_hash != transition['source_files_sha256'][name]
                    or current.get(name) != transition['target_files_sha256'][name]
                    or sha(root / name) != transition['target_files_sha256'][name]):
                raise ValueError('Empreinte source ou cible 1.4.0 divergente')
        raw_manifest = source(TRANSITION_140)
        expected_open = {**transition, 'measurement_commit': None,
                         'source_files_sha256': {name: None for name in names},
                         'target_files_sha256': {name: None for name in names}}
        if (old.get(TRANSITION_140) != hashlib.sha256(raw_manifest).hexdigest()
                or json.loads(raw_manifest) != expected_open):
            raise ValueError('Manifeste H1 différent de la préparation non fermée')
        if target.get('plugin_commit') is not None:
            destination = target['plugin_commit']
            if not isinstance(destination, str) or re.fullmatch(r'[0-9a-f]{40}', destination) is None:
                raise ValueError('SHA cible absent ou invalide')
            changed = subprocess.check_output(['git', '-c', 'safe.directory=' + str(root),
                'diff', '--name-only', commit, destination], cwd=root, stderr=subprocess.PIPE).decode().splitlines()
            if any(name not in MIGRATION_140 for name in changed):
                raise ValueError('Fichier Git supplémentaire dans la transition 1.4.0')
        for name, fingerprint in CYCLE_CONTRACTS.values():
            if (old.get(name) != fingerprint or current.get(name) != fingerprint
                    or sha(root / name) != fingerprint
                    or hashlib.sha256(source(name)).hexdigest() != fingerprint):
                raise ValueError('Contrat v2 ou v3 altéré')
        assignment = b'MEASUREMENT_140: str | None = None\n'
        raw_cli = source_bytes['scripts/cli_toolchains.py']
        expected_cli = raw_cli.replace(assignment, ("MEASUREMENT_140: str | None = '" + commit + "'\n").encode(), 1)
        if raw_cli.count(assignment) != 1 or (root / 'scripts/cli_toolchains.py').read_bytes() != expected_cli:
            raise ValueError('Modification du lecteur autre que la liaison H1')
        config = json.loads(source_bytes['scripts/measurement-cli.json'])
        name, fingerprint = CYCLE_CONTRACTS['1.4.0']
        if (config['prepared_cycles']['1.4.0'] != {'case_contract_file': name,
                'case_contract_sha256': fingerprint, 'measurement_commit': None}
                or commit in config['campaign_measurements']):
            raise ValueError('Verrou H1 déjà lié ou différent de la préparation')
        expected_config = copy.deepcopy(config)
        expected_config['prepared_cycles']['1.4.0']['measurement_commit'] = commit
        expected_config['campaign_measurements'][commit] = {
            'case_contract_sha256': fingerprint, 'campaign_cli': CAMPAIGN_140_CLI}
        if json.loads((root / 'scripts/measurement-cli.json').read_bytes()) != expected_config:
            raise ValueError('Modification du verrou autre que la liaison H1')
        contract = measurement_contract(root, commit)
        if contract != {'case_contract_sha256': fingerprint, 'campaign_cli': CAMPAIGN_140_CLI}:
            raise ValueError('Contrat de mesure 1.4.0 divergent')
    except (OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as exc:
        raise ValueError('Protocole ou outillage mesuré différent : transition 1.4.0 refusée') from exc
    return set(MIGRATION_140)


def compatibility_files(root: Path, measured: dict, target: dict) -> set[str]:
    """Transition L14 -> ADR 0013 : liste fermée et hashes exacts, pas d'exemption générale."""
    if MEASUREMENT_140_V4 is not None and measured.get('plugin_commit') == MEASUREMENT_140_V4:
        return transition_140_v4_files(root, measured, target)
    old, current = measured['toolchain_sha256'], target['toolchain_sha256']
    if MEASUREMENT_140 is not None and measured.get('plugin_commit') == MEASUREMENT_140:
        return transition_140_files(root, measured, target)
    if measured.get('plugin_commit') == MEASUREMENT_D and any(old.get(n) != current.get(n) for n in MIGRATION_D - {'CHANGELOG.md', '.gitattributes'}):
        try:
            transition = json.loads((root / TRANSITION_D).read_bytes())
            names = MIGRATION_D - {TRANSITION_D}
            if (transition['adr'] != 'docs/adr/0017-assemblage-campagne-d.md'
                    or transition['measurement_commit'] != MEASUREMENT_D
                    or set(transition['source_files_sha256']) != names
                    or set(transition['target_files_sha256']) != names
                    or current.get(TRANSITION_D) != sha(root / TRANSITION_D)):
                raise ValueError('Transition d non autorisée')
            for name in names:
                if name in {'CHANGELOG.md', '.gitattributes'}:
                    raw = subprocess.check_output(['git', '-c', 'safe.directory=' + str(root),
                        'show', MEASUREMENT_D + ':' + name], cwd=root)
                    source_hash = hashlib.sha256(raw).hexdigest()
                    target_hash = sha(root / name)
                else:
                    source_hash, target_hash = old.get(name), current.get(name)
                if (source_hash != transition['source_files_sha256'][name]
                        or target_hash != transition['target_files_sha256'][name]
                        or target_hash != sha(root / name)):
                    raise ValueError('Empreinte source ou cible de d divergente')
            contract = measurement_contract(root, MEASUREMENT_D)
            if (contract['case_contract_sha256'] != transition['case_contract_sha256']
                    or sha(root / 'scripts/cas-plugin-cycle-v2.json') != transition['case_contract_sha256']):
                raise ValueError('Contrat de cycle différent')
        except (OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as exc:
            raise ValueError('Protocole ou outillage mesuré différent : transition d refusée') from exc
        return set(MIGRATION_D)
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


def prepared_cycle_v4(root: Path) -> str:
    """V4 explicite à empreinte fermée ; aucune équivalence avec v2/v3."""
    value = json.loads((root / 'scripts/measurement-cli.json').read_bytes()).get('prepared_cycles', {}).get('1.4.0-v4')
    name, fingerprint = CYCLE_V4
    if (value != {'case_contract_file': name, 'case_contract_sha256': fingerprint,
                 'measurement_commit': MEASUREMENT_140_V4} or sha(root / name) != fingerprint):
        raise ValueError('Contrat de cycle v4 absent ou divergent')
    return name


def transition_140_v4_files(root: Path, measured: dict, target: dict) -> set[str]:
    """H1→H2 fermé sur trois chemins et les seules données de liaison décidées."""
    try:
        commit = MEASUREMENT_140_V4
        if (not isinstance(commit, str) or re.fullmatch(r'[0-9a-f]{40}', commit) is None
                or commit == MEASUREMENT_D or measured.get('plugin_commit') != commit):
            raise ValueError('SHA H1 non autorisé')
        old, current = measured['toolchain_sha256'], target['toolchain_sha256']
        if not isinstance(old, dict) or not isinstance(current, dict):
            raise ValueError('Inventaire de transition 1.4.0 invalide')
        transition = json.loads((root / TRANSITION_140_V4).read_bytes())
        names = MIGRATION_140_V4 - {TRANSITION_140_V4}
        if (not isinstance(transition, dict)
                or set(transition) != {'adr', 'measurement_commit', 'case_contract_sha256', 'campaign_cli',
                                'source_files_sha256', 'target_files_sha256'}
                or transition['adr'] != ADR_140_V4 or transition['measurement_commit'] != commit
                or transition['case_contract_sha256'] != CYCLE_V4[1]
                or transition['campaign_cli'] != CAMPAIGN_140_CLI
                or not isinstance(transition['source_files_sha256'], dict)
                or not isinstance(transition['target_files_sha256'], dict)
                or set(transition['source_files_sha256']) != names
                or set(transition['target_files_sha256']) != names
                or any(re.fullmatch(r'[0-9a-f]{64}', str(value)) is None
                       for key in ('source_files_sha256', 'target_files_sha256')
                       for value in transition[key].values())
                or current.get(TRANSITION_140_V4) != sha(root / TRANSITION_140_V4)):
            raise ValueError('Manifeste 1.4.0 non fermé ou divergent')
        if any(old.get(name) != current.get(name) for name in set(old) | set(current)
               if name not in MIGRATION_140_V4):
            raise ValueError('Fichier supplémentaire dans la transition 1.4.0')

        def source(name: str) -> bytes:
            return subprocess.check_output(['git', '-c', 'safe.directory=' + str(root),
                'show', commit + ':' + name], cwd=root, stderr=subprocess.PIPE)

        source_bytes = {name: source(name) for name in names}
        for name in names:
            source_hash = hashlib.sha256(source_bytes[name]).hexdigest()
            if (old.get(name) != source_hash or source_hash != transition['source_files_sha256'][name]
                    or current.get(name) != transition['target_files_sha256'][name]
                    or sha(root / name) != transition['target_files_sha256'][name]):
                raise ValueError('Empreinte source ou cible 1.4.0 divergente')
        raw_manifest = source(TRANSITION_140_V4)
        expected_open = {**transition, 'measurement_commit': None,
                         'source_files_sha256': {name: None for name in names},
                         'target_files_sha256': {name: None for name in names}}
        if (old.get(TRANSITION_140_V4) != hashlib.sha256(raw_manifest).hexdigest()
                or json.loads(raw_manifest) != expected_open):
            raise ValueError('Manifeste H1 différent de la préparation non fermée')
        if target.get('plugin_commit') is not None:
            destination = target['plugin_commit']
            if not isinstance(destination, str) or re.fullmatch(r'[0-9a-f]{40}', destination) is None:
                raise ValueError('SHA cible absent ou invalide')
            changed = subprocess.check_output(['git', '-c', 'safe.directory=' + str(root),
                'diff', '--name-only', commit, destination], cwd=root, stderr=subprocess.PIPE).decode().splitlines()
            if any(name not in MIGRATION_140_V4 for name in changed):
                raise ValueError('Fichier Git supplémentaire dans la transition 1.4.0')
        for name, fingerprint in (*CYCLE_CONTRACTS.values(), CYCLE_V4):
            if (old.get(name) != fingerprint or current.get(name) != fingerprint
                    or sha(root / name) != fingerprint
                    or hashlib.sha256(source(name)).hexdigest() != fingerprint):
                raise ValueError('Contrat v2, v3 ou v4 altéré')
        assignment = b'MEASUREMENT_140_V4: str | None = None\n'
        raw_cli = source_bytes['scripts/cli_toolchains.py']
        expected_cli = raw_cli.replace(assignment, ("MEASUREMENT_140_V4: str | None = '" + commit + "'\n").encode(), 1)
        if raw_cli.count(assignment) != 1 or (root / 'scripts/cli_toolchains.py').read_bytes() != expected_cli:
            raise ValueError('Modification du lecteur autre que la liaison H1')
        config = json.loads(source_bytes['scripts/measurement-cli.json'])
        name, fingerprint = CYCLE_V4
        if (config['prepared_cycles']['1.4.0-v4'] != {'case_contract_file': name,
                'case_contract_sha256': fingerprint, 'measurement_commit': None}
                or commit in config['campaign_measurements']):
            raise ValueError('Verrou H1 déjà lié ou différent de la préparation')
        expected_config = copy.deepcopy(config)
        expected_config['prepared_cycles']['1.4.0-v4']['measurement_commit'] = commit
        expected_config['campaign_measurements'][commit] = {
            'case_contract_sha256': fingerprint, 'campaign_cli': CAMPAIGN_140_CLI}
        if json.loads((root / 'scripts/measurement-cli.json').read_bytes()) != expected_config:
            raise ValueError('Modification du verrou autre que la liaison H1')
        contract = measurement_contract(root, commit)
        if contract != {'case_contract_sha256': fingerprint, 'campaign_cli': CAMPAIGN_140_CLI}:
            raise ValueError('Contrat de mesure 1.4.0 divergent')
    except (OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as exc:
        raise ValueError('Protocole ou outillage mesuré différent : transition 1.4.0 refusée') from exc
    return set(MIGRATION_140_V4)
