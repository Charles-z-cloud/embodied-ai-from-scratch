from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), layout="constrained")
axes[0].bar([0, 1], [0.2, 0.8], width=0.45, color="#338899")
axes[0].set(xticks=[0, 1], ylim=(0, 1), xlabel="Outcome", ylabel="Probability mass", title="Bernoulli: p = 0.8")
x = np.linspace(9.2, 10.8, 400)
density = np.exp(-0.5 * ((x - 10) / 0.2) ** 2) / (0.2 * np.sqrt(2 * np.pi))
axes[1].plot(x, density, color="#338899")
axes[1].fill_between(x, density, where=(x >= 9.8) & (x <= 10.2), alpha=0.3, color="#338899")
axes[1].set(xlabel="Position (cm)", ylabel="Density (1/cm)", title="Gaussian: shaded area is probability")
axes[2].plot([0, 0, 0.1, 0.1], [0, 10, 10, 0], color="#cc7733")
axes[2].fill_between([0.02, 0.05], [10, 10], alpha=0.3, color="#cc7733")
axes[2].set(xlim=(-0.01, 0.11), ylim=(0, 11), xlabel="x", ylabel="Density", title="Uniform: shaded area = 0.3")
folder = Path(__file__).resolve().parents[1] / "figures"
folder.mkdir(exist_ok=True)
fig.savefig(folder / "distributions.png", dpi=150)
print(folder / "distributions.png")
