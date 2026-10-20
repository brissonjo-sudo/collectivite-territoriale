"""Contrôle logiciel DCP-014 ; aucun répondant ou juge lancé."""
from __future__ import annotations

import json
from pathlib import Path

from dcp_reference import contract, reference

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Retourne zéro seulement si la référence autonome correspond au candidat."""
    try:
        protocol = contract()
        proof = reference(ROOT, ROOT / protocol["reference"]["evidence_path"])
        print(json.dumps({"status": "verified_standalone_reference", "compatible": True,
            "decision": protocol["decision"], "upstream_commit": proof["upstream_runtime_commit"],
            "proof_sha256": protocol["reference"]["sha256"], "runtime_files_verified": len(proof["summary"]["runtime_sha256"]),
            "selection_excluded": protocol["reference"]["selection_excluded"],
            "scope": proof["scope"], "human_legal_validation": proof["human_legal_validation"],
            "publication_ready": proof["publication_ready"],
            "plugin_measurement_transferred": False, "new_dcp_campaign_required": False,
            "model_called": False}, ensure_ascii=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"status": "blocked", "compatible": False, "decision": "DCP-014", "model_called": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
