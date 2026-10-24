import numpy as np


def forward_backward(x, y, parameters):
    w1, b1, w2, b2 = parameters
    a = x @ w1 + b1
    h = np.maximum(0.0, a)
    prediction = h @ w2 + b2
    residual = prediction - y
    loss = np.mean(residual ** 2)
    gz = 2 * residual / len(x)
    gw2 = h.T @ gz
    gb2 = gz.sum(axis=0)
    gh = gz @ w2.T
    ga = gh * (a > 0)
    gw1 = x.T @ ga
    gb1 = ga.sum(axis=0)
    return float(loss), [gw1, gb1, gw2, gb2]


if __name__ == "__main__":
    x = np.array([[0.2, -0.3], [0.8, 0.1]])
    y = np.array([[0.4], [-0.2]])
    parameters = [np.array([[0.3, -0.2, 0.4], [0.1, 0.3, -0.2]]),
                  np.array([0.5, -0.5, 0.2]), np.array([[0.4], [0.2], [-0.3]]), np.array([0.1])]
    loss, analytic = forward_backward(x, y, parameters)
    eps = 1e-5
    print("loss:", loss)
    for name, parameter, expected in zip(("w1", "b1", "w2", "b2"), parameters, analytic):
        numerical = np.zeros_like(parameter)
        for index in np.ndindex(parameter.shape):
            original = parameter[index]
            parameter[index] = original + eps
            plus, _ = forward_backward(x, y, parameters)
            parameter[index] = original - eps
            minus, _ = forward_backward(x, y, parameters)
            parameter[index] = original
            numerical[index] = (plus - minus) / (2 * eps)
        difference = np.max(np.abs(expected - numerical))
        print(name, "shape", parameter.shape, "max difference", difference)
        assert np.allclose(expected, numerical, atol=1e-8, rtol=1e-6)
