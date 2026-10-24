import copy
import itertools
import json
import math
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from model_parts import DecoderBlock, SinusoidalPosition

PAD, UNK, BOS, EOS = 0, 1, 2, 3


class TinyLanguageModel(nn.Module):
    def __init__(self, vocabulary_size, context):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, 32, padding_idx=PAD)
        self.position = SinusoidalPosition(32, context)
        self.blocks = nn.Sequential(DecoderBlock(32, 4, 128), DecoderBlock(32, 4, 128))
        self.norm = nn.LayerNorm(32)
        self.head = nn.Linear(32, vocabulary_size)

    def forward(self, ids):
        x = self.position(self.embedding(ids))
        logits = self.head(self.norm(self.blocks(x)))
        excluded = torch.zeros(logits.shape[-1], dtype=torch.bool, device=ids.device)
        excluded[PAD], excluded[BOS] = True, True
        return logits.masked_fill(excluded, float("-inf"))


def prepare():
    sentences = [prefix + "把" + color + "色" + shape + verb + direction + "边。"
                 for prefix, color, shape, verb, direction in itertools.product(
                     ["", "请", "现在"], ["红", "蓝", "绿"], ["方块", "圆球"], ["移到", "推到"], ["左", "右", "前", "后"])]
    order = np.random.default_rng(7).permutation(len(sentences))
    splits = {"train": [sentences[i] for i in order[:100]],
              "validation": [sentences[i] for i in order[100:122]],
              "test": [sentences[i] for i in order[122:]]}
    assert len(sentences) == len(set(sentences)) == 144
    assert set(splits["train"]).isdisjoint(splits["test"])
    assert set(splits["validation"]).isdisjoint(splits["test"])
    vocabulary = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"] + sorted(set("".join(splits["train"])))
    lookup = {token: i for i, token in enumerate(vocabulary)}
    encoded = {}
    for name, texts in splits.items():
        encoded[name] = [[BOS] + [lookup.get(char, UNK) for char in text] + [EOS] for text in texts]
        assert all(UNK not in row for row in encoded[name])
    return splits, vocabulary, encoded


def windows(sequences, context):
    inputs, lengths, targets = [], [], []
    for sequence in sequences:
        for t in range(1, len(sequence)):
            prefix = sequence[max(0, t - context):t]
            inputs.append(prefix + [PAD] * (context - len(prefix)))
            lengths.append(len(prefix))
            targets.append(sequence[t])
    return torch.tensor(inputs), torch.tensor(lengths), torch.tensor(targets)


def last_logits(model, data):
    x, lengths, _ = data
    logits = model(x)
    return logits[torch.arange(len(x)), lengths - 1]


def evaluate(model, data):
    model.eval()
    total, count = 0.0, len(data[0])
    with torch.no_grad():
        for start in range(0, count, 128):
            batch = tuple(item[start:start + 128] for item in data)
            total += F.cross_entropy(last_logits(model, batch), batch[2], reduction="sum").item()
    nll = total / count
    return {"nll": nll, "ppl": math.exp(nll), "target_tokens": count}


def generate(model, vocabulary, context, greedy, seed, temperature=0.8):
    generator = torch.Generator().manual_seed(seed)
    ids, text = [BOS], []
    model.eval()
    with torch.no_grad():
        for _ in range(30):
            logits = model(torch.tensor([ids[-context:]]))[0, -1]
            if greedy:
                token = int(logits.argmax())
            else:
                token = int(torch.multinomial(torch.softmax(logits / temperature, dim=-1), 1, generator=generator))
            if token == EOS:
                return {"text": "".join(text), "stop": "EOS"}
            text.append(vocabulary[token])
            ids.append(token)
    return {"text": "".join(text), "stop": "length_limit"}


def bigram_score(train, evaluation, vocabulary_size):
    counts = np.zeros((vocabulary_size, vocabulary_size))
    for row in train:
        for a, b in zip(row[:-1], row[1:]):
            counts[a, b] += 1
    allowed = [i for i in range(vocabulary_size) if i not in (PAD, BOS)]
    counts[:, allowed] += 0.1
    probability = counts / counts.sum(axis=1, keepdims=True)
    losses = [-np.log(probability[a, b]) for row in evaluation for a, b in zip(row[:-1], row[1:])]
    nll = float(np.mean(losses))
    return {"nll": nll, "ppl": math.exp(nll), "target_tokens": len(losses)}


def train_one(context, vocabulary, encoded, folder):
    torch.manual_seed(7)
    model = TinyLanguageModel(len(vocabulary), context)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    train = windows(encoded["train"], context)
    validation = windows(encoded["validation"], context)
    generator = torch.Generator().manual_seed(11)
    best_nll, best_state, best_step = float("inf"), None, None
    history = []
    for step in range(1, 401):
        model.train()
        indices = torch.randint(len(train[0]), (32,), generator=generator)
        batch = tuple(item[indices] for item in train)
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(last_logits(model, batch), batch[2])
        loss.backward()
        optimizer.step()
        if step % 50 == 0:
            score = evaluate(model, validation)
            history.append({"step": step, "validation": score})
            if score["nll"] < best_nll:
                best_nll, best_step = score["nll"], step
                best_state = copy.deepcopy(model.state_dict())
            print("context", context, "step", step, "validation", score, flush=True)
    model.load_state_dict(best_state)
    test = windows(encoded["test"], context)
    result = {"context": context, "best_step": best_step, "test": evaluate(model, test),
              "parameters": sum(p.numel() for p in model.parameters()), "history": history,
              "greedy": generate(model, vocabulary, context, True, 7),
              "samples": [generate(model, vocabulary, context, False, seed) for seed in (7, 8, 9)]}
    path = folder / f"model_context_{context}.pt"
    torch.save({"state": model.state_dict(), "context": context, "vocabulary": vocabulary}, path)
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    restored = TinyLanguageModel(len(checkpoint["vocabulary"]), checkpoint["context"])
    restored.load_state_dict(checkpoint["state"])
    restored.eval(); model.eval()
    with torch.no_grad():
        before = last_logits(model, tuple(item[:8] for item in test))
        after = last_logits(restored, tuple(item[:8] for item in test))
    assert torch.equal(before, after)
    print("context", context, "test", result["test"], "greedy", result["greedy"], "samples", result["samples"], flush=True)
    return result


if __name__ == "__main__":
    torch.set_num_threads(1)
    splits, vocabulary, encoded = prepare()
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    (folder / "splits.json").write_text(json.dumps(splits, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"torch_version": torch.__version__, "device": "cpu", "split_seed": 7,
              "model_seed": 7, "batch_seed": 11, "steps": 400, "batch_size": 32,
              "learning_rate": 0.003, "vocabulary": vocabulary,
              "split_sizes": {name: len(texts) for name, texts in splits.items()},
              "bigram_test": bigram_score(encoded["train"], encoded["test"], len(vocabulary))}
    print("bigram test:", report["bigram_test"], flush=True)
    report["models"] = [train_one(context, vocabulary, encoded, folder) for context in (4, 16)]
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
