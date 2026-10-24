import json
import sys
from pathlib import Path
import numpy as np
import torch
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/'53-vla-continuous-actions/examples'))
from continuous import load_model,load_heads,make_policy
from scene import scene,observation,teacher

def geometric(x,l):return teacher(x[4:6],x[2*l:2*l+2])

def episode(policy,seed,delay=0,drop=0.,perturb=False,invalid=False,max_age=3):
    p,targets,l=scene(seed);rng=np.random.default_rng(seed+50000)
    queue=[];latest=None;stale=0;bad=0;path=[p.tolist()]
    for k in range(100):
        if perturb and k==2:p=np.clip(p+np.array([.3,-.25],dtype=np.float32),-1,1)
        if rng.random()>=drop:queue.append((k+delay,k,observation(p,targets)))
        ready=[packet for packet in queue if packet[0]<=k]
        queue=[packet for packet in queue if packet[0]>k]
        if ready:latest=max(ready,key=lambda packet:packet[1])
        if latest is None or k-latest[1]>max_age:
            a=np.zeros(2);stale+=1
        else:
            a=np.asarray(policy(latest[2],l))
            if invalid and k==5:a=np.array([np.nan,0.])
            if a.shape!=(2,) or not np.isfinite(a).all():a=np.zeros(2);bad+=1
            a=np.clip(a,-.5,.5)
        p=np.clip(p+.1*a,-1,1).astype(np.float32);path.append(p.tolist())
        if np.linalg.norm(p-targets[l])<.09:break
    return dict(seed=seed,success=bool(np.linalg.norm(p-targets[l])<.09),steps=k+1,stale_stops=stale,invalid_actions=bad,path=path)

if __name__=='__main__':
    torch.set_num_threads(1);body=load_model();reg,_=load_heads()
    policies={'geometric':geometric,'regression':make_policy(body,reg,'regression')}
    conditions={'normal':{},'delay2':{'delay':2},'drop30':{'drop':.3},'mixed':{'delay':2,'drop':.3,'perturb':True},'stale5':{'delay':5},'invalid':{'invalid':True}}
    report={}
    for name,policy in policies.items():
        report[name]={}
        for condition,kwargs in conditions.items():
            rows=[episode(policy,s,**kwargs) for s in range(300,340)]
            score={key:float(np.mean([row[key] for row in rows])) for key in ['success','steps','stale_stops','invalid_actions']}
            report[name][condition]={'summary':score,'episodes':rows};print(name,condition,score,flush=True)
    out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,indent=2))
