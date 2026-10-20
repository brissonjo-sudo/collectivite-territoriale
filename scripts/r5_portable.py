"""Récupération publique et contrôle R5, sans import natif ni lecture d'état privé."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def manifest(path: Path) -> dict[str, Any]:
    """Valide une liste fermée de blobs Python, jamais des fichiers d'état."""
    value = read(path)
    require(value.get("schema_version") == 1, "Manifeste public inconnu")
    commit = value.get("source_commit", "")
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "Commit public complet requis")
    names = set()
    for item in value["modules"]:
        name, source = item["module"], item["path"]
        require(re.fullmatch(r"[a-z][a-z0-9_]*", name) is not None and name not in names,
                "Module public ambigu")
        names.add(name)
        path = PurePosixPath(source)
        require(not path.is_absolute() and ".." not in path.parts and "\\" not in source
                and ":" not in source and path.name == name + ".py",
                "Outillage historique divergent : chemin public interdit")
        require(item["commit"] == commit, "Gels contradictoires : commits publics")
        require(re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None,
                "Empreinte publique invalide")
    require(bool(names) and set(value["entrypoints"]).issubset(names), "Entrées publiques absentes")
    require(all(set(item["imports_publics"]).issubset(names) for item in value["modules"]),
            "Fermeture des dépendances incomplète")
    return value


def git(repository: Path, *args: str) -> bytes:
    """Git local seulement ; safe.directory est limité à cet appel."""
    return subprocess.run(
        ["git", "-c", "core.longpaths=true", "-c", "safe.directory=" + str(repository), *args],
        cwd=repository, check=True, capture_output=True, timeout=30,
    ).stdout


def public_blobs(repository: Path, value: dict[str, Any]) -> dict[str, bytes]:
    """Lit et contrôle tous les blobs avant la moindre création de destination."""
    result = {}
    for item in value["modules"]:
        raw = git(repository, "cat-file", "blob", item["commit"] + ":" + item["path"])
        require(sha(raw) == item["sha256"] and len(raw) == item["bytes"],
                "Outillage historique divergent : " + item["module"])
        result[item["module"] + ".py"] = raw
    return result


def recover(manifest_path: Path, destination: Path, *, repository: Path | None = None,
            bundle: Path | None = None, bundle_sha256: str | None = None) -> dict[str, Any]:
    """Récupère seulement les sources publiques depuis Git ou un bundle vérifié."""
    require(not destination.exists(), "Destination existante ; aucun remplacement")
    require(destination.parent.is_dir(), "Parent de destination explicite absent")
    require((repository is None) != (bundle is None), "Dépôt ou bundle explicite requis, exclusivement")
    value = manifest(manifest_path)
    if repository is not None:
        repository = repository.resolve()
        require(not destination.resolve().is_relative_to(repository), "Destination dans le dépôt source")
        blobs = public_blobs(repository, value)
    else:
        require(bundle is not None and bundle.is_file(), "Bundle public absent")
        require(bundle_sha256 is not None and re.fullmatch(r"[0-9a-f]{64}", bundle_sha256) is not None
                and sha(bundle.read_bytes()) == bundle_sha256, "Empreinte bundle divergente ou absente")
        # Git clone ne matérialise aucun checkout, état, profil ou preuve historique.
        with tempfile.TemporaryDirectory(prefix="r5-public-", dir=destination.parent) as temporary:
            bare = Path(temporary) / "objects.git"
            subprocess.run(["git", "clone", "--bare", "--", str(bundle.resolve()), str(bare)],
                           check=True, capture_output=True, timeout=120)
            git(bare, "bundle", "verify", str(bundle.resolve()))
            blobs = public_blobs(bare, value)
    destination.mkdir()  # Exclusif ; rien ne peut être écrasé en cas de concurrence.
    for name, raw in blobs.items():
        with (destination / name).open("xb") as stream:
            stream.write(raw)
    return {"public_modules": len(blobs), "source_commit": value["source_commit"],
            "model_inference": False, "state_copied": False, "release_ready": False}


def verify_source(source_root: Path, candidate_commit: str) -> str:
    """Exige un candidat Git exact, propre et explicitement choisi ; aucun gel hérité."""
    require(source_root.is_dir(), "Racine source absente")
    require(re.fullmatch(r"[0-9a-f]{40}", candidate_commit) is not None, "Commit candidat complet requis")
    require(git(source_root, "rev-parse", "HEAD").decode().strip() == candidate_commit,
            "Commit candidat différent de HEAD")
    require(not git(source_root, "status", "--porcelain=v1", "--untracked-files=all").strip(),
            "Racine source modifiée")
    return git(source_root, "rev-parse", candidate_commit + "^{tree}").decode().strip()


