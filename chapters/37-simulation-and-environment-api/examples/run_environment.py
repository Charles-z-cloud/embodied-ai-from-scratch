import json
from pathlib import Path
import numpy as np
import gymnasium
from PIL import Image
from tabletop_env import TabletopEnv,controller

def main():
    report={"gymnasium":gymnasium.__version__,"policies":{}}
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    for policy in ("random","feedback"):
        results=[]
        for seed in range(100,120):
            env=TabletopEnv();obs,_=env.reset(seed=seed);rng=np.random.default_rng(seed+1000)
            trace={"seed":seed,"initial":obs.tolist(),"steps":[]};total=0.
            for _ in range(env.max_steps):
                action=controller(obs) if policy=="feedback" else rng.uniform(-.5,.5,2).astype(np.float32)
                obs,reward,terminated,truncated,info=env.step(action);total+=reward
                assert env.observation_space.contains(obs)
                trace["steps"].append({"action":action.tolist(),"next_observation":obs.tolist(),"reward":reward,"terminated":terminated,"truncated":truncated})
                if terminated or truncated:break
            results.append({"seed":seed,"success":terminated,"steps":env.steps,"return":total,"final_distance":info["distance"]})
            if policy=="feedback" and seed==100:
                (folder/"trajectory.json").write_text(json.dumps(trace,indent=2));Image.fromarray(env.render()).save(folder/"final.png")
                replay=TabletopEnv();replay.reset(seed=seed)
                for row in trace["steps"]:
                    again,*_=replay.step(row["action"])
                    assert np.array_equal(again,np.array(row["next_observation"],dtype=np.float32))
        report["policies"][policy]={"success_rate":sum(r["success"] for r in results)/len(results),"mean_steps":float(np.mean([r["steps"] for r in results])),"episodes":results}
        print(policy,report["policies"][policy]["success_rate"],report["policies"][policy]["mean_steps"])
    (folder/"report.json").write_text(json.dumps(report,indent=2));print("Gymnasium",gymnasium.__version__,"replay exact")
if __name__=="__main__":main()
