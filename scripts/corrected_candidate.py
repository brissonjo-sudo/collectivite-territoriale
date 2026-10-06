"""Gèle un runtime corrigé committé, sans réutiliser les scores historiques."""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from instruction_overlays import validate_overlays

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'corrected-runtime-v1'
BASELINE = 'tests/evidence/qualification-dsi/gel-r3.json'
FIXED = {
    '.gitattributes', '.mcp.json', 'upstream.json', BASELINE,
    '.claude-plugin/marketplace.json', '.claude-plugin/plugin.json',
    '.codex-plugin/plugin.json', 'docs/protocole-coactivation-dsi.md',
    'docs/cas-coactivation-v2.md', 'docs/protocole-coactivation-v2.md',
}
HASH = re.compile(r'^[0-9a-f]{64}$')
COMMIT = re.compile(r'^[0-9a-f]{40}$')
MANIFEST_KEYS = {
    'schema_version', 'profile', 'candidate_commit', 'candidate_tree', 'created_at',
    'model', 'runtime_changed', 'historical_scores_reused', 'baseline_runtime_commit',
    'baseline_manifest_sha256', 'source_pins_sha256', 'declared_overlays', 'runtime_files', 'files',
}


def checksum(data: bytes) -> str:
    """Calcule l'empreinte des octets exacts, sans normalisation."""
    return hashlib.sha256(data).hexdigest()


def inventory(root: Path) -> set[str]:
    """Inclut tous les runtimes, surcharges, outils, cas et réglages projet."""
    paths = set(FIXED)
    for directory in ('skills', 'overlays', '.claude', '.agents', '.claude-plugin', '.codex-plugin'):
        paths.update(path.relative_to(root).as_posix() for path in (root / directory).rglob('*')
                     if path.is_file())
    paths.update(path.relative_to(root).as_posix() for path in (root / 'scripts').glob('*.py'))
    for pattern in ('*.py', '*.json'):
        paths.update(path.relative_to(root).as_posix() for path in (root / 'tests').glob(pattern))
    paths.update(name for name in ('CLAUDE.md', 'AGENTS.md') if (root / name).exists())
    return paths


def checked_path(root: Path, relative: str) -> Path:
    """Refuse les chemins hors dépôt et les liens, y compris les jonctions."""
    if not isinstance(relative, str) or '\\' in relative or ':' in relative:
        raise ValueError('Chemin de gel invalide')
    candidate = root / relative
    if (not relative or Path(relative).is_absolute() or '..' in Path(relative).parts
            or candidate.relative_to(root).as_posix() != relative
            or not candidate.resolve().is_relative_to(root.resolve())):
        raise ValueError('Chemin de gel hors dépôt')
    for path in (candidate, *candidate.parents):
        if path == root.parent:
            break
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError('Lien interdit dans le gel')
    if not candidate.is_file():
        raise ValueError('Fichier de gel absent : ' + relative)
    return candidate


def source_overlays(root: Path) -> dict[str, str]:
    """Vérifie les pins amont et les empreintes des insertions déclarées."""
    upstream = json.loads((root / 'upstream.json').read_text(encoding='utf-8'))
    skills = upstream['skills']
    if not isinstance(skills, dict) or not skills:
        raise ValueError('Inventaire amont vide')
    if set(skills) != {path.name for path in (root / 'skills').iterdir() if path.is_dir()}:
        raise ValueError('Skills amont et runtime divergents')
    hashes: dict[str, str] = {}
    for spec in skills.values():
        if not isinstance(spec.get('commit'), str) or not COMMIT.fullmatch(spec['commit']):
            raise ValueError('Pin amont non immuable')
        overlays = spec.get('instruction_overlays', [])
        validate_overlays(overlays)
        for overlay in overlays:
            relative = overlay['source']
            actual = checksum(checked_path(root, relative).read_bytes())
            if actual != overlay['source_sha256']:
                raise ValueError('Surcharge divergente : ' + relative)
            hashes[relative] = actual
    actual_sources = {path.relative_to(root).as_posix() for path in (root / 'overlays').rglob('*')
                      if path.is_file()}
    if actual_sources != set(hashes):
        raise ValueError('Surcharge absente de la déclaration amont')
    return dict(sorted(hashes.items()))


def git_bytes(root: Path, revision: str, paths: set[str]) -> dict[str, bytes]:
    """Lit les blobs committés en mémoire ; aucune extraction ni exécution."""
    command = ['git', '-c', 'safe.directory=' + root.as_posix(), 'archive',
               '--format=tar', revision, *sorted(paths)]
    archive = subprocess.check_output(command, cwd=root)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as stream:
        result = {member.name: stream.extractfile(member).read()
                  for member in stream.getmembers() if member.isfile()}
    if set(result) != paths:
        raise ValueError('Inventaire absent du commit')
    return result


