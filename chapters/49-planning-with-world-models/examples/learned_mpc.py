import json
import sys
from pathlib import Path
import numpy as np
import torch
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"47-learned-dynamics/examples"))
from dynamics import load_model,TabletopEnv
class ModelPlanner:
    def __init__(self,model,horizon,seed):
        self.model=model;self.horizon=horizon;self.rng=torch.Generator().manual_seed(seed);self.mean=torch.zeros(horizon,2)
    def cost(self,actions,obs):
        p=torch.tensor(obs[:2]).repeat(len(actions),1);g=torch.tensor(obs[2:]);total=torch.zeros(len(actions))
        for k in range(self.horizon):
            p=(p+.1*actions[:,k]).clamp(-1,1) if self.model is None else self.model(p,actions[:,k])
            total+=((p-g)**2).sum(-1)+.01*actions[:,k].square().sum(-1)
        return total+5*((p-g)**2).sum(-1)
    def __call__(self,obs):
        mean=self.mean.clone();std=torch.full_like(mean,.3);best_cost=float("inf")
        with torch.no_grad():
            for _ in range(3):
                actions=(mean+std*torch.randn(128,self.horizon,2,generator=self.rng)).clamp(-.5,.5)
                values=self.cost(actions,obs);elite=actions[values.argsort()[:16]]
                mean=elite.mean(0);std=elite.std(0,unbiased=False).clamp_min(.05);index=int(values.argmin())
                if float(values[index])<best_cost:best_cost=float(values[index]);best=actions[index].clone()
        self.mean=torch.cat([best[1:],torch.zeros(1,2)]);return best[0].numpy()

if __name__=="__main__":
    torch.set_num_threads(1);model=load_model();report={}
    settings=[(h,False) for h in (3,10,20)]+[(10,True)]
    for horizon,perturb in settings:
        for kind in ("known","learned"):
            results=[];errors=[];outside=[]
            for seed in range(200,220):
                env=TabletopEnv();obs,_=env.reset(seed=seed);planner=ModelPlanner(None if kind=="known" else model,horizon,seed+1000)
                for step in range(100):
                    if perturb and step==2:env.position=np.clip(env.position+[.35,-.25],-1,1);obs=env.observation()
                    action=planner(obs);outside.append(bool(np.any(np.abs(action)>.3)))
                    with torch.no_grad():predicted=model(torch.tensor(obs[:2]),torch.tensor(action)).numpy()
                    obs,_,done,truncated,_=env.step(action);errors.append(float(np.mean((predicted-obs[:2])**2)))
                    if done or truncated:break
                results.append([done,env.steps])
            score={"success_rate":float(np.mean([r[0] for r in results])),"mean_steps":float(np.mean([r[1] for r in results])),"executed_prediction_mse":float(np.mean(errors)),"outside_training_action_fraction":float(np.mean(outside))}
            report[f"{kind}_H{horizon}_perturb{perturb}"]=score;print(kind,horizon,perturb,score,flush=True)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True);(folder/"report.json").write_text(json.dumps(report,indent=2))
