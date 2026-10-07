"""Retire les chemins personnels des réponses, avec originaux privés empreintés."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSONAL_RUNTIME = re.compile(r"[A-Za-z]:[/\\]Users[/\\][^\s)]*?[/\\](\.agents[/\\]skills[/\\][^\s)]+)")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def redact(data):
    """Ne change que les chemins absolus personnels vers le runtime natif."""
    bindings = []
    for index,event in enumerate(data["events"]):
        if event["type"] != "reply":
            continue
        original = event["text"]
        public,count = PERSONAL_RUNTIME.subn(lambda m:m.group(1).replace("\\","/"),original)
        if count:
            event["text"] = public
            bindings.append({"event_index":index,"replacement_count":count,
                "original_reply_sha256":digest(original.encode()),"public_reply_sha256":digest(public.encode())})
    return bindings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence",type=Path,required=True)
    parser.add_argument("--private-dir",type=Path,required=True)
    args = parser.parse_args()
    path,private = args.evidence.resolve(),args.private_dir.resolve()
    if not path.is_relative_to(ROOT/"tests/evidence") or private.is_relative_to(ROOT):
        raise ValueError("Preuve sous tests/evidence et originaux hors dépôt requis")
    original = path.read_bytes()
    data = json.loads(original)
    if "redaction" in data:
        print("[DÉJÀ ASSAINI] "+path.name)
        return
    bindings = redact(data)
    if not bindings:
        return
    private.mkdir(parents=True,exist_ok=True)
    preserved = private/(path.parent.name+"--"+path.name)
    if preserved.exists() and preserved.read_bytes() != original:
        raise ValueError("Original privé différent : refus d'écrasement")
    preserved.write_bytes(original)
    data["redaction"] = {"policy":"Chemin personnel absolu du runtime remplacé par son chemin relatif ; contenu métier conservé.",
        "original_evidence_sha256":digest(original),"redactor_sha256":digest(Path(__file__).read_bytes()),
        "reply_bindings":bindings,"original_preserved_outside_repository":True}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print("[ASSAINI] "+path.name)


if __name__ == "__main__":
    main()
