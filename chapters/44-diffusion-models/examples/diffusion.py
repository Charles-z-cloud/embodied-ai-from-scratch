import json
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"43-latent-generative-models/examples"))
from vae import points
class Denoiser(nn.Module):
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Linear(7,64),nn.SiLU(),nn.Linear(64,64),nn.SiLU(),nn.Linear(64,2))
    def forward(self,x,t):
        t=t.reshape(-1,1)
        features=torch.cat([t,torch.sin(2*torch.pi*t),torch.cos(2*torch.pi*t),torch.sin(4*torch.pi*t),torch.cos(4*torch.pi*t)],1)
        return self.net(torch.cat([x,features],1))
def metrics(x):
    angle=2*np.pi*np.arange(8)/8;centers=np.stack([np.cos(angle),np.sin(angle)],1)
    distances=np.linalg.norm(x[:,None]-centers[None],axis=-1);nearest=distances.argmin(1);minimum=distances.min(1)
    return {"mean_nearest_distance":float(minimum.mean()),"within_0_2":float(np.mean(minimum<.2)),"covered_counts":[int(np.sum((nearest==k)&(minimum<.2))) for k in range(8)]}
if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);train=torch.tensor(points(100,1024));test=torch.tensor(points(101,256))
    beta=torch.linspace(.0001,.1,100);alpha=1-beta;abar=alpha.cumprod(0);previous=torch.cat([torch.ones(1),abar[:-1]])
    variance=beta*(1-previous)/(1-abar);model=Denoiser();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for step in range(2000):
        x0=train[torch.randint(len(train),(128,))];t=torch.randint(100,(128,));eps=torch.randn_like(x0);a=abar[t,None]
        xt=a.sqrt()*x0+(1-a).sqrt()*eps;loss=F.mse_loss(model(xt,(t+1)/100),eps)
        opt.zero_grad();loss.backward();opt.step()
    model.eval();torch.manual_seed(102)
    with torch.no_grad():
        t=torch.randint(100,(len(test),));eps=torch.randn_like(test);a=abar[t,None]
        noise_mse=float(F.mse_loss(model(a.sqrt()*test+(1-a).sqrt()*eps,(t+1)/100),eps))
        zero_mse=float(eps.square().mean());x=torch.randn(1024,2);snapshots={100:x.numpy().copy()}
        for index in reversed(range(100)):
            prediction=model(x,torch.full((len(x),),(index+1)/100))
            x=(x-beta[index]/torch.sqrt(1-abar[index])*prediction)/alpha[index].sqrt()
            if index>0:x=x+variance[index].sqrt()*torch.randn_like(x)
            if index in (75,50,25,0):snapshots[index]=x.numpy().copy()
    report={"test_noise_mse":noise_mse,"zero_noise_baseline":zero_mse,"terminal_alpha_bar":float(abar[-1]),"generated":metrics(x.numpy()),"reference_test":metrics(test.numpy())}
    fig,axes=plt.subplots(1,5,figsize=(12,3))
    for ax,t in zip(axes,[100,75,50,25,0]):
        a=snapshots[t];ax.scatter(a[:,0],a[:,1],s=2,alpha=.4);ax.set(title=f"noise step {t}",xlim=(-3,3),ylim=(-3,3));ax.set_aspect("equal")
    fig.tight_layout();root=Path(__file__).resolve().parents[1];(root/"figures").mkdir(exist_ok=True);fig.savefig(root/"figures/diffusion.png",dpi=150);plt.close(fig)
    folder=root/"examples/output";folder.mkdir(exist_ok=True);torch.save(model.state_dict(),folder/"denoiser.pt");np.save(folder/"samples.npy",x.numpy());(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
