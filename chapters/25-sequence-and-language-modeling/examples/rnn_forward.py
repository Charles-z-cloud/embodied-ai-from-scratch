import numpy as np

rng = np.random.default_rng(7)
vocab_size, embedding_dim, hidden_dim = 6, 4, 5
embedding = rng.normal(0, 0.2, (vocab_size, embedding_dim))
wx = rng.normal(0, 0.2, (embedding_dim, hidden_dim))
wh = rng.normal(0, 0.2, (hidden_dim, hidden_dim))
wo = rng.normal(0, 0.2, (hidden_dim, vocab_size))
ids = np.array([[0, 1, 2], [2, 1, 0]])
h = np.zeros((2, hidden_dim))
for t in range(ids.shape[1]):
    e = embedding[ids[:, t]]
    h = np.tanh(e @ wx + h @ wh)
    logits = h @ wo
    print("step", t, "hidden", h.shape, "logits", logits.shape)
print("same tokens, different order, hidden-state difference:", np.linalg.norm(h[0] - h[1]))
assert not np.allclose(h[0], h[1])
