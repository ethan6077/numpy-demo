import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


b = 1
w1 = 2
w2 = -1
w3 = 5

x1 = 0
x2 = 10
x3 = 2

z = b + w1 * x1 + w2 * x2 + w3 * x3

y = sigmoid(z)

print(f"z = {z:.3f}")
print(f"y = {y:.3f}")
