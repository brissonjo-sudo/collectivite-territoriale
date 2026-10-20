"""ADR 0021 : projection octet déterministe, originaux privés, vérification CI publique."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from typing import Any

SCHEMA = 'ct-public-projection-v1'
PIECES = 'tests/evidence/mesure-courante'
TABLE = 'tests/evidence/projection-publique.json'
REPORT = 'tests/evidence/verification-projection-locale.json'
HOME = re.compile(rb'(?i)(?:[A-Z]:[\\/]+Users[\\/]+[^\\/\s"\x27<>]+|/(?:home|Users)/[^/\s"\x27<>]+)')
INSTALL = re.compile(rb'(?i)(?:[A-Z]:[\\/]+|/(?:home|Users)/)[^\s"\x27<>()\[\]]*?(?=[\\/]+(?:\.agents[\\/]+)?skills[\\/]+)')
IDENTIFIER_KEY = re.compile(r'(?i)(?:thread|session|conversation)(?:[_-]?(?:id|uuid))$')
HASH = re.compile(r'^[0-9a-f]{64}$')
UUID = re.compile(rb'(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b')
SECRET = re.compile(rb'(?i)(?:\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b|Bearer\s+[A-Za-z0-9_.-]{16,}|eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|https?://[^\s/:]+:[^\s/@]+@)')
CREDENTIAL_KEY = re.compile(r'(?i)^(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|token|secret|password|authorization)$')


def digest(raw: bytes) -> str:
    """SHA-256 des octets exacts."""
    return hashlib.sha256(raw).hexdigest()


def policy_hash() -> str:
    """La règle est le module versionné, sans configuration appelante."""
    return digest(Path(__file__).read_bytes())


def safe(root: Path, relative: str) -> Path:
    """Chemin relatif canonique, sans jonction ni lien, borné à sa racine."""
    pure = PurePosixPath(relative)
    if not relative or pure.is_absolute() or '..' in pure.parts or ':' in relative or '\\' in relative or str(pure) != relative:
        raise ValueError('Chemin de projection non canonique')
    path = root / relative
    for parent in (path, *path.parents):
        if parent == root.parent:
            break
        if parent.is_symlink() or getattr(parent, 'is_junction', lambda: False)():
            raise ValueError('Projection redirigée')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Projection hors racine')
    return path


def decoded(name: str, raw: bytes) -> bytes:
    """Gzip borné ; aucun flux opaque ne peut masquer du contenu personnel."""
    if name.endswith('.gz'):
        import io
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
            raw = stream.read(4_000_001)
        if len(raw) > 4_000_000:
            raise ValueError('Pièce gzip trop grande')
    raw.decode('utf-8', errors='strict')
    return raw


def documents(name: str, raw: bytes) -> list[Any]:
    """Lit les données structurées sans modifier leur sérialisation."""
    text = decoded(name, raw).decode('utf-8')
    if name.removesuffix('.gz').endswith('.jsonl'):
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if name.removesuffix('.gz').endswith('.json'):
        return [json.loads(text)]
    return []


def strings(value: Any, parent: str = ''):
    """Champs de session explicites, y compris un id sous un objet de conversation."""
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str):
                yield key, item, parent
            yield from strings(item, key)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item, parent)


def identifier_field(key: str, parent: str) -> bool:
    """Liste fixe des clés, sans déduction d'un identifiant juridique."""
    return bool(IDENTIFIER_KEY.search(key) or key.lower() in {'thread', 'session', 'conversation'}
                or (key == 'id' and parent.lower() in {'thread', 'session', 'conversation'}))


def identifiers(files: dict[str, bytes]) -> dict[bytes, bytes]:
    """Collecte privée ; seule l'empreinte d'un identifiant sort de cette fonction."""
    result = {}
    for name, raw in files.items():
        for document in documents(name, raw):
            for key, value, parent in strings(document):
                if identifier_field(key, parent) and not HASH.fullmatch(value):
                    if not value or len(value) > 512:
                        raise ValueError('Identifiant de session non projetable')
                    hashed = digest(value.encode()).encode()
                    for spelling in (value.encode(), json.dumps(value, ensure_ascii=False)[1:-1].encode(),
                                     json.dumps(value, ensure_ascii=True)[1:-1].encode()):
                        result[spelling] = hashed
    return result


def project_bytes(name: str, raw: bytes, ids: dict[bytes, bytes]) -> bytes:
    """Substitutions seules ; aucune réécriture JSON, de jugement ou d'empreinte source."""
    content = decoded(name, raw)
    projected = content
    for original in sorted(ids, key=lambda item: (-len(item), item)):
        projected = projected.replace(original, ids[original])
    projected = INSTALL.sub(b'<INSTALL>', projected)
    projected = HOME.sub(b'<HOME>', projected)
    if name.endswith('.gz'):
        return raw if projected == content else gzip.compress(projected, mtime=0)
    return projected


