"""Complète uniquement des fixtures synthétiques ; aucune preuve historique réécrite."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import subprocess

from cli_toolchains import toolchains
from measurement_common import binding, snapshot
from qualify_distribution import fingerprint, load
from support_preuves_historiques import files_at


def closed_transition_root(test, source: Path) -> Path:
    """Isole les octets de la transition approuvée, sans suivre la tête de développement."""
    temporary = tempfile.TemporaryDirectory()
    test.addCleanup(temporary.cleanup)
    root = Path(temporary.name)
    commit = load(source, 'tests/evidence/release-1.3.0.json')['plugin_commit']
    for name, raw in files_at(source, commit, ('scripts', 'CHANGELOG.md', '.gitattributes')).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    gitdir = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=source).decode().strip()
    (root / '.git').write_text('gitdir: ' + gitdir + '\n', encoding='utf-8')
    return root


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8', newline='\n')


def refresh_smoke_snapshot(fixture) -> None:
    """Lie le smoke factice aux seuls nouveaux champs du contexte de test."""
    smoke = load(fixture.root, fixture.evidence['codex_smoke']['evidence_path'])
    current = snapshot(fixture.root)
    smoke.update({key: current[key] for key in ('toolchain_sha256', 'case_file_sha256', 'upstream_sha256')})
    fixture.write_proof('codex_smoke', smoke)


def complete_synthetic_contract(fixture, source: Path, measurement_commit: str | None = None) -> None:
    """Enrichit une copie temporaire, sans changer les assertions ni les blobs Git sources."""
    root, evidence = fixture.root, fixture.evidence
    for name in ('measurement-cli.json', 'smoke-cli.json'):
        (root / 'scripts' / name).write_bytes((source / 'scripts' / name).read_bytes())
    pins = toolchains(root, measurement_commit)
    evidence.update(copy.deepcopy(pins), test_only_synthetic_fixture=True, release_evidence=False)

    def receipt(phase: str) -> dict:
        pin = pins[phase]
        return {'test_only_synthetic_fixture': True, 'cli_version': pin['version'],
                'cli_sha256': pin['sha256'], 'cli_phase': phase, 'cli_toolchain': copy.deepcopy(pin)}

    native = load(root, evidence['native_campaign']['evidence_path'])
    reviews = load(root, evidence['distribution']['proofs']['assistant_review']['evidence_path'])
    response_hashes = {}
    for run in native['runs']:
        path = root / run['evidence_path']
        value = json.loads(path.read_bytes())
        previous = fingerprint(path)
        value.update(origin=receipt('campaign_cli'), test_only_synthetic_fixture=True, release_evidence=False)
        write(path, value)
        run['evidence_sha256'] = fingerprint(path)
        response_hashes[previous] = run['evidence_sha256']
    for run in reviews['runs']:
        path = root / run['evidence_path']
        value = json.loads(path.read_bytes())
        value.update(origin=receipt('campaign_cli'), test_only_synthetic_fixture=True, release_evidence=False,
                     evidence_sha256=response_hashes[value['evidence_sha256']])
        write(path, value)
        run['evidence_sha256'] = fingerprint(path)
    for category, value in (('native_campaign', native), ('assistant_review', reviews)):
        value.update(test_only_synthetic_fixture=True, release_evidence=False)
        fixture.write_proof(category, value)

    smoke = load(root, evidence['codex_smoke']['evidence_path'])
    smoke.update(smoke_cli=copy.deepcopy(pins['smoke_cli']), test_only_synthetic_fixture=True,
                 release_evidence=False)
    directory = (root / evidence['codex_smoke']['evidence_path']).parent
    for run in smoke['runs']:
        path = directory / (run['case_id'] + '-fixture-cli.json')
        write(path, {'test_only_synthetic_fixture': True, 'release_evidence': False,
                     'origin': receipt('smoke_cli')})
        run['proof'] = binding(path, directory)
    fixture.write_proof('codex_smoke', smoke)
    refresh_smoke_snapshot(fixture)
