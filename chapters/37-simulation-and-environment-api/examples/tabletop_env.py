import numpy as np
import gymnasium as gym
from gymnasium import spaces

class TabletopEnv(gym.Env):
    metadata={"render_modes":["rgb_array"],"render_fps":10}
    def __init__(self,render_mode=None,max_steps=100):
        if render_mode not in (None,"rgb_array"):raise ValueError("Unsupported render mode")
        self.render_mode=render_mode;self.max_steps=max_steps;self.dt=.1
        self.action_space=spaces.Box(-.5,.5,(2,),dtype=np.float32)
        self.observation_space=spaces.Box(-1.,1.,(4,),dtype=np.float32)
        self.finished=True
    def observation(self):return np.concatenate([self.position,self.goal]).astype(np.float32)
    def reset(self,*,seed=None,options=None):
        super().reset(seed=seed)
        if options is not None:
            self.position=np.asarray(options["position"],dtype=np.float64).copy()
            self.goal=np.asarray(options["goal"],dtype=np.float64).copy()
            for value in (self.position,self.goal):
                if value.shape!=(2,) or not np.isfinite(value).all() or np.any(np.abs(value)>1):raise ValueError("Invalid position or goal")
        else:
            while True:
                self.position=self.np_random.uniform(-.8,.8,2);self.goal=self.np_random.uniform(-.8,.8,2)
                if np.linalg.norm(self.position-self.goal)>.4:break
        self.steps=0;self.finished=False
        return self.observation(),{"distance":float(np.linalg.norm(self.position-self.goal))}
    def step(self,action):
        if self.finished:raise RuntimeError("Call reset before stepping")
        a=np.asarray(action,dtype=np.float64)
        if a.shape!=(2,) or not np.isfinite(a).all():raise ValueError("Invalid action")
        a=np.clip(a,-.5,.5);self.position=np.clip(self.position+self.dt*a,-1,1);self.steps+=1
        distance=float(np.linalg.norm(self.position-self.goal));terminated=distance<.05
        truncated=self.steps>=self.max_steps and not terminated
        self.finished=terminated or truncated
        return self.observation(),-distance,terminated,truncated,{"success":terminated,"distance":distance,"applied_action":a.tolist()}
    def render(self):
        image=np.full((64,64,3),240,np.uint8)
        for point,color in [(self.goal,[20,180,40]),(self.position,[30,80,230])]:
            col=int(round((point[0]+1)*31.5));row=int(round((1-point[1])*31.5))
            image[max(0,row-2):min(64,row+3),max(0,col-2):min(64,col+3)]=color
        return image

def controller(observation):return np.clip(4*(observation[2:]-observation[:2]),-.5,.5).astype(np.float32)
