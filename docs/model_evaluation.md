# SentinelAI — Fraud Detection Model Evaluation

## 1. Overview

SentinelAI is an AI-powered fraud and risk intelligence platform designed to identify potentially fraudulent transactions, provide model explanations, and support investigation workflows.

This report documents baseline model comparisons and decision-threshold experiments using the Credit Card Fraud Detection dataset.

The experiments focus on precision, recall, F1 score, ROC-AUC, average precision, and confusion-matrix counts. Accuracy is included but is not used as the sole measure of performance because fraud cases are rare.

## 2. Dataset

- **Dataset file:** `datasets/raw/creditcard.csv`
- **Total transactions:** 284,807
- **Legitimate transactions:** 284,315
- **Fraudulent transactions:** 492
- **Features:** 30
- **Target column:** `Class`
- **Train/test split:** 80% training and 20% testing
- **Random state:** 42
- **Stratification:** Enabled for the evaluation and model-comparison experiments

Fraud represents approximately 0.173% of the dataset. This severe class imbalance makes precision, recall, F1 score, and the number of false positives and false negatives particularly important.

## 3. Model Configuration

The existing SentinelAI Random Forest configuration is:

- Algorithm: Random Forest Classifier
- Number of trees: 200
- Class weighting: `balanced`
- Random state: 42
- Number of input features: 30
- Current application decision threshold: 0.60

A separate model was trained for the clean holdout evaluation using the same configuration. The existing saved model was not overwritten.

## 4. Model Comparison

Three models were evaluated using the same stratified train/test split. The comparison script uses each model's default prediction threshold.

| Model | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8267 | 0.6327 | 0.7168 | 0.9605 |
| SMOTE Logistic Regression | 0.0578 | 0.9184 | 0.1088 | 0.9708 |
| Random Forest (100 trees) | 0.9167 | 0.7857 | 0.8462 | 0.9573 |

### Interpretation

Random Forest achieved the highest precision and F1 score among these three comparison runs. It provided a more balanced trade-off between identifying fraud and limiting false alarms.

SMOTE Logistic Regression achieved the highest recall and ROC-AUC in this comparison, but its precision was low. This indicates that its default classification threshold generated many false-positive predictions.

These results do not establish that Random Forest is universally superior. The appropriate model depends on the operational cost of missed fraud, false alarms, and manual investigations.

## 5. Clean Holdout Evaluation

A separate 200-tree Random Forest was trained on 80% of the data and evaluated on the held-out 20%.

| Metric | Result |
|---|---:|
| Accuracy | 0.9995 |
| Precision | 0.9494 |
| Recall | 0.7653 |
| F1 Score | 0.8475 |
| ROC-AUC | 0.9613 |
| Average Precision | 0.8670 |

### Saved Model Consistency Verification

A read-only verification compared predictions from the existing serialized Random Forest model with predictions from a newly trained Random Forest using the reconstructed stratified 80/20 split (`random_state=42`). Both models used 200 estimators, `class_weight="balanced"`, and `random_state=42`.

The saved model contained 30 input features, matching the 30 dataset features, and used class labels `[0, 1]`. Predictions on the 227,845 reconstructed training rows achieved **100% agreement** between the saved model and the reconstructed model.

This result supports consistency between the saved model and the reconstructed training configuration. However, prediction agreement alone does not prove that the artifact was trained on the exact same data or during the documented training run. The verification was read-only and did not modify the saved model, decision threshold, or database.
### Confusion Matrix

At a decision threshold of 0.60:

| Actual / Predicted | Legitimate | Fraud |
|---|---:|---:|
| Legitimate | 56,860 | 4 |
| Fraud | 23 | 75 |

The model correctly identified 75 of 98 fraudulent transactions in the test set. It missed 23 fraudulent transactions and incorrectly flagged four legitimate transactions.

Precision was high, but the false negatives show that additional investigation is needed before selecting a threshold for operational use.

**Reproducibility note:** The saved model's training script and the clean evaluation script use the same dataset, stratified split, random state, and Random Forest configuration. Their identical metrics are consistent with recreating the same experiment. The saved model's original training history has not been independently verified through a stored experiment record.

## 6. Decision-Threshold Analysis

The same held-out test set was evaluated at five probability thresholds.

| Threshold | Precision | Recall | F1 Score | True Positives | False Negatives | False Positives |
|---:|---:|---:|---:|---:|---:|---:|
| 0.30 | 0.8400 | 0.8571 | 0.8485 | 84 | 14 | 16 |
| 0.40 | 0.8723 | 0.8367 | 0.8542 | 82 | 16 | 12 |
| 0.50 | 0.9277 | 0.7857 | 0.8508 | 77 | 21 | 6 |
| 0.60 | 0.9494 | 0.7653 | 0.8475 | 75 | 23 | 4 |
| 0.70 | 0.9610 | 0.7551 | 0.8457 | 74 | 24 | 3 |

### Interpretation

Lowering the threshold increases the number of transactions classified as fraud. This can improve fraud recall, but it also increases false alarms.

Raising the threshold reduces false alarms but allows more fraudulent transactions to be classified as legitimate.

