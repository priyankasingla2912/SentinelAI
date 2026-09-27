import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from imblearn.over_sampling import SMOTE


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")

X = df.drop("Class", axis=1)
y = df["Class"]


# ==========================================
# 2. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# ==========================================
# 3. Feature Scaling
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================
# 4. Logistic Regression
# ==========================================

logistic_model = LogisticRegression(
    max_iter=2000
)

logistic_model.fit(
    X_train_scaled,
    y_train
)

logistic_predictions = logistic_model.predict(X_test_scaled)

logistic_probabilities = logistic_model.predict_proba(
    X_test_scaled
)[:, 1]


# ==========================================
# 5. SMOTE Logistic Regression
# ==========================================

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train_scaled,
    y_train
)

smote_model = LogisticRegression(
    max_iter=2000
)

smote_model.fit(
    X_train_smote,
    y_train_smote
)

smote_predictions = smote_model.predict(
    X_test_scaled
)

smote_probabilities = smote_model.predict_proba(
    X_test_scaled
)[:, 1]


# ==========================================
# 6. Random Forest
# ==========================================

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

random_forest.fit(
    X_train,
    y_train
)

rf_predictions = random_forest.predict(
    X_test
)

rf_probabilities = random_forest.predict_proba(
    X_test
)[:, 1]


# ==========================================
# 7. Evaluation Function
# ==========================================

def evaluate_model(name, y_true, predictions, probabilities):

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_true,
        probabilities
    )

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    return {
        "Model": name,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC-AUC": roc_auc
    }


# ==========================================
# 8. Compare Models
# ==========================================

results = []

results.append(
    evaluate_model(
        "Logistic Regression",
        y_test,
        logistic_predictions,
        logistic_probabilities
    )
)

results.append(
    evaluate_model(
        "SMOTE Logistic Regression",
        y_test,
        smote_predictions,
        smote_probabilities
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        y_test,
        rf_predictions,
        rf_probabilities
    )
)


# ==========================================
# 9. Final Comparison Table
# ==========================================

results_df = pd.DataFrame(results)

print("\n\nFINAL MODEL COMPARISON")
print("=" * 70)

print(results_df.to_string(index=False))