import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def simulate(kp=4.,kd=3.,ki=0.,disturbance=0.,delay=0):
    dt=.02;x=v=integral=0.;history=[(x,v)];rows=[]
    for k in range(500):
        observed=history[max(0,len(history)-1-delay)];error=1-observed[0]
        integral=np.clip(integral+error*dt,-.8,.8)
        u=float(np.clip(kp*error-kd*observed[1]+ki*integral,-2,2))
        d=disturbance if k*dt>=2 else 0.
        x,v=x+dt*v,v+dt*(u-.2*v+d)
        history.append((x,v));rows.append([(k+1)*dt,x,v,u])
    a=np.array(rows)
    score={"last_2s_rmse":float(np.sqrt(np.mean((a[-100:,1]-1)**2))),"overshoot_m":float(max(0,a[:,1].max()-1)),"final_velocity":float(v)}
    return a,score

if __name__=="__main__":
    settings={"P":{"kd":0},"PD":{},"PD + disturbance":{"disturbance":.4},"PID + disturbance":{"ki":1.,"disturbance":.4},"PD + delay":{"delay":10}}
    report={};fig,ax=plt.subplots(figsize=(8,4.5))
    for name,kwargs in settings.items():
        a,report[name]=simulate(**kwargs);ax.plot(a[:,0],a[:,1],label=name)
    ax.axhline(1,color="black",linestyle="--",alpha=.5);ax.set(xlabel="time (s)",ylabel="position (m)",title="Force control of a point mass");ax.legend();fig.tight_layout()
    root=Path(__file__).resolve().parents[1];(root/"figures").mkdir(exist_ok=True)
    fig.savefig(root/"figures/control.png",dpi=150);plt.close(fig)
    folder=root/"examples/output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
