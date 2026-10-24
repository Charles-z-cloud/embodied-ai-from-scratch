import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

def data(seed,n):
    rng=np.random.default_rng(seed);g=np.column_stack([rng.uniform(.8,1.2,n),rng.uniform(-.1,.1,n)]).astype("float32")
    h=rng.uniform(.35,.55,n).astype("float32");goals=np.repeat(g,2,axis=0)
    middle=goals/2;middle[:,1]+=np.repeat(h,2)*np.tile([1,-1],n)
    actions=np.stack([middle,goals-middle],1).astype("float32")
    return torch.tensor(goals),torch.tensor(actions)

def mlp(inputs,outputs):return nn.Sequential(nn.Linear(inputs,64),nn.SiLU(),nn.Linear(64,64),nn.SiLU(),nn.Linear(64,outputs))
def collision(a,b,c,r=.18):
    d=b-a;t=np.clip(np.dot(c-a,d)/max(np.dot(d,d),1e-12),0,1)
    return np.linalg.norm(a+t*d-c)<r

def judge(path,goal):
    hit=any(collision(a,b,goal/2) for a,b in zip(path[:-1],path[1:]))
    return bool(not hit and np.linalg.norm(path[-1]-goal)<.12),bool(hit)

def generate(flow,goals,noise):
    x=noise.clone()
    with torch.no_grad():
        for k in range(32):x=x+flow(torch.cat([x,goals,torch.full((len(x),1),k/32)],1))/32
    return x.reshape(-1,2,2)

if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);g,a=data(100,256)
    positions=torch.stack([torch.zeros_like(g),a[:,0]],1)
    obs=torch.cat([positions,g[:,None,:].expand(-1,2,-1)],2).reshape(-1,4);labels=a.reshape(-1,2)
    bc,chunk,flow=mlp(4,2),mlp(2,4),mlp(7,4)
    optimizers=[torch.optim.Adam(m.parameters(),lr=.003) for m in (bc,chunk,flow)]
    for step in range(2000):
        idx=torch.randint(len(g),(128,));j=torch.randint(len(obs),(128,))
        real=a[idx].flatten(1);noise=torch.randn_like(real);t=torch.rand(128,1)
        losses=[F.mse_loss(bc(obs[j]),labels[j]),F.mse_loss(chunk(g[idx]),real),F.mse_loss(flow(torch.cat([(1-t)*noise+t*real,g[idx],t],1)),real-noise)]
        for opt,loss in zip(optimizers,losses):opt.zero_grad();loss.backward();opt.step()
    test_g,_=data(101,128);test_g=test_g[::2].repeat_interleave(8,dim=0);torch.manual_seed(102)
    with torch.no_grad():
        actions={"chunk_MSE":chunk(test_g).reshape(-1,2,2),"flow_chunk":generate(flow,test_g,torch.randn(len(test_g),4))}
        pos=torch.zeros_like(test_g);steps=[]
        for _ in range(2):
            act=bc(torch.cat([pos,test_g],1));steps.append(act);pos=pos+act
        actions["single_step_BC"]=torch.stack(steps,1)
    report={}
    for name,values in actions.items():
        paths=np.concatenate([np.zeros((len(values),1,2)),values.numpy().cumsum(1)],1)
        outcomes=[judge(path,goal) for path,goal in zip(paths,test_g.numpy())]
        report[name]={"success_rate":float(np.mean([o[0] for o in outcomes])),"collision_rate":float(np.mean([o[1] for o in outcomes])),"mean_final_error":float(np.linalg.norm(paths[:,-1]-test_g.numpy(),axis=1).mean()),"trials":len(outcomes)}
    fig,axes=plt.subplots(1,2,figsize=(9,4));goal=torch.tensor([[1.,0.]]).repeat(8,1)
    with torch.no_grad():
        deterministic=chunk(goal[:1]).reshape(1,2,2).numpy();samples=generate(flow,goal,torch.randn(8,4)).numpy()
    for ax,title,values in zip(axes,["Deterministic chunk MSE","Flow chunks: 8 draws"],[deterministic,samples]):
        for value in values:
            path=np.vstack([np.zeros(2),np.cumsum(value,axis=0)]);ax.plot(path[:,0],path[:,1],"o-",alpha=.6)
        ax.add_patch(plt.Circle((.5,0),.18,color="gray",alpha=.5));ax.scatter([1],[0],marker="*",s=100,color="green");ax.set(title=title,xlim=(-.1,1.2),ylim=(-.8,.8));ax.set_aspect("equal")
    fig.tight_layout();root=Path(__file__).resolve().parents[1];(root/"figures").mkdir(exist_ok=True);fig.savefig(root/"figures/chunks.png",dpi=150);plt.close(fig)
    folder=root/"examples/output";folder.mkdir(exist_ok=True);(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
