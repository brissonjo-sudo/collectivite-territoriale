"""Campagne Vibe 2.26.0, modes guidé/naturel, sans promotion automatique en release.

Le runtime Python public de Vibe fournit les événements et les demandes de
permission. Aucun flux brut ni raisonnement interne n'est conservé.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import tomllib
from urllib.parse import urlsplit

from configure_vibe import ROOT, MCP_ALIAS, MCP_TOOLS, config_text, oauth_server, skill_names, write_profile

SUPPORTED_VIBE = "2.26.0"


def build_prompt(case: dict, mode: str) -> str:
    prompt = case["prompt"]
    if mode == "natural":
        return prompt
    sequence = " puis ".join(f"`{name}`" for name in case["activation_sequence"])
    return f"Charge avec l'outil skill, dans cet ordre, {sequence}, avant de répondre.\n\n{prompt}"


def enabled_tools(case: dict) -> list[str]:
    tools = ["skill", "read_file"]
    if case["mcp_mode"] == "required":
        tools += [f"{MCP_ALIAS}_{name}" for name in MCP_TOOLS]
    if case["web_mode"] == "official_source":
        tools.append("web_fetch")
    return tools


def official_url(url: str, case: dict) -> bool:
    value = urlsplit(url)
    return (case["web_mode"] == "official_source" and value.scheme == "https"
            and value.hostname in case.get("official_source_hosts", [])
            and value.port in (None, 443) and not value.username and not value.password)


def allow_effect(detail: dict, case: dict, root: Path) -> bool:
    """No blanket approval: callback inputs must match this scenario's tool scope."""
    args = detail.get("input") or {}
    name = detail.get("toolName", detail.get("tool_name", ""))
    kind = detail.get("kind")
    if name not in enabled_tools(case) or not isinstance(args, dict):
        return False
    if kind == "skill":
        return args.get("name") in skill_names(root)
    if kind == "file_read":
        path = args.get("filePath", args.get("file_path"))
        if not isinstance(path, str) or not Path(path).is_absolute():
            return False
        resolved = Path(path).resolve()
        return resolved.is_relative_to((root / "skills").resolve()) and resolved.is_file()
    if kind == "web_fetch":
        try:
            return official_url(args.get("url", ""), case)
        except ValueError:
            return False
    return kind == "tool" and name in enabled_tools(case) and name.startswith(MCP_ALIAS + "_")


def sanitize_entry(entry: dict, case: dict, root: Path) -> dict | None:
    """Allow-list the persisted fields of public completed entries."""
    if entry.get("type") == "message" and entry.get("role") == "assistant":
        content = entry.get("content") or []
        return {"type": "assistant", "text": "\n".join(x["text"] for x in content
                if x.get("type") == "text" and isinstance(x.get("text"), str))}
    if entry.get("type") != "effect":
        return None
    detail, state = entry.get("detail") or {}, entry.get("state") or {}
    terminal = state.get("status")
    if terminal not in {"completed", "failed", "cancelled", "skipped"}:
        return None
    name = detail.get("toolName", detail.get("tool_name", ""))
    kind = detail.get("kind")
    args = detail.get("input") or {}
    allowed = allow_effect(detail, case, root)
    output = state.get("output")
    # MCP success includes a protocol/tool error check, not just a completed transport.
    tool_error = isinstance(output, dict) and (
        bool(output.get("isError", output.get("is_error", False))) or output.get("ok") is False)
    display_failed = (state.get("display") or {}).get("success") is False
    record = {"type": "tool", "name": name, "kind": kind, "status": terminal,
              "succeeded": terminal == "completed" and not tool_error and not display_failed,
              "allowed": allowed}
    if kind == "skill" and allowed:
        record["skill"] = args["name"]
    elif kind == "file_read" and allowed:
        path = args.get("filePath", args.get("file_path"))
        record["path"] = Path(path).resolve().relative_to(root.resolve()).as_posix()
    elif kind == "web_fetch" and allowed:
        parsed = urlsplit(args["url"])
        record["source"] = parsed._replace(query="", fragment="").geturl()
    # Raw arguments, tool outputs, errors, tokens and reasoning never enter the trace.
    return record


