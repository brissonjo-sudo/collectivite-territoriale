"""Contrôle supplémentaire des sélections de références rejetées en v3 initial."""
import argparse
import hashlib
import json
from pathlib import Path
import run_codex_campaign as campaign

ROOT=campaign.ROOT


def sha(data):
    return hashlib.sha256(data).hexdigest()


def audit(evidence,commands):
    """N'admet une reclassification que si chaque sortie égale le segment figé."""
    events=json.loads(json.dumps(evidence['events']))
    verified=[]
    for index,event in enumerate(events):
        if event['type']!='unexpected_command':
            continue
        matches=[]
        for entry in commands:
            spec=campaign.read_reference_slice(entry['command'])
            if not spec:
                continue
            path=ROOT/'skills'/spec['path'].removeprefix('.agents/skills/')
            if not path.is_file() or event['exit_code']!=0 or event['status']!='completed':
                continue
            if sha(path.read_bytes()) != evidence['runtime_sha256'].get(path.relative_to(ROOT).as_posix()):
                raise ValueError('Référence différente du runtime mesuré')
            lines=path.read_text(encoding='utf-8').splitlines(keepends=True)
            content=''.join(lines[spec['start']:spec['start']+spec['count']])
            # Get-Content/Select-Object terminent chaque ligne par un LF.
            if content and not content.endswith('\n'):
                content+='\n'
            if sha(content.encode()) == event['output_sha256']:
                matches.append((entry,spec))
        if not matches:
            continue
        entry,spec=matches[0]
        verified.append({'event_index':index,'command':entry['command'],
            'source_rollout_sha256':entry['source_rollout_sha256'],
            'output_sha256':event['output_sha256'],'reference_slice':spec})
        event.update(type='native_read',paths=[spec['path']],complete_content_verified=[])
    case=next(c for c in campaign.load_cases() if c['id']==evidence['case_id'])
    errors=campaign.failures(events,case,evidence['process_exit'],evidence['profile'])
    return verified,errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir',type=Path,required=True)
    parser.add_argument('--commands',type=Path,required=True)
    args=parser.parse_args()
    directory=args.evidence_dir.resolve()
    if not directory.is_relative_to(ROOT/'tests/evidence'):
        raise ValueError('Dossier de preuves extérieur')
    extracted=json.loads(args.commands.read_text(encoding='utf-8'))
    records=[]
    for path in sorted(directory.glob('plugin-*.json')):
        evidence=json.loads(path.read_text(encoding='utf-8'))
        commands=extracted.get(evidence['case_id'],[])
        verified,errors=audit(evidence,commands)
        records.append({'case_id':evidence['case_id'],'evidence_sha256':sha(path.read_bytes()),
            'original_technical_status':evidence['technical_status'],
            'verified_technical_status':'failed' if errors else 'passed',
            'verified_reference_slices':verified,'remaining_failures':errors})
    result={'profile':'audit-selections-references-v1','execution_profile':campaign.PROFILE,
        'validator_sha256':sha(Path(campaign.__file__).read_bytes()),
        'auditor_sha256':sha(Path(__file__).read_bytes()),'commands_sha256':sha(args.commands.read_bytes()),
        'case_count':len(records),'verified_passed_count':sum(r['verified_technical_status']=='passed' for r in records),
        'runs':records,'human_legal_validation':False,'publication_ready':False,
        'scope':'Correction du rejet de lectures ciblées autorisées ; réponses et statuts initiaux conservés.'}
    (directory/'audit-lectures.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'cases':len(records),'verified_passed':result['verified_passed_count'],
        'reclassified_commands':sum(len(r['verified_reference_slices']) for r in records)}))


if __name__=='__main__':
    main()
