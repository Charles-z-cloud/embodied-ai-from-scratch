import numpy as np


def loss(theta):
    w, b = theta
    return (w * 2.0 + b - 5.0) ** 2


def analytic_gradient(theta):
    w, b = theta
    residual = w * 2.0 + b - 5.0
    return np.array([2 * residual * 2.0, 2 * residual])


def central_gradient(fn, theta, h=1e-5):
    theta = np.asarray(theta, dtype=float)
    result = np.zeros_like(theta)
    for i in range(theta.size):
        plus, minus = theta.copy(), theta.copy()
        plus[i] += h
        minus[i] -= h
        result[i] = (fn(plus) - fn(minus)) / (2 * h)
    return result


if __name__ == "__main__":
    theta = np.array([1., 0.])
    analytic = analytic_gradient(theta)
    numerical = central_gradient(loss, theta)
    print("loss:", loss(theta))
    print("analytic / numerical:", analytic, numerical)
    assert np.allclose(analytic, numerical, rtol=1e-6, atol=1e-7)
    updated = theta - 0.01 * analytic
    print("updated parameters / loss:", updated, loss(updated))
    assert loss(updated) < loss(theta)
    for h in (0.1, 0.001, 1e-8, 1e-15):
        estimate = ((3 * (2 + h) + 1) ** 2 - (3 * (2 - h) + 1) ** 2) / (2 * h)
        print("h / derivative / absolute error:", h, estimate, abs(estimate - 42.0))
