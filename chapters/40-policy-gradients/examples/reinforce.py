import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical

def rollout(policy,batch):
    position=torch.full((batch,),2,dtype=torch.long);alive=torch.ones(batch,dtype=torch.bool)
    log_probs=[];rewards=[];masks=[];success=torch.zeros(batch,dtype=torch.bool)
    for t in range(8):
        distribution=Categorical(logits=policy(t*5+position))
        action=distribution.sample();log_probs.append(distribution.log_prob(action));masks.append(alive.float())
        nxt=(position+2*action-1).clamp(0,4)
        reward=torch.where(nxt==4,1.,torch.where(nxt==0,-1.,-.01))*alive
        rewards.append(reward);success|=alive&(nxt==4)
        position=torch.where(alive,nxt,position);alive&=(position!=0)&(position!=4)
    return torch.stack(log_probs),torch.stack(rewards),torch.stack(masks),success

def evaluate(policy):
    rng_state=torch.get_rng_state();torch.manual_seed(101)
    with torch.no_grad():
        _,rewards,_,success=rollout(policy,1000)
    torch.set_rng_state(rng_state)
    return {"success_rate":float(success.float().mean()),"mean_return":float(rewards.sum(0).mean())}

def train(seed):
    torch.manual_seed(seed);policy=nn.Embedding(40,2);nn.init.zeros_(policy.weight)
    before=evaluate(policy);opt=torch.optim.Adam(policy.parameters(),lr=.08)
    for update in range(150):
        logp,rewards,mask,_=rollout(policy,32)
        running=torch.zeros(32);returns=torch.zeros_like(rewards)
        for t in reversed(range(8)):
            running=rewards[t]+running;returns[t]=running
        loss=-(logp*returns.detach()*mask).sum()/32
        opt.zero_grad();loss.backward();opt.step()
    return {"seed":seed,"before":before,"after":evaluate(policy)}
if __name__=="__main__":
    torch.set_num_threads(1);report=[train(seed) for seed in (7,8,9)]
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
