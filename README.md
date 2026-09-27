# SentinelAI

## AI-Powered Fraud & Risk Intelligence Platform

SentinelAI is an AI-powered fraud and risk intelligence platform that analyzes financial transactions, estimates fraud probability, classifies transaction risk, explains model predictions using SHAP, and provides recommended actions for fraud investigation.

The platform combines machine learning, explainable AI, backend APIs, database persistence, and an interactive web application into an end-to-end fraud analysis workflow.

---

## Project Status

**Current Status: Functional End-to-End Prototype**

The current implementation includes:

- Random Forest fraud detection model
- Validated fraud classification threshold
- SHAP explainability
- FastAPI backend
- SQLite database
- Next.js / React frontend
- Transaction Analyzer
- Fraud risk classification
- Recommended actions
- Transaction History
- Risk and prediction filters
- Pagination
- Transaction Details
- Dashboard
- API status monitoring
- Sample transaction testing

---

## Key Features

### 1. AI Fraud Detection

SentinelAI uses a Random Forest classification model to estimate the probability that a transaction is fraudulent.

The model uses:

- Transaction Time
- Transaction Amount
- V1-V28 anonymized transaction features

### 2. Threshold Optimization

The fraud classification threshold was evaluated using validation data.

The selected threshold is:

**0.60**

Classification logic:

- Fraud Probability >= 0.60 → **FRAUD**
- Fraud Probability < 0.60 → **LEGITIMATE**

### 3. Risk Classification

SentinelAI provides four operational risk levels:

| Fraud Probability | Risk Level |
|---|---|
| >= 0.90 | **CRITICAL** |
| >= 0.60 | **HIGH** |
| >= 0.30 | **MEDIUM** |
| < 0.30 | **LOW** |

Each risk level is associated with a recommended operational action.

### 4. Explainable AI

SHAP is used to explain individual model predictions.

The application displays the top features influencing the prediction and indicates whether each feature:

- Increased fraud risk
- Lowered fraud risk

This provides more context than presenting only a fraud probability.

### 5. Transaction Analysis

Users can submit transactions through the web-based Analyzer and receive:

- Fraud probability
- Prediction
- Risk level
- Recommended action
- SHAP risk factors

The Analyzer also provides sample transactions for testing.

### 6. Transaction History

Analyzed transactions are persisted in SQLite and can be viewed through the History page.

History supports:

- Risk filtering
- Prediction filtering
- Clear filters
- Pagination
- Transaction navigation

### 7. Transaction Details

Each analyzed transaction has a dedicated details page containing:

- Transaction amount
- Fraud probability
- Classification threshold
- Prediction
- Risk level
- Recommended action
- SHAP factors

### 8. Dashboard

The Dashboard provides an overview of analyzed transactions, including:

- Total transactions
- Fraud detected
- Fraud rate
- Critical risk count
- Risk distribution
- Recent transactions
- API status
- Refresh functionality
- Risk filtering

---

## System Architecture

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
    |    FastAPI Backend   |
    +----------+-----------+
               |
       +-------+-------+-------+
       |               |       |
       v               v       v
    +--------+      +------+  +----------------+
    |Random  |      | SHAP |  | Risk & Business|
    |Forest  |      | XAI  |  | Rules          |
    | Model  |      +------+  +----------------+
    +--------+          |              |
       |                |              |
       +----------------+--------------+
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
             +----------+----------+
             |          |          |
             v          v          v
         Dashboard   History   Transaction
                                Details

For more information, see the Architecture documentation in:

docs/Architecture.md

---

## End-to-End Workflow

    User
      |
      v
    Next.js Transaction Analyzer
      |
      v
    FastAPI /predict
      |
      v
    Random Forest Model
      |
      v
    Fraud Probability
      |
      v
    Classification Threshold (0.60)
      |
      +-----------------------+
      |                       |
      v                       v
    FRAUD                 LEGITIMATE
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
      +-------------+-------------+
      |             |             |
      v             v             v
    History     Dashboard    Transaction Details

---

## Machine Learning Model

The project evaluated multiple approaches:

- Logistic Regression
- SMOTE Logistic Regression
- Random Forest

Random Forest was selected based on the evaluation results and its precision, recall, and F1-score trade-off.

### Final Test Performance

Using the held-out test set, the selected Random Forest model achieved:

| Metric | Result |
|---|---:|
| Precision | **0.9302** |
| Recall | **0.8163** |
| F1 Score | **0.8696** |
| ROC-AUC | **0.9679** |

The fraud classification threshold of **0.60** was selected using validation data.

---

## Explainable AI

SentinelAI uses SHAP with the Random Forest model.

The purpose of SHAP is to provide feature-level explanations for individual predictions.

For each transaction, SentinelAI identifies the top contributing features and communicates their direction of impact:

