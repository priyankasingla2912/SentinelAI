import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")

print("Total Dataset Size:", len(df))


# ==========================================
# 2. Separate Features and Target
# ==========================================

X = df.drop("Class", axis=1)
y = df["Class"]


# ==========================================
# 3. First Split
# Training = 80%
# Temporary = 20%
# ==========================================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. Second Split
# Validation = 10%
# Test = 10%
# ==========================================

X_validation, X_test, y_validation, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)


# ==========================================
# 5. Display Dataset Sizes
# ==========================================

print("\nDataset Split")
print("=" * 50)

print("Training Samples   :", len(X_train))
print("Validation Samples :", len(X_validation))
print("Test Samples       :", len(X_test))


# ==========================================
# 6. Display Fraud Distribution
# ==========================================

print("\nFraud Distribution")
print("=" * 50)

print("Training:")
print(y_train.value_counts())

print("\nValidation:")
print(y_validation.value_counts())

print("\nTest:")
print(y_test.value_counts())


# ==========================================
# 7. Train Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nRandom Forest trained successfully!")


# ==========================================
# 8. Validation Probabilities
# ==========================================

validation_probabilities = model.predict_proba(
    X_validation
)[:, 1]


# ==========================================
# 9. Test Different Thresholds
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

    validation_predictions = (
        validation_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_validation,
        validation_predictions,
        zero_division=0
    )

    recall = recall_score(
        y_validation,
        validation_predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_validation,
        validation_predictions,
        zero_division=0
    )

    results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })


# ==========================================
# 10. Validation Results
# ==========================================

results_df = pd.DataFrame(results)

print("\nValidation Threshold Results")
print("=" * 70)

print(results_df.to_string(index=False))


# ==========================================
# 11. Select Best Threshold
# ==========================================

best_row = results_df.loc[
    results_df["F1"].idxmax()
]

best_threshold = best_row["Threshold"]


print("\nSelected Threshold")
print("=" * 50)

print("Threshold:", best_threshold)
print("Validation Precision:", best_row["Precision"])
print("Validation Recall:", best_row["Recall"])
print("Validation F1:", best_row["F1"])


# ==========================================
# 12. FINAL TEST EVALUATION
# ==========================================

test_probabilities = model.predict_proba(
    X_test
)[:, 1]


test_predictions = (
    test_probabilities >= best_threshold
).astype(int)


test_precision = precision_score(
    y_test,
    test_predictions,
    zero_division=0
)

test_recall = recall_score(
    y_test,
    test_predictions,
    zero_division=0
)

test_f1 = f1_score(
    y_test,
    test_predictions,
    zero_division=0
)

test_roc_auc = roc_auc_score(
    y_test,
    test_probabilities
)


# ==========================================
# 13. Final Results
# ==========================================

print("\nFINAL TEST RESULTS")
print("=" * 70)

print("Threshold :", best_threshold)
print(f"Precision : {test_precision:.4f}")
print(f"Recall    : {test_recall:.4f}")
print(f"F1 Score  : {test_f1:.4f}")
print(f"ROC-AUC   : {test_roc_auc:.4f}")