import copy
import json
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"37-simulation-and-environment-api/examples"))
from tabletop_env import TabletopEnv
OUT=Path(__file__).resolve().parent/"output"
class Dynamics(nn.Module):
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Linear(4,64),nn.Tanh(),nn.Linear(64,64),nn.Tanh(),nn.Linear(64,2))
    def forward(self,p,a):return (p+.1*self.net(torch.cat([p,a],-1))).clamp(-1,1)

def collect(seeds,limit):
    trajectories=[]
    for seed in seeds:
        env=TabletopEnv();obs,_=env.reset(seed=seed);rng=np.random.default_rng(seed+1000);rows=[]
        for _ in range(25):
            action=rng.uniform(-limit,limit,2).astype(np.float32);before=obs[:2].copy()
            obs,_,done,truncated,_=env.step(action);rows.append([before.tolist(),action.tolist(),obs[:2].tolist()])
            if done or truncated:break
        trajectories.append({"seed":seed,"rows":rows})
    return trajectories

def flatten(trajectories):
    array=np.array([row for trajectory in trajectories for row in trajectory["rows"]],dtype="float32")
    return tuple(torch.tensor(array[:,i]) for i in range(3))
def load_model():
    model=Dynamics();model.load_state_dict(torch.load(OUT/"dynamics.pt",weights_only=True,map_location="cpu"));model.eval();return model

def evaluate(model,trajectories):
    p,a,target=flatten(trajectories)
    with torch.no_grad():
        report={"one_step_mse":float(F.mse_loss(model(p,a),target)),"persistence_mse":float(F.mse_loss(p,target)),"rollout":{}}
        for horizon in (1,5,10,20):
            errors=[]
            for trajectory in trajectories:
                rows=trajectory["rows"]
                if len(rows)<horizon:continue
                predicted=torch.tensor(rows[0][0],dtype=torch.float32)
                for row in rows[:horizon]:predicted=model(predicted,torch.tensor(row[1],dtype=torch.float32))
                errors.append(float(F.mse_loss(predicted,torch.tensor(rows[horizon-1][2]))))
            report["rollout"][str(horizon)]={"mse":float(np.mean(errors)),"trajectories":len(errors)}
    return report
if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7)
    splits={"train":collect(range(80),.3),"validation":collect(range(100,120),.3),"test":collect(range(200,220),.3),"ood":collect(range(300,320),.5)}
    p,a,target=flatten(splits["train"]);vp,va,vt=flatten(splits["validation"])
    model=Dynamics();opt=torch.optim.Adam(model.parameters(),lr=.003);best=float("inf");history=[]
    for step in range(1,1001):
        idx=torch.randint(len(p),(128,));loss=F.mse_loss(model(p[idx],a[idx]),target[idx]);opt.zero_grad();loss.backward();opt.step()
        if step%50==0:
            with torch.no_grad():value=float(F.mse_loss(model(vp,va),vt))
            history.append([step,value])
            if value<best:best=value;state=copy.deepcopy(model.state_dict());best_step=step
    model.load_state_dict(state);OUT.mkdir(exist_ok=True);torch.save(model.state_dict(),OUT/"dynamics.pt")
    report={"best_step":best_step,"validation":history,"test":evaluate(model,splits["test"]),"ood":evaluate(model,splits["ood"])}
    (OUT/"trajectories.json").write_text(json.dumps(splits));(OUT/"report.json").write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!="validation"})
