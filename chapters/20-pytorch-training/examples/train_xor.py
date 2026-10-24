import json
from pathlib import Path
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader


class XORNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 1))

    def forward(self, x):
        return self.layers(x)


def main():
    torch.manual_seed(7)
    torch.set_num_threads(1)
    device = torch.device("cpu")
    x = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=torch.float32)
    y = torch.tensor([[0.], [1.], [1.], [0.]], dtype=torch.float32)
    loader = DataLoader(TensorDataset(x, y), batch_size=2, shuffle=True, num_workers=0,
                        generator=torch.Generator().manual_seed(7))
    model = XORNet().to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    with torch.no_grad():
        initial_loss = criterion(model(x), y).item()
    history = []
    for epoch in range(400):
        model.train()
        total, count = 0.0, 0
        for features, targets in loader:
            features, targets = features.to(device), targets.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(features)
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()
            total += loss.item() * len(features)
            count += len(features)
        history.append(total / count)
    model.eval()
    with torch.no_grad():
        logits = model(x)
        probability = torch.sigmoid(logits)
        final_loss = criterion(logits, y).item()
        accuracy = ((probability >= 0.5) == y.bool()).float().mean().item()
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    path = folder / "xor_weights.pt"
    torch.save(model.state_dict(), path)
    restored = XORNet().to(device)
    restored.load_state_dict(torch.load(path, map_location=device, weights_only=True))
    restored.eval()
    with torch.no_grad():
        reloaded_logits = restored(x)
    assert torch.equal(logits, reloaded_logits)
    assert final_loss < initial_loss and accuracy == 1.0
    report = {"torch_version": torch.__version__, "device": str(device), "seed": 7,
              "epochs": 400, "batch_size": 2, "learning_rate": 0.03,
              "parameter_count": sum(p.numel() for p in model.parameters()),
              "initial_loss": initial_loss, "final_loss": final_loss,
              "truth_table_fit_accuracy": accuracy, "probabilities": probability.flatten().tolist(),
              "reload_equal": True, "epoch_mean_losses": history}
    (folder / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("torch / device:", torch.__version__, device)
    print("parameters:", report["parameter_count"])
    print("loss:", initial_loss, "->", final_loss)
    print("probabilities:", report["probabilities"])
    print("truth-table fit accuracy:", accuracy, "reload exactly equal:", True)


if __name__ == "__main__":
    main()
