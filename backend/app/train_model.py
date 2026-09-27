import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

# -------------------------------
# Load Dataset
# -------------------------------

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")

# -------------------------------
# Features (X)
# -------------------------------

X = df.drop("Class", axis=1)

# -------------------------------
# Target (y)
# -------------------------------

y = df["Class"]

print("\nFeatures Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)

# -------------------------------
# Train Test Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# -------------------------------
# Create Model
# -------------------------------

model = LogisticRegression(max_iter=1000)

# -------------------------------
# Train Model
# -------------------------------

model.fit(X_train, y_train)

print("\nModel Trained Successfully!")

# -------------------------------
# Prediction
# -------------------------------

predictions = model.predict(X_test)

# -------------------------------
# Accuracy
# -------------------------------

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

probabilities = model.predict_proba(X_test)[:, 1]

print("\nROC-AUC:")
print(roc_auc_score(y_test, probabilities))