def git_revision(root: Path, revision: str) -> str:
    """Obtient une identité Git précise sans changer le checkout."""
    return subprocess.check_output(['git', '-c', 'safe.directory=' + root.as_posix(),
                                    'rev-parse', revision], cwd=root, text=True).strip()


def frozen_failures_corrected(frozen: dict[str, Any], *, root: Path = ROOT,
                             require_git: bool = False) -> list[str]:
    """Recalcule l'inventaire exact ; Git est requis pour la mesure vivante."""
    if (not isinstance(frozen, dict) or frozen.get('schema_version') != 3
            or frozen.get('profile') != PROFILE or not isinstance(frozen.get('files'), dict)
            or set(frozen) != MANIFEST_KEYS):
        return ['corrected_manifest_schema_required']
    if (frozen.get('historical_scores_reused') is not False
            or frozen.get('runtime_changed') is not True
            or frozen.get('model') != 'claude-sonnet-4-6'
            or any(not isinstance(frozen.get(key), str) or not COMMIT.fullmatch(frozen[key])
                   for key in ('candidate_commit', 'candidate_tree'))):
        return ['corrected_candidate_identity_invalid']
    files = frozen['files']
    try:
        expected = inventory(root)
        if set(files) != expected:
            return ['corrected_inventory_mismatch']
        for relative, expected_hash in files.items():
            if (not isinstance(expected_hash, str) or not HASH.fullmatch(expected_hash)
                    or checksum(checked_path(root, relative).read_bytes()) != expected_hash):
                return ['gel_divergent:' + relative]
        runtime = {path for path in expected if path.startswith('skills/')}
        if frozen.get('runtime_files') != len(runtime):
            return ['corrected_runtime_count_mismatch']
        prior = json.loads((root / BASELINE).read_text(encoding='utf-8'))
        if (frozen.get('baseline_manifest_sha256') != files[BASELINE]
                or frozen.get('baseline_runtime_commit') != prior['candidate_commit']
                or frozen.get('source_pins_sha256') != files['upstream.json']
                or frozen.get('declared_overlays') != source_overlays(root)):
            return ['corrected_source_identity_mismatch']
        old_runtime = {path: digest for path, digest in prior['files'].items()
                       if path.startswith('skills/')}
        if old_runtime == {path: files[path] for path in runtime}:
            return ['corrected_runtime_change_required']
        if require_git:
            if (git_revision(root, 'HEAD') != frozen['candidate_commit']
                    or git_revision(root, 'HEAD^{tree}') != frozen['candidate_tree']):
                return ['corrected_head_mismatch']
            committed = git_bytes(root, frozen['candidate_commit'], expected)
            if any(checksum(data) != files[path] for path, data in committed.items()):
                return ['corrected_committed_bytes_mismatch']
    except (ValueError, KeyError, OSError, TypeError, subprocess.CalledProcessError) as error:
        return ['corrected_validation_failed:' + type(error).__name__]
    return []


def build_manifest(root: Path = ROOT) -> dict[str, Any]:
    """Refuse les modifications non committées avant de créer une identité neuve."""
    paths = inventory(root)
    commit = git_revision(root, 'HEAD')
    tree = git_revision(root, 'HEAD^{tree}')
    committed = git_bytes(root, commit, paths)
    files = {}
    for relative in sorted(paths):
        data = checked_path(root, relative).read_bytes()
        if data != committed[relative]:
            raise ValueError('Octets locaux différents du commit : ' + relative)
        files[relative] = checksum(data)
    prior = json.loads((root / BASELINE).read_text(encoding='utf-8'))
    frozen = {'schema_version': 3, 'profile': PROFILE, 'candidate_commit': commit,
              'candidate_tree': tree, 'created_at': datetime.now(timezone.utc).isoformat(),
              'model': 'claude-sonnet-4-6', 'runtime_changed': True,
              'historical_scores_reused': False, 'baseline_runtime_commit': prior['candidate_commit'],
              'baseline_manifest_sha256': files[BASELINE],
              'source_pins_sha256': files['upstream.json'], 'declared_overlays': source_overlays(root),
              'runtime_files': sum(path.startswith('skills/') for path in files), 'files': files}
    if failures := frozen_failures_corrected(frozen, root=root, require_git=True):
        raise ValueError(' | '.join(failures))
    return frozen


def measured_failures(frozen: dict[str, Any]) -> list[str]:
    """La mesure contrôle HEAD et les blobs, avant et après chaque cas."""
    return frozen_failures_corrected(frozen, require_git=True)
