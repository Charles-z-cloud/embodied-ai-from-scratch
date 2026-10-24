import json
from pathlib import Path
import numpy as np
import torch
from torch import nn

TRAIN_TEXTS = ["把红块移到左边", "把蓝块移到右边", "抓红块", "红块在蓝块左边"]
SPECIAL = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"]
vocab = SPECIAL + sorted(set("".join(TRAIN_TEXTS)))
to_id = {token: i for i, token in enumerate(vocab)}


def encode(text):
    return [to_id["<BOS>"]] + [to_id.get(char, to_id["<UNK>"]) for char in text] + [to_id["<EOS>"]]


def decode(ids):
    return "".join(vocab[i] for i in ids if i not in (0, 2, 3))


def bag(text):
    return np.bincount([to_id.get(char, 1) for char in text], minlength=len(vocab))


if __name__ == "__main__":
    for text in TRAIN_TEXTS:
        assert decode(encode(text)) == text
    print("vocabulary size:", len(vocab))
    print("known encoding:", encode(TRAIN_TEXTS[0]))
    print("unknown roundtrip:", decode(encode("抓黄块")))
    sequences = [encode(text) for text in TRAIN_TEXTS[:3]]
    length = max(len(row) for row in sequences)
    padded = [row + [0] * (length - len(row)) for row in sequences]
    ids = torch.tensor(padded, dtype=torch.long)
    torch.manual_seed(7)
    embedding = nn.Embedding(len(vocab), 8, padding_idx=0)
    vectors = embedding(ids)
    content_mask = (ids != 0) & (ids != 2) & (ids != 3)
    counts = content_mask.sum(dim=1, keepdim=True)
    if torch.any(counts == 0):
        raise ValueError("Empty instructions need an explicit handling rule")
    pooled = (vectors * content_mask.unsqueeze(-1)).sum(dim=1) / counts
    print("id / embedded / pooled shapes:", tuple(ids.shape), tuple(vectors.shape), tuple(pooled.shape))
    print("content lengths:", counts.flatten().tolist())
    assert torch.equal(embedding.weight[0], torch.zeros(8))
    assert np.array_equal(bag("红块在蓝块左边"), bag("蓝块在红块左边"))
    print("opposite relations have identical bag-of-characters:", True)
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    (folder / "vocab.json").write_text(json.dumps({"tokens": vocab, "unit": "Unicode code point", "normalization": "none"}, ensure_ascii=False, indent=2), encoding="utf-8")
