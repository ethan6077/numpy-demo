"""How sklearn uses the sigmoid function: logistic regression.

Logistic regression fits a straight line  z = w*x + b  to the data, then
passes that line through the sigmoid to get a probability between 0 and 1:

    P(y=1 | x) = sigmoid(w*x + b) = 1 / (1 + e^-(w*x + b))

This demo trains a 1-feature model on toy "hours studied -> passed exam" data
so we can plot the fitted sigmoid curve and confirm sklearn is doing exactly
that under the hood.

Run from the project root:
    python src/sigmoid_sklearn_demo.py
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 1. Toy dataset: hours studied (feature) vs. passed the exam (0 = no, 1 = yes).
#    sklearn expects X as a 2D array of shape (n_samples, n_features).
hours = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
passed = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])
X = hours.reshape(-1, 1)

# 2. Fit the model. sklearn finds the best weight (w) and bias (b).
model = LogisticRegression()
model.fit(X, passed)

w = model.coef_[0][0]
b = model.intercept_[0]
print(f"Learned weight (w): {w:.3f}")
print(f"Learned bias   (b): {b:.3f}")

# 3. Prove the point: sklearn's predict_proba == sigmoid(w*x + b).
sample = np.array([[2.75]])
sklearn_prob = model.predict_proba(sample)[0][1]  # probability of class 1
manual_prob = sigmoid(w * 2.75 + b)  # same math, done by hand
print(f"\nFor a student who studied 2.75 hours:")
print(f"  sklearn predict_proba -> {sklearn_prob:.4f}")
print(f"  manual sigmoid(w*x+b) -> {manual_prob:.4f}  (identical)")

# The decision boundary is where the probability crosses 0.5, i.e. w*x + b = 0.
boundary = -b / w
print(f"\nDecision boundary at x = {boundary:.2f} hours (P = 0.5)")

# 4. Plot the data points and the fitted sigmoid curve.
x_line = np.linspace(0, 5.5, 200).reshape(-1, 1)
y_line = model.predict_proba(x_line)[:, 1]  # P(pass) across the range

plt.figure(figsize=(8, 5))
plt.scatter(hours, passed, color="crimson", zorder=3, label="training data")
plt.plot(x_line, y_line, color="steelblue", linewidth=2, label="fitted sigmoid")
plt.axhline(0.5, color="gray", linestyle="--", linewidth=0.8, label="decision (P=0.5)")
plt.axvline(boundary, color="green", linestyle="--", linewidth=0.8)

plt.title("Logistic Regression = Sigmoid over a Fitted Line")
plt.xlabel("hours studied")
plt.ylabel("probability of passing")
plt.legend()
plt.grid(True, alpha=0.3)

# 5. Save the diagram.
output_path = "./output/sigmoid_sklearn_demo.png"
plt.savefig(output_path, dpi=120, bbox_inches="tight")
print(f"\nSaved diagram to {output_path}")

plt.show()
