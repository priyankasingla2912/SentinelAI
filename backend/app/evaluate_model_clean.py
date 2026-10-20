
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "raw" / "creditcard.csv"
SAVED_MODEL_PATH = PROJECT_ROOT / "models" / "fraud_random_forest.pkl"

THRESHOLD = 0.60
RANDOM_STATE = 42
TEST_SIZE = 0.20


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    print(f"Dataset rows: {len(df)}")
    print(f"Features: {X.shape[1]}")
    print(f"Legitimate transactions: {(y == 0).sum()}")
    print(f"Fraud transactions: {(y == 1).sum()}")

    # Stratification preserves the fraud/legitimate class proportions.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Fraud cases in test set: {int(y_test.sum())}")

    # Read the existing model's configuration only.
    # Do not fit or save over the existing model.
    saved_model = joblib.load(SAVED_MODEL_PATH)

    if not isinstance(saved_model, RandomForestClassifier):
        raise TypeError("The saved model is not a RandomForestClassifier.")

    if saved_model.n_features_in_ != X.shape[1]:
        raise ValueError(
            f"Saved model expects {saved_model.n_features_in_} features, "
            f"but dataset contains {X.shape[1]}."
        )

    # Create a separate, fresh model with the same hyperparameters.
    evaluation_model = RandomForestClassifier(
        **saved_model.get_params()
    )

    print("\nTraining a separate evaluation model...")
    evaluation_model.fit(X_train, y_train)

    # The test set is not used for fitting.
    probabilities = evaluation_model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= THRESHOLD).astype(int)

    print("\n" + "=" * 60)
    print("CLEAN HOLDOUT EVALUATION")
    print("Separate model; stratified 80/20 split")
    print(f"Decision threshold: {THRESHOLD:.2f}")
    print("=" * 60)

    print(f"Accuracy:          {accuracy_score(y_test, predictions):.4f}")
    print(
        f"Precision:         "
        f"{precision_score(y_test, predictions, zero_division=0):.4f}"
    )
    print(
        f"Recall:            "
        f"{recall_score(y_test, predictions, zero_division=0):.4f}"
    )
    print(f"F1 score:          {f1_score(y_test, predictions, zero_division=0):.4f}")
    print(f"ROC-AUC:           {roc_auc_score(y_test, probabilities):.4f}")
    print(
        f"Average precision: "
        f"{average_precision_score(y_test, probabilities):.4f}"
    )

    print("\nConfusion matrix [[TN, FP], [FN, TP]]:")
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

    print("\nExisting saved model was not modified.")
    print("Existing database and threshold file were not modified.")


if __name__ == "__main__":
    main()
