import numpy as np

angle = np.pi / 2
R = np.array([[np.cos(angle), -np.sin(angle)],
              [np.sin(angle), np.cos(angle)]])
points = np.array([[3., 4.], [1., 0.], [-2., 1.]])
rotated = points @ R.T
before = np.linalg.norm(points, axis=1)
after = np.linalg.norm(rotated, axis=1)
print("rotated:\n", np.round(rotated, 6))
print("lengths:", before, after)
assert np.allclose(before, after)
assert np.allclose(R.T @ R, np.eye(2))
S = np.diag([2., 1.])
x = np.array([1., 0.])
print("scale then rotate:", np.round(R @ S @ x, 6))
print("rotate then scale:", np.round(S @ R @ x, 6))
A = np.array([[2., 1.], [1., -1.]])
b = np.array([5., 1.])
solution = np.linalg.solve(A, b)
print("solution:", solution)
assert np.allclose(A @ solution, b)
collapsed = np.array([[1., 0.], [0., 0.]])
print("collapsed rank:", np.linalg.matrix_rank(collapsed))
u = np.array([1., 1.])
v = np.array([2., 0.])
projection = (u @ v) / (u @ u) * u
print("projection:", projection, "orthogonality:", u @ (v - projection))
measurements = np.array([2., 3., 4.])
design = np.ones((3, 1))
fit, _, rank, _ = np.linalg.lstsq(design, measurements, rcond=None)
residual = design @ fit - measurements
print("least squares:", fit, "squared residual:", residual @ residual, "rank:", rank)
assert np.allclose(fit, [3.])
try:
    np.linalg.solve(collapsed, np.array([1., 2.]))
except np.linalg.LinAlgError:
    print("singular solve correctly rejected")
else:
    raise AssertionError("Expected singular matrix to be rejected")
