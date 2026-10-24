import math

xs = [2, 4, 6]
total = 0
product = 1
square_sum = 0
for x in xs:
    total = total + x
    product = product * x
    square_sum = square_sum + x ** 2
print("和、平方和、和的平方、连乘：", total, square_sum, total ** 2, product)


def f(x):
    return 2 * x + 1


def g(x):
    return x ** 2


print("复合：", f(g(3)), g(f(3)))
print("log2(8)：", math.log2(8))
print("exp(log(4))：", math.exp(math.log(4)))
print("90度的sin：", math.sin(math.pi / 2))
