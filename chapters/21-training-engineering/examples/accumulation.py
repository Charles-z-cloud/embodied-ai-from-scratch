import copy
import torch
from torch import nn

torch.manual_seed(7)
x = torch.randn(5, 2, dtype=torch.float64)
y = torch.randn(5, 1, dtype=torch.float64)
whole = nn.Linear(2, 1).double()
chunks = copy.deepcopy(whole)
((whole(x) - y) ** 2).mean().backward()
for start, end in ((0, 3), (3, 5)):
    loss_sum = ((chunks(x[start:end]) - y[start:end]) ** 2).sum()
    (loss_sum / len(x)).backward()
for name, full, partial in zip(("weight", "bias"), whole.parameters(), chunks.parameters()):
    error = (full.grad - partial.grad).abs().max().item()
    print(name, "gradient difference:", error)
    assert torch.allclose(full.grad, partial.grad, atol=1e-12, rtol=1e-12)
