## Day 7 – Exploratory Data Analysis (EDA)

### Key Findings

- Successfully loaded the Credit Card Fraud Detection dataset.
- Verified that the dataset contains 284,807 transactions and 31 columns.
- Confirmed there are no missing values.
- Identified 30 input features and one target variable (Class).
- Learned that the dataset is highly imbalanced, with only 492 fraudulent transactions (0.17%) and 284,315 legitimate transactions (99.83%).
- Understood that accuracy alone is not sufficient for evaluating fraud detection models due to the class imbalance.

### My Understanding

EDA is the first practical step in any machine learning project. It helps understand the dataset before preprocessing or model training. Through EDA, I confirmed that the data is clean, identified the severe class imbalance, and learned why choosing appropriate evaluation metrics is critical for fraud detection.
## Day 8 - Data Visualization

### What I Learned

- Learned how to visualize data using Matplotlib and Seaborn.
- Created a bar chart to compare fraud and legitimate transactions.
- Generated histograms to understand the distribution of transaction amounts and transaction times.
- Created a correlation heatmap to analyze relationships between features.
- Observed that the dataset is highly imbalanced, with fraud transactions representing only a small percentage of the data.
- Learned that PCA-transformed features have low correlation, indicating reduced redundancy.

### My Understanding

Data visualization is an essential step in exploratory data analysis. It helps reveal patterns, identify outliers, understand feature relationships, and evaluate data quality before building machine learning models. The correlation heatmap confirmed that PCA successfully transformed the original features into mostly independent components, making them suitable for model training.

# Week 2 - Day 9: Machine Learning Fundamentals

## Objective

Today I learned the basic concepts of Machine Learning that are required before building a fraud detection model. Understanding these concepts helps explain how the model learns from historical data and predicts fraud for new transactions.

---

# 1. What is Machine Learning?

Machine Learning (ML) is a branch of Artificial Intelligence that enables computers to learn patterns from historical data and make predictions without being explicitly programmed.

Instead of writing fixed rules such as:

IF Amount > $5000 THEN Fraud

Machine Learning studies thousands of historical transactions and automatically learns complex fraud patterns.

---

# 2. Types of Machine Learning

### Supervised Learning

The model learns using labeled data.

Example:

Transaction → Fraud (Yes/No)

Our fraud detection project uses Supervised Learning because every historical transaction already has a Class label.

---

### Unsupervised Learning

The model finds hidden patterns without knowing the correct answer.

Example:

Customer Segmentation

Fraud Pattern Discovery

---

### Reinforcement Learning

The model learns through rewards and penalties.

Example:

Robotics

Game Playing

Autonomous Vehicles

---

# 3. Why Are We Using Supervised Learning?

Our dataset already contains the Class column.

Class = 0 → Legitimate

Class = 1 → Fraud

The model studies historical examples and learns the relationship between the transaction features and the fraud label.

---

# 4. What are Features (X)?

Features are the input variables provided to the machine learning model.

For our project:

Time

V1

V2

...

V28

Amount

These features describe each transaction.

---

# 5. What is the Target Variable (y)?

The target variable is the correct answer that the model learns to predict.

For SentinelAI:

y = Class

0 = Legitimate

1 = Fraud

---

# 6. What are X and y in Python?

Machine Learning libraries separate the dataset into inputs (X) and outputs (y).

Example:

X = All columns except Class

y = Class column

This tells the model:

"Learn how X predicts y."

---

# 7. What is Train-Test Split?

We never train and evaluate the model using the same data.

Instead, we divide the dataset into two parts.

Training Data (80%)

Used to teach the model.

Testing Data (20%)

Used to evaluate the model on unseen transactions.

Example:

284,807 transactions

↓

Training = 227,845

Testing = 56,962

This helps measure how well the model performs on new data.

---

# 8. Why Can't We Train and Test on the Same Data?

Imagine a teacher gives students the answers before an exam.

The students will score 100%.

But they did not actually learn.

The same problem happens in Machine Learning.

Testing on the same data gives misleadingly high accuracy.

Therefore, we always evaluate using unseen data.

---

# 9. What is Overfitting?

Overfitting happens when the model memorizes the training data instead of learning general patterns.

Characteristics:

Very high training accuracy

Poor performance on new data

Example:

The model memorizes every historical transaction but cannot detect fraud in future transactions.

---

# 10. What is Underfitting?

Underfitting happens when the model is too simple.

Characteristics:

Low training accuracy

Low testing accuracy

The model cannot identify meaningful fraud patterns.

---

# 11. What is a Good Machine Learning Model?

A good model:

Learns meaningful fraud patterns

Generalizes to unseen transactions

Balances bias and variance

Produces reliable predictions

