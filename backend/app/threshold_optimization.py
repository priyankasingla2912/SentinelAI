import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")


# ==========================================
# 2. Features and Target
# ==========================================

X = df.drop("Class", axis=1)
y = df["Class"]


# ==========================================
# 3. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. Train Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Random Forest trained successfully!")


# ==========================================
# 5. Get Fraud Probabilities
# ==========================================

probabilities = model.predict_proba(X_test)[:, 1]


# ==========================================
# 6. Test Different Thresholds
# ==========================================

thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]


results = []


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })


# ==========================================
# 7. Display Results
# ==========================================

results_df = pd.DataFrame(results)

print("\nThreshold Comparison")
print("=" * 60)

print(results_df.to_string(index=False))


# ==========================================
# 8. Best F1 Threshold
# ==========================================

best_row = results_df.loc[
    results_df["F1"].idxmax()
]

print("\nBest F1 Threshold")
print("=" * 60)

print(best_row)