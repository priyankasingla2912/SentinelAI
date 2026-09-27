import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# 1. Load Dataset
# ==========================================

DATA_PATH = "../datasets/raw/creditcard.csv"

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)


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

print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Random Forest trained successfully!")


# ==========================================
# 5. Create Model Directory
# ==========================================

MODEL_DIR = "../models"

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# 6. Save Model
# ==========================================

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fraud_random_forest.pkl"
)

joblib.dump(model, MODEL_PATH)

print("Model saved successfully!")
print("Model Path:", MODEL_PATH)


# ==========================================
# 7. Save Threshold
# ==========================================

threshold_path = os.path.join(
    MODEL_DIR,
    "threshold.txt"
)

with open(threshold_path, "w") as f:
    f.write("0.60")

print("Threshold saved successfully!")
print("Threshold:", 0.60)