Explains its decisions

---

# 12. Why Start with Logistic Regression?

Logistic Regression is one of the most commonly used baseline classification algorithms.

Advantages:

Simple to understand

Fast to train

Easy to interpret

Works well for binary classification

Provides a good baseline before trying more complex models.

Later, SentinelAI will also evaluate:

Decision Tree

Random Forest

XGBoost

LightGBM

CatBoost

Neural Networks

The best-performing model will be selected.

---

# 13. Machine Learning Workflow

Credit Card Transactions

↓

Data Cleaning

↓

EDA

↓

Train-Test Split

↓

Model Training

↓

Prediction

↓

Evaluation

↓

SHAP Explainability

↓

Risk Score

↓

AI Agent Decision Support

↓

Dashboard

---

# 14. My Understanding

Machine Learning learns patterns from historical labeled transactions. Features (X) describe each transaction, while the target variable (y) provides the correct answer during training. To evaluate performance fairly, the dataset is divided into training and testing sets. Overfitting and underfitting are common challenges that affect model performance. Logistic Regression is a simple and effective baseline algorithm for binary fraud detection before experimenting with more advanced models.

---

# Day 9 Questions & Answers

## 1. What is Machine Learning?

Machine Learning is a branch of Artificial Intelligence that enables computers to learn patterns from historical data and make predictions without explicit programming.

---

## 2. Why is our project using Supervised Learning?

Because the dataset contains labeled examples where each transaction is already classified as legitimate or fraudulent.

---

## 3. What are Features?

Features are the input variables used by the model to make predictions.

Examples include Time, Amount, and V1–V28.

---

## 4. What is the Target Variable?

The target variable is the value the model is trying to predict.

In our dataset, the target variable is the Class column.

---

## 5. What are X and y?

X contains the input features.

y contains the target labels.

The model learns the relationship between X and y.

---

## 6. What is Train-Test Split?

Train-Test Split divides the dataset into separate training and testing datasets so the model can be evaluated on unseen data.

---

## 7. Why shouldn't we train and test on the same dataset?

Because the model would simply memorize the data, producing unrealistically high accuracy without proving it can generalize to new transactions.

---

## 8. What is Overfitting?

Overfitting occurs when a model memorizes the training data instead of learning general patterns, leading to poor performance on new data.

---

## 9. What is Underfitting?

Underfitting occurs when the model is too simple to capture meaningful patterns, resulting in poor performance on both training and testing data.

---

## 10. Why do we start with Logistic Regression?

Logistic Regression is simple, fast, interpretable, and provides an excellent baseline for binary classification problems like fraud detection.

# Day 10 - First Machine Learning Model

## What I Learned

Today I built my first supervised machine learning model using Logistic Regression.

I separated the dataset into features (X) and target labels (y), divided the data into training and testing sets using an 80/20 split, trained the model using historical transactions, and generated predictions on unseen transactions.

I also learned that model accuracy alone is not enough for fraud detection because the dataset is highly imbalanced.

## New Concepts

- Scikit-Learn
- X and y
- train_test_split()
- Logistic Regression
- model.fit()
- model.predict()
- accuracy_score()

## My Understanding

Machine learning models learn patterns from historical labeled transactions during training. Once trained, the model can predict whether new transactions are fraudulent or legitimate. The first model serves as a baseline before improving performance using advanced algorithms and evaluation metrics.

# Day 10 - First Machine Learning Model Results

## Model Used

Logistic Regression

## Results

- Accuracy: 99.90%
- Precision: 84%
- Recall: 53%
- F1 Score: 65%
- ROC-AUC: 95.76%

## Confusion Matrix

- True Negatives: 56,854
- False Positives: 10
- False Negatives: 46
- True Positives: 52

## Key Observations

- The model achieved very high overall accuracy.
- It correctly classified almost all legitimate transactions.
- It missed 46 fraudulent transactions.
- Recall is relatively low, indicating that many fraud cases were not detected.
- The ROC-AUC score shows the model has strong overall discrimination ability.

## My Understanding

Although the model achieved high accuracy, fraud detection requires more than accuracy because the dataset is highly imbalanced. Metrics such as Precision, Recall, F1 Score, and ROC-AUC provide a more meaningful evaluation of the model's performance.

# Day 12 - Feature Scaling and Class Imbalance

## What is Feature Scaling?

Feature Scaling is the process of transforming numerical features so they have similar ranges. This helps many machine learning algorithms learn more efficiently.

## What is StandardScaler?

StandardScaler standardizes each feature by removing the mean and scaling to unit variance. After scaling, most values are centered around zero.

## What is Class Imbalance?

