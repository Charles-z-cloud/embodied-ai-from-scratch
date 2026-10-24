import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

def data(seed,n):
    rng=np.random.default_rng(seed);x=rng.uniform(-.5,.5,n);v=rng.uniform(-.05,.05,n);actions=rng.uniform(-.03,.03,(n,12))
    inputs=[];targets=[]
    for t in range(12):
        visible=not 3<=t<=7
        inputs.append(np.stack([x if visible else np.zeros(n),np.full(n,float(visible)),actions[:,t]],1))
        x=x+v+actions[:,t];targets.append(x.copy())
    return torch.tensor(np.stack(inputs,1),dtype=torch.float32),torch.tensor(np.stack(targets,1),dtype=torch.float32)
class Memory(nn.Module):
    def __init__(self):
        super().__init__();self.gru=nn.GRU(3,32,batch_first=True);self.head=nn.Linear(32,1)
    def forward(self,x):return self.head(self.gru(x)[0]).squeeze(-1)
class Stateless(nn.Module):
    def __init__(self):super().__init__();self.net=nn.Sequential(nn.Linear(3,32),nn.Tanh(),nn.Linear(32,1))
    def forward(self,x):return self.net(x).squeeze(-1)

def score(predicted,target):
    return {"all_mse":float(F.mse_loss(predicted,target)),"occluded_mse":float(F.mse_loss(predicted[:,3:8],target[:,3:8]))}
if __name__=="__main__":
    torch.set_num_threads(1);x,y=data(100,512);vx,vy=data(101,128);tx,ty=data(102,128)
    free=tx.clone();free[:,3:,:2]=0.;report={}
    for name,cls in [("single_frame",Stateless),("GRU",Memory)]:
        torch.manual_seed(7);model=cls();opt=torch.optim.Adam(model.parameters(),lr=.003);best=float("inf")
        for step in range(1,1001):
            idx=torch.randint(len(x),(32,));loss=F.mse_loss(model(x[idx]),y[idx]);opt.zero_grad();loss.backward();opt.step()
            if step%100==0:
                with torch.no_grad():value=float(F.mse_loss(model(vx),vy))
                if value<best:best=value;state=copy.deepcopy(model.state_dict());best_step=step
        model.load_state_dict(state);model.eval()
        with torch.no_grad():
            report[name]={"test":score(model(tx),ty),"no_future_observations":score(model(free),ty),"best_step":best_step,"parameters":sum(p.numel() for p in model.parameters())}
    predicted=[];position=torch.zeros(len(tx))
    for t in range(12):
        position=torch.where(tx[:,t,1]>0,tx[:,t,0],position)+tx[:,t,2];predicted.append(position.clone())
    report["last_seen_plus_actions"]=score(torch.stack(predicted,1),ty)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True);(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
