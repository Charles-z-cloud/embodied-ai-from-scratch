import numpy as np

def returns(rewards,gamma):
    result=np.zeros(len(rewards));running=0.
    for t in reversed(range(len(rewards))):
        running=rewards[t]+gamma*running;result[t]=running
    return result
if __name__=="__main__":
    values=returns([-1,-1,10],.9);assert np.allclose(values,[6.2,8,10])
    cues=np.array([0,1]*50);np.random.default_rng(7).shuffle(cues)
    current_observations=np.zeros(100,dtype=int)
    current_only=np.ones_like(current_observations)
    with_memory=cues.copy()
    print("returns",values,"current only",np.mean(current_only==cues),"with memory",np.mean(with_memory==cues))