Class imbalance occurs when one class has significantly more examples than another. In our dataset, legitimate transactions greatly outnumber fraudulent ones, making fraud detection more challenging.

## What is SMOTE?

SMOTE (Synthetic Minority Over-sampling Technique) creates synthetic examples of the minority class to help machine learning models learn fraud patterns more effectively.

## My Understanding

Feature scaling improves the performance of algorithms such as Logistic Regression, while SMOTE helps address class imbalance by providing additional synthetic fraud examples during training.

# Day 13 - SMOTE Experiment

## SMOTE Results

Before SMOTE:

- Legitimate transactions: 227,451
- Fraud transactions: 394

After SMOTE:

- Legitimate transactions: 227,451
- Synthetic fraud transactions: 227,451

## Model Performance

| Metric | Baseline Logistic Regression | SMOTE Logistic Regression |
|---|---:|---:|
| Accuracy | 99.90% | 97% |
| Fraud Precision | 84% | 6% |
| Fraud Recall | 53% | 92% |
| Fraud F1 | 65% | 11% |

## Key Finding

SMOTE significantly improved fraud Recall from 53% to 92%, meaning the model detected substantially more fraudulent transactions. However, Precision decreased dramatically to 6%, meaning the model generated many false-positive fraud alerts.

## Business Interpretation

The SMOTE model is better at catching fraud but creates too many false alarms. Therefore, SentinelAI should not select a model based only on Recall or Accuracy. The platform needs to balance fraud detection, false positives, customer experience, and investigation workload.

## My Understanding

Fraud detection is a trade-off between catching fraudulent transactions and avoiding unnecessary alerts for legitimate customers. This experiment demonstrated why model evaluation must consider both technical metrics and business impact.

# Day 14 - Model Comparison Results

## Results

| Model | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 82.67% | 63.27% | 71.68% | 96.05% |
| SMOTE Logistic Regression | 5.78% | 91.84% | 10.88% | 97.08% |
| Random Forest | 91.67% | 78.57% | 84.62% | 95.73% |

## Key Findings

Logistic Regression provided a reasonable baseline.

SMOTE Logistic Regression achieved the highest fraud Recall at 91.84%, but its Precision dropped significantly to 5.78%. This means the model catches more fraud but generates a very large number of false-positive alerts.

Random Forest provided the best overall balance among the tested models, achieving 91.67% Precision, 78.57% Recall, and an F1 Score of 84.62%.

## Model Selection

Based on the current evaluation criteria, Random Forest is the strongest candidate for SentinelAI because it provides the best balance between Precision, Recall, and F1 Score.

However, model selection is not final. Different business costs for false positives and false negatives could lead to different model or threshold choices.

## My Understanding

A machine learning model should not be selected based on one metric. Fraud detection requires balancing the ability to detect fraud with the ability to avoid unnecessary alerts. Model selection should consider both technical performance and business requirements.
# Day 15 - Fraud Probability and Risk Scoring

## What I Learned

Today I learned the difference between model predictions and prediction probabilities. The `predict()` method produces a final classification, while `predict_proba()` provides the probability associated with each class.

For SentinelAI, I use the probability of Class 1 to estimate the likelihood that a transaction is fraudulent.

## Classification Threshold

A classification threshold determines when a probability should be converted into a fraud prediction. A common default threshold is 0.50, but the optimal threshold depends on the business requirements.

Lowering the threshold can increase Recall but may also increase false positives. Increasing the threshold can improve Precision but may cause the model to miss more fraudulent transactions.

## SentinelAI Risk Levels

The project uses initial risk categories:

- 0%–30% → LOW
- 30%–60% → MEDIUM
- 60%–85% → HIGH
- 85%–100% → CRITICAL

These thresholds are initial project assumptions and will be optimized later using validation data and business requirements.

## My Understanding

A fraud detection system should not only produce a binary fraud/legitimate prediction. Providing a fraud probability allows SentinelAI to assign a risk level and prioritize transactions for fraud analysts. This creates a foundation for explainability, investigation workflows, and AI-assisted decision support.

## Day 16 - Threshold Optimization

## Objective

Today I tested different classification thresholds for the Random Forest fraud detection model to understand how changing the threshold affects Precision, Recall, and F1 Score.

## Results

| Threshold | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.10 | 57.14% | 89.80% | 69.84% |
| 0.20 | 71.67% | 87.76% | 78.90% |
| 0.30 | 83.00% | 84.69% | 83.84% |
| 0.40 | 88.04% | 82.65% | 85.26% |
| 0.50 | 90.59% | 78.57% | 84.15% |
| 0.60 | 95.00% | 77.55% | 85.39% |
| 0.70 | 97.37% | 75.51% | 85.06% |
| 0.80 | 97.10% | 68.37% | 80.24% |
| 0.90 | 96.55% | 57.14% | 71.79% |

