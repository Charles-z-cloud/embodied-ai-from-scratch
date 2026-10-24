import torch
from attention import attention

torch.manual_seed(7)
batch, length, width, heads = 2, 3, 8, 2
head_dim = width // heads
x = torch.randn(batch, length, width)
wq, wk, wv, wo = [torch.randn(width, width) * 0.2 for _ in range(4)]


def split_heads(tensor):
    return tensor.reshape(batch, length, heads, head_dim).transpose(1, 2)


q, k, v = [split_heads(x @ weight) for weight in (wq, wk, wv)]
result, weights = attention(q, k, v)
merged = result.transpose(1, 2).reshape(batch, length, width)
output = merged @ wo
print("Q/K/V:", q.shape, k.shape, v.shape)
print("scores:", weights.shape, "merged:", merged.shape, "output:", output.shape)
assert tuple(weights.shape) == (2, 2, 3, 3) and output.shape == x.shape