def privacy_errors(name: str, raw: bytes) -> list[str]:
    """Refuse les résidus ; ne masque jamais un secret pour le faire passer."""
    content = decoded(name, raw)
    errors = []
    for label, pattern in (('home', HOME), ('installation', INSTALL), ('identifiant UUID', UUID), ('secret', SECRET)):
        if pattern.search(content):
            errors.append(label + ' résiduel : ' + name)
    for document in documents(name, raw):
        for key, value, parent in strings(document):
            for label, pattern in (('home', HOME), ('installation', INSTALL), ('identifiant UUID', UUID), ('secret', SECRET)):
                if pattern.search(value.encode()):
                    errors.append(label + ' résiduel : ' + name)
            if identifier_field(key, parent) and not HASH.fullmatch(value):
                errors.append('Identifiant de session résiduel : ' + name)
            if CREDENTIAL_KEY.fullmatch(key) and value.strip():
                errors.append('Credential résiduel : ' + name)
    return sorted(set(errors))


def graph(files: dict[str, bytes], entries: dict) -> list[dict]:
    """Relie aussi les empreintes des fiche/résumé originaux inscrites dans les avis."""
    by_hash = {}
    for name, item in entries.items():
        by_hash.setdefault(item['original_sha256'], []).append(name)
    links = []

    def visit(value, pointer, source):
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, pointer + '/' + key.replace('~', '~0').replace('/', '~1'), source)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, pointer + '/' + str(index), source)
        elif isinstance(value, str) and value in by_hash:
            for target in sorted(by_hash[value]):
                links.append({'source': source, 'pointer': pointer, 'target': target,
                              'original_sha256': value, 'projection_sha256': entries[target]['projection_sha256']})

    for name, raw in sorted(files.items()):
        for index, document in enumerate(documents(name, raw)):
            visit(document, str(index), name)
    return links


def read_pieces(root: Path) -> dict[str, bytes]:
    """Inventaire complet, aucun fichier caché ou format opaque exclu du contrôle."""
    result = {}
    for path in sorted(safe(root, PIECES).rglob('*')):
        relative = path.relative_to(root).as_posix()
        safe(root, relative)
        if path.is_file():
            if path.suffix not in {'.json', '.jsonl', '.md', '.gz'}:
                raise ValueError('Format de pièce non projetable : ' + relative)
            result[relative] = path.read_bytes()
    if not result:
        raise ValueError('Pièces de projection absentes')
    return result


