# Week 1 Research Notes

# Day 1
## 1. What is Financial Fraud?

Financial fraud is any illegal or unauthorized activity where a person or organization tries to obtain money, financial assets, or sensitive information through deception. Examples include stolen credit cards, identity theft, account takeover, and money laundering. Financial fraud causes significant financial losses for banks and customers.

---

## 2. Types of Financial Fraud

### Credit Card Fraud
Someone steals or illegally uses another person's credit card information to make purchases without permission.

### Identity Theft
Someone uses another person's personal information to open bank accounts, apply for loans, or make purchases.

### Account Takeover
A fraudster gains unauthorized access to a customer's bank account and performs transactions.

### Money Laundering
The process of making illegally earned money appear legal by passing it through legitimate businesses or financial systems.

### Insider Fraud
Fraud committed by employees who misuse their access to steal money or confidential information.

---

## 3. How Banks Process Transactions

Customer
↓
Merchant
↓
Payment Network (Visa / Mastercard)
↓
Issuing Bank
↓
Fraud Detection System
↓
Approve / Decline

The fraud detection system checks whether the transaction appears suspicious before approving it.

---

## 4. What is a Fraud Analyst?

A fraud analyst investigates suspicious transactions, reviews fraud alerts, analyzes customer behavior, and determines whether a transaction is genuine or fraudulent. Their goal is to reduce financial losses while minimizing inconvenience for legitimate customers.

---

## 5. Problems Faced by Fraud Analysts

- Large number of fraud alerts every day
- High number of false positives
- Lack of explanation for AI predictions
- Time-consuming manual investigations
- Difficulty prioritizing high-risk transactions

---

## 6. Why AI is Used in Banking

Banks use AI to:
- Detect fraudulent transactions quickly
- Reduce false positives
- Identify hidden fraud patterns
- Prioritize investigations
- Improve customer experience
- Assist analysts with recommendations

---

## 7. Why Machine Learning Alone is Not Enough

Machine learning can predict whether a transaction is fraudulent, but it often cannot explain why. Fraud analysts need explanations, risk scores, compliance guidance, and recommendations before making a final decision.

---

## 8. My Understanding

SentinelAI will be an Enterprise Agentic AI Fraud Intelligence Platform that combines Machine Learning, Explainable AI, RAG, and AI Agents to help fraud analysts investigate suspicious transactions more efficiently.

# Day 2 Research Notes

## 1. How Banks Detect Fraud

Banks process millions of transactions every day. Since it is impossible for humans to review every transaction manually, banks use a combination of business rules, machine learning models, and AI systems to identify suspicious activities. Transactions that appear risky are sent to fraud analysts for further investigation before a final decision is made.

---

## 2. Rule Engine

A Rule Engine is the first layer of fraud detection. It consists of predefined business rules created by fraud experts based on historical fraud patterns.

Examples:
- If transaction amount > $2,000, increase risk score.
- If the transaction is from a foreign country, increase risk score.
- If a new device is used, increase risk score.
- If multiple transactions occur within a few minutes, flag the transaction.

Rule engines are fast and easy to understand, but they cannot detect new or unknown fraud patterns.

---

## 3. Machine Learning

Machine Learning is the second layer of fraud detection. Instead of using fixed rules, machine learning learns patterns from historical transaction data.

It analyzes many factors such as:
- Transaction amount
- Customer spending behavior
- Merchant category
- Transaction location
- Device information
- Previous fraud history

The model predicts the probability that a transaction is fraudulent and helps identify fraud patterns that traditional rules may miss.

---

## 4. False Positives

A False Positive occurs when the system incorrectly identifies a legitimate transaction as fraud.

Example:
A customer travels to another country and uses their credit card. The system blocks the transaction because it appears unusual, even though it is a genuine purchase.

False positives reduce customer satisfaction and create unnecessary work for fraud analysts.

---

## 5. False Negatives

A False Negative occurs when the system incorrectly classifies a fraudulent transaction as legitimate.

Example:
A stolen credit card is used to make a purchase, but the system approves the transaction because it does not recognize the suspicious behavior.

False negatives are dangerous because they lead to direct financial losses for both customers and banks.

---

## 6. Explainable AI (SHAP)

Machine learning models can predict whether a transaction is fraudulent, but they often do not explain why.

Explainable AI (SHAP) helps by showing which features contributed most to the prediction.

For example:
- High transaction amount
- New device
- Foreign country
- Unusual transaction time

This allows fraud analysts to understand and trust the model's predictions before taking action.

---

## 7. Retrieval-Augmented Generation (RAG)

