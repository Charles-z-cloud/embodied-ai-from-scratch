import numpy as np
import torch
from torch import nn

x_np = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=np.float32)
w1 = np.array([[1., 1.], [1., 1.]], dtype=np.float32)
b1 = np.array([0., -1.], dtype=np.float32)
w2 = np.array([[10.], [-20.]], dtype=np.float32)
b2 = np.array([-5.], dtype=np.float32)
reference = np.maximum(0, x_np @ w1 + b1) @ w2 + b2
model = nn.Sequential(nn.Linear(2, 2), nn.ReLU(), nn.Linear(2, 1))
with torch.no_grad():
    model[0].weight.copy_(torch.from_numpy(w1.T))
    model[0].bias.copy_(torch.from_numpy(b1))
    model[2].weight.copy_(torch.from_numpy(w2.T))
    model[2].bias.copy_(torch.from_numpy(b2))
    result = model(torch.from_numpy(x_np))
print("numpy logits:", reference.ravel())
print("torch logits:", result.flatten().tolist())
assert np.allclose(reference, result.numpy())
w = torch.tensor(2., requires_grad=True)
(w * w).backward()
print("first gradient:", w.grad.item())
(w * w).backward()
print("accumulated gradient:", w.grad.item())
assert w.grad.item() == 8
w.grad = None
(w * w).backward()
assert w.grad.item() == 4
print("after clearing:", w.grad.item())
