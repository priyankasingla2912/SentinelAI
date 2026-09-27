import pandas as pd

# Load dataset
df = pd.read_csv("../datasets/raw/creditcard.csv")

print("=" * 60)
print("SentinelAI - Dataset Exploration")
print("=" * 60)

print("\n1. First Five Rows")
print(df.head())

print("\n2. Last Five Rows")
print(df.tail())

print("\n3. Dataset Shape")
print(df.shape)

print("\n4. Column Names")
print(df.columns.tolist())

print("\n5. Dataset Information")
df.info()

print("\n6. Missing Values")
print(df.isnull().sum())

print("\n7. Statistical Summary")
print(df.describe())

print("\n8. Fraud Distribution")
print(df["Class"].value_counts())