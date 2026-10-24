import numpy as np
LEVELS=np.array([-.5,0.,.5],dtype=np.float32)
ACTIONS=np.array([[x,y] for x in LEVELS for y in LEVELS],dtype=np.float32)
X,Y=np.meshgrid(np.linspace(-1,1,16),np.linspace(1,-1,16))
def render(position,targets):
    image=np.zeros((3,16,16),dtype=np.float32)
    for channel,point in [(0,targets[0]),(2,targets[1]),(1,position)]:
        image[channel]=np.exp(-((X-point[0])**2+(Y-point[1])**2)/(2*.1**2))
    return image

def vision(image):
    result=[]
    for channel in (0,2):
        weight=image[channel];den=max(float(weight.sum()),1e-8)
        result.extend([float((weight*X).sum()/den),float((weight*Y).sum()/den)])
    return np.array(result,dtype=np.float32)

def scene(seed,held=False):
    rng=np.random.default_rng(seed);instruction=seed%2
    while True:
        targets=rng.uniform(-.8,.8,(2,2)).astype(np.float32);g=targets[instruction]
        forbidden=(g[0]>0 and g[1]>0) if instruction==0 else (g[0]<0 and g[1]<0)
        if forbidden==held and np.linalg.norm(targets[0]-targets[1])>.5:break
    while True:
        p=rng.uniform(-.8,.8,2).astype(np.float32)
        if np.linalg.norm(p-g)>.4:break
    return p,targets,instruction

def teacher(p,target):return np.clip(4*(target-p),-.5,.5).astype(np.float32)
def token(action):return int(((ACTIONS-action)**2).sum(1).argmin())
def observation(p,targets):return np.concatenate([vision(render(p,targets)),p]).astype(np.float32)

def collect(seeds,held=False):
    features,instructions,labels,continuous=[],[],[],[]
    for seed in seeds:
        p,targets,l=scene(seed,held)
        for _ in range(100):
            a=teacher(p,targets[l]);label=token(a)
            features.append(observation(p,targets));instructions.append(l);labels.append(label);continuous.append(a)
            p=np.clip(p+.1*ACTIONS[label],-1,1)
            if np.linalg.norm(p-targets[l])<.09:break
    return np.stack(features),np.array(instructions),np.array(labels),np.stack(continuous)

def run(policy,seed,held=False,mode="normal",perturb=False):
    p,targets,l=scene(seed,held);path=[p.copy()]
    for step in range(100):
        if perturb and step==2:p=np.clip(p+[.3,-.25],-1,1).astype(np.float32)
        features=observation(p,targets)
        if mode=="black":features[:4]=0
        used_l=1-l if mode=="swap_language" else l
        a=np.asarray(policy(features,used_l),dtype=np.float32)
        if a.shape!=(2,) or not np.isfinite(a).all():raise ValueError("Invalid policy action")
        p=np.clip(p+.1*np.clip(a,-.5,.5),-1,1);path.append(p.copy())
        if np.linalg.norm(p-targets[l])<.09:break
    return {"seed":seed,"success":bool(np.linalg.norm(p-targets[l])<.09),"steps":step+1,"distance":float(np.linalg.norm(p-targets[l])),"path":np.array(path).tolist()}