def write_json(path: Path, value: dict) -> None:
    """Écriture exclusive UTF-8/LF des seules nouvelles tables techniques."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def verify_local(original_root: Path, public_root: Path) -> dict:
    """Exige tous les originaux et re-dérive chaque octet, sans relecture modèle."""
    table = json.loads(safe(public_root, TABLE).read_bytes())
    originals, public = read_pieces(original_root), read_pieces(public_root)
    if (original_root.resolve().is_relative_to(public_root.resolve())
            or table['schema'] != SCHEMA or table['policy_sha256'] != policy_hash()
            or table['links'] != graph(public, table['pieces'])):
        raise ValueError('Table de re-dérivation divergente')
    if set(originals) != set(public) or set(public) != set(table['pieces']):
        raise ValueError('Original ou projection absent')
    ids = identifiers(originals)
    for name, raw in originals.items():
        expected = project_bytes(name, raw, ids)
        item = table['pieces'][name]
        if (item != {'original_sha256': digest(raw), 'projection_sha256': digest(expected),
                     'original_octets': len(raw), 'projection_octets': len(expected)} or public[name] != expected):
            raise ValueError('Re-dérivation divergente : ' + name)
    return {'schema': SCHEMA, 'status': 'ok', 'policy_sha256': policy_hash(),
            'table_sha256': digest(safe(public_root, TABLE).read_bytes()),
            'pieces_verified': len(public), 'originals_required_locally': True,
            'originals_preserved_outside_repository': True}


def publish(original_root: Path, public_root: Path, release_relative: str) -> Path:
    """Projette une sortie privée déjà contrôlée ; aucun original personnel n'est publié."""
    if public_root.exists() or public_root.resolve().is_relative_to(original_root.resolve()):
        raise ValueError('Destination de projection existante ou privée')
    originals = read_pieces(original_root)
    ids = identifiers(originals)
    public = {name: project_bytes(name, raw, ids) for name, raw in originals.items()}
    for name, raw in public.items():
        errors = privacy_errors(name, raw)
        if errors:
            raise ValueError('; '.join(errors))
    public_root.mkdir(parents=True)
    for path in sorted(original_root.rglob('*')):
        relative = path.relative_to(original_root).as_posix()
        safe(original_root, relative)
        if path.is_file() and relative != release_relative and relative not in originals:
            target = safe(public_root, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    entries = {}
    for name, raw in public.items():
        path = safe(public_root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        entries[name] = {'original_sha256': digest(originals[name]), 'projection_sha256': digest(raw),
                         'original_octets': len(originals[name]), 'projection_octets': len(raw)}
    table = {'schema': SCHEMA, 'policy_sha256': policy_hash(), 'pieces': entries,
             'links': graph(public, entries)}
    write_json(safe(public_root, TABLE), table)
    report = verify_local(original_root, public_root)
    write_json(safe(public_root, REPORT), report)
    release_raw = project_bytes(release_relative, safe(original_root, release_relative).read_bytes(), ids)
    evidence = json.loads(release_raw)
    evidence['public_projection'] = {
        'table': {'evidence_path': TABLE, 'sha256': digest(safe(public_root, TABLE).read_bytes())},
        'local_verification': {'evidence_path': REPORT, 'sha256': digest(safe(public_root, REPORT).read_bytes())}}
    target = safe(public_root, release_relative)
    write_json(target, evidence)
    verify_ci(public_root, evidence)
    return target


class ProjectionView:
    """Traduit un lien original vers sa projection déjà vérifiée, sans original en CI."""
    def __init__(self, root: Path, entries: dict):
        self.root, self.entries = root, entries

    def fingerprint(self, path: Path) -> str:
        """L'empreinte source garde son sens ; la projection est contrôlée séparément."""
        name = path.resolve().relative_to(self.root.resolve()).as_posix()
        raw = safe(self.root, name).read_bytes()
        if name in self.entries:
            if digest(raw) != self.entries[name]['projection_sha256']:
                raise ValueError('Projection altérée : ' + name)
            return self.entries[name]['original_sha256']
        return digest(raw)

    def bound(self, base: Path, link: dict) -> Path:
        """Lien source résolu via la table ; aucun original privé n'est requis."""
        path = safe(base, link['evidence_path'])
        if self.fingerprint(path) != link['sha256']:
            raise ValueError('Lien source de projection divergent')
        return path


def verify_ci(root: Path, evidence: dict) -> ProjectionView:
    """Contrôle complet des pièces publiques, table, graphe et résultat local lié."""
    descriptor = evidence['public_projection']
    if set(descriptor) != {'table', 'local_verification'}:
        raise ValueError('Descripteur de projection différent')
    documents_bound = []
    for key, expected_path in (('table', TABLE), ('local_verification', REPORT)):
        link = descriptor[key]
        raw = safe(root, link['evidence_path']).read_bytes()
        if link['evidence_path'] != expected_path or digest(raw) != link['sha256']:
            raise ValueError('Table ou vérification locale altérée')
        errors = privacy_errors(expected_path, raw)
        if errors:
            raise ValueError('; '.join(errors))
        documents_bound.append(json.loads(raw))
    table, report = documents_bound
    if (set(table) != {'schema', 'policy_sha256', 'pieces', 'links'}
            or table['schema'] != SCHEMA or table['policy_sha256'] != policy_hash()):
        raise ValueError('Politique de projection différente')
    files = read_pieces(root)
    if set(files) != set(table['pieces']):
        raise ValueError('Projection incomplète ou pièce ajoutée')
    for name, raw in files.items():
        item = table['pieces'][name]
        if (set(item) != {'original_sha256', 'projection_sha256', 'original_octets', 'projection_octets'}
                or not all(HASH.fullmatch(item[key]) for key in ('original_sha256', 'projection_sha256'))
                or type(item['original_octets']) is not int or item['original_octets'] < 0
                or item['projection_sha256'] != digest(raw) or item['projection_octets'] != len(raw)):
            raise ValueError('Projection altérée : ' + name)
        errors = privacy_errors(name, raw)
        if errors:
            raise ValueError('; '.join(errors))
    if table['links'] != graph(files, table['pieces']):
        raise ValueError('Liens de projection divergents')
    expected_report = {'schema': SCHEMA, 'status': 'ok', 'policy_sha256': policy_hash(),
        'table_sha256': descriptor['table']['sha256'], 'pieces_verified': len(files),
        'originals_required_locally': True, 'originals_preserved_outside_repository': True}
    if report != expected_report:
        raise ValueError('Vérification locale incomplète ou non liée')
    errors = privacy_errors('release-1.3.0.json', json.dumps(evidence, ensure_ascii=False).encode())
    if errors:
        raise ValueError('; '.join(errors))
    return ProjectionView(root, table['pieces'])


def main() -> int:
    """Rejoue la re-dérivation locale sans publier de chemins privés dans stdout."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original-dir', type=Path, required=True)
    parser.add_argument('--public-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify_local(args.original_dir.resolve(), args.public_dir.resolve())
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({'status': 'blocked', 'reason_type': type(exc).__name__,
                          'reason_sha256': digest(str(exc).encode())}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
