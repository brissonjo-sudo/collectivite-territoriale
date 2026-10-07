"""Extrait les seules lectures ciblées de nos sessions CLI identifiées."""
import argparse
from datetime import datetime,timedelta
import hashlib
import json
import re
from pathlib import Path
import run_codex_campaign as campaign


def commands(payload):
    if payload.get('name','').endswith('exec_command'):
        try: return [json.loads(payload.get('arguments','{}')).get('cmd','')]
        except ValueError: return []
    if payload.get('name')!='exec':
        return []
    result=[]
    for match in re.finditer(r'\bcmd\s*:\s*(["\'`])((?:\\.|(?!\1).)*?)\1',payload.get('input',''),re.S):
        quote,body=match.groups()
        if quote=='"':
            try: body=json.loads('"'+body+'"')
            except ValueError: continue
        else:
            body=body.replace('\\n','\n').replace('\\r','\r').replace('\\\\','\\').replace("\\'","'")
        result.append(body)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session-dir',type=Path,required=True)
    parser.add_argument('--evidence-dir',type=Path,required=True)
    args=parser.parse_args()
    directory=args.evidence_dir.resolve()
    if not directory.is_relative_to(campaign.ROOT/'tests/evidence'):
        raise ValueError('Dossier extérieur')
    cases={c['id']:c for c in campaign.load_cases()}
    proofs={p.stem:json.loads(p.read_text(encoding='utf-8')) for p in directory.glob('plugin-*.json')}
    ends={name:datetime.fromisoformat(p['completed_at']) for name,p in proofs.items()}
    result={name:[] for name in proofs}
    matched={name:0 for name in proofs}
    paths=sorted(args.session_dir.glob('*.jsonl'),key=lambda p:p.stat().st_mtime,reverse=True)[:32]
    for path in paths:
        with path.open(encoding='utf-8') as stream:
            first=json.loads(next(stream))
            meta=first.get('payload') or {}
            if 'ct-codex-campagne-' not in meta.get('cwd',''):
                continue
            start=datetime.fromisoformat(meta['timestamp'].replace('Z','+00:00'))
            eligible=[name for name,end in ends.items() if end-timedelta(seconds=420)<=start<=end]
            if not eligible:
                continue
            records=[json.loads(line) for line in stream if line.strip()]
        names=set()
        for row in records:
            item=row.get('payload') or {}
            if row.get('type')=='response_item' and item.get('type')=='message' and item.get('role')=='user':
                content='\n'.join(c.get('text','') for c in item.get('content',[]) if isinstance(c,dict))
                names.update(name for name in eligible if cases[name]['prompt'] in content)
        for name in names:
            matched[name]+=1
            for row in records:
                item=row.get('payload') or {}
                if row.get('type')!='response_item' or item.get('type') not in ('function_call','custom_tool_call'):
                    continue
                for command in commands(item):
                    if campaign.read_reference_slice(command):
                        result[name].append({'command':campaign.read_body(command),
                            'source_rollout_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    if any(count!=1 for count in matched.values()):
        raise ValueError('Identification non unique des sessions : '+str(matched))
    (directory/'diagnostic-lectures.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'sessions':len(matched),'reference_selections':sum(map(len,result.values()))}))


if __name__=='__main__':
    main()