def technical_failures(trace: list[dict], case: dict, mode: str) -> list[str]:
    errors = []
    successful = [x for x in trace if x.get("succeeded")]
    activated = [x["skill"] for x in successful if "skill" in x]
    if not set(case["skills"]).issubset(activated):
        errors.append("expected_skills_not_observed")
    if mode == "guided" and activated != case["activation_sequence"]:
        errors.append("guided_activation_sequence_mismatch")
    if any(x.get("type") == "tool" and not x.get("allowed") for x in trace):
        errors.append("unexpected_tool_scope")
    mcp = [x for x in trace if x.get("name", "").startswith(MCP_ALIAS + "_")]
    if case["mcp_mode"] == "required" and not any(x.get("succeeded") for x in mcp):
        errors.append("plugin_mcp_success_missing")
    if case["mcp_mode"] == "disabled" and mcp:
        errors.append("plugin_mcp_call_unexpected")
    if case["web_mode"] == "official_source" and not any(
            x.get("kind") == "web_fetch" and x.get("allowed") and x.get("succeeded") for x in trace):
        errors.append("official_web_success_missing")
    if not trace or trace[-1].get("type") != "assistant" or not trace[-1].get("text", "").strip():
        errors.append("final_response_missing")
    return errors


async def execute(case: dict, mode: str, workspace: Path, limits: dict,
                  trace: list[dict]) -> tuple[list[dict], dict]:
    # Imported only after VIBE_HOME is set, so config paths cannot bind to the usual profile.
    from contextlib import aclosing
    from vibe.app_server.events import CallbackRequested, HistoryEntryAdded, HistoryEntryUpdated
    from vibe.app_server.local import ClientDescriptor, LocalHarness, LocalHarnessOptions
    from vibe.app_server.models import ApprovalCallbackOutput, ApprovalDecision, ApprovalDecisionType
    from vibe.app_server.protocol import ClientCapabilities, ClientInfo, SessionOptions

    options = LocalHarnessOptions(
        client=ClientDescriptor(info=ClientInfo(name="ct_vibe_campaign", version=SUPPORTED_VIBE,
                                               entrypoint="programmatic"),
                                capabilities=ClientCapabilities(callback_kinds=["approval", "user_input"])),
        session_options=SessionOptions(cwd=str(workspace), agent="accept-edits", headless=True,
            trust_workspace=True, enabled_tools=enabled_tools(case),
            max_turns=limits["turns"], max_price=limits["price"], max_session_tokens=limits["tokens"]),
    )
    session = await LocalHarness(options).start()
    seen = set()
    try:
        await session.resources.runtime.wait_until_ready()
        async with aclosing(session.act(build_prompt(case, mode))) as events:
            async for event in events:
                if isinstance(event, CallbackRequested):
                    callback = event.callback
                    detail = callback.detail
                    if detail.kind == "approval" and allow_effect(detail.effect.model_dump(mode="json", by_alias=True), case, ROOT):
                        await session.respond_to_callback(callback.id, ApprovalCallbackOutput(
                            decision=ApprovalDecision(type=ApprovalDecisionType.APPROVE)))
                    else:
                        await session.deny_callback(callback)
                if isinstance(event, (HistoryEntryAdded, HistoryEntryUpdated)):
                    entry = event.entry
                    if str(entry.generation_status) == "completed" and entry.id not in seen:
                        record = sanitize_entry(entry.model_dump(mode="json", by_alias=True), case, ROOT)
                        if record is not None:
                            seen.add(entry.id)
                            trace.append(record)
        state = session.state
        turn = state.latest_turn
        usage = state.session.token_usage
        return trace, {"stop_reason": str(turn.stop_reason) if turn else None,
                       "model_observed": state.session.model, "harness": state.session.harness,
                       "token_usage": usage.model_dump(mode="json") if usage else None,
                       "cost_usd": None}
    finally:
        await session.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--mode", choices=["guided", "natural"], required=True)
    parser.add_argument("--model", required=True, help="Alias connu de Vibe 2.26.0, figé pour la campagne")
    parser.add_argument("--output", type=Path, required=True, help="Nouveau fichier de preuve")
    parser.add_argument("--max-price", type=float, required=True, help="Plafond pilote à calibrer, USD")
    parser.add_argument("--max-turns", type=int, default=30)
    parser.add_argument("--max-tokens", type=int, default=100000)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--client-id")
    parser.add_argument("--callback-port", type=int)
    args = parser.parse_args()
    if args.max_price <= 0 or args.max_turns <= 0 or args.max_tokens <= 0 or args.timeout <= 0:
        parser.error("Les plafonds doivent être strictement positifs")
    if args.output.exists():
        parser.error("La preuve existe déjà ; aucun écrasement")
    cases = json.loads((ROOT / "tests/cas-plugin.json").read_text(encoding="utf-8"))
    case = next((x for x in cases if x["id"] == args.case), None)
    if case is None:
        parser.error("ID de scénario inconnu")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    evidence = {"date": datetime.now(timezone.utc).isoformat(), "case_id": args.case, "mode": args.mode,
                "plugin_commit": commit, "worktree_dirty": dirty,
                "case_sha256": hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest(),
                "skill_sha256": {n: hashlib.sha256((ROOT / "skills" / n / "SKILL.md").read_bytes()).hexdigest()
                                 for n in skill_names(ROOT)},
                "model_requested": args.model, "mcp_mode": case["mcp_mode"],
                "web_mode": case["web_mode"], "status": "blocked", "blockers": [], "trace": [],
                "invariants": {x: None for x in case["invariants"]},
                "human_legal_validation": False, "release_ready": False}
    try:
        version = importlib.metadata.version("mistral-vibe")
    except importlib.metadata.PackageNotFoundError:
        version = None
    evidence["vibe_version"] = version
    evidence["limits"] = {"price_usd": args.max_price, "turns": args.max_turns,
                          "tokens": args.max_tokens, "timeout_seconds": args.timeout}
    if version != SUPPORTED_VIBE:
        evidence["blockers"].append("vibe_2_26_0_required")
    if not os.environ.get("MISTRAL_API_KEY"):
        evidence["blockers"].append("mistral_api_key_not_available")
    if case["mcp_mode"] == "required" and version == SUPPORTED_VIBE:
        import keyring
        if type(keyring.get_keyring()).__module__ == "keyring.backends.fail":
            evidence["blockers"].append("oauth_keyring_unavailable")
    # Remove Vibe environment overrides; never read/copy any .env or credential store.
    for key in list(os.environ):
        if key.startswith("VIBE_"):
            del os.environ[key]
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="ct-vibe-campaign-") as temporary:
        base = Path(temporary)
        home, workspace = base / "home", base / "workspace"
        workspace.mkdir()
        text = config_text(ROOT, mcp=case["mcp_mode"] == "required", client_id=args.client_id,
                           port=args.callback_port, model=args.model)
        write_profile(home, text)
        os.environ["VIBE_HOME"] = str(home)
        os.environ["LOG_LEVEL"] = "CRITICAL"
        evidence["config_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        if version == SUPPORTED_VIBE:
            from vibe.core.config import VibeConfigSchema
            from vibe.core.config.harness_files import init_harness_files_manager
            init_harness_files_manager("user", "project")
            parsed = VibeConfigSchema.model_validate(tomllib.loads(text))
            model = parsed.get_active_model()
            evidence["model_config"] = model.model_dump(mode="json")
            evidence["model_serving_version_verified"] = False
            if model.alias != args.model:
                evidence["blockers"].append("unknown_model_alias")
            if model.input_price <= 0 or model.output_price <= 0:
                evidence["blockers"].append("model_price_not_configured")
        if not evidence["blockers"]:
            try:
                async def run():
                    return await asyncio.wait_for(execute(case, args.mode, workspace,
                        {"turns": args.max_turns, "price": args.max_price, "tokens": args.max_tokens},
                        evidence["trace"]), args.timeout)
                trace, metrics = asyncio.run(run())
                evidence["trace"], evidence["metrics"] = trace, metrics
                errors = technical_failures(trace, case, args.mode)
                evidence["technical_failures"] = errors
                evidence["status"] = ("interrupted" if metrics["stop_reason"] == "limit" else
                    "technical_failed" if errors else "technical_passed_pending_review")
            except Exception as error:
                evidence["status"] = "interrupted"
                evidence["error_type"] = type(error).__name__
                # No raw exception: provider errors may contain credentials or payloads.
    evidence["duration_seconds"] = round(time.monotonic() - started, 3)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(evidence, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"{args.case} / {args.mode}: {evidence['status']}")
    return 0 if evidence["status"] == "technical_passed_pending_review" else 2


if __name__ == "__main__":
    raise SystemExit(main())
