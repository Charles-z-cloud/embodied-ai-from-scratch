import copy
import json
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

def data(seed, n):
    rng = np.random.default_rng(seed)
    y = np.arange(n)%2; rng.shuffle(y)
    x = rng.uniform(0,.08,(n,3,16,16)).astype("float32")
    for i,label in enumerate(y):
        center = rng.integers(4,12)
        color = rng.uniform(.5,1,(3,1,1))
        if label==0: x[i,:,center-1:center+1,2:14] = color
        else: x[i,:,2:14,center-1:center+1] = color
    return torch.tensor(x), torch.tensor(y)

def patchify(x):
    b,c,h,w = x.shape
    if h%4 or w%4: raise ValueError("Height and width must divide by 4")
    return x.unfold(2,4,4).unfold(3,4,4).permute(0,2,3,1,4,5).reshape(b,-1,c*16)

class TinyViT(nn.Module):
    def __init__(self):
        super().__init__()
        self.project = nn.Linear(48,24)
        self.position = nn.Parameter(torch.randn(1,16,24)*.02)
        self.block = nn.TransformerEncoderLayer(24,4,48,dropout=0.,batch_first=True,norm_first=True,activation="gelu")
        self.norm = nn.LayerNorm(24)
        self.head = nn.Linear(24,2)
    def forward(self,x):
        z = self.project(patchify(x))+self.position
        return self.head(self.norm(self.block(z)).mean(1))

class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(nn.Conv2d(3,16,3,padding=1),nn.ReLU(),nn.Conv2d(16,16,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Linear(16,2))
    def forward(self,x): return self.network(x)

def main():
    torch.set_num_threads(1)
    train_x,train_y = data(100,512); val_x,val_y = data(101,128); test_x,test_y = data(102,128)
    numbered = torch.arange(256).reshape(1,1,16,16)
    assert torch.equal(patchify(numbered)[0,0],numbered[0,0,:4,:4].flatten())
    report = {"majority_baseline":float((test_y==train_y.bincount().argmax()).float().mean()),"models":{}}
    for name, cls in [("CNN",TinyCNN),("ViT",TinyViT)]:
        torch.manual_seed(7); model=cls();opt=torch.optim.Adam(model.parameters(),lr=.003)
        rng=torch.Generator().manual_seed(11);best=float("inf");history=[];start=time.perf_counter()
        for step in range(1,401):
            model.train(); idx=torch.randint(len(train_x),(32,),generator=rng)
            loss=F.cross_entropy(model(train_x[idx]),train_y[idx]);opt.zero_grad();loss.backward();opt.step()
            if step%50==0:
                model.eval()
                with torch.no_grad(): value=F.cross_entropy(model(val_x),val_y).item()
                history.append([step,value])
                if value<best: best=value;state=copy.deepcopy(model.state_dict());best_step=step
        model.load_state_dict(state);model.eval()
        with torch.no_grad(): accuracy=float((model(test_x).argmax(-1)==test_y).float().mean())
        report["models"][name]={"test_accuracy":accuracy,"parameters":sum(p.numel() for p in model.parameters()),"best_step":best_step,"seconds":time.perf_counter()-start,"validation":history}
        print(name,report["models"][name],flush=True)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,indent=2))
if __name__=="__main__":main()
