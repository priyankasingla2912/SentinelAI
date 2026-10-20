
from pathlib import Path

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "raw" / "creditcard.csv"
N_SPLITS = 5
THRESHOLD = 0.60
RANDOM_STATE = 42


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    print(f"Dataset rows: {len(df)}")
    print(f"Fraud cases: {int(y.sum())}")
    print(f"Legitimate cases: {int((y == 0).sum())}")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1,
    )

    cv = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    print(f"\nRunning {N_SPLITS}-fold stratified cross-validation...")
    print("This may take several minutes.")

    # Each row receives a probability from a model that did not train on it.
    probabilities = cross_val_predict(
        model,
        X,
        y,
        cv=cv,
        method="predict_proba",
        n_jobs=1,
    )[:, 1]

    predictions = (probabilities >= THRESHOLD).astype(int)

    print("\nCROSS-VALIDATION RESULTS")
    print("=" * 50)
    print(f"Threshold:         {THRESHOLD:.2f}")
    print(f"Precision:         {precision_score(y, predictions, zero_division=0):.4f}")
    print(f"Recall:            {recall_score(y, predictions, zero_division=0):.4f}")
    print(f"F1 score:          {f1_score(y, predictions, zero_division=0):.4f}")
    print(f"ROC-AUC:           {roc_auc_score(y, probabilities):.4f}")
    print(f"Average precision: {average_precision_score(y, probabilities):.4f}")

    print("\nThis is out-of-fold evaluation of the dataset,")
    print("not an independent external test set.")
    print("No model or database files were saved or modified.")


if __name__ == "__main__":
    main()