def parameters(*, source_root: Path | None, candidate_commit: str | None,
               state_root: Path | None, installed_path: Path | None,
               cli: Path | None, cli_sha256: str | None, cli_version: str | None) -> dict[str, Any]:
    """Valide des identités nouvelles sans exécuter le CLI ni ouvrir l'état."""
    require(source_root is not None and candidate_commit is not None, "Racine source et candidat explicites requis")
    require(state_root is not None and installed_path is not None, "Chemins d'état explicites requis")
    require(cli is not None and cli.is_file(), "CLI explicite absent")
    require(cli_sha256 is not None and sha(cli.read_bytes()) == cli_sha256, "Empreinte CLI divergente")
    require(cli_version is not None and re.fullmatch(r"codex-cli [^\r\n]+", cli_version) is not None,
            "Version CLI explicite requise")
    source_root, state_root, installed_path, cli = (p.resolve() for p in (source_root, state_root, installed_path, cli))
    require(not state_root.exists() and not installed_path.exists(), "État neuf requis ; aucun cache historique")
    require(installed_path.is_relative_to(state_root) and installed_path != state_root,
            "Cache candidat hors état explicite")
    require(not state_root.is_relative_to(source_root) and not source_root.is_relative_to(state_root),
            "Racine source et état doivent être séparés")
    tree = verify_source(source_root, candidate_commit)
    return {"source_git_root": str(source_root), "candidate_commit": candidate_commit, "candidate_tree": tree,
            "state_root": str(state_root), "installed_path": str(installed_path), "cli": str(cli),
            "cli_sha256": cli_sha256, "cli_version": cli_version}


def contract(value: dict[str, Any], identity: dict[str, Any]) -> None:
    """Ne permet ni identité héritée ni assouplissement des limites R5."""
    require(value.get("schema_version") == "r5-portable-contract-v1", "Contrat portable explicite requis")
    require(value.get("identity") == identity, "Contrat candidat ou chemins divergents")
    require(value.get("permissions") == {"sandbox": "read-only", "approval_policy": "never"}
            and value.get("attempts_per_case") == 1
            and value.get("timeout_seconds_per_case") == 240
            and value.get("max_seconds") == 5700, "Contrat de campagne modifié")
    require(value.get("status") == "non_mesure" and value.get("historical_scores_reused") is False,
            "Statut historique non transférable")
    forbidden = {"legacy_root", "candidate_gel_path", "r3_manifest_path", "previous_cli", "legacy_protocol_sha256"}
    require(not (set(value) & forbidden), "Référence à un état historique interdite")
    require(isinstance(value.get("cases"), list) and bool(value["cases"]), "Cas explicites requis")


def verify_tools(folder: Path, value: dict[str, Any], expected: dict[str, str]) -> dict[str, bytes]:
    """Vérifie l'inventaire exact et les hashes publics, avant tout import éventuel."""
    wanted = {item["module"] + ".py": item["sha256"] for item in value["modules"]}
    require(expected == wanted, "Gels contradictoires : contrat et manifeste public")
    require(folder.is_dir() and not folder.is_symlink(), "Outillage public absent")
    require({p.name for p in folder.iterdir()} == set(wanted), "Gel R5 divergent : inventaire public")
    result = {}
    for name, digest in wanted.items():
        target = folder / name
        require(target.is_file() and not target.is_symlink() and sha(target.read_bytes()) == digest,
                "Gel R5 divergent : " + name)
        result[name] = target.read_bytes()
    return result


def check(folder: Path, manifest_path: Path, contract_path: Path, contract_sha256: str,
          launcher: Path, **settings: Any) -> dict[str, Any]:
    """Contrôle local complet ; ne charge ni harnais natif, profil, gel ou cache."""
    value = manifest(manifest_path)
    identity = parameters(**settings)
    document = read(contract_path)
    contract(document, identity)
    require(sha(contract_path.read_bytes()) == contract_sha256, "Contrat de campagne modifié : empreinte")
    verify_tools(folder, value, document["public_tools_sha256"])
    require(sha(launcher.read_bytes()) == document["launcher_sha256"],
            "Le lanceur exécuté diffère du lanceur attendu")
    return {"inputs_verified": True, "public_modules": len(value["modules"]),
            "candidate_commit": identity["candidate_commit"], "case_count": len(document["cases"]),
            "model_inference": False, "historical_scores_reused": False, "release_ready": False}


def plan(manifest_path: Path, repository: Path, destination: Path, contract_path: Path,
         contract_sha256: str, launcher: Path, **settings: Any) -> dict[str, Any]:
    """Vérifie une récupération proposée ; ne crée aucun fichier et ne lance rien."""
    require(not destination.exists(), "Destination existante ; aucun remplacement")
    value = manifest(manifest_path)
    identity = parameters(**settings)
    document = read(contract_path)
    contract(document, identity)
    require(sha(contract_path.read_bytes()) == contract_sha256, "Contrat de campagne modifié : empreinte")
    expected = {item["module"] + ".py": item["sha256"] for item in value["modules"]}
    require(document["public_tools_sha256"] == expected, "Gels contradictoires : contrat et manifeste public")
    public_blobs(repository, value)
    require(sha(launcher.read_bytes()) == document["launcher_sha256"],
            "Le lanceur exécuté diffère du lanceur attendu")
    return {**identity, "model_inference": False, "historical_scores_reused": False,
            "release_ready": False, "public_modules": len(expected)}
