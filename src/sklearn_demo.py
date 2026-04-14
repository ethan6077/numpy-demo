import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

# 1. Load a built-in dataset
iris = load_iris()
X, y = iris.data, iris.target
print(f"Dataset shape: {X.shape}")
print(f"Classes: {iris.target_names}")

# 2. Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTrain size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

# 3. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Train a logistic regression model
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train_scaled, y_train)

# 5. Predict and evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2%}")
print(
    f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=iris.target_names)}"
)

# 6. Try a single prediction
sample = X_test_scaled[0].reshape(1, -1)
prediction = model.predict(sample)
print(
    f"Sample prediction: {iris.target_names[prediction[0]]} (actual: {iris.target_names[y_test[0]]})"
)
