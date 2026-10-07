"""Lit les octets Git d'un runtime historique sans conversion des lignes."""
import hashlib
import subprocess
from pathlib import Path


def runtime_at(root: Path, commit: str) -> dict[str, str]:
    """Compare les preuves historiques à leur commit, jamais au candidat courant."""
    listing = subprocess.run(["git", "ls-tree", "-r", "-z", commit, "--", "skills"],
                             cwd=root, check=True, capture_output=True).stdout
    entries = []
    for record in listing.split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            _, kind, oid = metadata.split()
            if kind != b"blob":
                raise ValueError("Runtime historique : entrée non fichier")
            entries.append((name.decode(), oid))
    data = subprocess.run(["git", "cat-file", "--batch"], cwd=root, check=True,
                          input=b"".join(oid+b"\n" for _, oid in entries), capture_output=True).stdout
    offset = 0
    result = {}
    for name, expected_oid in entries:
        end = data.index(b"\n", offset)
        oid, kind, size = data[offset:end].split()
        if oid != expected_oid or kind != b"blob":
            raise ValueError("Objet Git historique inattendu")
        start = end + 1
        stop = start + int(size)
        result[name] = hashlib.sha256(data[start:stop]).hexdigest()
        offset = stop + 1
    if offset != len(data):
        raise ValueError("Réponse Git historique incomplète")
    return result
