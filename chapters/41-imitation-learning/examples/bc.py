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
from tabletop_env import TabletopEnv,controller
OUT=Path(__file__).resolve().parent/"output"
class Policy(nn.Module):
    def __init__(self,mean,scale):
        super().__init__();self.register_buffer("mean",mean);self.register_buffer("scale",scale)
        self.net=nn.Sequential(nn.Linear(4,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU(),nn.Linear(64,2),nn.Tanh())
    def forward(self,x):return .5*self.net((x-self.mean)/self.scale)

def demonstrations(seeds):
    observations,actions,episodes=[],[],[]
    for seed in seeds:
        env=TabletopEnv();obs,_=env.reset(seed=seed);count=0
        while True:
            action=controller(obs);observations.append(obs.copy());actions.append(action.copy());count+=1
            obs,_,done,truncated,_=env.step(action)
            if done or truncated:break
        episodes.append({"seed":seed,"samples":count})
    return torch.tensor(np.stack(observations)),torch.tensor(np.stack(actions)),episodes

def load_policy():
    ckpt=torch.load(OUT/"bc.pt",weights_only=True,map_location="cpu")
    model=Policy(ckpt["state"]["mean"],ckpt["state"]["scale"]);model.load_state_dict(ckpt["state"]);model.eval()
    def act(obs):
        with torch.no_grad():return model(torch.as_tensor(obs,dtype=torch.float32)).numpy()
    return act

def rollout(policy,seed,perturb=False):
    env=TabletopEnv();obs,_=env.reset(seed=seed);total=0.
    for step in range(env.max_steps):
        if perturb and step==2:
            env.position=np.clip(env.position+np.array([.35,-.25]),-1,1);obs=env.observation()
        obs,reward,done,truncated,info=env.step(policy(obs));total+=reward
        if done or truncated:break
    return {"seed":seed,"success":done,"steps":env.steps,"return":total,"distance":info["distance"]}

def main():
    torch.set_num_threads(1);torch.manual_seed(7)
    x,y,train_info=demonstrations(range(80));vx,vy,val_info=demonstrations(range(100,120));tx,ty,test_info=demonstrations(range(200,220))
    model=Policy(x.mean(0),x.std(0,unbiased=False).clamp_min(.001));opt=torch.optim.Adam(model.parameters(),lr=.003)
    best=float("inf");history=[]
    for step in range(1,601):
        idx=torch.randint(len(x),(128,));loss=F.mse_loss(model(x[idx]),y[idx]);opt.zero_grad();loss.backward();opt.step()
        if step%50==0:
            with torch.no_grad():value=F.mse_loss(model(vx),vy).item()
            history.append([step,value])
            if value<best:best=value;state=copy.deepcopy(model.state_dict());best_step=step
    model.load_state_dict(state);OUT.mkdir(exist_ok=True)
    torch.save({"state":model.state_dict()},OUT/"bc.pt")
    with torch.no_grad():test_mse=F.mse_loss(model(tx),ty).item()
    report={"test_action_mse":test_mse,"best_step":best_step,"validation":history,"splits":{"train":train_info,"validation":val_info,"test":test_info},"closed_loop":{}}
    learned=load_policy()
    for name,policy in [("teacher",controller),("BC",learned)]:
        for perturb in (False,True):
            rows=[rollout(policy,seed,perturb) for seed in range(200,220)]
            report["closed_loop"][f"{name}_perturb_{perturb}"]={"success_rate":float(np.mean([r["success"] for r in rows])),"mean_steps":float(np.mean([r["steps"] for r in rows])),"episodes":rows}
    (OUT/"report.json").write_text(json.dumps(report,indent=2))
    print("test MSE",test_mse,"best_step",best_step)
    for name,value in report["closed_loop"].items():print(name,value["success_rate"],value["mean_steps"])
if __name__=="__main__":main()
