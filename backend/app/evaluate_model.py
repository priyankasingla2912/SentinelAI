
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "raw" / "creditcard.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "fraud_random_forest.pkl"

THRESHOLD = 0.60
RANDOM_STATE = 42


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    print(f"Dataset shape: {df.shape}")
    print(f"Fraud cases: {int(y.sum())}")
    print(f"Legitimate cases: {int((y == 0).sum())}")

    # Provisional split: independence from model training is not verified.
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print("\nLoading existing Random Forest...")
    model = joblib.load(MODEL_PATH)

    expected_features = getattr(model, "n_features_in_", None)
    if expected_features != X_test.shape[1]:
        raise ValueError(
            f"Model expects {expected_features} features, "
            f"but dataset contains {X_test.shape[1]}."
        )

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= THRESHOLD).astype(int)

    print("\n" + "=" * 55)
    print("PROVISIONAL RANDOM FOREST EVALUATION")
    print("Training-data overlap has not been ruled out.")
    print(f"Decision threshold: {THRESHOLD:.2f}")
    print(f"Evaluation samples: {len(y_test)}")
    print("=" * 55)

    print(f"Accuracy:  {accuracy_score(y_test, predictions):.4f}")
    print(
        f"Precision: {precision_score(y_test, predictions, zero_division=0):.4f}"
    )
    print(f"Recall:    {recall_score(y_test, predictions, zero_division=0):.4f}")
    print(f"F1 score:  {f1_score(y_test, predictions, zero_division=0):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, probabilities):.4f}")
    print(
        "Average precision: "
        f"{average_precision_score(y_test, probabilities):.4f}"
    )

    print("\nConfusion matrix [ [TN, FP], [FN, TP] ]:")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Legitimate", "Fraud"],
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()
