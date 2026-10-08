"""Relance manuelle unique du setup autorisé, puis sonde sans modèle."""
from __future__ import annotations
from datetime import datetime, timezone
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent

def main() -> int:
    """Conserve chaque tentative et retourne un échec tant que le gate est fermé."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True, type=Path)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("sandbox_preparation", ROOT / "configurer_sandbox_isole_20261008.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CLI = args.cli.resolve(strict=True)
    version = subprocess.check_output([str(module.CLI), "--version"], env=module.environment()).decode().strip()
    if version != "codex-cli 0.162.0-alpha.2":
        raise RuntimeError("CLI différent du protocole contrôlé ; réviser le protocole avant setup")
    label = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    module.RUN = ROOT / ("configuration-sandbox-isole-reprise-" + label)
    assert module.RUN.parent == ROOT and not module.RUN.exists()
    print("Windows peut afficher une invite UAC : valider cette invite sur ce PC.", flush=True)
    print("Tentative conservée dans : " + str(module.RUN), flush=True)
    module.inspect()
    for name in ("configurer_sandbox_isole_20261008.py", Path(__file__).name):
        source = ROOT / name
        (module.RUN / name).write_bytes(source.read_bytes())
    module.write_new(module.RUN / "harnais-empreintes.json", {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ("configurer_sandbox_isole_20261008.py", Path(__file__).name)})
    module.setup()
    result = json.loads((module.RUN / "setup-result.json").read_bytes())
    if not result["success"]:
        print("Setup non confirmé ; lecture et campagne non lancées.", flush=True)
        return 1
    module.probe()
    probe = json.loads((module.RUN / "lecture-result.json").read_bytes())
    module.write_new(module.RUN / "reprise-terminee.json", {"sandbox_setup_success": True, "synthetic_read_success": probe["success"], "model_inference": False, "campaign_started": False})
    print("Lecture opérationnelle confirmée." if probe["success"] else "Lecture refusée ; campagne non lancée.", flush=True)
    return 0 if probe["success"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
