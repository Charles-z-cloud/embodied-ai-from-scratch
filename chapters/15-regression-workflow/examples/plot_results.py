import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent / "output"
data = np.loadtxt(folder / "motion.csv", delimiter=",", skiprows=1)
history = np.loadtxt(folder / "training.csv", delimiter=",", skiprows=1)
report = json.loads((folder / "report.json").read_text())
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
for split, color in (("train", "#338899"), ("test", "#cc7733")):
    ids = report[split + "_ids"]
    axes[0].scatter(data[ids, 0], data[ids, 1], s=12, alpha=0.6, label=split, color=color)
x = np.linspace(-1, 1, 100)
axes[0].plot(x, report["w"] * x + report["b"], color="black", label="Fitted line")
axes[0].set(xlabel="Command", ylabel="Displacement (cm)", title="Synthetic observations and prediction")
axes[0].legend()
axes[1].plot(history[:, 0], history[:, 1])
axes[1].set(xlabel="Update", ylabel="Training MSE (cm squared)", yscale="log", title="Training loss")
out = Path(__file__).resolve().parents[1] / "figures"
out.mkdir(exist_ok=True)
fig.savefig(out / "regression.png", dpi=150)
print(out / "regression.png")
