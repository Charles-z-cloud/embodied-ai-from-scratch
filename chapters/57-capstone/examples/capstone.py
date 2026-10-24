import json
import sys
import time
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[3];CHAPTERS=ROOT/'chapters'
for folder in ['41-imitation-learning','49-planning-with-world-models','53-vla-continuous-actions']:
    sys.path.insert(0,str(CHAPTERS/folder/'examples'))
from bc import load_policy
from learned_mpc import ModelPlanner,load_model as load_dynamics
from continuous import load_model as load_body,load_heads,make_policy
from scene import run,teacher
REQUIRED={
'41-imitation-learning/examples/output/bc.pt':'41-imitation-learning/examples/bc.py',
'47-learned-dynamics/examples/output/dynamics.pt':'47-learned-dynamics/examples/dynamics.py',
'52-vla-discrete-actions/examples/output/discrete.pt':'52-vla-discrete-actions/examples/train_vla.py',
'53-vla-continuous-actions/examples/output/heads.pt':'53-vla-continuous-actions/examples/continuous.py'}
class ConstantDynamics(torch.nn.Module):
    def forward(self,p,a):return p

def selected(x,l):return np.concatenate([x[4:6],x[2*l:2*l+2]]).astype(np.float32)

def main():
    missing=[f'python chapters/{command}' for path,command in REQUIRED.items() if not (CHAPTERS/path).exists()]
    if missing:raise SystemExit('先按顺序运行缺失权重的生成命令：\n'+'\n'.join(missing))
    torch.set_num_threads(1);bc=load_policy();body=load_body();reg,_=load_heads();dynamics=load_dynamics()
    names=['geometric','state_bc','instruction_regression','learned_mpc','instruction_black','instruction_swap','known_mpc','constant_mpc']
    report={};lines=['# 毕业项目实际结果','','[正文](README.md) · [验收清单](acceptance.md)','','运行日期：2026-10-24。CPU；冻结已有权重，新场景种子400—419，每组20例。平均步数包括失败的100步；策略耗时不含共同图像与重心计算。','','| 组别 | 系统 | 成功数/20 | 平均步数 | 平均策略毫秒 |','|---|---|---:|---:|---:|']
    for held in [False,True]:
        group='held' if held else 'seen';report[group]={}
        for name in names:
            rows=[];timings=[]
            for seed in range(400,420):
                mode='black' if name=='instruction_black' else 'swap_language' if name=='instruction_swap' else 'normal'
                if name=='geometric':policy=lambda x,l:teacher(x[4:6],x[2*l:2*l+2])
                elif name=='state_bc':policy=lambda x,l:bc(selected(x,l))
                elif name.startswith('instruction'):policy=make_policy(body,reg,'regression')
                else:
                    model=dynamics if name=='learned_mpc' else None if name=='known_mpc' else ConstantDynamics()
                    planner=ModelPlanner(model,3,seed+1000)
                    policy=lambda x,l:planner(selected(x,l))
                def timed(x,l):
                    start=time.perf_counter();a=policy(x,l);timings.append((time.perf_counter()-start)*1000);return a
                rows.append(run(timed,seed,held,mode))
            successes=sum(r['success'] for r in rows)
            result={'successes':successes,'n':len(rows),'success_rate':successes/len(rows),'mean_steps':float(np.mean([r['steps'] for r in rows])),'mean_policy_ms':float(np.mean(timings)),'episodes':rows}
            report[group][name]=result
            lines.append(f"| {group} | {name} | {successes}/20 | {result['mean_steps']:.2f} | {result['mean_policy_ms']:.3f} |")
            print(group,name,successes,result['mean_steps'],flush=True)
    lines+=['','## 一个按预先规则选择的失败案例','','规则：依照上表组别、系统顺序，取第一条失败轨迹，不选最戏剧化的一条。']
    found=False
    for group in report:
        for name,score in report[group].items():
            failures=[r for r in score['episodes'] if not r['success']]
            if failures and not found:
                row=failures[0];lines.append(f"\n系统{group}/{name}，种子{row['seed']}，执行{row['steps']}步，最终目标距离{row['distance']:.4f}米。起点{row['path'][0]}，终点{row['path'][-1]}。这是待解释的观察，不能单凭端点确定全部原因。完整动作效果可从相邻轨迹位置差除以0.1获得。");found=True
    lines+=['','## 解释范围','','这是复用不同训练数据和结构先验的系统集成比较，不是相同训练预算的架构排名。完整轨迹保存在本地examples/output/report.json，可由脚本重建。20例全成功仍只有有限样本证据。历史信息的价值由第38、48章单独实验，不混入当前完整状态任务。']
    out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,indent=2))
    (Path(__file__).resolve().parents[1]/'results.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
