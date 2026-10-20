
from app.knowledge.graph_workflow import run_investigation


def test_graph_preserves_prediction_and_risk():
    report = run_investigation(
        {
            "prediction": "FRAUD",
            "risk_level": "CRITICAL",
            "fraud_probability": 0.95,
            "top_risk_factors": [
                {"feature": "V14", "shap_value": 0.12}
            ],
        }
    )

    assert report["prediction"] == "FRAUD"
    assert report["risk_level"] == "CRITICAL"
    assert report["fraud_probability"] == 0.95


def test_graph_requires_human_review_for_fraud():
    report = run_investigation(
        {
            "prediction": "FRAUD",
            "risk_level": "CRITICAL",
            "fraud_probability": 0.95,
            "top_risk_factors": [],
        }
    )

    assert report["requires_human_review"] is True


def test_graph_returns_policy_evidence():
    report = run_investigation(
        {
            "prediction": "FRAUD",
            "risk_level": "CRITICAL",
            "fraud_probability": 0.95,
            "top_risk_factors": [
                {"feature": "V14", "shap_value": 0.12}
            ],
        }
    )

    policies = report["retrieved_policies"]

    assert policies
    assert all(
        "id" in policy and "content" in policy
        for policy in policies
    )
