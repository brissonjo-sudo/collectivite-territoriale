"""Connexion interactive officielle, à déclencher explicitement une fois.

Ce compagnon ne lance ni campagne, ni modèle, ni installation. Le CLI gère
ses identifiants ; le script ne les lit pas et ne les copie pas.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import time
from urllib.parse import urlsplit
import uuid
import campagne_native_complete_dev7_20261009 as campaign

PROVIDER = "dev-7soa32jfmxpejzhs.eu.auth0.com"

def validate_authorization_url(value: object) -> str:
    if not isinstance(value, str) or len(value) > 16_384 or any(ord(c) < 32 for c in value):
        raise campaign.GateError("URL officielle absente ou malformée")
    url = urlsplit(value)
    campaign.require(url.scheme == "https" and url.hostname == PROVIDER
                     and url.port in (None,443) and url.username is None and url.password is None,
                     "Origine OAuth différente : arrêt avant ouverture")
    return value

def safe_error(value: object) -> dict | None:
    if value is None:
        return None
    message = str(value)
    return {"message_exported":False,"message_sha256":campaign.sha(message.encode()),
            "markers":[s for s in ("timeout","timed out","Auth required","invalid_client","access_denied")
                       if s.casefold() in message.casefold()]}

def completion(params: dict, started: dict) -> dict:
    campaign.require(params.get("name") == "droit-francais", "Notification d'un autre serveur")
    if started.get("loginId") is not None:
        campaign.require(started["loginId"] == params.get("loginId"), "Notification d'une autre connexion")
    campaign.require(type(params.get("success")) is bool, "Statut de connexion absent ou malformé")
    campaign.require(not params["success"] or params.get("error") is None,
                     "Statut de connexion contradictoire")
    return {"completed":True,"success":params["success"],"error":safe_error(params.get("error"))}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ouvrir", action="store_true", required=True,
                        help="Déclenche une connexion interactive dans le navigateur")
    parser.parse_args()
    protocol, r3 = campaign.inputs()
    case = next(c for c in protocol["cases"] if c["source_requirements_unchanged"]["mcp_mode"] == "required"
                and c["source_requirements_unchanged"]["web_mode"] == "disabled")
    folder = campaign.destination(campaign.ROOT / ("connexion-juridique-dev7-" +
        datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]))
    folder.mkdir()
    (folder / "workspace").mkdir()
    config_before = (campaign.STATE / "config.toml").read_bytes()
    env, _ = campaign.environment()
    client = None
    receipt = {"started_at":campaign.now(),"completed":False,"model_inference":False,
               "auth_secrets_read":False,"automatic_retry":False,"oauth_login_attempted":False,
               "browser_opened":False,"release_ready":False}
    try:
        client = campaign.Client(Path(protocol["cli"]),folder/"workspace",campaign.overrides(protocol,case),env)
        client.initialized()
        config = client.request("config/read", {"includeLayers":False})
        campaign.configuration_check(config["config"],protocol,case)
        receipt["oauth_login_attempted"] = True
        result = client.request("mcpServer/oauth/login", {"name":"droit-francais","timeoutSecs":600},timeout=40)
        authorization_url = validate_authorization_url(result.get("authorizationUrl"))
        campaign.write_new(folder/"autorisation.private.json",result)
        os.startfile(authorization_url)
        receipt["browser_opened"] = True
        print("Connexion juridique ouverte dans le navigateur. Terminer la connexion ; délai de 10 minutes.",flush=True)
        deadline = time.monotonic() + 600
        while time.monotonic() < deadline:
            try:
                message = client.messages.get(timeout=min(30,max(.01,deadline-time.monotonic())))
            except queue.Empty:
                continue
            campaign.require(not any(message.get(k) for k in ("server_eof","capture_limit","invalid_jsonl")),
                             "Connexion officielle interrompue")
            if message.get("method") == "mcpServer/oauthLogin/completed":
                params = message.get("params",{})
                receipt.update(completion(params,result))
                break
        if not receipt["completed"]:
            receipt["flow_timeout"] = True
    except (OSError,ValueError,queue.Empty,KeyError) as error:
        receipt.update(error_type=type(error).__name__,error=safe_error(error))
    finally:
        if client:
            client.close()
        receipt.update(completed_at=campaign.now(),
            configuration_file_unchanged=(campaign.STATE/"config.toml").read_bytes()==config_before,
            candidate_cache_unchanged=campaign.inventory(Path(protocol["installed_path"]))==r3["installed_files"])
        campaign.write_new(folder/"resultat-assaini.json",receipt)
    print(json.dumps({**receipt,"receipt":str(folder/"resultat-assaini.json")},ensure_ascii=False))
    raise SystemExit(0 if receipt.get("success") and receipt["configuration_file_unchanged"]
                     and receipt["candidate_cache_unchanged"] else 2)

if __name__ == "__main__":
    main()
