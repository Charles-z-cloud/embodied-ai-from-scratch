import copy
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

NAMES = ["red square", "red circle", "blue square", "blue circle"]


def make_data(n, seed, shifted=False):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[:32, :32]
    images, labels, centers = [], [], []
    colors = np.array([[0.9, 0.15, 0.12], [0.12, 0.2, 0.9]])
    for _ in range(n):
        label = int(rng.integers(4))
        cx, cy = rng.integers(7, 25, size=2)
        radius = int(rng.integers(3, 6))
        background = np.full((32, 32), rng.uniform(0.02, 0.12))
        if shifted:
            background = 0.3 + 0.25 * ((xx // 3) % 2)
        image = np.repeat(background[..., None], 3, axis=2)
        if label % 2 == 0:
            mask = (np.abs(xx - cx) <= radius) & (np.abs(yy - cy) <= radius)
        else:
            mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius ** 2
        image[mask] = colors[label // 2]
        image = np.clip(image + rng.normal(0, 0.015, image.shape), 0, 1)
        images.append(image.transpose(2, 0, 1))
        labels.append(label)
        centers.append([cx / 31, cy / 31])
    return (torch.tensor(np.array(images), dtype=torch.float32), torch.tensor(labels, dtype=torch.long),
            torch.tensor(centers, dtype=torch.float32))


class TinyVision(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(nn.Conv2d(3, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                                      nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                                      nn.Flatten(), nn.Linear(16 * 8 * 8, 64), nn.ReLU())
        self.class_head = nn.Linear(64, 4)
        self.center_head = nn.Linear(64, 2)

    def forward(self, x):
        features = self.features(x)
        return self.class_head(features), torch.sigmoid(self.center_head(features))


def evaluate(model, data):
    model.eval()
    x, labels, centers = data
    with torch.no_grad():
        logits, predicted_centers = model(x)
        ce = nn.functional.cross_entropy(logits, labels).item()
        mse = nn.functional.mse_loss(predicted_centers, centers).item()
        accuracy = (logits.argmax(1) == labels).float().mean().item()
        distance = ((predicted_centers - centers) * 31).norm(dim=1).mean().item()
    return {"ce": ce, "position_mse": mse, "total_loss": ce + 5 * mse,
            "accuracy": accuracy, "center_distance_pixels": distance}, logits, predicted_centers


def main():
    torch.set_num_threads(1)
    torch.manual_seed(7)
    train, validation = make_data(512, 100), make_data(128, 101)
    model = TinyVision()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loader = DataLoader(TensorDataset(*train), batch_size=32, shuffle=True,
                        generator=torch.Generator().manual_seed(7))
    history, best_loss, best_state, best_epoch = [], float("inf"), None, None
    for epoch in range(1, 26):
        model.train()
        total = 0.0
        for x, labels, centers in loader:
            optimizer.zero_grad(set_to_none=True)
            logits, predicted_centers = model(x)
            loss = nn.functional.cross_entropy(logits, labels) + 5 * nn.functional.mse_loss(predicted_centers, centers)
            loss.backward()
            optimizer.step()
            total += loss.item() * len(x)
        val_metrics, _, _ = evaluate(model, validation)
        history.append({"epoch": epoch, "train_loss": total / len(train[0]), "validation": val_metrics})
        if val_metrics["total_loss"] < best_loss:
            best_loss, best_epoch = val_metrics["total_loss"], epoch
            best_state = copy.deepcopy(model.state_dict())
        if epoch in (1, 5, 10, 15, 20, 25):
            print("epoch", epoch, "train loss", history[-1]["train_loss"], "validation", val_metrics, flush=True)
    model.load_state_dict(best_state)
    majority = train[1].bincount(minlength=4).argmax()
    center_mean = train[2].mean(dim=0)
    report = {"model_seed": 7, "train_seed": 100, "validation_seed": 101, "test_seed": 102,
              "shifted_test_seed": 103, "epochs": 25, "batch_size": 32, "learning_rate": 0.003,
              "best_epoch": best_epoch, "parameters": sum(p.numel() for p in model.parameters()), "history": history}
    fig, axes = plt.subplots(2, 4, figsize=(12, 6), layout="constrained")
    for row, (name, seed, shift) in enumerate((("same_condition", 102, False), ("changed_background", 103, True))):
        data = make_data(128, seed, shift)
        result, logits, predicted = evaluate(model, data)
        result["baseline_accuracy"] = (data[1] == majority).float().mean().item()
        result["baseline_center_distance_pixels"] = ((data[2] - center_mean) * 31).norm(dim=1).mean().item()
        report[name] = result
        print(name, result, flush=True)
        for col in range(4):
            ax = axes[row, col]
            ax.imshow(data[0][col].permute(1, 2, 0).numpy())
            true_center, prediction = data[2][col].numpy() * 31, predicted[col].numpy() * 31
            ax.scatter(*true_center, marker="+", c="lime", s=90, linewidths=2)
            ax.scatter(*prediction, marker="x", c="yellow", s=55)
            ax.set_title("true: " + NAMES[int(data[1][col])] + "\npred: " + NAMES[int(logits[col].argmax())], fontsize=9)
            ax.set_xticks([]); ax.set_yticks([])
        axes[row, 0].set_ylabel(name.replace("_", " "))
    root = Path(__file__).resolve().parents[1]
    (root / "figures").mkdir(exist_ok=True)
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    fig.savefig(root / "figures" / "predictions.png", dpi=150)
    torch.save(model.state_dict(), folder / "vision_weights.pt")
    (folder / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("best epoch / parameters:", best_epoch, report["parameters"])


if __name__ == "__main__":
    main()
