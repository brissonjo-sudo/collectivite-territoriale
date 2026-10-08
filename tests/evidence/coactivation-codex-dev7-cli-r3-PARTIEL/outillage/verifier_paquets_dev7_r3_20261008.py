"""Vérifie les empreintes des paquets scellés avant création de juges frais."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUN = ROOT / "qualification-coactivation-dev7-cli-r3"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify() -> list[dict]:
    rows = []
    for identifier in ("plugin-mcp-indisponible", "plugin-dsi-technique", "plugin-dsi-source-indisponible"):
        folder = RUN / identifier
        packet_folder = RUN / "judge-packets" / identifier
        exported = json.loads((packet_folder / "manifest.json").read_bytes())
        packet = json.loads((packet_folder / "packet.json").read_bytes())
        assert exported["packet_sha256"] == sha((packet_folder / "packet.json").read_bytes())
        assert exported["trace_file_sha256"] == sha((packet_folder / "trace.json").read_bytes())
        assert exported["prompt_sha256"] == sha((packet_folder / "prompt.md").read_bytes())
        assert exported["native_file_sha256"] == sha((folder / "native-rollout.local.jsonl").read_bytes())
        assert exported["execution_sha256"] == sha((folder / "execution.json").read_bytes())
        assert exported["run_manifest_sha256"] == sha((RUN / "manifest.json").read_bytes())
        assert packet["trace_sha256"] == exported["trace_sha256"] == sha(canonical(packet["trace"]))
        assert len(packet["atoms"]) == exported["atom_count"]
        rows.append({"case_id": identifier, "packet_sha256": exported["packet_sha256"],
                     "trace_sha256": exported["trace_sha256"], "exported_at": exported["exported_at"],
                     "atom_count": exported["atom_count"], "technical_issues": packet["technical_control"]["issues"]})
    return rows


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False))
