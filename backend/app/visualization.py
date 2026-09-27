import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("../datasets/raw/creditcard.csv")

print("Dataset Loaded Successfully!")

# -------------------------------
# 1. Fraud Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.countplot(x="Class", data=df)
plt.title("Fraud vs Legitimate Transactions")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

# -------------------------------
# 2. Transaction Amount
# -------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["Amount"], bins=50)
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.show()

# -------------------------------
# 3. Transaction Time
# -------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["Time"], bins=50)
plt.title("Transaction Time Distribution")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.show()

# -------------------------------
# 4. Correlation Matrix
# -------------------------------
plt.figure(figsize=(12,10))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()