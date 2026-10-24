import json
import math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
def wilson(k,n):
    p=k/n;z=1.96;den=1+z*z/n;center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-half,center+half]
def check(data):
    if data["action_unit"]!="m/s" or data["dt_s"]!=.1:raise ValueError("Schema unit/period mismatch")
    for episode in data["episodes"]:
        previous=None
        for row in episode["steps"]:
            a=np.array(row["action"],dtype=float)
            if a.shape!=(2,) or not np.isfinite(a).all() or np.any(np.abs(a)>.5):raise ValueError("Invalid action")
            if previous is not None and not np.isclose(row["time_s"]-previous,.1):raise ValueError("Invalid timestamp spacing")
            previous=row["time_s"]
if __name__=="__main__":
    sample={"action_unit":"m/s","dt_s":.1,"episodes":[{"episode_id":i,"instruction_id":i%2,"steps":[{"time_s":round(t*.1,6),"action":[.2,0.]} for t in range(5)]} for i in range(3)]}
    check(sample)
    try:check({**sample,"action_unit":"mm/s"})
    except ValueError:print("unit mismatch rejected")
    else:raise AssertionError("Expected rejection")
    source=ROOT/"chapters/53-vla-continuous-actions/examples/output/report.json"
    if not source.exists():raise SystemExit("Run chapter53 first")
    groups=json.loads(source.read_text())["groups"];report={};rng=np.random.default_rng(7)
    for group,models in groups.items():
        rows={}
        for name,result in models.items():
            k=sum(e["success"] for e in result["episodes"]);n=len(result["episodes"])
            rows[name]={"successes":k,"episodes":n,"wilson95":wilson(k,n)}
        a={e["seed"]:int(e["success"]) for e in models["flow4"]["episodes"]};b={e["seed"]:int(e["success"]) for e in models["discrete"]["episodes"]}
        assert a.keys()==b.keys()
        strata=[np.array([a[s]-b[s] for s in a if s%2==c]) for c in (0,1)]
        differences=[np.concatenate([rng.choice(v,len(v),replace=True) for v in strata]).mean() for _ in range(2000)]
        rows["flow4_minus_discrete"]={"difference":float(np.concatenate(strata).mean()),"stratified_paired_bootstrap95":np.quantile(differences,[.025,.975]).tolist()};report[group]=rows
    folder=Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"sample.json").write_text(json.dumps(sample,indent=2));(folder/"evaluation.json").write_text(json.dumps(report,indent=2));print(report)
