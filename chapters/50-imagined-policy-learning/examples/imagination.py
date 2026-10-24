import json
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"47-learned-dynamics/examples"))
from dynamics import load_model,TabletopEnv
class Actor(nn.Module):
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Linear(4,64),nn.Tanh(),nn.Linear(64,64),nn.Tanh(),nn.Linear(64,2),nn.Tanh())
    def forward(self,obs):return .5*self.net(obs)

def evaluate(actor,model):
    rows=[]
    with torch.no_grad():
        for seed in range(200,220):
            env=TabletopEnv();obs,_=env.reset(seed=seed);total=0.;done=False
            for step in range(100):
                state=torch.tensor(obs);action=actor(state)
                if model is None:
                    obs,reward,done,truncated,_=env.step(action.numpy())
                else:
                    pos=model(state[:2],action).numpy();obs=np.concatenate([pos,obs[2:]]).astype(np.float32)
                    distance=float(np.linalg.norm(obs[:2]-obs[2:]));reward=-distance;done=distance<.05;truncated=step==99 and not done
                total+=reward
                if done or truncated:break
            rows.append([done,total,step+1])
    return {"success_rate":float(np.mean([r[0] for r in rows])),"mean_return":float(np.mean([r[1] for r in rows])),"mean_steps":float(np.mean([r[2] for r in rows]))}
if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);model=load_model();model.requires_grad_(False)
    original={k:v.clone() for k,v in model.state_dict().items()};actor=Actor();opt=torch.optim.Adam(actor.parameters(),lr=.003)
    starts=torch.tensor(np.stack([TabletopEnv().reset(seed=s)[0] for s in range(80)]))
    report={"before":{"imagined":evaluate(actor,model),"real":evaluate(actor,None)}}
    for update in range(500):
        obs=starts[torch.randint(len(starts),(64,))];position=obs[:,:2];goal=obs[:,2:];loss=0.
        for _ in range(15):
            action=actor(torch.cat([position,goal],1));position=model(position,action)
            loss=loss+((position-goal).square().sum(-1)+.01*action.square().sum(-1)).mean()/15
        opt.zero_grad();loss.backward()
        if update==0:assert sum(float(p.grad.abs().sum()) for p in actor.parameters())>0
        opt.step()
    assert all(torch.equal(original[k],v) for k,v in model.state_dict().items())
    report["after"]={"imagined":evaluate(actor,model),"real":evaluate(actor,None)}
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True);torch.save(actor.state_dict(),folder/"actor.pt");(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