RAG combines document retrieval with a Large Language Model (LLM).

Instead of relying only on the model's training knowledge, RAG searches trusted documents such as:
- AML (Anti-Money Laundering) policies
- PCI DSS (Payment Card Industry Data Security Standard)
- Internal fraud investigation guidelines
- Compliance documents

The retrieved information is then used to generate accurate and reliable answers for fraud analysts.

---

## 8. Agentic AI

Agentic AI uses multiple AI agents that collaborate to complete complex tasks instead of relying on a single chatbot.

For SentinelAI, different agents can perform different responsibilities:

- Fraud Detection Agent → Predicts fraudulent transactions.
- Risk Assessment Agent → Calculates transaction risk.
- Compliance Agent → Searches policies using RAG.
- Investigation Agent → Summarizes suspicious transactions.
- Report Agent → Generates investigation reports.

This approach improves automation, accuracy, and analyst productivity.

---

## 9. Complete Fraud Investigation Workflow

Customer
↓
Merchant
↓
Payment Network (Visa / Mastercard)
↓
Issuing Bank
↓
Rule Engine
↓
Machine Learning Model
↓
Explainable AI (SHAP)
↓
RAG (Policy Search)
↓
AI Agents
↓
Fraud Analyst
↓
Approve / Decline / Escalate

This workflow combines traditional fraud detection with modern AI technologies to support faster and more informed decision-making.

---

## 10. My Understanding

Traditional fraud detection systems focus only on predicting whether a transaction is fraudulent. SentinelAI goes beyond prediction by combining Rule Engines, Machine Learning, Explainable AI, RAG, and Agentic AI into a single platform. This enables fraud analysts to understand predictions, retrieve relevant compliance information, prioritize investigations, and make better decisions while reducing fraud losses and improving customer experience.

# Day 3 Research Notes

## 1. Target Users

### Fraud Analyst

### Risk Manager

### Compliance Officer

### Executive

---

## 2. Problems

- Too many alerts
- False positives
- No explanations
- Manual reports
- Policy search takes time

---

## 3. Product Features

- Dashboard
- Fraud Prediction
- Risk Score
- SHAP
- RAG
- AI Agents
- Reports

---

## 4. AI Agents

### Fraud Agent

Predict fraud.

### Risk Agent

Calculate risk.

### Compliance Agent

Search policies.

### Investigation Agent

Summarize investigation.

### Report Agent

Generate reports.

---

## 5. MVP

- Upload Dataset
- Fraud Detection
- Risk Score
- Dashboard
- AI Summary

---

## 6. Future Features

- Real-time Detection
- Mobile App
- Alerts
- Authentication
- Streaming Data

---

## 7. My Understanding

SentinelAI is not just a fraud detection model. It is an enterprise AI platform that combines machine learning, explainable AI, RAG, and multiple AI agents to help fraud analysts investigate suspicious transactions more efficiently.
# Day 4 Research Notes

## 1. What is System Architecture?

System Architecture is the overall design of a software system that defines how different components interact with each other. It serves as a blueprint for the application by describing the frontend, backend, database, machine learning models, AI services, APIs, and how data flows between them. A well-designed architecture makes the application scalable, maintainable, secure, and easy to enhance in the future.

---

## 2. Why React / Next.js?

React (using Next.js) is used to build the frontend of SentinelAI. It provides an interactive and responsive user interface where fraud analysts can monitor transactions, investigate fraud cases, view dashboards, interact with AI agents, and generate reports. Next.js also provides better performance, routing, and scalability for enterprise applications.

The frontend will display:
- Dashboard
- Transaction List
- Fraud Alerts
- Risk Scores
- SHAP Explanations
- AI Chat Assistant
- Investigation Reports

---

## 3. Why FastAPI?

FastAPI is the backend framework that connects all components of SentinelAI. It receives requests from the frontend, processes business logic, communicates with the database, calls the machine learning model, invokes AI agents, and returns results to the frontend.

FastAPI is chosen because it is:
- Fast and lightweight
- Easy to build REST APIs
- Supports asynchronous programming
- Automatically generates API documentation (Swagger)
- Easy to integrate with Python AI libraries

---

## 4. Why PostgreSQL?

PostgreSQL is the relational database used to store structured information.

It stores:
- Customer information
- Transaction history
- Fraud investigation records
- Risk scores
- AI-generated reports
- User accounts
- Audit logs

A database allows SentinelAI to efficiently store, retrieve, and analyze millions of transactions while maintaining data integrity and security.

---

## 5. Machine Learning Workflow

