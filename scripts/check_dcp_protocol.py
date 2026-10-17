"""Constat logiciel du protocole DCP épinglé ; aucun répondant ou juge lancé."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    """Retourne 2 tant que la combinaison décidée n'est pas portée."""
    protocol = json.loads(Path(__file__).with_name("dcp-protocol.json").read_bytes())
    compatible = protocol["mixed_engine_supported"] is True and protocol["effort_parameter_supported"] is True
    print(json.dumps({"status": "compatible" if compatible else "blocked", "compatible": compatible,
        "upstream_commit": protocol["upstream_commit"], "requested_responder": protocol["requested_responder"],
        "requested_judge": protocol["requested_judge"], "model_called": False,
        "reason": protocol["reason"]}, ensure_ascii=True))
    return 0 if compatible else 2


if __name__ == "__main__":
    raise SystemExit(main())
