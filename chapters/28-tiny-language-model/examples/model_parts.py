import math
import torch
from torch import nn


class SinusoidalPosition(nn.Module):
    def __init__(self, width, max_length):
        super().__init__()
        if width % 2:
            raise ValueError("This teaching implementation requires even width")
        position = torch.arange(max_length, dtype=torch.float32)[:, None]
        frequency = torch.exp(torch.arange(0, width, 2) * (-math.log(10000.0) / width))
        table = torch.zeros(max_length, width)
        table[:, 0::2] = torch.sin(position * frequency)
        table[:, 1::2] = torch.cos(position * frequency)
        self.register_buffer("table", table)

    def forward(self, x):
        if x.shape[1] > len(self.table):
            raise ValueError("Sequence exceeds configured context")
        return x + self.table[:x.shape[1]].to(dtype=x.dtype)


class CausalAttention(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.heads, self.head_dim = heads, width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.output = nn.Linear(width, width)

    def forward(self, x):
        batch, length, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q, k, v = [item.reshape(batch, length, self.heads, self.head_dim).transpose(1, 2)
                   for item in (q, k, v)]
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
        allowed = torch.ones(length, length, device=x.device, dtype=torch.bool).tril()
        weights = torch.softmax(scores.masked_fill(~allowed, float("-inf")), dim=-1)
        mixed = (weights @ v).transpose(1, 2).reshape(batch, length, width)
        return self.output(mixed)


class DecoderBlock(nn.Module):
    def __init__(self, width=16, heads=4, ff_width=64):
        super().__init__()
        self.norm1 = nn.LayerNorm(width)
        self.attention = CausalAttention(width, heads)
        self.norm2 = nn.LayerNorm(width)
        self.ffn = nn.Sequential(nn.Linear(width, ff_width), nn.GELU(), nn.Linear(ff_width, width))

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        return x + self.ffn(self.norm2(x))
