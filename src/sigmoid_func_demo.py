"""Educational demo of the sigmoid (logistic) function.

The sigmoid squashes any real number into the range (0, 1), which makes it
handy for turning a raw score into something we can read as a probability.

    sigmoid(x) = 1 / (1 + e^-x)

Run from the project root:
    python src/sigmoid_func_demo.py
"""

import numpy as np
import matplotlib.pyplot as plt


# 1. Define the sigmoid function.
#    np.exp works element-wise, so this handles both single numbers and arrays.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# 2. Look at a few individual values to build intuition.
#    - Large negative input  -> output near 0
#    - Input of 0            -> output of exactly 0.5 (the midpoint)
#    - Large positive input  -> output near 1
print("A few sample values:")
for x in [-10, -2, -1, 0, 1, 2, 10]:
    print(f"  sigmoid({x:>3}) = {sigmoid(x):.4f}")

# 3. Build a smooth range of inputs to plot the whole curve.
x = np.linspace(-10, 10, 200)  # 200 evenly spaced points from -10 to 10
y = sigmoid(x)

# 4. Plot the curve and highlight the key landmarks.
plt.figure(figsize=(8, 5))
plt.plot(x, y, color="steelblue", linewidth=2, label="sigmoid(x)")

# The two horizontal limits the curve approaches but never reaches.
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axhline(1, color="gray", linestyle="--", linewidth=0.8)

# The midpoint: sigmoid(0) = 0.5.
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
plt.plot(0, 0.5, "o", color="crimson", label="midpoint (0, 0.5)")

plt.title("The Sigmoid Function:  1 / (1 + e^-x)")
plt.xlabel("input (x)")
plt.ylabel("output (probability between 0 and 1)")
plt.legend()
plt.grid(True, alpha=0.3)

# 5. Save the diagram so it can be viewed after the script finishes.
output_path = "./output/sigmoid_func_demo.png"
plt.savefig(output_path, dpi=120, bbox_inches="tight")
print(f"\nSaved diagram to {output_path}")

# Also try to open an interactive window (harmless if no display is available).
plt.show()
