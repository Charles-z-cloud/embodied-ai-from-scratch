import json
from pathlib import Path
import numpy as np
WALLS={7,12,17};GOAL=24
STATES=[s for s in range(25) if s not in WALLS and s!=GOAL]
DELTAS=[(-1,0),(1,0),(0,-1),(0,1)]
def transition(s,a):
    if s==GOAL:return GOAL,0.,True
    row,col=divmod(s,5);dr,dc=DELTAS[a];r,c=row+dr,col+dc
    nxt=5*r+c if 0<=r<5 and 0<=c<5 and 5*r+c not in WALLS else s
    return nxt,-1.,nxt==GOAL

def optimal():
    v=np.zeros(25)
    for _ in range(10000):
        new=v.copy()
        for s in STATES:
            new[s]=max(r+.95*(not done)*v[n] for n,r,done in [transition(s,a) for a in range(4)])
        change=np.max(np.abs(new-v));v=new
        if change<1e-10:break
    q=np.zeros((25,4))
    for s in STATES:
        for a in range(4):
            n,r,done=transition(s,a);q[s,a]=r+.95*(not done)*v[n]
    return q

def evaluate(q,seed=101):
    rng=np.random.default_rng(seed);rows=[]
    for start in STATES:
        for repeat in range(5):
            s=start;total=0.
            for step in range(1,101):
                action=int(rng.integers(4)) if q is None else int(q[s].argmax())
                s,reward,done=transition(s,action);total+=reward
                if done:break
            rows.append({"start":start,"success":bool(done),"steps":step,"return":total})
    return {"episodes":len(rows),"success_rate":float(np.mean([r["success"] for r in rows])),"mean_steps":float(np.mean([r["steps"] for r in rows]))}

if __name__=="__main__":
    rng=np.random.default_rng(7);q=np.zeros((25,4))
    for episode in range(3000):
        s=int(rng.choice(STATES))
        for step in range(100):
            a=int(rng.integers(4)) if rng.random()<.2 else int(q[s].argmax())
            nxt,r,done=transition(s,a)
            target=r+.95*(not done)*q[nxt].max()
            q[s,a]+=.2*(target-q[s,a]);s=nxt
            if done:break
    reference=optimal()
    report={"random":evaluate(None),"Q_learning":evaluate(q),"value_iteration":evaluate(reference),"max_Q_error":float(np.abs(q[STATES]-reference[STATES]).max())}
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    np.save(folder/"q.npy",q);(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
