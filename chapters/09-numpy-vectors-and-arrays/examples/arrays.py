import numpy as np

X = np.array([[2, 5], [3, 5], [4, 6]], dtype=float)
A = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
B = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
product = A @ B
print("X形状与轴数：", X.shape, X.ndim)
print("矩阵乘积：\n", product)
print("按轴0求和：", X.sum(axis=0))
print("按轴1求和：", X.sum(axis=1))
print("平移后：\n", X + np.array([1., -1.]))
prediction = np.array([1., 2., 3.])
target = np.array([[1.], [2.], [3.]])
wrong_error = prediction - target
correct_error = prediction.reshape(3, 1) - target
print("错误与正确误差形状：", wrong_error.shape, correct_error.shape)
print("正确误差：\n", correct_error)
independent = X[:, 0].copy()
independent[0] = 99
print("副本变化后原数组首项：", X[0, 0])
