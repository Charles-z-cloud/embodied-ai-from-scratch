import json
import sys
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"44-diffusion-models/examples"))
from diffusion import Denoiser,metrics,points
# Reuse the architecture only; this model predicts velocity, not noise.
class VelocityField(Denoiser):pass

def sample(model,initial,steps):
    x=initial.clone()
    with torch.no_grad():
        for k in range(steps):x=x+model(x,torch.full((len(x),),k/steps))/steps
    return x

if __name__=="__main__":
    torch.set_num_threads(1);torch.manual_seed(7);train=torch.tensor(points(100,1024));test=torch.tensor(points(101,256))
    model=VelocityField();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for step in range(2000):
        x1=train[torch.randint(len(train),(128,))];x0=torch.randn_like(x1);t=torch.rand(128,1)
        xt=(1-t)*x0+t*x1;loss=F.mse_loss(model(xt,t[:,0]),x1-x0)
        opt.zero_grad();loss.backward();opt.step()
    model.eval();torch.manual_seed(102)
    with torch.no_grad():
        x0=torch.randn_like(test);t=torch.rand(len(test),1)
        velocity_mse=float(F.mse_loss(model((1-t)*x0+t*test,t[:,0]),test-x0))
    initial=torch.randn(1024,2);report={"test_velocity_mse":velocity_mse,"steps":{},"reference_test":metrics(test.numpy())}
    fig,axes=plt.subplots(1,4,figsize=(11,3.2))
    for ax,steps in zip(axes,[1,4,16,64]):
        start=time.perf_counter();generated=sample(model,initial,steps).numpy();elapsed=time.perf_counter()-start
        report["steps"][str(steps)]={**metrics(generated),"sample_seconds":elapsed}
        ax.scatter(generated[:,0],generated[:,1],s=3,alpha=.4);ax.set(title=f"Euler steps {steps}",xlim=(-1.6,1.6),ylim=(-1.6,1.6));ax.set_aspect("equal")
    fig.tight_layout();root=Path(__file__).resolve().parents[1];(root/"figures").mkdir(exist_ok=True);fig.savefig(root/"figures/flow.png",dpi=150);plt.close(fig)
    folder=root/"examples/output";folder.mkdir(exist_ok=True);torch.save(model.state_dict(),folder/"velocity.pt");(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
