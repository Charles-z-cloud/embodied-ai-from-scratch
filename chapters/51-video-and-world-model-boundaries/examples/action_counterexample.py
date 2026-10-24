import json
from pathlib import Path
import numpy as np
if __name__=="__main__":
    rng=np.random.default_rng(7);p=rng.uniform(-.5,.5,(100,2));right=np.tile([.5,0.],(100,1));left=-right
    def real(a):return p+.2*a
    ignored=p+.2*right
    report={"observation_only_right_mse":float(np.mean((ignored-real(right))**2)),
            "paired_intervention_ignored_mse":float(np.mean(np.stack([(ignored-real(right))**2,(ignored-real(left))**2]))),
            "action_conditioned_mse":float(np.mean(np.stack([(p+.2*a-real(a))**2 for a in (right,left)]))),"true_left_right_position_difference":float(np.linalg.norm(real(right)-real(left),axis=1).mean()),"ignored_model_difference":float(np.linalg.norm(ignored-ignored,axis=1).mean()),"initial_states":100}
    assert np.isclose(report["paired_intervention_ignored_mse"],.01)
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True);(folder/"report.json").write_text(json.dumps(report,indent=2));print(report)
