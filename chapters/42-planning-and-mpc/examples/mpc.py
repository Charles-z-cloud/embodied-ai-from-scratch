import json
import sys
import time
from pathlib import Path
import numpy as np
import torch
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"41-imitation-learning/examples"))
from bc import load_policy,controller,TabletopEnv

def costs(actions,obs):
    position=np.repeat(obs[None,:2],len(actions),axis=0).astype(float);goal=obs[2:];total=np.zeros(len(actions))
    for t in range(actions.shape[1]):
        position=np.clip(position+.1*actions[:,t],-1,1)
        total+=np.sum((position-goal)**2,axis=1)+.01*np.sum(actions[:,t]**2,axis=1)
    return total+5*np.sum((position-goal)**2,axis=1)

class Planner:
    def __init__(self,kind,seed):
        self.kind=kind;self.rng=np.random.default_rng(seed);self.mean=np.zeros((10,2))
    def __call__(self,obs):
        if self.kind=="shooting":
            candidates=self.rng.uniform(-.5,.5,(384,10,2));return candidates[costs(candidates,obs).argmin(),0].astype(np.float32)
        mean=self.mean.copy();std=np.full((10,2),.3);best_cost=float("inf");best=None
        for _ in range(3):
            candidates=np.clip(self.rng.normal(mean,std,(128,10,2)),-.5,.5);values=costs(candidates,obs)
            elite=candidates[np.argsort(values)[:16]];mean=elite.mean(0);std=np.maximum(elite.std(0),.05)
            index=values.argmin()
            if values[index]<best_cost:best_cost=values[index];best=candidates[index].copy()
        self.mean=np.concatenate([best[1:],np.zeros((1,2))]);return best[0].astype(np.float32)

def main():
    torch.set_num_threads(1);bc=load_policy();report={}
    for kind in ("feedback","BC","shooting","CEM"):
        for perturb in (False,True):
            results=[];times=[]
            for seed in range(200,220):
                policy=controller if kind=="feedback" else bc if kind=="BC" else Planner(kind,seed+1000)
                env=TabletopEnv();obs,_=env.reset(seed=seed)
                for step in range(100):
                    if perturb and step==2:env.position=np.clip(env.position+[.35,-.25],-1,1);obs=env.observation()
                    start=time.perf_counter();action=policy(obs);times.append((time.perf_counter()-start)*1000)
                    obs,_,done,truncated,_=env.step(action)
                    if done or truncated:break
                results.append([bool(done),env.steps])
            score={"success_rate":float(np.mean([r[0] for r in results])),"mean_steps":float(np.mean([r[1] for r in results])),"mean_ms":float(np.mean(times)),"p95_ms":float(np.percentile(times,95)),"episodes":results}
            report[f"{kind}_perturb_{perturb}"]=score;print(kind,perturb,{k:v for k,v in score.items() if k!="episodes"},flush=True)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True);(folder/"report.json").write_text(json.dumps(report,indent=2))
if __name__=="__main__":main()
