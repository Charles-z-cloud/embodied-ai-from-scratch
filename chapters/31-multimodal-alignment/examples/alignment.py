import itertools
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
PAIRS=list(itertools.product(range(3),range(3)))
HELD={(0,2),(2,0)}

def draw(rng,color,shape):
    x=rng.uniform(0,.03,(3,12,12)).astype("float32")
    cy,cx=rng.integers(4,8,size=2)
    mask=np.zeros((12,12),bool)
    if shape in (0,2):mask[cy-1:cy+1,2:10]=True
    if shape in (1,2):mask[2:10,cx-1:cx+1]=True
    x[:,mask]=0.;x[color,mask]=rng.uniform(.6,1.)
    return x

class Dual(nn.Module):
    def __init__(self):
        super().__init__()
        self.visual=nn.Sequential(nn.Flatten(),nn.Linear(432,64),nn.ReLU(),nn.Linear(64,16))
        self.words=nn.Embedding(6,16)
        self.text=nn.Linear(16,16)
    def image(self,x):return F.normalize(self.visual(x),dim=-1)
    def language(self,pairs):
        return F.normalize(self.text(self.words(pairs[:,0])+self.words(pairs[:,1]+3)),dim=-1)

def main():
    torch.set_num_threads(1);torch.manual_seed(7);rng=np.random.default_rng(7)
    train=[p for p in PAIRS if p not in HELD];pairs=torch.tensor(train)
    model=Dual();opt=torch.optim.Adam(model.parameters(),lr=.003)
    labels=torch.arange(len(train))
    for step in range(600):
        images=torch.tensor(np.stack([draw(rng,*p) for p in train]))
        scores=model.image(images)@model.language(pairs).T/.1
        loss=(F.cross_entropy(scores,labels)+F.cross_entropy(scores.T,labels))/2
        opt.zero_grad();loss.backward();opt.step()
    model.eval();rng=np.random.default_rng(101);counts={"seen":[0,0],"unseen":[0,0]}
    with torch.no_grad():
        text=model.language(torch.tensor(PAIRS))
        for index,pair in enumerate(PAIRS):
            images=torch.tensor(np.stack([draw(rng,*pair) for _ in range(40)]))
            predicted=(model.image(images)@text.T).argmax(1)
            key="unseen" if pair in HELD else "seen"
            counts[key][0]+=int((predicted==index).sum());counts[key][1]+=40
    report={k:{"correct":v[0],"count":v[1],"recall_at_1":v[0]/v[1]} for k,v in counts.items()}
    report["last_training_loss"]=float(loss.detach())
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,indent=2))
    torch.save(model.state_dict(),folder/"dual.pt")
    print(report)
if __name__=="__main__":main()
