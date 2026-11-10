# SentinelAI User Guide
## 1. Overview

SentinelAI is an AI-powered fraud detection and risk intelligence platform.

It helps users:
- Analyze transaction data.
- Identify potentially fraudulent transactions.
- Understand fraud risk scores and prediction results.
- Review important transaction risk factors using SHAP explainability.
- Investigate suspicious transactions using AI-assisted investigation workflows.
- Manage fraud investigation cases.
- View prediction history and dashboard statistics.

SentinelAI is designed as a decision-support prototype. Its predictions and recommendations should support human review and must not be treated as definitive proof of fraud or automatic authorization to block transactions.

## 2. Login and Authentication

1. Open the SentinelAI application in your browser.
2. Navigate to the login page.
3. Enter your registered email address and password.
4. Click the Login button.
5. After successful authentication, access the dashboard.

SentinelAI uses role-based access control. Available actions depend on the user's assigned role.

If you forget your password, use the Forgot Password option and follow the verification instructions.

For security, do not share your login credentials with others.

## 3. Dashboard

The dashboard provides an overview of fraud detection activity and prediction statistics.

Users can review:
- Total transaction predictions.
- Fraudulent transaction counts.
- Legitimate transaction counts.
- Fraud detection statistics.
- Recent prediction activity.

Dashboard information helps users monitor fraud detection activity and identify patterns requiring further investigation.

## 4. Transaction Analysis

The transaction analysis feature allows users to submit transaction information for fraud prediction.

Steps:

1. Navigate to the transaction analysis page.
2. Enter the required transaction information.
3. Provide the transaction amount and required transaction features.
4. Submit the transaction for analysis.
5. Review the prediction result.

The system returns information such as:
- Prediction result (FRAUD or LEGITIMATE).
- Fraud probability.
- Classification threshold.
- Risk level.
- Recommended action.
- Top SHAP risk factors.

The model uses anonymized transaction features V1–V28, along with transaction time and amount.

## 5. Risk Levels and Prediction Results

SentinelAI categorizes transaction risk using fraud probability.

| Fraud Probability | Risk Level |
|---|---|
| 90% or higher | CRITICAL |
| 60% to below 90% | HIGH |
| 30% to below 60% | MEDIUM |
| Below 30% | LOW |

The classification threshold is 0.60.

A prediction indicates potential risk and should be reviewed alongside other available evidence.

## 6. Explainable AI (SHAP)

SentinelAI uses SHAP (SHapley Additive exPlanations) to explain important factors influencing fraud predictions.

Users can review:
- Top contributing transaction features.
- SHAP values.
- Factors that increase or decrease the model's fraud prediction.

SHAP explanations help analysts understand why a transaction received a particular prediction.

These explanations describe model behavior and do not establish that a transaction is fraudulent.

## 7. AI-Assisted Investigation

The investigation workflow provides additional context for reviewing suspicious transactions.

Steps:

1. Submit or identify a transaction prediction.
2. Open the investigation feature.
3. Provide the required prediction information.
4. Run the investigation workflow.
5. Review the generated investigation report.

The report can include:
- Prediction result.
- Risk level and fraud probability.
- Risk assessment.
- Model evidence and SHAP factors.
- Retrieved policy guidance.
- Human-review recommendation.

The current policy retrieval system uses keyword matching against sample development policies. These policies must be validated before any real banking use.

## 8. Fraud Case Management

Fraud cases can be created and managed through the case management functionality.

Users can:
- View fraud cases.
- Review case details.
- Assign analysts where permitted.
- Update case status where permitted.
- Add investigation notes.

Supported case statuses:

- NEW
- IN_PROGRESS
- RESOLVED

Available case management actions depend on the user's assigned role and permissions.

Fraud analysts can update cases assigned to them but cannot assign or reassign cases.

## 9. Prediction History

The history feature allows users to review previously submitted transaction predictions.

Users can:
- View historical predictions.
- Open individual prediction records.
- Review prediction results.
- Examine stored SHAP factors.

History supports ongoing monitoring and investigation.

## 10. User Roles and Permissions

SentinelAI supports four user roles.

| Role | Description |
|---|---|
| ADMIN | Administrative access and user management |
| SENIOR_FRAUD_ANALYST | Senior investigation and case management permissions |
| FRAUD_ANALYST | Fraud investigation and assigned case management |
| VIEWER | Read-only access to permitted information |

The application enforces permissions through backend authorization checks.

## 11. Security Guidelines

Users should follow these security practices:

- Keep login credentials confidential.
- Use strong passwords.
- Log out after completing work.
- Do not share sensitive transaction information unnecessarily.
- Access only information permitted by your assigned role.
- Report unexpected access or application behavior.

## 12. Important Limitations

SentinelAI is currently a research and development prototype.

Important limitations include:

- It uses a public credit card fraud dataset.
- V1–V28 are anonymized transaction features.
- It is not connected to a live banking payment network.
- It does not automatically approve, decline, or block real transactions.
- Investigation policies are sample development content.
- Predictions and recommendations require human review.

The platform should not be treated as a certified production banking fraud prevention system.

## 13. Support and Troubleshooting

If the application does not work as expected:

1. Verify that the backend service is running.
2. Verify that the frontend application is running.
3. Check the backend API health endpoint.
4. Confirm that the database connection is available.
5. Review application logs for errors.
6. Verify that the required model file is available.

For technical issues, consult the project README and API Documentation.

---
**Document:** SentinelAI User Guide

**Purpose:** Application usage and operational reference

**Status:** Development prototype documentation