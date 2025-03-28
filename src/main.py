import math
import collections

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from_list = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("from_list shape: ", from_list.shape)
print("from_list dtype: ", from_list.dtype)

zero_1d = np.zeros(8)
print("zero_1d: ", zero_1d)

zero_2d = np.zeros((8, 8), np.int32)
# print("zero_2d: ", zero_2d)
print("zero_2d ndim: ", zero_2d.ndim)

linear = np.linspace(0, 100, 11)
print("linear: ", linear)
# plt.plot(linear, "o")
# plt.show()

nd_arranged = np.arange(10)
print("nd_arranged: ", nd_arranged)

spaced = np.arange(0, 100, 10)
print(f"spaced: {spaced} with the size: {spaced.size}")

rand_2d = np.random.random(size=(10, 10))
# print("rand_2d: ", rand_2d)
randn_2d = np.random.randn(10, 10)
# print("randn_2d: ", randn_2d)
randint_2d = np.random.randint(0, 100, size=(10, 10))
# print("randint_2d: ", randint_2d)
# np.savetxt("./output/randint_2d.csv", randint_2d, delimiter=",", fmt="%d")
# np.savetxt("./output/randint_2d.txt", randint_2d, fmt="%d")
