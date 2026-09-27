import pandas as pd
import shap

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
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))


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
# 5. Select One Transaction
# ==========================================

# ==========================================
# Select an Actual Fraud Transaction
# ==========================================

fraud_indices = y_test[y_test == 1].index

transaction_index = fraud_indices[0]

transaction = X_test.loc[[transaction_index]]

actual_class = y_test.loc[transaction_index]

print("\nActual Class:")
print(actual_class)

print("\nTransaction Selected:")
print(transaction)




# ==========================================
# 6. Fraud Probability
# ==========================================

probability = model.predict_proba(transaction)[0][1]

print("\nFraud Probability:")
print(f"{probability:.8f}")


# ==========================================
# 7. SHAP Explainer
# ==========================================

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(transaction)


# ==========================================
# 8. SHAP Values
# ==========================================

print("\nSHAP Values Calculated Successfully!")


# ==========================================
# 9. Display Feature Contributions
# ==========================================

feature_names = X.columns

if isinstance(shap_values, list):

    fraud_shap_values = shap_values[1][0]

else:

    fraud_shap_values = shap_values[0, :, 1]


feature_contributions = pd.DataFrame({
    "Feature": feature_names,
    "SHAP_Value": fraud_shap_values,
    "Feature_Value": transaction.iloc[0].values
})


# ==========================================
# 10. Sort by Absolute SHAP Value
# ==========================================

feature_contributions["Absolute_SHAP"] = (
    feature_contributions["SHAP_Value"].abs()
)

feature_contributions = feature_contributions.sort_values(
    by="Absolute_SHAP",
    ascending=False
)


# ==========================================
# 11. Display Top 10 Features
# ==========================================

print("\nTop 10 Features Influencing Prediction:")
print(
    feature_contributions[
        [
            "Feature",
            "Feature_Value",
            "SHAP_Value"
        ]
    ].head(10).to_string(index=False)
)