- Increased fraud risk
- Lowered fraud risk

This makes the model output more interpretable than presenting only a fraud probability.

---

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- Pydantic

### Machine Learning

- Scikit-learn
- Random Forest
- SHAP

### Data Processing

- Pandas
- NumPy

### Database

- SQLite

### Development

- Git
- VS Code
- Python Virtual Environment
- npm

---

## Project Structure

    SentinelAI/
    |
    +-- backend/
    |   |
    |   +-- app/
    |   |   |
    |   |   +-- config.py
    |   |   +-- constants.py
    |   |   +-- database.py
    |   |   +-- eda.py
    |   |   +-- fraud_engine.py
    |   |   +-- improved_model.py
    |   |   +-- main.py
    |   |   +-- model_comparison.py
    |   |   +-- proper_validation.py
    |   |   +-- risk_scoring.py
    |   |   +-- routes.py
    |   |   +-- save_model.py
    |   |   +-- shap_explanation.py
    |   |   +-- smote_model.py
    |   |   +-- test_database.py
    |   |   +-- test_shap.py
    |   |   +-- threshold_optimization.py
    |   |   +-- train_model.py
    |   |   +-- visualization.py
    |   |
    |   +-- requirements.txt
    |
    +-- datasets/
    |   |
    |   +-- processed/
    |   +-- raw/
    |
    +-- docs/
    |   |
    |   +-- API_Documentation.md
    |   +-- Architecture.md
    |   +-- Database_Design.md
    |   +-- Deployment_Guide.md
    |   +-- PRD.md
    |   +-- User_Guide.md
    |
    +-- frontend/
    |   |
    |   +-- app/
    |   |   |
    |   |   +-- analyze/
    |   |   |   +-- page.tsx
    |   |   |
    |   |   +-- history/
    |   |   |   +-- page.tsx
    |   |   |
    |   |   +-- transaction/
    |   |       +-- [id]/
    |   |           +-- page.tsx
    |   |
    |   +-- globals.css
    |   +-- layout.tsx
    |   +-- page.tsx
    |   +-- package.json
    |   +-- tsconfig.json
    |
    +-- models/
    |   |
    |   +-- threshold.txt
    |
    +-- research/
    |   |
    |   +-- Week1.md
    |   +-- Week2.md
    |
    +-- .gitignore
    +-- README.md

The large training dataset and trained Random Forest model are intentionally excluded from Git using .gitignore.

---

## Running the Project

### Backend

Open a terminal and run:

    cd /Users/priyankabansal/Documents/Projects/SentinelAI/backend
    source venv/bin/activate
    uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

### Frontend

Open another terminal and run:

    cd /Users/priyankabansal/Documents/Projects/SentinelAI/frontend
    npm run dev

Frontend:

http://localhost:3000

---

## Application Pages

| Page | Route | Purpose |
|---|---|---|
| Dashboard | / | Monitor fraud and risk metrics |
| Analyzer | /analyze | Analyze transactions |
| History | /history | Review analyzed transactions |
| Transaction Details | /transaction/{id} | Review individual prediction details |

---

## Database

SQLite is used to store analyzed transactions.

Stored information includes:

- Transaction ID
- Amount
- Fraud probability
- Threshold
- Prediction
- Risk level
- Recommended action
- SHAP factors
- Timestamp

This persistence allows predictions to be reviewed after analysis through the History and Transaction Details pages.

For more information, see:

docs/Database_Design.md

---

## API

The FastAPI backend provides endpoints for:

- Health checks
- Transaction prediction
- Transaction history
- Transaction statistics
- Individual transaction details

For more information, see:

docs/API_Documentation.md

---

## Limitations

The current implementation is a prototype designed for fraud analysis and demonstration.

Important limitations include:

- The model is trained using a historical public credit card fraud dataset.
- V1-V28 are anonymized features and are not directly interpretable as business attributes.
- The system does not connect to a live banking transaction network.
- The current application uses SQLite for local persistence.
- The system does not currently execute real financial transaction blocking.
- Model performance may change when applied to a different real-world transaction population.
- The current application does not represent a production banking fraud infrastructure.

---

## Future Improvements

Potential future improvements include:

- Real-time transaction streaming
- Production-grade database such as PostgreSQL
- Authentication and role-based access
- Fraud analyst case management
- Model monitoring and drift detection
- Automated model retraining
- Real-time alerts
- Integration with banking or payment systems
- Advanced fraud investigation workflows
- RAG-based compliance knowledge retrieval
- Agentic AI fraud analyst assistance
- Cloud deployment
- Production monitoring and observability

---

## Project Goal

The long-term goal of SentinelAI is to evolve from a fraud prediction prototype into an intelligent fraud and risk intelligence platform that combines machine learning, explainable AI, knowledge retrieval, and intelligent workflow assistance.