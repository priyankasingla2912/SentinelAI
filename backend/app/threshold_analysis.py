
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "raw" / "creditcard.csv"
SAVED_MODEL_PATH = PROJECT_ROOT / "models" / "fraud_random_forest.pkl"

THRESHOLDS = [0.30, 0.40, 0.50, 0.60, 0.70]
RANDOM_STATE = 42
TEST_SIZE = 0.20


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Fraud cases in test set: {int(y_test.sum())}")

    # Read the saved model's configuration without modifying the file.
    saved_model = joblib.load(SAVED_MODEL_PATH)

    if not isinstance(saved_model, RandomForestClassifier):
        raise TypeError("Expected a saved RandomForestClassifier.")

    # Train a separate evaluation model.
    model = RandomForestClassifier(**saved_model.get_params())

    print("\nTraining temporary evaluation model...")
    model.fit(X_train, y_train)

    # Calculate test-set probabilities only once.
    probabilities = model.predict_proba(X_test)[:, 1]

    # Evaluate how the decision threshold changes the results.
    results = []

    for threshold in THRESHOLDS:
        predictions = (probabilities >= threshold).astype(int)

        tn = int(((y_test == 0) & (predictions == 0)).sum())
        fp = int(((y_test == 0) & (predictions == 1)).sum())
        fn = int(((y_test == 1) & (predictions == 0)).sum())
        tp = int(((y_test == 1) & (predictions == 1)).sum())

        results.append(
            {
                "Threshold": threshold,
                "Accuracy": accuracy_score(y_test, predictions),
                "Precision": precision_score(
                    y_test, predictions, zero_division=0
                ),
                "Recall": recall_score(
                    y_test, predictions, zero_division=0
                ),
                "F1": f1_score(y_test, predictions, zero_division=0),
                "True Positives": tp,
                "False Negatives": fn,
                "False Positives": fp,
                "True Negatives": tn,
            }
        )

    results_df = pd.DataFrame(results)

    print("\nTHRESHOLD COMPARISON")
    print("=" * 110)
    print(results_df.round(4).to_string(index=False))

    print("\nThreshold-independent ranking metrics:")
    print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.4f}")
    print(
        "Average precision: "
        f"{average_precision_score(y_test, probabilities):.4f}"
    )

    print("\nExisting production model was not modified.")
    print("Database and threshold file were not modified.")
    print("No evaluation model was saved.")


if __name__ == "__main__":
    main()
