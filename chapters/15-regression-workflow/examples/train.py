import csv
import json
from pathlib import Path
import numpy as np


def metrics(prediction, target):
    if prediction.shape != target.shape:
        raise ValueError("Prediction and target shapes must match")
    residual = prediction - target
    mse = float(np.mean(residual ** 2))
    return {"mse_cm2": mse, "rmse_cm": float(np.sqrt(mse)),
            "mae_cm": float(np.mean(np.abs(residual)))}


def main():
    folder = Path(__file__).resolve().parent / "output"
    data = np.loadtxt(folder / "motion.csv", delimiter=",", skiprows=1, ndmin=2)
    if data.shape != (240, 2) or not np.all(np.isfinite(data)):
        raise ValueError("Expected 240 finite rows with two columns")
    rng = np.random.default_rng(7)
    order = rng.permutation(len(data))
    train_ids, test_ids = order[:180], order[180:]
    x_train, y_train = data[train_ids, 0], data[train_ids, 1]
    x_test, y_test = data[test_ids, 0], data[test_ids, 1]
    assert set(train_ids).isdisjoint(set(test_ids))
    w, b = 0.0, 0.0
    learning_rate, steps = 0.1, 500
    history = []
    for step in range(steps + 1):
        residual = w * x_train + b - y_train
        history.append((step, float(np.mean(residual ** 2))))
        if step == steps:
            break
        grad_w = 2 * np.mean(residual * x_train)
        grad_b = 2 * np.mean(residual)
        w -= learning_rate * grad_w
        b -= learning_rate * grad_b
    baseline = np.full_like(y_test, y_train.mean())
    prediction = w * x_test + b
    reference = np.linalg.lstsq(np.column_stack([x_train, np.ones_like(x_train)]),
                                y_train, rcond=None)[0]
    assert np.allclose([w, b], reference, atol=1e-6)
    report = {"data_seed": 2026, "split_seed": 7, "train_count": 180, "test_count": 60,
              "learning_rate": learning_rate, "steps": steps, "w": float(w), "b": float(b),
              "initial_train_mse_cm2": history[0][1], "final_train_mse_cm2": history[-1][1],
              "test_baseline": metrics(baseline, y_test), "test_model": metrics(prediction, y_test),
              "lstsq_reference": reference.tolist(), "train_ids": train_ids.tolist(), "test_ids": test_ids.tolist()}
    (folder / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (folder / "training.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["step", "train_mse_cm2"])
        writer.writerows(history)
    print("w / b:", w, b)
    print("training MSE:", history[0][1], "->", history[-1][1])
    print("baseline test:", report["test_baseline"])
    print("model test:", report["test_model"])
    print("lstsq agrees; report saved to", folder / "report.json")


if __name__ == "__main__":
    main()
