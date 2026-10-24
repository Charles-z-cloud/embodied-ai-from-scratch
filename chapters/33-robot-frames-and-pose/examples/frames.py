import numpy as np

def rz(theta):
    c,s=np.cos(theta),np.sin(theta)
    return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def transform(rotation,translation):
    if not np.allclose(rotation.T@rotation,np.eye(3)) or not np.isclose(np.linalg.det(rotation),1):
        raise ValueError("Rotation must be proper orthogonal")
    result=np.eye(4);result[:3,:3]=rotation;result[:3,3]=translation
    return result

def inverse(t):
    result=np.eye(4);r=t[:3,:3];p=t[:3,3]
    result[:3,:3]=r.T;result[:3,3]=-r.T@p
    return result

if __name__=="__main__":
    t_wc=transform(rz(np.pi/2),[1,2,0]);p_c=np.array([1,0,0,1.]);p_w=t_wc@p_c
    assert np.allclose(p_w,[1,3,0,1]);assert np.allclose(inverse(t_wc)@p_w,p_c)
    t_ce=transform(rz(-np.pi/2),[.2,0,.1]);p_e=np.array([.3,.4,.5,1])
    assert np.allclose((t_wc@t_ce)@p_e,t_wc@(t_ce@p_e))
    direction=np.array([1,0,0,0.]);assert np.allclose(t_wc@direction,[0,1,0,0])
    print("world point",p_w,"inverse translation",inverse(t_wc)[:3,3])
    print("composition point",t_wc@t_ce@p_e,"roundtrip max error",np.max(np.abs(inverse(t_wc)@t_wc-np.eye(4))))
