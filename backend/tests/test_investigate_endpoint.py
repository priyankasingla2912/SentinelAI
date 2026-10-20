
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_investigate_endpoint_returns_report():
    """Verify that the investigation endpoint returns a complete report."""

    payload = {
        "prediction": "FRAUD",
        "risk_level": "CRITICAL",
        "fraud_probability": 0.95,
        "top_risk_factors": [
            {"feature": "V14", "shap_value": 0.12},
            {"feature": "V12", "shap_value": 0.08},
            {"feature": "V10", "shap_value": 0.05},
        ],
    }

    response = client.post("/investigate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "FRAUD"
    assert data["risk_level"] == "CRITICAL"
    assert data["fraud_probability"] == 0.95
    assert data["requires_human_review"] is True

    assert "assessment" in data
    assert "model_evidence" in data
    assert "retrieved_policies" in data
    assert "disclaimer" in data

    policy_ids = [policy["id"] for policy in data["retrieved_policies"]]

    assert "POL-001" in policy_ids
    assert len(data["model_evidence"]) == 3


def test_investigate_endpoint_rejects_missing_fields():
    """Verify that an incomplete request receives HTTP 422."""

    payload = {
        "prediction": "FRAUD",
        "risk_level": "CRITICAL",
    }

    response = client.post("/investigate", json=payload)

    assert response.status_code == 422


def test_investigate_endpoint_flags_legitimate_low_risk():
    """Verify that a low-risk legitimate transaction is reported correctly."""

    payload = {
        "prediction": "LEGITIMATE",
        "risk_level": "LOW",
        "fraud_probability": 0.05,
        "top_risk_factors": [
            {"feature": "V14", "shap_value": -0.12},
            {"feature": "V12", "shap_value": -0.08},
        ],
    }

    response = client.post("/investigate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == "LEGITIMATE"
    assert data["risk_level"] == "LOW"
    assert data["requires_human_review"] is False
