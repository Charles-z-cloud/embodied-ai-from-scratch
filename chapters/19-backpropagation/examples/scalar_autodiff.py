class Node:
    def __init__(self, value, parents=()):
        self.value = float(value)
        self.parents = list(parents)
        self.grad = 0.0

    def backward(self):
        order, seen = [], set()

        def visit(node):
            if node in seen:
                return
            seen.add(node)
            for parent, _ in node.parents:
                visit(parent)
            order.append(node)

        visit(self)
        for node in order:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(order):
            for parent, local_derivative in node.parents:
                parent.grad += node.grad * local_derivative


def add(a, b):
    return Node(a.value + b.value, [(a, 1.0), (b, 1.0)])


def multiply(a, b):
    return Node(a.value * b.value, [(a, b.value), (b, a.value)])


def relu(a):
    return Node(max(0.0, a.value), [(a, float(a.value > 0))])


if __name__ == "__main__":
    x = Node(3)
    loss = add(multiply(x, x), x)
    loss.backward()
    print("x*x+x value / gradient:", loss.value, x.grad)
    assert loss.value == 12 and x.grad == 7
    loss.backward()
    assert x.grad == 7
    w, x, b = Node(2), Node(3), Node(1)
    prediction = add(multiply(w, x), b)
    residual = add(prediction, Node(-5))
    loss = multiply(residual, residual)
    loss.backward()
    print("linear squared loss:", loss.value, "grad_w:", w.grad, "grad_b:", b.grad)
    assert loss.value == 4 and w.grad == 12 and b.grad == 4
    shared = Node(2)
    a = multiply(shared, shared)
    add(a, a).backward()
    assert shared.grad == 8
    for value in (-2, 0, 2):
        node = Node(value)
        relu(node).backward()
        print("ReLU value / gradient:", value, node.grad)
