"""Génère un inventaire documentaire exact ; ne modifie ni contrôle ni mesure."""
from __future__ import annotations

from pathlib import Path

BEGIN = '<!-- ct-reference-inventory:start -->'
END = '<!-- ct-reference-inventory:end -->'


def reference_paths(root: Path, skill: str) -> list[str]:
    """Chemins relatifs réels des fichiers references/ et objets/, sans liens."""
    directory = root / 'skills' / skill
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError('Skill absent ou redirigé')
    paths = []
    for name in ('references', 'objets'):
        for path in (directory / name).rglob('*'):
            if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
                raise ValueError('Référence redirigée')
            if path.is_file():
                paths.append(path.relative_to(directory).as_posix())
    return sorted(paths)


def render(root: Path, skill: str) -> str:
    """Bloc exact à ajouter à une surcharge, sans reconstruire un nom de fichier."""
    paths = reference_paths(root, skill)
    return (BEGIN + '\n## Inventaire local des références embarquées — 2026-10-18\n\n'
            'Les chemins ci-dessous sont relatifs au dossier de ce skill installé.\n'
            'Pour ses références et objets, ne jamais lire ni citer un chemin absent de\n'
            'cet inventaire ; ne pas reconstruire un nom de fichier. Si une référence\n'
            'manque, signaler cette limite et demander le document, sans supposer son nom.\n'
            'Cet inventaire atteste la présence des fichiers, pas la vigueur de leur contenu.\n\n'
            + ''.join('- `' + path + '`\n' for path in paths) + END + '\n')


def listed(text: str) -> list[str]:
    """Lit uniquement le bloc généré fermé ; absence ou doublon explicite refusé."""
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('Inventaire généré absent ou dupliqué')
    body = text.split(BEGIN, 1)[1].split(END, 1)[0]
    return [line[3:-1] for line in body.splitlines() if line.startswith('- `') and line.endswith('`')]
