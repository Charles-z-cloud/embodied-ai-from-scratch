import numpy as np


def sigmoid(z):
    return np.exp(-np.logaddexp(0.0, -z))


def forward(x, w1, b1, w2, b2):
    preactivation = x @ w1 + b1
    hidden = np.maximum(0.0, preactivation)
    logits = hidden @ w2 + b2
    return hidden, logits


if __name__ == "__main__":
    x = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    w1 = np.array([[1., 1.], [1., 1.]])
    b1 = np.array([0., -1.])
    w2 = np.array([[10.], [-20.]])
    b2 = np.array([-5.])
    hidden, logits = forward(x, w1, b1, w2, b2)
    probability = sigmoid(logits)
    print("XOR hidden:\n", hidden)
    print("XOR logits:", logits.ravel())
    print("XOR probabilities:", probability.ravel())
    assert np.array_equal((probability.ravel() >= 0.5).astype(int), [0, 1, 1, 0])
    rng = np.random.default_rng(2026)
    batch = rng.normal(size=(5, 3))
    w1 = rng.normal(0, np.sqrt(2 / 3), size=(3, 4))
    b1 = np.zeros(4)
    w2 = rng.normal(0, np.sqrt(1 / 4), size=(4, 2))
    b2 = np.zeros(2)
    hidden, logits = forward(batch, w1, b1, w2, b2)
    parameter_count = sum(array.size for array in (w1, b1, w2, b2))
    print("random MLP shapes:", batch.shape, hidden.shape, logits.shape)
    print("parameter count:", parameter_count)
    assert parameter_count == 26 and logits.shape == (5, 2)
