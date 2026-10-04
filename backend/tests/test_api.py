import pytest
from fastapi.testclient import TestClient

from app.main import app


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

    assert "fraud_probability" in data
    assert "prediction" in data
    assert "risk_level" in data
    assert "recommended_action" in data
    assert "top_risk_factors" in data

    assert 0 <= data["fraud_probability"] <= 1
    assert data["prediction"] in ["FRAUD", "LEGITIMATE"]
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert isinstance(data["top_risk_factors"], list)
    assert len(data["top_risk_factors"]) > 0


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