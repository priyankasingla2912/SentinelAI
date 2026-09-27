# SentinelAI Architecture

## 1. Overview

SentinelAI is an AI-powered Fraud & Risk Intelligence Platform designed to analyze financial transactions, estimate fraud probability, classify transaction risk, explain model predictions, and provide recommended actions.

The platform combines machine learning, explainable AI, backend APIs, database persistence, and a web-based frontend into one end-to-end application.

---

## 2. High-Level Architecture

```text
                         SENTINELAI
                             |
                             v
                  +----------------------+
                  |   Next.js / React    |
                  |      Frontend        |
                  +----------+-----------+
                             |
                         REST API
                             |
                             v
                  +----------------------+
                  |    FastAPI Backend    |
                  +----------+-----------+
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
       +-------------+ +-------------+ +-------------+
       | Random      | |    SHAP     | |   Risk &   |
       | Forest      | | Explainable | |  Business  |
       | Model       | |     AI      | |   Rules    |
       +------+------+ +------+------+ +------+------+
              |               |               |
              +---------------+---------------+
                              |
                              v
                     Fraud Probability
                              |
                              v
                     Threshold Decision
                         (0.60)
                              |
                              v
                       Risk Classification
                              |
                              v
                     Recommended Action
                              |
                              v
                       SQLite Database
                              |
               +--------------+--------------+
               |              |              |
               v              v              v
          Dashboard        History          Transaction
                                           Details

3. Frontend Architecture
The frontend is built using Next.js, React, TypeScript, and Tailwind CSS.
Main Application Pages
Dashboard
Route:
/
The Dashboard provides:
Total transactions
Fraud detected
Fraud rate
Critical risk count
Risk distribution
Recent transactions
API status
Refresh functionality
Risk filtering
Transaction Analyzer
Route:
/analyze
The Analyzer allows users to:
Enter transaction amount
Enter transaction time
Load a legitimate sample
Load a fraud sample
View advanced V1–V28 model features
Submit a transaction
View fraud probability
View prediction
View risk level
View recommended action
View SHAP risk factors
Transaction History
Route:
/history
The History page provides:
Previously analyzed transactions
Risk filtering
Prediction filtering
Clear filters
Pagination
Navigation to transaction details
Transaction Details
Route:
/transaction/{id}
The Transaction Details page displays:
Transaction amount
Fraud probability
Classification threshold
Prediction
Risk level
Recommended action
SHAP risk factors
4. Backend Architecture
The backend is built using Python and FastAPI.
The backend provides APIs for:
Health checking
Transaction prediction
Transaction history
Transaction statistics
Individual transaction details
Main Prediction Endpoint
POST /predict
The prediction workflow is:
Transaction Input
       |
       v
Feature Preparation
       |
       v
Random Forest Model
       |
       v
Fraud Probability
       |
       v
0.60 Classification Threshold
       |
       v
Prediction
       |
       v
Risk Classification
       |
       v
Recommended Action
       |
       v
SHAP Explanation
       |
       v
SQLite Storage
5. Machine Learning Architecture
SentinelAI uses a Random Forest classifier for fraud detection.
The model development process included comparison of:
Logistic Regression
SMOTE Logistic Regression
Random Forest
The Random Forest model was selected based on the evaluation results and the balance between precision, recall, and F1 score.
Model Input
The model uses:
Time
V1–V28 anonymized transaction features
Amount
Model Output
The model produces a fraud probability.
The probability is then passed through the application decision logic to determine the transaction classification and risk level.
6. Classification Threshold
SentinelAI uses a validated classification threshold of:
0.60
The threshold was selected using a validation dataset rather than the final test dataset.
The classification logic is:
Fraud Probability >= 0.60
        |
        v
      FRAUD

Fraud Probability < 0.60
        |
        v
    LEGITIMATE
This threshold is separate from the operational risk-level boundaries.
7. Risk Classification
SentinelAI assigns an operational risk level based on fraud probability.
Probability >= 0.90  → CRITICAL

Probability >= 0.60  → HIGH

Probability >= 0.30  → MEDIUM

Probability < 0.30   → LOW
The system also generates a recommended action for each risk level.
Recommended Actions
CRITICAL
Block transaction and immediately escalate to fraud analyst.

HIGH
Hold transaction for additional fraud verification.

MEDIUM
Monitor transaction and perform additional verification.

LOW
Allow transaction and continue normal monitoring.
8. Explainable AI
SentinelAI uses SHAP (SHapley Additive exPlanations) to explain individual model predictions.
For each analyzed transaction, SHAP identifies features that contributed to the model output.
The application displays the top risk factors and indicates whether each factor:
Increased fraud risk
Lowered fraud risk
This provides an explanation layer around the machine learning prediction rather than presenting only a probability.
9. Database Architecture
SQLite is used to persist analyzed transactions.
The database stores:
Transaction ID
Transaction amount
Fraud probability
Classification threshold
Prediction
Risk level
Recommended action
SHAP factors
Creation timestamp
This information is used by:
Dashboard
Transaction History
Transaction Details
10. End-to-End Data Flow
The complete application workflow is:
User
 |
 v
Next.js Transaction Analyzer
 |
 v
POST /predict
 |
 v
FastAPI Backend
 |
 v
Random Forest Model
 |
 v
Fraud Probability
 |
 v
Classification Threshold
 |
 +--------------------------+
 |                          |
 v                          v
FRAUD                    LEGITIMATE
 |
 +------------+
              |
              v
       Risk Classification
              |
              v
       Recommended Action
              |
              v
        SHAP Explanation
              |
              v
        SQLite Database
              |
       +------+------+
       |             |
       v             v
   History       Dashboard
       |
       v
Transaction Details
11. Technology Stack
Frontend
Next.js
React
TypeScript
Tailwind CSS
Backend
Python
FastAPI
Pydantic
Machine Learning
Scikit-learn
Random Forest
SHAP
Data Processing
Pandas
NumPy
Database
SQLite
Development Tools
Git
VS Code
Python Virtual Environment
npm