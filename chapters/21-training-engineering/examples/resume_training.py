from pathlib import Path
import torch
from torch import nn


def create():
    model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Dropout(0.2), nn.Linear(8, 1))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
    return model, optimizer, scheduler


def run(model, optimizer, scheduler, x, y, steps):
    model.train()
    losses = []
    for _ in range(steps):
        ids = torch.randint(len(x), (4,))
        optimizer.zero_grad(set_to_none=True)
        loss = ((model(x[ids]) - y[ids]) ** 2).mean()
        loss.backward()
        optimizer.step()
        scheduler.step()
        losses.append(loss.item())
    return losses


if __name__ == "__main__":
    torch.set_num_threads(1)
    torch.manual_seed(2026)
    x = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.], [-1., 0.], [0., -1.]])
    y = 2 * x[:, :1] - x[:, 1:] + 0.3
    model, optimizer, scheduler = create()
    run(model, optimizer, scheduler, x, y, 20)
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    path = folder / "checkpoint.pt"
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                "scheduler": scheduler.state_dict(), "cpu_rng": torch.get_rng_state(),
                "step": 20, "config": {"seed": 2026, "batch_size": 4, "initial_lr": 0.01}}, path)
    uninterrupted = run(model, optimizer, scheduler, x, y, 30)
    restored, opt2, sched2 = create()
    checkpoint = torch.load(path, weights_only=True, map_location="cpu")
    restored.load_state_dict(checkpoint["model"])
    opt2.load_state_dict(checkpoint["optimizer"])
    sched2.load_state_dict(checkpoint["scheduler"])
    torch.set_rng_state(checkpoint["cpu_rng"])
    resumed = run(restored, opt2, sched2, x, y, 30)
    same_parameters = all(torch.equal(a, b) for a, b in zip(model.parameters(), restored.parameters()))
    print("resumed steps:", len(resumed), "loss sequence equal:", uninterrupted == resumed)
    print("parameters exactly equal:", same_parameters, "final lr:", sched2.get_last_lr())
    assert uninterrupted == resumed and same_parameters
