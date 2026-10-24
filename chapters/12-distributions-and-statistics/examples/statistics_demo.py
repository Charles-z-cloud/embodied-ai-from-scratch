import numpy as np


def main(seed=2026):
    rng = np.random.default_rng(seed)
    small = np.array([1., 2., 3.])
    print("small mean / var0 / var1:", small.mean(), small.var(), small.var(ddof=1))
    x = rng.normal(loc=10., scale=0.2, size=2000)
    print("position mean / sample std:", x.mean(), x.std(ddof=1))
    z = (x - x.mean()) / x.std(ddof=0)
    print("standardized mean / var:", z.mean(), z.var())
    assert np.allclose([z.mean(), z.var()], [0., 1.])
    print("n | empirical std of 400 means | theoretical standard error")
    for n in (10, 100, 1000):
        trials = rng.normal(loc=10., scale=0.2, size=(400, n))
        estimates = trials.mean(axis=1)
        print(n, estimates.std(ddof=1), 0.2 / np.sqrt(n))
    xv = np.array([-1., 0., 1.])
    yv = xv ** 2
    covariance = np.mean((xv - xv.mean()) * (yv - yv.mean()))
    print("dependent but covariance zero:", covariance)
    bernoulli = (rng.random(10000) < 0.8).astype(float)
    categories = rng.choice(["red", "blue", "green"], size=10000, p=[0.5, 0.3, 0.2])
    print("Bernoulli mean / variance:", bernoulli.mean(), bernoulli.var())
    print("category frequencies:", {name: np.mean(categories == name) for name in ("red", "blue", "green")})


if __name__ == "__main__":
    main()