The Machine Learning model receives transaction information and predicts whether a transaction is fraudulent.

Typical workflow:

Transaction Data
↓
Data Preprocessing
↓
Feature Engineering
↓
Trained ML Model (XGBoost)
↓
Fraud Probability

The ML model analyzes features such as:
- Transaction amount
- Customer history
- Device information
- Merchant category
- Country
- Transaction time

The model outputs a fraud probability but does not explain why.

---

## 6. Explainable AI (SHAP)

SHAP (SHapley Additive exPlanations) explains why the machine learning model made a particular prediction.

Instead of only displaying:

Fraud Probability = 96%

SHAP explains:

- High transaction amount (+30%)
- Foreign country (+22%)
- New device (+18%)
- Night transaction (+15%)

This allows fraud analysts to understand and trust the prediction before making a decision.

---

## 7. LangGraph

LangGraph is an AI orchestration framework used to coordinate multiple AI agents.

Instead of using one chatbot, LangGraph manages specialized agents that work together.

Example agents:

- Fraud Detection Agent
- Risk Assessment Agent
- Compliance Agent
- Investigation Agent
- Report Generation Agent

LangGraph controls the sequence of tasks, shares information between agents, and manages the overall investigation workflow.

---

## 8. RAG Workflow

RAG (Retrieval-Augmented Generation) combines document retrieval with a Large Language Model.

Instead of relying only on the LLM's training data, RAG searches trusted enterprise documents before generating a response.

Example documents:

- AML Policy
- PCI DSS Guidelines
- Internal Fraud Investigation Rules
- Compliance Documents

Workflow:

Analyst Question
↓
Search Knowledge Base
↓
Retrieve Relevant Documents
↓
LLM Reads Retrieved Documents
↓
Generate Accurate Answer

This produces reliable and policy-based responses.

---

## 9. Complete System Architecture

The complete SentinelAI architecture consists of several connected components.

User
↓
React / Next.js Dashboard
↓
FastAPI Backend
↓
PostgreSQL Database
↓
Machine Learning Model
↓
SHAP Explanation
↓
LangGraph
↓
RAG + LLM
↓
Response to Dashboard

Each component has a specific responsibility, making the platform modular and scalable.

---

## 10. My Understanding

SentinelAI is an Enterprise Agentic AI Fraud Intelligence Platform that combines modern AI technologies into one solution. React provides the user interface, FastAPI connects all services, PostgreSQL stores enterprise data, the Machine Learning model predicts fraud, SHAP explains predictions, LangGraph coordinates AI agents, and RAG retrieves trusted knowledge for compliance-related questions. Together, these components help fraud analysts investigate suspicious transactions faster, make informed decisions, reduce fraud losses, and improve customer experience.

# Day 5 Research Notes

## 1. What is a Dataset?

A dataset is a collection of organized data used to train and evaluate a machine learning model. In fraud detection, each row in the dataset represents one financial transaction, while each column represents information about that transaction, such as the amount, country, merchant, device, transaction time, and whether the transaction was fraudulent.

The dataset helps the machine learning model learn patterns from historical transactions so it can predict whether future transactions are fraudulent.

---

## 2. Features vs Target

Features are the input variables provided to the machine learning model. They describe the characteristics of each transaction.

Examples of features:
- Transaction Amount
- Merchant Category
- Country
- Device Type
- Transaction Time
- Customer History

The target is the output variable that the model is trying to predict.

For SentinelAI:

0 = Legitimate Transaction

1 = Fraudulent Transaction

The model learns the relationship between the features and the target.

---

## 3. Exploratory Data Analysis (EDA)

Exploratory Data Analysis (EDA) is the process of understanding the dataset before building a machine learning model.

EDA helps answer questions such as:

- How many rows and columns are present?
- Are there missing values?
- Are there duplicate records?
- How many fraudulent transactions exist?
- What is the distribution of transaction amounts?
- Which features may influence fraud?

EDA improves data quality and helps select appropriate machine learning techniques.

---

## 4. Data Cleaning

Data cleaning is the process of preparing raw data before training a machine learning model.

Common data cleaning tasks include:

- Removing duplicate records
- Handling missing values
- Correcting incorrect data
- Converting data into the correct format
- Removing unnecessary columns

Clean data improves model performance and reduces prediction errors.

---

## 5. Class Imbalance

Class imbalance occurs when one class has significantly more samples than another.

In fraud detection:

Legitimate Transactions = 99.8%

Fraud Transactions = 0.2%

Because fraud is very rare, the model may become biased toward predicting legitimate transactions.

Handling class imbalance is one of the biggest challenges in fraud detection.

