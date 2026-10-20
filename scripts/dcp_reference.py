"""DCP-014 : référence autonome fermée, distincte de toute mesure du plugin."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import stat


def redirected(path: Path) -> bool:
    """Symlink/jonction refusés, y compris avec le Python 3.11 de la CI."""
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def contract() -> dict:
    """Contrat versionné ; aucun hash ou fichier exclu fourni par la CLI."""
    value = json.loads(Path(__file__).with_name("dcp-protocol.json").read_bytes())
    if value.get("decision") != "DCP-014" or value["reference"]["selection_excluded"] != ["LICENSE"]:
        raise ValueError("Contrat DCP-014 absent ou sélection non autorisée")
    return value


def reference(root: Path, path: Path | None) -> dict:
    """Vérifie la preuve autorisée et tous ses octets runtime contre le candidat."""
    if path is None or not path.is_file():
        raise ValueError("Mesure DCP absente")
    protocol = contract()
    expected = protocol["reference"]
    pin = json.loads((root / "upstream.json").read_bytes())["skills"]["dcp-fpt"]["commit"]
    proof_bytes = path.read_bytes()
    proof = json.loads(proof_bytes)
    if proof.get("upstream_runtime_commit") != pin or pin != protocol["upstream_commit"]:
        raise ValueError("Pin DCP différent de la référence autonome")
    summary = proof["summary"]
    serialized = (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if (hashlib.sha256(serialized).hexdigest() != proof.get("source_summary_sha256")
            or proof.get("source_summary_sha256") != expected["source_summary_sha256"]):
        raise ValueError("Empreinte source_summary_sha256 DCP divergente")
    if (proof.get("source_repository") != expected["source_repository"]
            or proof.get("source_proof_commit") != expected["source_proof_commit"]):
        raise ValueError("Provenance publique DCP différente")
    if hashlib.sha256(proof_bytes).hexdigest() != expected["sha256"]:
        raise ValueError("Empreinte du fichier de preuve DCP divergente")
    folder = root / "skills/dcp-fpt"
    if redirected(folder):
        raise ValueError("Runtime DCP redirigé")
    installed = {}
    for item in folder.rglob("*"):
        if redirected(item):
            raise ValueError("Runtime DCP redirigé")
        if item.is_file():
            installed[item.relative_to(folder).as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    measured = summary["runtime_sha256"]
    for name, digest in measured.items():
        relative = PurePosixPath(name)
        if (relative.is_absolute() or relative.as_posix() != name or ".." in relative.parts
                or "\\" in name or ":" in name or installed.get(name) != digest):
            raise ValueError("Octets DCP mesurés divergents : " + name)
    if set(installed) - set(measured) != set(expected["selection_excluded"]):
        raise ValueError("Sélection DCP différente : seul LICENSE est hors mesure")
    if (summary["case_count"] != 28 or summary["threshold_passed"] is not True
            or summary["critical_failures"]):
        raise ValueError("Mesure autonome DCP incomplète ou seuil non atteint")
    return proof


def copy_reference(root: Path, source: Path, destination: Path) -> dict:
    """Copie exacte, sans sceau plugin ajouté ni réécriture de scope ou d'avis."""
    original = reference(root, source)
    # Vérification de la copie aussi : une source changée entre les lectures est refusée.
    with destination.open("xb") as stream:
        stream.write(source.read_bytes())
    copied = reference(root, destination)
    if copied != original:
        raise ValueError("Référence DCP modifiée pendant la copie")
    return copied
