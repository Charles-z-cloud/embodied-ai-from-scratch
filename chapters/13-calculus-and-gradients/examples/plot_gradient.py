from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from gradients import loss, analytic_gradient

theta = np.array([1., 0.])
gradient = analytic_gradient(theta)
direction = gradient / np.linalg.norm(gradient)
alphas = np.linspace(-0.5, 0.5, 101)
values = np.array([loss(theta + alpha * direction) for alpha in alphas])
linear = loss(theta) + alphas * (gradient @ direction)
fig, ax = plt.subplots(figsize=(6.5, 4), layout="constrained")
ax.plot(alphas, values, label="Actual loss")
ax.plot(alphas, linear, "--", label="Local linear approximation")
ax.scatter([0], [loss(theta)], color="black", zorder=3)
ax.axvline(0, color="gray", alpha=0.4)
ax.set(xlabel="Signed step along unit gradient", ylabel="Squared error", title="Negative steps reduce loss locally")
ax.legend()
folder = Path(__file__).resolve().parents[1] / "figures"
folder.mkdir(exist_ok=True)
fig.savefig(folder / "gradient-direction.png", dpi=150)
print(folder / "gradient-direction.png")