Threshold 0.40 produced the highest F1 score among the five tested thresholds. Threshold 0.30 detected the most fraud cases, while threshold 0.70 generated the fewest false positives.

These are candidate operating points, not a final production decision. Threshold selection should consider fraud-loss costs, investigation capacity, and the business impact of false positives and false negatives.

### Additional Validation and Final Test Evaluation

A separate threshold-validation experiment was conducted using a temporary 200-tree Random Forest classifier with `class_weight="balanced"` and `random_state=42`. The dataset was divided into training, validation, and reserved test subsets using stratified splitting.

The temporary model was trained on 170,883 transactions and evaluated on 56,962 validation transactions. The reserved test set contained 56,962 transactions, including 98 fraudulent transactions.

#### Validation Results

| Threshold | Precision | Recall | F1 Score | False Positives | False Negatives |
|---:|---:|---:|---:|---:|---:|
| 0.30 | 0.8556 | 0.7778 | 0.8148 | 13 | 22 |
| 0.40 | 0.8929 | 0.7576 | 0.8197 | 9 | 24 |
| 0.50 | 0.9012 | 0.7374 | 0.8111 | 8 | 26 |
| 0.60 | 0.9333 | 0.7071 | 0.8046 | 5 | 29 |

Validation ROC-AUC was 0.9556, and average precision was 0.8032. Threshold 0.40 achieved the highest F1 score among the four thresholds tested on the validation subset.

#### Reserved Test Results

After threshold candidates were selected using the validation subset, the temporary model was evaluated on the reserved test subset.

| Metric | Threshold 0.40 | Threshold 0.60 |
|---|---:|---:|
| Precision | 0.8913 | 0.9481 |
| Recall | 0.8367 | 0.7449 |
| F1 Score | 0.8632 | 0.8343 |
| False Positives | 10 | 4 |
| False Negatives | 16 | 25 |

The test-set ROC-AUC was 0.9662, and average precision was 0.8603.

At threshold 0.40, the temporary model detected 82 of 98 fraudulent transactions, compared with 73 at threshold 0.60. This reduced false negatives from 25 to 16 while increasing false positives from 4 to 10.

#### Interpretation and Limitations

Threshold 0.40 achieved a higher F1 score and recall than threshold 0.60 in this experiment, while threshold 0.60 maintained higher precision and fewer false positives. These results illustrate the trade-off between detecting fraud and generating additional alerts.

The evaluation used a temporary model trained on the training subset. It does not directly establish the performance of the existing saved application model. Because the reserved test results have now been examined, this test subset should not be treated as untouched for future model or threshold selection.

The production model and its current decision threshold of 0.60 were not modified. Further validation is needed before adopting a new production threshold.

## 7. Explainability and Investigation

SentinelAI also includes model-explanation and investigation components intended to help analysts review potentially fraudulent transactions.

The platform uses SHAP-based risk factors to explain model predictions and provides an investigation workflow with retrieved sample policies.

These components provide decision support. SHAP explanations do not prove that a transaction is fraudulent, and sample policies must be validated before being treated as official banking policies.

## 8. Limitations

1. The dataset is highly imbalanced, with only 492 fraudulent transactions.
2. Threshold results come from a single reproducible holdout split.
3. The saved model's original training history has not been independently recorded and verified.
4. The model-comparison experiment uses a 100-tree Random Forest, whereas the application's saved model configuration uses 200 trees.
5. The threshold analysis uses a separately trained evaluation model and does not directly validate the exact saved production model.
6. The experiments use a public dataset and do not establish performance on live banking transactions.
7. No claim of production readiness, real-world fraud-loss reduction, or regulatory compliance is made by these experiments.

## 9. Next Steps

- Validate performance across multiple stratified folds or repeated evaluation splits.
- Compare thresholds using an explicit cost model for false positives and false negatives.
- Record dataset version, model parameters, split strategy, and evaluation metrics for reproducibility.
- Test API and case-management behavior with automated tests.
- Monitor prediction quality and investigate model drift when suitable real-world data becomes available.

## 10. 5-Fold Stratified Cross-Validation

A 5-fold stratified cross-validation experiment was conducted using a Random Forest classifier with 200 estimators, `class_weight="balanced"`, and `random_state=42`. Out-of-fold probabilities were generated for the full dataset, and predictions were classified using the existing threshold of 0.60.

| Metric | Cross-validation result |
|---|---:|
| Precision | 0.9481 |
| Recall | 0.7805 |
| F1 score | 0.8562 |
| ROC-AUC | 0.9648 |
| Average precision | 0.8537 |

The cross-validation results are broadly consistent with the earlier holdout evaluation. They provide additional evidence of model performance across stratified training folds. However, this evaluation uses the same overall dataset and is not an independent external test. The threshold was held fixed at 0.60; these results do not establish that it is optimal.

No model artifacts or database files were modified by the cross-validation script.

## 11. Conclusion
The initial experiments indicate that Random Forest provides a promising baseline for SentinelAI's fraud-detection workflow. The threshold analysis demonstrates a measurable trade-off between fraud detection and false alarms.

Further validation, reproducible experiment tracking, and business-cost analysis are necessary before finalizing a production threshold or claiming real-world effectiveness.
