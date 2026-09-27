import pandas as pd
import shap

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# =====================================================
# 1. LOAD DATASET
# =====================================================

df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")


# =====================================================
# 2. SEPARATE FEATURES AND TARGET
# =====================================================

X = df.drop("Class", axis=1)
y = df["Class"]


# =====================================================
# 3. TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =====================================================
# 4. TRAIN RANDOM FOREST
# =====================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Random Forest trained successfully!")


# =====================================================
# 5. CREATE SHAP EXPLAINER
# =====================================================

explainer = shap.TreeExplainer(model)

print("SHAP Explainer created successfully!")


# =====================================================
# 6. SELECT A FRAUD TRANSACTION
# =====================================================

fraud_indices = y_test[y_test == 1].index

transaction_index = fraud_indices[0]

transaction = X_test.loc[[transaction_index]]

actual_class = y_test.loc[transaction_index]


# =====================================================
# 7. CALCULATE FRAUD PROBABILITY
# =====================================================

fraud_probability = model.predict_proba(
    transaction
)[0][1]


# =====================================================
# 8. APPLY THRESHOLD
# =====================================================

threshold = 0.60

if fraud_probability >= threshold:
    prediction = 1
else:
    prediction = 0


# =====================================================
# 9. DETERMINE RISK LEVEL
# =====================================================

if fraud_probability >= 0.90:

    risk_level = "CRITICAL"

elif fraud_probability >= 0.60:

    risk_level = "HIGH"

elif fraud_probability >= 0.30:

    risk_level = "MEDIUM"

else:

    risk_level = "LOW"


# =====================================================
# 10. CALCULATE SHAP VALUES
# =====================================================

shap_values = explainer.shap_values(transaction)


# =====================================================
# 11. HANDLE SHAP OUTPUT
# =====================================================

if isinstance(shap_values, list):

    fraud_shap_values = shap_values[1][0]

else:

    fraud_shap_values = shap_values[0, :, 1]


# =====================================================
# 12. CREATE EXPLANATION TABLE
# =====================================================

feature_contributions = pd.DataFrame({

    "Feature": X.columns,

    "Feature_Value": transaction.iloc[0].values,

    "SHAP_Value": fraud_shap_values

})


# =====================================================
# 13. SORT FEATURES BY IMPORTANCE
# =====================================================

feature_contributions["Absolute_SHAP"] = (
    feature_contributions["SHAP_Value"].abs()
)


feature_contributions = feature_contributions.sort_values(
    by="Absolute_SHAP",
    ascending=False
)


# =====================================================
# 14. GET TOP RISK FACTORS
# =====================================================

risk_factors = feature_contributions[
    feature_contributions["SHAP_Value"] > 0
].head(5)


# =====================================================
# 15. DETERMINE RECOMMENDATION
# =====================================================

if risk_level == "CRITICAL":

    recommendation = (
        "Block transaction and immediately escalate "
        "to fraud analyst."
    )

elif risk_level == "HIGH":

    recommendation = (
        "Send transaction for fraud analyst review."
    )

elif risk_level == "MEDIUM":

    recommendation = (
        "Monitor transaction and perform additional verification."
    )

else:

    recommendation = (
        "Allow transaction and continue monitoring."
    )


# =====================================================
# 16. DISPLAY SENTINELAI RESULT
# =====================================================

print("\n")
print("=" * 60)
print("              SENTINELAI ANALYSIS")
print("=" * 60)

print("\nTransaction Index:")
print(transaction_index)

print("\nActual Class:")
print(actual_class)

print("\nAmount:")
print(transaction["Amount"].iloc[0])

print("\nFraud Probability:")
print(f"{fraud_probability:.8f}")

print("\nThreshold:")
print(threshold)

print("\nPrediction:")
print("FRAUD" if prediction == 1 else "LEGITIMATE")

print("\nRisk Level:")
print(risk_level)


print("\nTop Risk Factors")
print("-" * 60)

print(
    risk_factors[
        ["Feature", "Feature_Value", "SHAP_Value"]
    ].to_string(index=False)
)


print("\nRecommended Action:")
print(recommendation)

print("\n" + "=" * 60)