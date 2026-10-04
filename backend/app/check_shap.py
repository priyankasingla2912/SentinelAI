import pandas as pd
import joblib
import shap


# ==========================================
# 1. Load Dataset
# ==========================================

DATA_PATH = "../datasets/raw/creditcard.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully!")


# ==========================================
# 2. Prepare Features
# ==========================================

X = df.drop("Class", axis=1)

print("Features Shape:")
print(X.shape)


# ==========================================
# 3. Load Trained Model
# ==========================================

MODEL_PATH = "../models/fraud_random_forest.pkl"

model = joblib.load(MODEL_PATH)

print("Random Forest Model Loaded Successfully!")


# ==========================================
# 4. Create SHAP Explainer
# ==========================================

explainer = shap.TreeExplainer(model)

print("SHAP Explainer Created Successfully!")


# ==========================================
# 5. Select One Transaction
# ==========================================

transaction = X.iloc[[77348]]

print("\nTransaction Selected:")
print(transaction)


# ==========================================
# 6. Predict Fraud Probability
# ==========================================

probability = model.predict_proba(transaction)[0][1]

print("\nFraud Probability:")
print(f"{probability:.8f}")


# ==========================================
# 7. Calculate SHAP Values
# ==========================================

shap_values = explainer.shap_values(transaction)

print("\nSHAP Values Calculated Successfully!")


# ==========================================
# 8. Get Fraud SHAP Values
# ==========================================

if isinstance(shap_values, list):

    fraud_shap = shap_values[1][0]

else:

    fraud_shap = shap_values[0, :, 1]


# ==========================================
# 9. Create Explanation Table
# ==========================================

explanation = pd.DataFrame({
    "Feature": transaction.columns,
    "Feature_Value": transaction.iloc[0].values,
    "SHAP_Value": fraud_shap
})


# ==========================================
# 10. Sort by Importance
# ==========================================

explanation["Absolute_SHAP"] = explanation["SHAP_Value"].abs()

explanation = explanation.sort_values(
    "Absolute_SHAP",
    ascending=False
)


# ==========================================
# 11. Display Top 10 Risk Factors
# ==========================================

print("\nTop 10 Features Influencing Prediction:")

print(
    explanation[
        ["Feature", "Feature_Value", "SHAP_Value"]
    ].head(10).to_string(index=False)
)