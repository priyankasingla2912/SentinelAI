# SentinelAI API Documentation

## 1. Overview

SentinelAI provides a FastAPI backend for transaction fraud prediction,
risk classification, SHAP-based explanations, transaction history, and
fraud investigation support.

When running locally, the API base URL is:

`http://127.0.0.1:8001`

Interactive API documentation is available at:

`http://127.0.0.1:8001/docs`

## 2. Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome and status information |
| GET | `/health` | Health check |
| POST | `/predict` | Predict fraud probability and save the result |
| POST | `/investigate` | Run the investigation workflow |
| GET | `/history` | Retrieve recent prediction history |
| GET | `/history/{prediction_id}` | Retrieve one transaction prediction |
| GET | `/stats` | Retrieve prediction statistics |

The application also contains fraud-case management endpoints. Consult
the interactive API documentation at `/docs` for their current request
schemas and available operations.

## 3. Health Check

**Request**

`GET /health`

**Example response**

```json
{
  "status": "healthy"
}
```

## 4. Transaction Prediction

**Request**

`POST /predict`

The request body must include all 30 model input features:
`Time`, `V1` through `V28`, and `Amount`.

- `Time`: number greater than or equal to zero.
- `V1` through `V28`: numeric values.
- `Amount`: number greater than or equal to zero.

Example request structure:

```json
{
  "Time": 0,
  "V1": 0,
  "V2": 0,
  "V3": 0,
  "V4": 0,
  "V5": 0,
  "V6": 0,
  "V7": 0,
  "V8": 0,
  "V9": 0,
  "V10": 0,
  "V11": 0,
  "V12": 0,
  "V13": 0,
  "V14": 0,
  "V15": 0,
  "V16": 0,
  "V17": 0,
  "V18": 0,
  "V19": 0,
  "V20": 0,
  "V21": 0,
  "V22": 0,
  "V23": 0,
  "V24": 0,
  "V25": 0,
  "V26": 0,
  "V27": 0,
  "V28": 0,
  "Amount": 0
}
```

This is a schema example, not a guarantee that the values represent
a realistic legitimate transaction.

**Response fields**

| Field | Description |
|---|---|
| `prediction_id` | ID of the saved prediction |
| `case_id` | Created fraud-case ID, or `null` when no case is created |
| `amount` | Submitted transaction amount |
| `fraud_probability` | Model-estimated fraud probability |
| `threshold` | Current classification threshold |
| `prediction` | `FRAUD` or `LEGITIMATE` |
| `risk_level` | `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` |
| `top_risk_factors` | Up to five features with their SHAP values |
| `recommended_action` | Action recommendation based on risk level |

The prediction is classified as `FRAUD` when the estimated probability
is greater than or equal to the configured threshold. Otherwise, it is
classified as `LEGITIMATE`.

A prediction classified as fraud automatically creates a fraud case.
The endpoint saves the prediction and returns its identifier.

## 5. Transaction Investigation

**Request**

`POST /investigate`

The request body must contain these fields:

- `prediction`
- `risk_level`
- `fraud_probability`
- `top_risk_factors`

Example request structure:

```json
{
  "prediction": "FRAUD",
  "risk_level": "HIGH",
  "fraud_probability": 0.75,
  "top_risk_factors": [
    {
      "feature": "V14",
      "shap_value": 0.12
    }
  ]
}
```

This example illustrates the expected structure. Its values are illustrative.

The endpoint runs the investigation workflow and returns the workflow
result. The application uses the workflow for risk assessment, policy
evidence retrieval, and human-review recommendations.

If required fields are missing, the endpoint returns HTTP `422` with
a message and a list of missing fields.

## 6. Prediction History

**Request**

`GET /history`

Optional query parameter:

| Parameter | Default | Constraint |
|---|---:|---|
| `limit` | `20` | Integer from 1 to 100 |

Example:

`GET /history?limit=10`

The response contains a `count` and a `predictions` array. Each prediction
includes its ID, amount, fraud probability, threshold, classification,
risk level, recommended action, SHAP factors, and creation timestamp.

## 7. Transaction Details

**Request**

`GET /history/{prediction_id}`

Replace `{prediction_id}` with the saved transaction's ID.

The response contains the prediction details, including SHAP factors.
If the ID does not exist, the endpoint returns HTTP `404` with the
detail `Transaction not found`.

## 8. Prediction Statistics

**Request**

`GET /stats`

Returns the prediction statistics produced by the database statistics
function.

The exact response fields depend on that function's implementation.

## 9. Risk Classification

The current risk-level boundaries are:

| Fraud probability | Risk level |
|---|---|
| Greater than or equal to 0.90 | `CRITICAL` |
| Greater than or equal to 0.60 and below 0.90 | `HIGH` |
| Greater than or equal to 0.30 and below 0.60 | `MEDIUM` |
| Below 0.30 | `LOW` |

The fraud classification threshold and risk-level boundaries serve
different purposes. The current application threshold is `0.60`.

## 10. Error Handling

Observed endpoint behavior includes:

- HTTP `404` when a requested transaction or fraud case is not found.
- HTTP `422` when request validation fails or required investigation
  fields are missing.
- The history endpoint rejects `limit` values outside the range 1–100.

Other errors may depend on runtime conditions and the underlying
components.

## 11. Limitations

SentinelAI is a prototype for fraud analysis and decision support.
It does not connect to a live banking transaction network and does
not execute real payment blocking or authorization.

SHAP values describe model contributions; they do not establish the
cause of fraud. Investigation recommendations should be reviewed by
a human analyst when appropriate.

## 12. Fraud Case Management

Fraud cases track transactions that require investigation. A fraud case
can be created automatically when `/predict` classifies a transaction as
fraudulent, or manually for an existing prediction.

### List Fraud Cases

**Request:** `GET /cases`

Returns a `count` and a `cases` array. Each case includes its case ID,
prediction ID, status, analyst, investigation notes, creation timestamp,
and last-updated timestamp.

### Retrieve a Fraud Case

**Request:** `GET /cases/{case_id}`

Returns the details of the specified case.

If the case does not exist, the API returns HTTP `404` with
`Fraud case not found`.

### Create a Fraud Case

**Request:** `POST /cases`

**Success status:** HTTP `201 Created`

Example request:

```json
{
  "prediction_id": 1,
  "analyst": "Fraud Analyst",
  "investigation_notes": "Review the transaction and supporting evidence."
}
```

`prediction_id` is required and must be greater than zero.
`analyst` is optional and limited to 100 characters.
`investigation_notes` is optional and limited to 2,000 characters.

The referenced prediction must exist. Otherwise, the API returns
HTTP `404` with `Transaction not found`.

The response contains the new case ID, prediction ID, status, analyst,
investigation notes, and timestamps.

### Update a Fraud Case

**Request:** `PUT /cases/{case_id}`

Example request:

```json
{
  "status": "IN_PROGRESS",
  "analyst": "Fraud Analyst",
  "investigation_notes": "Reviewing the transaction evidence."
}
```

Updates only the fields included in the request. Supported statuses are:

- `NEW`
- `IN_PROGRESS`
- `RESOLVED`

Status values are normalized to uppercase. An explicitly null status
returns HTTP `400`; an unsupported status also returns HTTP `400`.
Missing cases return HTTP `404`.

The analyst field is limited to 100 characters and investigation notes
to 2,000 characters. The response contains the updated case details.
