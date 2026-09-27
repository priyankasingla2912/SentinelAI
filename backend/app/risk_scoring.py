import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")


# ==========================================
# 2. Separate Features and Target
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

fraud_probability = model.predict_proba(X_test)[:, 1]


# ==========================================
# 6. Create Risk Levels
# ==========================================

def get_risk_level(probability):

    if probability < 0.30:
        return "LOW"

    elif probability < 0.60:
        return "MEDIUM"

    elif probability < 0.85:
        return "HIGH"

    else:
        return "CRITICAL"


# ==========================================
# 7. Create Results
# ==========================================

results = X_test.copy()

results["Actual_Class"] = y_test.values

results["Fraud_Probability"] = fraud_probability

results["Risk_Level"] = [
    get_risk_level(probability)
    for probability in fraud_probability
]


# ==========================================
# 8. Display Results
# ==========================================

print("\nSample Risk Predictions")

print(
    results[
        [
            "Amount",
            "Actual_Class",
            "Fraud_Probability",
            "Risk_Level"
        ]
    ].head(20)
)


# ==========================================
# 9. Risk Distribution
# ==========================================

print("\nRisk Level Distribution")

print(
    results["Risk_Level"].value_counts()
)