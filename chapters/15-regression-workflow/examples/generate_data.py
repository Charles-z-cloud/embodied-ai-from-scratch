from pathlib import Path
import numpy as np

SEED = 2026
folder = Path(__file__).resolve().parent / "output"
folder.mkdir(exist_ok=True)
rng = np.random.default_rng(SEED)
x = rng.uniform(-1.0, 1.0, size=240)
y = 2.5 * x + 0.4 + rng.normal(0.0, 0.2, size=240)
np.savetxt(folder / "motion.csv", np.column_stack([x, y]), delimiter=",",
           header="command,displacement_cm", comments="")
print("Generated 240 independent synthetic samples:", folder / "motion.csv")
