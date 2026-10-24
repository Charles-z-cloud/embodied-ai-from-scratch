import csv
from pathlib import Path
import numpy as np

def latest_past(source_times,query_times,max_age):
    if np.any(np.diff(source_times)<=0):raise ValueError("Times must increase strictly")
    indices=np.searchsorted(source_times,query_times,side="right")-1
    if np.any(indices<0):raise ValueError("No past sample")
    age=query_times-source_times[indices]
    if np.any(age>max_age):raise ValueError("Stale sample")
    return indices,age

def project(points,k):
    if np.any(points[:,2]<=0):raise ValueError("Nonpositive camera depth")
    homogeneous=points@k.T
    return homogeneous[:,:2]/homogeneous[:,2:]

if __name__=="__main__":
    k=np.array([[100.,0,32],[0,100,24],[0,0,1]])
    point=np.array([[.2,.1,2.]])
    uv=project(point,k)
    restored=np.column_stack([(uv[:,0]-32)*2/100,(uv[:,1]-24)*2/100,[2.]])
    assert np.allclose(restored,point)
    joint_times=np.arange(101)/100;positions=.3+.2*joint_times
    camera_times=.005+np.arange(30)/30
    indices,age=latest_past(joint_times,camera_times,.011)
    assert np.all(joint_times[indices]<=camera_times)
    try:latest_past(np.array([0.,.01]),np.array([.06]),.02)
    except ValueError:print("stale sample rejected")
    else:raise AssertionError("Expected stale rejection")
    delta=np.array([.02,-.01,.03]);current=np.array([.3,.4,.5]);absolute=current+delta
    assert np.allclose(absolute-current,delta)
    mu,sigma=.01,.02;z=(delta-mu)/sigma;assert np.allclose(z*sigma+mu,delta)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    with (folder/"aligned.csv").open("w",newline="") as f:
        writer=csv.writer(f);writer.writerow(["camera_time_s","joint_time_s","age_s","position_m"])
        for t,j,a in zip(camera_times,indices,age):writer.writerow([t,joint_times[j],a,positions[j]])
    print("projected pixels",uv,"aligned rows",len(indices),"max age",age.max(),"absolute targets",absolute)
