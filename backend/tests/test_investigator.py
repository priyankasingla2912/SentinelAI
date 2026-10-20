
from app.knowledge.investigator import investigate_transaction


def test_high_risk_fraud_requires_human_review():
    report = investigate_transaction(
        {
            "prediction": "FRAUD",
            "risk_level": "CRITICAL",
            "fraud_probability": 0.95,
            "top_risk_factors": [
                {"feature": "V14", "shap_value": 0.12}
            ],
        }
    )

    assert report["requires_human_review"] is True
    assert report["prediction"] == "FRAUD"
    assert report["model_evidence"][0]["feature"] == "V14"


def test_low_risk_report_does_not_guarantee_legitimacy():
    report = investigate_transaction(
        {
            "prediction": "LEGITIMATE",
            "risk_level": "LOW",
            "fraud_probability": 0.01,
            "top_risk_factors": [],
        }
    )

    assert report["requires_human_review"] is False
    assert "does not guarantee legitimacy" in report["assessment"]


def test_report_includes_retrieved_policies():
    report = investigate_transaction(
        {
            "prediction": "FRAUD",
            "risk_level": "HIGH",
            "fraud_probability": 0.8,
            "top_risk_factors": [
                {"feature": "V14", "shap_value": 0.1}
            ],
        }
    )

    assert "retrieved_policies" in report
    assert isinstance(report["retrieved_policies"], list)
    assert "disclaimer" in report