## Best F1 Threshold

The highest F1 Score occurred at a threshold of 0.60.

- Precision: 95.00%
- Recall: 77.55%
- F1 Score: 85.39%

## Key Finding

Lower thresholds increase Recall but can create more false-positive alerts. Higher thresholds generally increase Precision but can cause the model to miss more fraud cases.

A threshold of 0.60 provided the best F1 Score among the tested thresholds.

## Business Interpretation

For the current SentinelAI prototype, a 0.60 threshold is a strong candidate because it provides a good balance between detecting fraud and reducing false-positive alerts. However, this threshold should not be considered a final production banking threshold. A production threshold would need to be validated using appropriate validation data and business costs.

## My Understanding

The probability threshold is an important part of a fraud detection system. The ML model produces a probability, while the threshold determines how that probability is converted into a decision. Therefore, model performance depends not only on the algorithm but also on the decision threshold.

# Day 16.5 - Proper Validation and Test Set Protection

## Problem Identified

In the initial threshold optimization experiment, I selected the classification threshold using the test set. This is not ideal because the test set should remain untouched during model selection.

## Improved Approach

I changed the dataset strategy to:

- 80% Training
- 10% Validation
- 10% Final Test

The Random Forest model is trained using the training set.

The validation set is used to test different classification thresholds and select the threshold with the best F1 Score.

The final test set is kept untouched until the final evaluation.

## Dataset Distribution

Training:
- Legitimate: 227,451
- Fraud: 394

Validation:
- Legitimate: 28,432
- Fraud: 49

Test:
- Legitimate: 28,432
- Fraud: 49

## Selected Threshold

The validation experiment selected:

Threshold = 0.60

Validation performance:

- Precision: 97.30%
- Recall: 73.47%
- F1 Score: 83.72%

## Final Test Results

Using the selected 0.60 threshold on the untouched test set:

- Precision: 93.02%
- Recall: 81.63%
- F1 Score: 86.96%
- ROC-AUC: 96.79%

## Key Learning

The validation set should be used for model-selection decisions such as threshold optimization. The final test set should be kept separate and used only for final performance evaluation.

## My Understanding

Separating training, validation, and test data produces a more reliable estimate of how the model will perform on unseen transactions. This reduces the risk of overfitting our modeling decisions to the test set.

# Day 17 - SHAP Explainability

## SHAP Experiment

I tested SHAP on both a legitimate transaction and an actual fraudulent transaction.

### Legitimate Transaction

- Actual Class: 0
- Amount: $23.00
- Fraud Probability: approximately 0
- Major SHAP contributions were negative.

This means the strongest features pushed the model away from the fraud class.

### Fraudulent Transaction

- Actual Class: 1
- Time: 57007
- Amount: $0.01
- Fraud Probability: 97%

The model correctly identified this transaction as high risk because the probability of fraud was above the 0.60 classification threshold.

### Top Fraud-Contributing Features

- V14: +0.135569
- V17: +0.087875
- V12: +0.082236
- V10: +0.081993
- V4: +0.039854

These positive SHAP values indicate that these features pushed the model toward the fraud prediction.

### Risk-Reducing Features

- V20: -0.010993
- V19: -0.010497

These features pushed the prediction slightly away from fraud.

## Key Learning

SHAP does not predict fraud by itself. The Random Forest makes the prediction, while SHAP explains which features contributed to that prediction.

## SentinelAI Value

Combining machine learning with SHAP allows SentinelAI to provide both a fraud risk prediction and an explanation that can help a fraud analyst understand the model's decision.

## Dataset Limitation

V1-V28 are anonymized PCA-derived features. Therefore, they cannot be directly interpreted as business attributes such as merchant, location, device, or country.

# Day 18 - SentinelAI Risk and Explanation Engine

I combined the Random Forest model, fraud probability, classification threshold, risk levels, SHAP explanations, and business recommendations into a single SentinelAI fraud analysis engine.

For an actual fraudulent transaction, the model produced a fraud probability of 97%. Since this was above the 0.60 threshold, SentinelAI classified the transaction as FRAUD and assigned it a CRITICAL risk level.

The strongest SHAP risk factors were V14, V17, V12, V10, and V4. These positive SHAP values indicate that these features pushed the model toward the fraud prediction.

The system then generated a business recommendation to block the transaction and immediately escalate it to a fraud analyst.

This was an important step because SentinelAI is no longer only making an ML prediction. It now combines prediction, explainability, risk classification, and an actionable recommendation into one workflow.

The ML model answers "How risky is the transaction?", SHAP answers "Why is it risky?", and the business rules answer "What should we do?"
