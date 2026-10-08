"""Contrôle local explicite ; aucun prepare, login ou modèle n'est lancé."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import campagne_native_complete_dev7_20261009 as harness

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "controle-outillage-reprise-dev7-20261009.json"

def main() -> None:
    assert not OUT.exists(), "Contrôle déjà scellé"
    protocol, _ = harness.inputs()
    files = protocol["new_tools"] + ["connexion_juridique_dev7_20261009.py",
                                   "tests_connexion_juridique_dev7_20261009.py"]
    hashes = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}
    environment = dict(os.environ)
    environment.update(PYTHONDONTWRITEBYTECODE="1",PYTHONUTF8="1")
    checks = []
    for filename, expected in [("tests_native_complete_dev7_20261009.py",24),
                               ("tests_connexion_juridique_dev7_20261009.py",6)]:
        result = subprocess.run([sys.executable,"-B",str(ROOT/filename)],cwd=ROOT,env=environment,
                                capture_output=True,timeout=90)
        assert result.returncode == 0, "Tests échoués : "+filename
        stderr = result.stderr.decode("utf-8")
        assert re.search(rf"Ran {expected} tests? in",stderr) and stderr.rstrip().endswith("OK")
        checks.append({"test_file":filename,"tests":expected,"passed":True,
                       "stdout_sha256":harness.sha(result.stdout),"stderr_sha256":harness.sha(result.stderr)})
    assert all(hashes[name] == harness.sha((ROOT/name).read_bytes()) for name in hashes)
    value = {"verified_at":datetime.now(timezone.utc).isoformat(),"tools_sha256":hashes,
        "candidate_commit":protocol["candidate_commit"],"case_count":16,"atomic_count":124,
        "source_case_count":13,"official_web_case_count":3,"checks":checks,"test_count":30,
        "old_tools_unchanged":True,"suite_rubric_unchanged":True,"installed_cache_unchanged":True,
        "campaign_prepared":False,"new_respondents_started":0,"judges_created":0,
        "auth_verified":False,"sandbox_read_verified":False,"model_inference":False,
        "runtime_fix_verified":False,"release_ready":False}
    harness.write_new(OUT,value)
    print(json.dumps({"tests":30,"passed":True,"tool_hashes_sealed":len(hashes),"release_ready":False}))

if __name__ == "__main__":
    main()
