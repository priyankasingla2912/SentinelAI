
import pytest
from fastapi.testclient import TestClient

from app.main import app
from unittest.mock import patch


client = TestClient(app)


@pytest.fixture
def valid_transaction():
    return {
        "Time": 406.0,
        "V1": -2.312227,
        "V2": 1.951992,
        "V3": -1.609851,
        "V4": 3.997906,
        "V5": -0.522188,
        "V6": -1.426545,
        "V7": -2.537387,
        "V8": 1.391657,
        "V9": -2.770089,
        "V10": -2.772272,
        "V11": 3.202033,
        "V12": -2.899907,
        "V13": -0.595222,
        "V14": -4.289254,
        "V15": 0.389724,
        "V16": -1.140747,
        "V17": -2.830056,
        "V18": -0.016822,
        "V19": 0.416956,
        "V20": 0.126911,
        "V21": 0.517232,
        "V22": -0.035049,
        "V23": -0.465211,
        "V24": 0.320198,
        "V25": 0.044519,
        "V26": 0.177840,
        "V27": 0.261145,
        "V28": -0.143276,
        "Amount": 0.0,
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_history_endpoint():
    response = client.get("/history")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "count" in data
    assert "predictions" in data
    assert isinstance(data["predictions"], list)


def test_transaction_not_found():
    response = client.get("/history/99999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Transaction not found"


def test_predict_transaction(valid_transaction):
    response = client.post("/predict", json=valid_transaction)

    assert response.status_code == 200

    data = response.json()

    # Verify required response fields
    assert "prediction_id" in data
    assert "case_id" in data
    assert "fraud_probability" in data
    assert "threshold" in data
    assert "prediction" in data
    assert "risk_level" in data
    assert "recommended_action" in data
    assert "top_risk_factors" in data

    # Verify prediction ID
    assert isinstance(data["prediction_id"], int)
    assert data["prediction_id"] > 0

    # Verify probability and threshold
    assert 0 <= data["fraud_probability"] <= 1
    assert 0 <= data["threshold"] <= 1

    # Verify prediction and risk classifications
    assert data["prediction"] in ["FRAUD", "LEGITIMATE"]
    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    # Verify recommended action and SHAP factors
    assert isinstance(data["recommended_action"], str)
    assert len(data["recommended_action"]) > 0
    assert isinstance(data["top_risk_factors"], list)
    assert len(data["top_risk_factors"]) > 0

    # Verify case ID matches automatic case-creation behavior
    if data["prediction"] == "FRAUD":
        assert isinstance(data["case_id"], int)
        assert data["case_id"] > 0
    else:
        assert data["case_id"] is None


def test_negative_amount_rejected(valid_transaction):
    transaction = valid_transaction.copy()
    transaction["Amount"] = -10.0

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422


def test_negative_time_rejected(valid_transaction):
    transaction = valid_transaction.copy()
    transaction["Time"] = -1.0

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422


def test_history_limit_zero_rejected():
    response = client.get("/history?limit=0")

    assert response.status_code == 422


def test_history_limit_too_large_rejected():
    response = client.get("/history?limit=101")

    assert response.status_code == 422


def test_invalid_predict_payload_rejected():
    response = client.post("/predict", json={})

    assert response.status_code == 422


def test_fraud_case_can_be_retrieved(valid_transaction):
    # Create a prediction through the API
    prediction_response = client.post(
        "/predict",
        json=valid_transaction,
    )

    assert prediction_response.status_code == 200
    prediction_data = prediction_response.json()

    prediction_id = prediction_data["prediction_id"]
    assert isinstance(prediction_id, int)
    assert prediction_id > 0

    # Create a fraud case explicitly for this prediction.
    # This avoids depending on the model's classification.
    case_response = client.post(
        "/cases",
        json={
            "prediction_id": prediction_id,
            "analyst": "Test Analyst",
            "investigation_notes": "Automated API test.",
        },
    )

    assert case_response.status_code == 201
    case_data = case_response.json()

    case_id = case_data["case_id"]
    assert isinstance(case_id, int)
    assert case_id > 0

    # Retrieve the case and verify its saved details.
    retrieval_response = client.get(f"/cases/{case_id}")

    assert retrieval_response.status_code == 200

    retrieved_case = retrieval_response.json()

    assert retrieved_case["case_id"] == case_id
    assert retrieved_case["prediction_id"] == prediction_id
    assert retrieved_case["status"] == "NEW"
    assert retrieved_case["analyst"] == "Test Analyst"
    assert retrieved_case["investigation_notes"] == (
        "Automated API test."
    )

def test_predict_fraud_automatically_creates_case(valid_transaction):
    with (
        patch("app.main.model.predict_proba", return_value=[[0.05, 0.95]]),
        patch(
            "app.main.explainer.shap_values",
            return_value=[[0.0] * 30, [0.0] * 30],
        ),
    ):
        response = client.post("/predict", json=valid_transaction)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "FRAUD"
    assert data["fraud_probability"] == 0.95
    assert isinstance(data["prediction_id"], int)
    assert isinstance(data["case_id"], int)
    assert data["case_id"] > 0

    case_response = client.get(f"/cases/{data['case_id']}")

    assert case_response.status_code == 200

    case_data = case_response.json()

    assert case_data["prediction_id"] == data["prediction_id"]
    assert case_data["status"] == "NEW"
    assert "Automatically created" in case_data["investigation_notes"]


def test_predict_legitimate_does_not_create_case(valid_transaction):
    with (
        patch("app.main.model.predict_proba", return_value=[[0.95, 0.05]]),
        patch(
            "app.main.explainer.shap_values",
            return_value=[[0.0] * 30, [0.0] * 30],
        ),
    ):
        response = client.post("/predict", json=valid_transaction)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "LEGITIMATE"
    assert data["fraud_probability"] == 0.05
    assert isinstance(data["prediction_id"], int)
    assert data["prediction_id"] > 0
    assert data["case_id"] is None
