import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt

def points(seed,n):
    rng=np.random.default_rng(seed);angle=2*np.pi*rng.integers(8,size=n)/8
    return np.stack([np.cos(angle),np.sin(angle)],1).astype("float32")+rng.normal(0,.06,(n,2)).astype("float32")
class VAE(nn.Module):
    def __init__(self):
        super().__init__();self.encoder=nn.Sequential(nn.Linear(2,64),nn.ReLU(),nn.Linear(64,4));self.decoder=nn.Sequential(nn.Linear(2,64),nn.ReLU(),nn.Linear(64,2))
    def encode(self,x):
        mu,logvar=self.encoder(x).chunk(2,-1);return mu,logvar.clamp(-8,8)
    def loss(self,x):
        mu,lv=self.encode(x);z=mu+torch.exp(.5*lv)*torch.randn_like(mu)
        reconstruction=((x-self.decoder(z))**2).sum(-1)/(2*.15**2)
        kl=.5*(mu**2+lv.exp()-1-lv).sum(-1)
        return (reconstruction+kl).mean(),reconstruction.mean(),kl.mean()
if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);train=torch.tensor(points(100,1024));test=torch.tensor(points(101,256))
    model=VAE();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for step in range(1200):
        x=train[torch.randint(len(train),(128,))];loss,_,_=model.loss(x);opt.zero_grad();loss.backward();opt.step()
    model.eval();torch.manual_seed(102)
    with torch.no_grad():
        mu,lv=model.encode(test);reconstructed=model.decoder(mu)
        terms=[model.loss(test) for _ in range(20)]
        means=model.decoder(torch.randn(1024,2));generated=means+.15*torch.randn_like(means)
    report={"mean_decode_test_mse":float(((reconstructed-test)**2).mean()),"test_negative_elbo_without_constant":float(torch.stack([t[0] for t in terms]).mean()),"test_kl":float(torch.stack([t[2] for t in terms]).mean()),"steps":1200}
    fig,axes=plt.subplots(1,3,figsize=(10,3.5))
    for ax,title,data in zip(axes,["Held-out / reconstruction","Prior decoder means","Prior generated x"],[reconstructed.numpy(),means.numpy(),generated.numpy()]):
        if ax is axes[0]:ax.scatter(test[:,0],test[:,1],s=7,alpha=.25,label="data")
        ax.scatter(data[:,0],data[:,1],s=5,alpha=.4);ax.set(title=title,xlim=(-1.7,1.7),ylim=(-1.7,1.7));ax.set_aspect("equal")
    fig.tight_layout();root=Path(__file__).resolve().parents[1];(root/"figures").mkdir(exist_ok=True);fig.savefig(root/"figures/vae.png",dpi=150);plt.close(fig)
    folder=root/"examples/output";folder.mkdir(exist_ok=True);torch.save(model.state_dict(),folder/"vae.pt");(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
