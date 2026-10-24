import numpy as np

TRAIN = ["把红块移到左边", "把蓝块移到右边", "把红块移到右边", "把蓝块移到左边",
         "抓起红块", "抓起蓝块", "放下红块", "放下蓝块"]
VALIDATION = ["把红块放到左边", "把蓝块放到右边"]
BOS, EOS, UNK = 0, 1, 2
vocab = ["<BOS>", "<EOS>", "<UNK>"] + sorted(set("".join(TRAIN)))
lookup = {token: i for i, token in enumerate(vocab)}


def encode(text):
    return [BOS] + [lookup.get(char, UNK) for char in text] + [EOS]


def fit(texts, alpha=0.1):
    counts = np.zeros((len(vocab), len(vocab)))
    for text in texts:
        sequence = encode(text)
        for previous, target in zip(sequence[:-1], sequence[1:]):
            counts[previous, target] += 1
    counts[:, 1:] += alpha
    return counts / counts.sum(axis=1, keepdims=True)


def score(texts, probability):
    total, length = 0.0, 0
    for text in texts:
        sequence = encode(text)
        for previous, target in zip(sequence[:-1], sequence[1:]):
            total -= np.log(probability[previous, target])
            length += 1
    nll = total / length
    return float(nll), float(np.exp(nll)), length


def generate(probability, greedy=False, temperature=1.0, seed=7, max_tokens=24):
    if temperature <= 0:
        raise ValueError("Use greedy=True for argmax; temperature must be positive")
    rng = np.random.default_rng(seed)
    previous, result = BOS, []
    for _ in range(max_tokens):
        p = probability[previous].copy()
        if greedy:
            token = int(p.argmax())
        else:
            weights = np.zeros_like(p)
            positive = p > 0
            logits = np.log(p[positive]) / temperature
            weights[positive] = np.exp(logits - logits.max())
            weights /= weights.sum()
            token = int(rng.choice(len(vocab), p=weights))
        if token == EOS:
            return "".join(result), "EOS"
        result.append(vocab[token])
        previous = token
    return "".join(result), "length_limit"


if __name__ == "__main__":
    p = fit(TRAIN)
    assert np.allclose(p.sum(axis=1), 1) and np.all(p[:, BOS] == 0)
    print("train NLL / PPL / tokens:", score(TRAIN, p))
    print("held-out NLL / PPL / tokens:", score(VALIDATION, p))
    print("greedy:", generate(p, greedy=True))
    for temperature in (0.7, 1.0, 1.5):
        print("sample temperature", temperature, generate(p, temperature=temperature))
    print("input:", [vocab[i] for i in encode("抓起红块")[:-1]])
    print("target:", [vocab[i] for i in encode("抓起红块")[1:]])
