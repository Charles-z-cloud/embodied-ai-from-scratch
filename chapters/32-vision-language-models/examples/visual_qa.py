import json
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
CHAPTERS=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(CHAPTERS/"31-multimodal-alignment/examples"))
sys.path.insert(0,str(CHAPTERS/"27-transformer/examples"))
from alignment import draw, PAIRS
from transformer_block import DecoderBlock,SinusoidalPosition
EOS=6
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.vision=nn.Sequential(nn.Flatten(),nn.Linear(432,64),nn.ReLU(),nn.Linear(64,32))
        self.connector=nn.Linear(32,32)
        self.questions=nn.Embedding(2,32);self.answers=nn.Embedding(7,32)
        self.pos=SinusoidalPosition(32,3);self.block=DecoderBlock(32,4,64)
        self.head=nn.Sequential(nn.LayerNorm(32),nn.Linear(32,7))
    def forward(self,x,q,a=None):
        parts=[self.connector(self.vision(x))[:,None],self.questions(q)[:,None]]
        if a is not None:parts.append(self.answers(a)[:,None])
        return self.head(self.block(self.pos(torch.cat(parts,1))))
    def generate(self,x,q):
        a=self(x,q)[:,1].argmax(1)
        stop=self(x,q,a)[:,2].argmax(1)
        return a,stop

def batch(rng,repeats):
    images,questions,answers,properties=[],[],[],[]
    for color,shape in PAIRS:
        for _ in range(repeats):
            image=draw(rng,color,shape)
            for q in (0,1):
                images.append(image);questions.append(q);answers.append(color if q==0 else shape+3)
                properties.append([color,shape+3])
    return torch.tensor(np.stack(images)),torch.tensor(questions),torch.tensor(answers),torch.tensor(properties)

def main():
    torch.set_num_threads(1);torch.manual_seed(7);rng=np.random.default_rng(7)
    model=Model();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for step in range(500):
        x,q,a,_=batch(rng,2)
        logits=model(x,q,a)[:,1:]
        target=torch.stack([a,torch.full_like(a,EOS)],1)
        loss=F.cross_entropy(logits.flatten(0,1),target.flatten())
        opt.zero_grad();loss.backward();opt.step()
    x,q,a,properties=batch(np.random.default_rng(101),20)
    model.eval();report={}
    permutation=torch.randperm(len(x),generator=torch.Generator().manual_seed(102))
    with torch.no_grad():
        for name,image in [("normal",x),("black",torch.zeros_like(x)),("shuffled",x[permutation])]:
            answer,stop=model.generate(image,q)
            match=(answer==a)&(stop==EOS)
            report[name]={"exact_match":float(match.float().mean()),"color":float(match[q==0].float().mean()),"shape":float(match[q==1].float().mean())}
            if name=="shuffled":
                new_answers=properties[permutation, q]
                report[name]["new_image_exact_match"]=float(((answer==new_answers)&(stop==EOS)).float().mean())
    report["count"]=len(x)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,indent=2));torch.save(model.state_dict(),folder/"vlm.pt")
    print(report)
if __name__=="__main__":main()