Common techniques include:
- SMOTE (Synthetic Minority Oversampling Technique)
- Undersampling
- Oversampling
- Class weighting

---

## 6. Machine Learning Pipeline

The machine learning pipeline is the sequence of steps used to build and deploy a machine learning model.

Workflow:

Raw Dataset
↓
Data Cleaning
↓
Exploratory Data Analysis (EDA)
↓
Feature Engineering
↓
Train-Test Split
↓
Machine Learning Model
↓
Model Evaluation
↓
Explainable AI (SHAP)
↓
Deployment

Each stage improves the quality and reliability of the final model.

---

## 7. Evaluation Metrics

### Accuracy

Accuracy measures the percentage of correct predictions.

Formula:

Accuracy = Correct Predictions / Total Predictions

Although accuracy is useful, it is not reliable for highly imbalanced datasets like fraud detection.

---

### Precision

Precision measures how many predicted fraud transactions were actually fraudulent.

High precision means fewer false positives.

Banks use precision to reduce unnecessary investigations.

---

### Recall

Recall measures how many actual fraud transactions were successfully detected.

High recall means fewer fraud cases are missed.

Banks usually prioritize recall because missing fraud can result in financial losses.

---

### F1 Score

F1 Score is the balance between Precision and Recall.

It is useful when both false positives and false negatives are important.

---

### ROC-AUC

ROC-AUC measures how well the model separates fraudulent transactions from legitimate ones.

A higher ROC-AUC score indicates better model performance across different decision thresholds.

---

## 8. Models for Fraud Detection

Several machine learning models can be used for fraud detection.

### Logistic Regression

A simple baseline classification model.

Advantages:
- Easy to understand
- Fast to train

Disadvantages:
- Limited ability to capture complex patterns

---

### Decision Tree

Creates decision rules based on transaction features.

Advantages:
- Easy to visualize
- Easy to explain

Disadvantages:
- Can overfit the training data

---

### Random Forest

An ensemble of multiple decision trees.

Advantages:
- More accurate than a single decision tree
- Reduces overfitting

Disadvantages:
- Slower than simpler models

---

### XGBoost

An advanced gradient boosting algorithm.

Advantages:
- High prediction accuracy
- Excellent performance on structured data
- Handles feature interactions effectively

This will be the primary machine learning model used in SentinelAI.

---

## 9. My Understanding

The quality of a machine learning model depends heavily on the quality of the data used for training. Before building any model, it is essential to understand the dataset through Exploratory Data Analysis and clean the data properly. Fraud detection is a highly imbalanced classification problem, making evaluation metrics such as Precision, Recall, F1 Score, and ROC-AUC more important than accuracy. SentinelAI will use a complete machine learning pipeline, beginning with data preparation and ending with Explainable AI using SHAP to help fraud analysts understand model predictions.

# Week 2 - Day 6: Understanding the Dataset Deeply

## 1. What is a Dataset?

A dataset is a structured collection of data used to train, validate, and test a machine learning model. In SentinelAI, each row represents one credit card transaction, and each column contains information about that transaction. The model learns patterns from historical transactions and uses those patterns to predict whether future transactions are fraudulent.

Example:

| Time | V1 | V2 | ... | Amount | Class |
|------|----|----|-----|--------|-------|
| 0 | -1.35 | -0.07 | ... | 149.62 | 0 |

Each row represents one completed transaction.

---

## 2. Features vs Target Variable

Machine Learning works with two types of variables.

### Features (Input Variables)

Features are the information given to the model so it can make a prediction.

In our dataset, the features are:

- Time
- V1
- V2
- ...
- V28
- Amount

These describe each transaction.

### Target Variable

The target variable is the correct answer that the model tries to learn.

In our dataset:

Class = 0 → Legitimate Transaction

Class = 1 → Fraudulent Transaction

The machine learning model learns the relationship between the features and the target variable.

---

## 3. Training vs Prediction

### Training Phase

During training, the model already knows the correct answers.

Example:

| Amount | Time | V1 | Class |
|--------|------|----|-------|
| 149.62 | 0 | -1.35 | 0 |
| 378.66 | 1 | -1.35 | 0 |
| 2500 | 52000 | 2.10 | 1 |

The model studies thousands of examples and learns patterns.

### Prediction Phase

When a new transaction arrives, the Class value is unknown.

Example:

| Amount | Time | V1 |
|--------|------|----|
| 820 | 175000 | 0.56 |

The model predicts:

Fraud Probability = 93%

Predicted Class = 1 (Fraud)

