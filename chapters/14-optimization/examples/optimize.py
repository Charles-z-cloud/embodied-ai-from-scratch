import numpy as np


def loss(theta):
    w, b = theta
    return (w - 3) ** 2 + 4 * (b + 1) ** 2


def gradient(theta):
    w, b = theta
    return np.array([2 * (w - 3), 8 * (b + 1)])


def optimize(method, learning_rate, steps=100):
    theta = np.array([0., 2.])
    first = np.zeros_like(theta)
    second = np.zeros_like(theta)
    history = [theta.copy()]
    for t in range(1, steps + 1):
        g = gradient(theta)
        if method == "gd":
            direction = g
        elif method == "momentum":
            first = 0.9 * first + g
            direction = first
        elif method == "adam":
            first = 0.9 * first + 0.1 * g
            second = 0.999 * second + 0.001 * g ** 2
            corrected_first = first / (1 - 0.9 ** t)
            corrected_second = second / (1 - 0.999 ** t)
            direction = corrected_first / (np.sqrt(corrected_second) + 1e-8)
        else:
            raise ValueError("Unknown method")
        theta = theta - learning_rate * direction
        if not np.all(np.isfinite(theta)):
            raise FloatingPointError("Non-finite parameters")
        history.append(theta.copy())
    return theta, np.array(history)


if __name__ == "__main__":
    cases = [("gd", 0.02, 100), ("gd", 0.2, 100), ("gd", 0.3, 20),
             ("momentum", 0.05, 100), ("adam", 0.1, 100)]
    for method, lr, steps in cases:
        theta, history = optimize(method, lr, steps)
        print(method, "lr=", lr, "steps=", steps, "theta=", theta,
              "loss=", loss(theta), "gradient_norm=", np.linalg.norm(gradient(theta)))
        if method == "gd" and lr == 0.3:
            assert loss(theta) > loss(history[0])
        else:
            assert loss(theta) < loss(history[0])
