import copy
import json
import sys
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"52-vla-discrete-actions/examples"))
from train_vla import load_model,policy_for,summary
from scene import collect,run
OUT=Path(__file__).resolve().parent/"output"
def regression():return nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,2),nn.Tanh())
def flow_network():return nn.Sequential(nn.Linear(67,64),nn.SiLU(),nn.Linear(64,64),nn.SiLU(),nn.Linear(64,2))
def load_heads():
    checkpoint=torch.load(OUT/"heads.pt",weights_only=True,map_location="cpu");reg=regression();flow=flow_network();reg.load_state_dict(checkpoint["regression"]);flow.load_state_dict(checkpoint["flow"]);reg.eval();flow.eval();return reg,flow

def make_policy(body,head,kind,seed=7,steps=16):
    rng=torch.Generator().manual_seed(seed)
    def policy(x,l):
        with torch.no_grad():
            context=body.features(torch.tensor(x)[None],torch.tensor([l]))
            if kind=="regression":return (.5*head(context))[0].numpy()
            z=torch.randn(1,2,generator=rng)
            for k in range(steps):z=z+head(torch.cat([z,context,torch.full((1,1),k/steps)],1))/steps
            return (.5*z.clamp(-1,1))[0].numpy()
    return policy

if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);body=load_model();body.requires_grad_(False)
    x,l,_,a=collect(range(160));vx,vl,_,va=collect(range(200,220))
    with torch.no_grad():
        context=body.features(torch.tensor(x),torch.tensor(l));vc=body.features(torch.tensor(vx),torch.tensor(vl))
    a=torch.tensor(a)/.5;va=torch.tensor(va)/.5
    reg=regression();flow=flow_network();opts=[torch.optim.Adam(h.parameters(),lr=.003) for h in (reg,flow)]
    val_rng=torch.Generator().manual_seed(101);vz=torch.randn(va.shape,generator=val_rng);vt=torch.rand(len(va),1,generator=val_rng)
    best=[float("inf"),float("inf")];states=[None,None];best_steps=[None,None]
    for step in range(1,1001):
        idx=torch.randint(len(a),(128,));real=a[idx];z=torch.randn_like(real);t=torch.rand(128,1)
        losses=[F.mse_loss(reg(context[idx]),real),F.mse_loss(flow(torch.cat([(1-t)*z+t*real,context[idx],t],1)),real-z)]
        for opt,loss in zip(opts,losses):opt.zero_grad();loss.backward();opt.step()
        if step%100==0:
            with torch.no_grad():values=[float(F.mse_loss(reg(vc),va)),float(F.mse_loss(flow(torch.cat([(1-vt)*vz+vt*va,vc,vt],1)),va-vz))]
            for i,value in enumerate(values):
                if value<best[i]:best[i]=value;states[i]=copy.deepcopy((reg,flow)[i].state_dict());best_steps[i]=step
    reg.load_state_dict(states[0]);flow.load_state_dict(states[1]);OUT.mkdir(exist_ok=True);torch.save({"regression":reg.state_dict(),"flow":flow.state_dict()},OUT/"heads.pt")
    report={"best_steps":best_steps,"groups":{}}
    for held in (False,True):
        group={}
        for name in ("discrete","regression","flow4","flow16"):
            rows=[];times=[]
            for seed in range(300,340):
                if name=="discrete":policy=policy_for(body)
                else:policy=make_policy(body,reg if name=="regression" else flow,"regression" if name=="regression" else "flow",seed+1000,4 if name=="flow4" else 16)
                def timed(x,l):
                    start=time.perf_counter();value=policy(x,l);times.append((time.perf_counter()-start)*1000);return value
                rows.append(run(timed,seed,held))
            score=summary(rows);score["mean_policy_ms"]=float(np.mean(times));group[name]=score
            print("held",held,name,score["success_rate"],score["mean_steps"],score["mean_policy_ms"],flush=True)
        report["groups"]["held" if held else "seen"]=group
    (OUT/"report.json").write_text(json.dumps(report,indent=2))