This prediction is then reviewed by the bank or fraud analyst.

---

## 4. What is PCA?

PCA stands for Principal Component Analysis.

It is a mathematical technique used to transform the original features into new numerical features while preserving most of the important information.

The original dataset may have contained information such as:

- Merchant Name
- Country
- Device
- Customer Age
- Credit Card Number

To protect customer privacy, these features were transformed into:

V1

V2

V3

...

V28

Although the original information is hidden, the transformed features still contain useful patterns for machine learning.

---

## 5. Why Are PCA Values Negative?

Many people think negative values indicate fraud.

This is incorrect.

PCA creates new mathematical dimensions.

Each transaction is represented as a point on these new dimensions.

Values can be:

Positive

Negative

Zero

Negative values simply indicate that the data point lies on one side of the new mathematical axis.

Positive values lie on the opposite side.

The machine learning model learns patterns from both positive and negative values.

---

## 6. Understanding the Time Column

The Time column represents the number of seconds elapsed since the first transaction recorded in the dataset.

It is not the actual date or time.

Example:

Time = 0

The first transaction.

Time = 20

Twenty seconds after the first transaction.

Time = 3600

One hour after the first transaction.

This allows the model to identify transaction timing patterns while protecting customer privacy.

---

## 7. Understanding the Amount Column

The Amount column represents the monetary value of one individual transaction.

Examples:

Amount = 2.69

A purchase worth $2.69.

Amount = 149.62

A purchase worth $149.62.

Amount = 378.66

A purchase worth $378.66.

It does NOT represent:

- Customer account balance
- Monthly spending
- Daily spending
- Total money in the bank

It only represents the value of that particular transaction.

---

## 8. Why Does the Dataset Already Have the Answer?

The dataset contains historical transactions that have already been investigated by the bank.

Therefore, every transaction already has a label:

0 = Legitimate

1 = Fraud

The model learns from these known examples.

When the model is deployed in a real bank, new transactions will not have a Class value.

The trained model will predict whether they are fraudulent.

---

## 9. Feature Engineering

Feature Engineering is the process of creating better input features to improve machine learning performance.

Although our dataset already contains PCA-transformed features, real banks often create additional features such as:

- Number of transactions in the last hour
- Average transaction amount
- Number of countries visited recently
- Distance between consecutive transactions
- Number of failed login attempts
- Customer spending behavior

Good features usually improve model accuracy.

---

## 10. My Understanding

Machine Learning depends heavily on understanding the dataset before building any model. Features describe each transaction, while the target variable tells the model the correct answer during training. PCA protects customer privacy by transforming sensitive information into anonymous numerical features. During prediction, new transactions do not have labels, so the trained model predicts whether they are fraudulent. Understanding the dataset is the first step toward building a reliable fraud detection system.

---

# Day 6 Questions & Answers

## 1. What is the difference between a feature and a target variable?

Features are the input variables used by the machine learning model to make predictions. They describe the characteristics of a transaction, such as Time, Amount, and V1–V28. The target variable is the output that the model is trying to predict. In this dataset, the target variable is the Class column, where 0 represents a legitimate transaction and 1 represents a fraudulent transaction.

---

## 2. Why does the training dataset contain the Class column but new transactions do not?

The training dataset contains historical transactions whose outcomes are already known. These labels help the model learn fraud patterns. New transactions occur in real time, so their Class value is unknown until the bank investigates them. The trained model predicts the Class for these new transactions.

---

## 3. Why was PCA applied to this dataset?

PCA was applied to protect customer privacy by transforming sensitive financial information into anonymous numerical features. It preserves most of the useful information while preventing researchers from identifying customers or their financial details.

---

## 4. Why can PCA values be negative?

PCA creates new mathematical dimensions called principal components. Each transaction is represented as coordinates on these dimensions. Values can be positive or negative depending on their position. Negative values do not indicate fraud; they are simply mathematical representations.

---

## 5. What does the Time column represent?

The Time column represents the number of seconds elapsed since the first transaction in the dataset. It is not the actual date or time.

---

## 6. What does the Amount column represent?

The Amount column represents the monetary value of a single transaction. It is not the customer's account balance or total spending.

---

## 7. What is Feature Engineering?

Feature Engineering is the process of creating new or improved input features from existing data to help machine learning models make better predictions. Good features often improve model performance significantly.

---

## 8. Why is understanding the dataset important before building a machine learning model?

Understanding the dataset helps identify data quality issues, understand feature meanings, detect class imbalance, and choose appropriate preprocessing and machine learning techniques. A well-understood dataset leads to a more accurate and reliable model.