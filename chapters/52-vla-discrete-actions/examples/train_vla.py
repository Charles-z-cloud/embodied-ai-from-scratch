import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from scene import ACTIONS,collect,run
OUT=Path(__file__).resolve().parent/"output"
class VLA(nn.Module):
    def __init__(self):
        super().__init__();self.language=nn.Embedding(2,4);self.trunk=nn.Sequential(nn.Linear(10,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU());self.head=nn.Linear(64,9)
    def features(self,x,l):return self.trunk(torch.cat([x,self.language(l)],-1))
    def forward(self,x,l):return self.head(self.features(x,l))
def load_model():
    model=VLA();model.load_state_dict(torch.load(OUT/"discrete.pt",weights_only=True,map_location="cpu"));model.eval();return model

def policy_for(model):
    def policy(x,l):
        with torch.no_grad():return ACTIONS[int(model(torch.tensor(x)[None],torch.tensor([l])).argmax(-1))]
    return policy

def summary(rows):return {"success_rate":float(np.mean([r["success"] for r in rows])),"mean_steps":float(np.mean([r["steps"] for r in rows])),"episodes":rows}
if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7)
    x,l,y,_=collect(range(160));vx,vl,vy,_=collect(range(200,220))
    x,l,y=torch.tensor(x),torch.tensor(l),torch.tensor(y);vx,vl,vy=torch.tensor(vx),torch.tensor(vl),torch.tensor(vy)
    model=VLA();opt=torch.optim.Adam(model.parameters(),lr=.003);best=float("inf")
    for step in range(1,1001):
        idx=torch.randint(len(x),(128,));loss=F.cross_entropy(model(x[idx],l[idx]),y[idx]);opt.zero_grad();loss.backward();opt.step()
        if step%100==0:
            with torch.no_grad():value=float(F.cross_entropy(model(vx,vl),vy))
            if value<best:best=value;state=copy.deepcopy(model.state_dict());best_step=step
    model.load_state_dict(state);OUT.mkdir(exist_ok=True);torch.save(model.state_dict(),OUT/"discrete.pt");policy=policy_for(model);report={"best_step":best_step,"groups":{}}
    for held in (False,True):
        tx,tl,ty,_=collect(range(300,340),held)
        with torch.no_grad():accuracy=float((model(torch.tensor(tx),torch.tensor(tl)).argmax(-1)==torch.tensor(ty)).float().mean())
        key="held" if held else "seen";report["groups"][key]={"offline_action_accuracy":accuracy}
        for mode in ("normal","black","swap_language"):
            rows=[run(policy,seed,held,mode) for seed in range(300,340)];result=summary(rows);report["groups"][key][mode]=result
            print(key,mode,result["success_rate"],result["mean_steps"],flush=True)
    (OUT/"report.json").write_text(json.dumps(report,indent=2));print("best step",best_step)
