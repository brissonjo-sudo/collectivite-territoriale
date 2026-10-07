"""Smoke hors modèle contre Vibe 2.26.0 réellement installé ; aucun appel réseau."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import tomllib

from configure_vibe import ROOT, config_text, oauth_server, skill_names


def check() -> dict:
    version = importlib.metadata.version("mistral-vibe")
    if version != "2.26.0":
        raise ValueError("Ce smoke est figé sur Vibe 2.26.0 ; revoir les API avant une mise à jour")
    with tempfile.TemporaryDirectory(prefix="ct-vibe-smoke-") as temporary:
        os.environ["VIBE_HOME"] = temporary
        from vibe.core.config import VibeConfigSchema
        from vibe.core.config.harness_files import HarnessFilesManager, init_harness_files_manager
        from vibe.core.plugins.inspection import inspect_plugin
        from vibe.core.plugins._claude import ClaudePluginAdapter
        from vibe.core.plugins._codex import CodexPluginAdapter
        from vibe.core.skills.models import SkillScope
        from vibe.core.skills.manager import SkillManager
        from vibe.core.tools.builtins.skill import render_skill_result, sample_skill_files
        from vibe.app_server.local import ClientDescriptor, LocalHarnessOptions
        from vibe.app_server.protocol import ClientCapabilities, ClientInfo, SessionOptions
        from vibe.app_server.models import PublicEffectEntry, PublicMessageEntry
        from run_vibe_campaign import allow_effect, sanitize_entry

        inspected = inspect_plugin(ROOT)
        assert not inspected.valid and inspected.source_format.value == "ambiguous"
        assert any(x.code == "plugin.compatibility.format_ambiguous" for x in inspected.diagnostics)
        imported_auth = {}
        for adapter in (ClaudePluginAdapter(), CodexPluginAdapter()):
            result = adapter.adapt(root=ROOT, data_root_base=Path(temporary), scope=SkillScope.GLOBAL)
            assert result.package is not None
            assert len(result.package.mcp_servers) == 1
            imported_auth[type(adapter).__name__] = result.package.mcp_servers[0].server.auth.type
            assert imported_auth[type(adapter).__name__] == "static"

        init_harness_files_manager()
        text = config_text(ROOT)
        parsed = VibeConfigSchema.model_validate(tomllib.loads(text))
        server = parsed.mcp_servers[0]
        expected = oauth_server(ROOT)
        assert server.auth.type == "oauth"
        assert server.auth.client_id == expected["auth"]["client_id"]
        assert server.auth.redirect_port == expected["auth"]["redirect_port"]
        assert server.auth.scopes == [] and not server.sampling_enabled
        assert parsed.session_logging.enabled is False
        manager = SkillManager(lambda: parsed, harness_files=HarnessFilesManager(sources=()), include_builtins=False)
        assert set(manager.available_skills) == set(skill_names(ROOT))
        counts, digests = {}, {}
        for name, info in manager.available_skills.items():
            loaded = render_skill_result(info, sample_skill_files(info.skill_dir))
            assert loaded.name == name and info.prompt in loaded.content
            assert Path(loaded.skill_dir).resolve() == (ROOT / "skills" / name).resolve()
            references = list(info.skill_dir.rglob("*.md"))
            assert len(references) > 1
            for path in references:
                path.read_text(encoding="utf-8")
            counts[name] = len(references)
            digests[name] = hashlib.sha256(info.skill_path.read_bytes()).hexdigest()
        degraded = VibeConfigSchema.model_validate(tomllib.loads(config_text(ROOT, mcp=False)))
        assert degraded.mcp_servers == []
        # Validate the same public constructor shapes used by the live runner, offline.
        LocalHarnessOptions(client=ClientDescriptor(
            info=ClientInfo(name="ct_vibe_campaign", version=version, entrypoint="programmatic"),
            capabilities=ClientCapabilities(callback_kinds=["approval", "user_input"])),
            session_options=SessionOptions(cwd=temporary, agent="accept-edits", headless=True,
                trust_workspace=True, enabled_tools=["skill", "read_file"], max_turns=30,
                max_price=1.0, max_session_tokens=100000))
        # Real public protocol objects, with synthetic inputs: no model result implied.
        case = json.loads((ROOT / "tests/cas-plugin.json").read_text())[0]
        base = {"id": "fixture", "session_id": "fixture", "created_at": 0,
                "updated_at": 0, "generation_status": "completed"}
        effect = PublicEffectEntry.model_validate({**base, "title": "Skill",
            "detail": {"kind": "skill", "tool_name": "skill",
                       "input": {"name": case["skills"][0]},
                       "display": {"summary": "Skill", "status_text": "Loading"}},
            "state": {"status": "completed", "display": {"success": True, "message": "Loaded"}}})
        serialized = effect.model_dump(mode="json", by_alias=True)
        assert allow_effect(serialized["detail"], case, ROOT)
        assert sanitize_entry(serialized, case, ROOT)["skill"] == case["skills"][0]
        message = PublicMessageEntry.model_validate({**base, "role": "assistant",
            "content": [{"type": "text", "text": "Synthetic response"}]})
        assert sanitize_entry(message.model_dump(mode="json", by_alias=True), case, ROOT) == {
            "type": "assistant", "text": "Synthetic response"}
        return {"vibe_version": version, "scope": "offline_configuration_and_skill_loading",
                "source_plugin_inspection": "ambiguous", "foreign_adapter_auth": imported_auth,
                "dedicated_config_auth": server.auth.type,
                "callback_uri": f"http://127.0.0.1:{server.auth.redirect_port}/callback",
                "skills": sorted(manager.available_skills), "markdown_files_read": counts,
                "skill_sha256": digests, "degraded_mcp_servers": 0,
                "public_protocol_fixture_verified": True,
                "live_oauth_verified": False, "live_model_verified": False,
                "release_ready": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    print("[OK] Vibe 2.26.0 : cinq skills chargés, OAuth explicite et mode dégradé validés hors modèle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
