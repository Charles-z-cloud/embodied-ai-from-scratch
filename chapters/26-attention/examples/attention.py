import math
import torch
import torch.nn.functional as F


def attention(q, k, v, allowed=None):
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if allowed is not None:
        if not bool(allowed.any(dim=-1).all()):
            raise ValueError("Every query must have at least one allowed key")
        scores = scores.masked_fill(~allowed, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return weights @ v, weights


if __name__ == "__main__":
    q = torch.tensor([[math.log(2)]], dtype=torch.float64)
    k = torch.tensor([[1.], [0.], [0.]], dtype=torch.float64)
    v = torch.tensor([[2., 0.], [0., 2.], [2., 2.]], dtype=torch.float64)
    output, weights = attention(q, k, v)
    print("hand weights / output:", weights.tolist(), output.tolist())
    assert torch.allclose(output, torch.tensor([[1.5, 1.]], dtype=torch.float64))
    torch.manual_seed(7)
    x = torch.randn(1, 4, 8, dtype=torch.float64)
    causal = torch.ones(4, 4, dtype=torch.bool).tril()
    original, weights = attention(x, x, x, causal)
    changed = x.clone()
    changed[:, 3, :] += 20
    after, _ = attention(changed, changed, changed, causal)
    causal_difference = (original[:, :3] - after[:, :3]).abs().max().item()
    unrestricted, _ = attention(x, x, x)
    unrestricted_changed, _ = attention(changed, changed, changed)
    unrestricted_difference = (unrestricted[:, :3] - unrestricted_changed[:, :3]).abs().max().item()
    assert causal_difference == 0 and unrestricted_difference > 1e-6
    reference = F.scaled_dot_product_attention(x, x, x, attn_mask=causal, dropout_p=0.0)
    assert torch.allclose(original, reference, atol=1e-12, rtol=1e-12)
    print("future change: causal / unrestricted:", causal_difference, unrestricted_difference)
    key_valid = torch.tensor([True, True, True, False])
    allowed = causal & key_valid[None, :]
    _, padded_weights = attention(x, x, x, allowed)
    assert torch.all(padded_weights[..., 3] == 0)
    assert torch.allclose(padded_weights.sum(-1), torch.ones(1, 4, dtype=torch.float64))
    try:
        attention(x, x, x, torch.zeros(4, 4, dtype=torch.bool))
    except ValueError:
        print("all-masked query correctly rejected")
    else:
        raise AssertionError("All-masked query should fail")
    print("padding / row sums / official reference checks passed")
