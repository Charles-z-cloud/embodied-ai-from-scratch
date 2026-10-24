import math
from pathlib import Path
import matplotlib.pyplot as plt

xs = []
linear = []
square = []
exponential = []
positive_xs = []
logarithm = []
for i in range(161):
    x = -2 + i / 40
    xs.append(x)
    linear.append(2 * x + 1)
    square.append(x ** 2)
    exponential.append(math.exp(x))
    if x > 0:
        positive_xs.append(x)
        logarithm.append(math.log(x))

plt.figure(figsize=(9, 6))
curves = [(xs, linear, "2x + 1"), (xs, square, "x squared"),
          (xs, exponential, "exp(x)"), (positive_xs, logarithm, "ln(x), x > 0")]
for index, curve in enumerate(curves):
    x_values, y_values, title = curve
    plt.subplot(2, 2, index + 1)
    plt.plot(x_values, y_values)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3)
plt.tight_layout()
output_dir = Path(__file__).resolve().parent.parent / "figures"
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / "functions.png", dpi=160)
plt.close()
print("图像已保存到", output_dir / "functions.png")
