import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# -------------------------
# Load Dataset
# -------------------------

df = pd.read_csv("../datasets/raw/creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

# -------------------------
# Train Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------
# Scaling
# -------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# SMOTE
# -------------------------

print("Before SMOTE")

print(y_train.value_counts())

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("\nAfter SMOTE")

print(pd.Series(y_train_smote).value_counts())

# -------------------------
# Train Model
# -------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train_smote, y_train_smote)

predictions = model.predict(X_test_scaled)

print("\nClassification Report")

print(classification_report(y_test, predictions))