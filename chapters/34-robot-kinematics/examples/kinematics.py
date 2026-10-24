from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
L1=L2=1.
def forward(q):
    a,b=q
    return np.array([L1*np.cos(a)+L2*np.cos(a+b),L1*np.sin(a)+L2*np.sin(a+b)])
def jacobian(q):
    a,b=q
    return np.array([[-L1*np.sin(a)-L2*np.sin(a+b),-L2*np.sin(a+b)],
                     [L1*np.cos(a)+L2*np.cos(a+b),L2*np.cos(a+b)]])
def analytic(target):
    x,y=target;c=(x*x+y*y-L1*L1-L2*L2)/(2*L1*L2)
    if abs(c)>1+1e-10:raise ValueError("Target is unreachable")
    result=[]
    for b in (np.arccos(np.clip(c,-1,1)),-np.arccos(np.clip(c,-1,1))):
        a=np.arctan2(y,x)-np.arctan2(L2*np.sin(b),L1+L2*np.cos(b));result.append(np.array([a,b]))
    return result
def numerical(target,q):
    q=np.array(q,dtype=float)
    for step in range(200):
        error=target-forward(q)
        if np.linalg.norm(error)<1e-6:return q,step,True
        j=jacobian(q);delta=j.T@np.linalg.solve(j@j.T+.05**2*np.eye(2),error)
        delta*=min(1.,.2/max(np.linalg.norm(delta),1e-12));q+=delta
    return q,200,False
if __name__=="__main__":
    target=np.array([1.,1.]);solutions=analytic(target)
    for q in solutions:assert np.allclose(forward(q),target)
    q=np.array([.3,.7]);eps=1e-6
    numeric=np.column_stack([(forward(q+eps*e)-forward(q-eps*e))/(2*eps) for e in np.eye(2)])
    assert np.allclose(numeric,jacobian(q),atol=1e-8)
    result,steps,success=numerical(target,[.2,.2]);assert success
    try:analytic([3.,0.])
    except ValueError:print("unreachable target rejected")
    else:raise AssertionError("Expected rejection")
    print("solutions",solutions,"numerical steps",steps,"error",np.linalg.norm(forward(result)-target),"straight rank",np.linalg.matrix_rank(jacobian([0,0])))
    fig,ax=plt.subplots(figsize=(7,4))
    for i,q in enumerate(solutions):
        elbow=np.array([np.cos(q[0]),np.sin(q[0])]);points=np.stack([np.zeros(2),elbow,forward(q)])
        ax.plot(points[:,0],points[:,1],"o-",label=f"solution {i+1}")
    ax.scatter([3],[0],marker="x",color="red",s=80,label="unreachable")
    ax.add_patch(plt.Circle((0,0),2,fill=False,linestyle="--",alpha=.4))
    ax.set(xlim=(-.3,3.3),ylim=(-.3,2.2),xlabel="x (m)",ylabel="y (m)",title="Two solutions, one target")
    ax.set_aspect("equal");ax.legend();fig.tight_layout()
    folder=Path(__file__).resolve().parents[1]/"figures";folder.mkdir(exist_ok=True)
    fig.savefig(folder/"arms.png",dpi=150);plt.close(fig)
