import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'chapters/53-vla-continuous-actions/examples/output/report.json'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if __name__=='__main__':
    report=json.loads(SOURCE.read_text());result={}
    for group in ['seen','held']:
        a=report['groups'][group]['flow4']['episodes'];b=report['groups'][group]['flow16']['episodes']
        assert [x['seed'] for x in a]==[x['seed'] for x in b]
        counts={key:0 for key in ['both_success','only4','only16','both_fail']}
        for x,y in zip(a,b):
            key='both_success' if x['success'] and y['success'] else 'only4' if x['success'] else 'only16' if y['success'] else 'both_fail'
            counts[key]+=1
        result[group]={'pairs':len(a),'counts':counts,'success_difference':(counts['only16']-counts['only4'])/len(a)}
    paths=[SOURCE,ROOT/'chapters/53-vla-continuous-actions/examples/continuous.py',ROOT/'chapters/53-vla-continuous-actions/examples/output/heads.pt',ROOT/'chapters/52-vla-discrete-actions/examples/output/discrete.pt',Path(__file__).resolve()]
    result['sha256']={str(p.relative_to(ROOT)):digest(p) for p in paths}
    result['scope']='Reanalysis of existing chapter 53 outputs; no new training or independent rerun.'
    out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True)
    (out/'reproduction.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
