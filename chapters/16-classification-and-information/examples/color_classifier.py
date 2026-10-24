import json
from pathlib import Path
import numpy as np


def log_softmax(z):
    shifted = z - z.max(axis=1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))


def objective(x, y, w, b):
    logp = log_softmax(x @ w + b)
    return float(-logp[np.arange(len(y)), y].mean())


def main():
    rng = np.random.default_rng(2026)
    centers = np.array([[0.8, 0.2, 0.2], [0.2, 0.8, 0.2], [0.2, 0.2, 0.8]])
    y = np.repeat(np.arange(3), 100)
    x = np.clip(centers[y] + rng.normal(0, 0.18, size=(300, 3)), 0, 1)
    ids = np.random.default_rng(7).permutation(len(y))
    train, test = ids[:240], ids[240:]
    xt, yt = x[train], y[train]
    w, b = np.zeros((3, 3)), np.zeros(3)
    target = np.eye(3)[yt]
    history = []
    for step in range(501):
        history.append(objective(xt, yt, w, b))
        if step == 500:
            break
        p = np.exp(log_softmax(xt @ w + b))
        dz = (p - target) / len(yt)
        grad_w = xt.T @ dz
        grad_b = dz.sum(axis=0)
        w -= 0.5 * grad_w
        b -= 0.5 * grad_b
    logp = log_softmax(x[test] @ w + b)
    p = np.exp(logp)
    predicted = p.argmax(axis=1)
    majority = np.bincount(yt, minlength=3).argmax()
    report = {"seed": 2026, "split_seed": 7, "steps": 500, "learning_rate": 0.5,
              "train_count": len(train), "test_count": len(test),
              "initial_train_ce": history[0], "final_train_ce": history[-1],
              "test_ce": float(-logp[np.arange(len(test)), y[test]].mean()),
              "test_accuracy": float(np.mean(predicted == y[test])),
              "majority_baseline_accuracy": float(np.mean(y[test] == majority)),
              "weights": w.tolist(), "bias": b.tolist()}
    assert np.allclose(p.sum(axis=1), 1)
    assert np.isfinite(log_softmax(np.array([[1000., 0., -1000.]]))).all()
    assert history[-1] < history[0]
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for key in ("initial_train_ce", "final_train_ce", "test_ce", "test_accuracy", "majority_baseline_accuracy"):
        print(key, report[key])
    print("extreme log probabilities:", log_softmax(np.array([[1000., 0., -1000.]])))


if __name__ == "__main__":
    main()
