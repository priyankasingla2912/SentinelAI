
from typing import Any

from app.knowledge.retriever import retrieve_policies


def investigate_transaction(
    prediction: dict[str, Any],
) -> dict[str, Any]:
    """Create an evidence-grounded investigation report."""

    risk_level = str(
        prediction.get("risk_level", "UNKNOWN")
    ).upper()

    fraud_probability = prediction.get("fraud_probability")
    predicted_class = str(
        prediction.get("prediction", "UNKNOWN")
    ).upper()

    factors = prediction.get("top_risk_factors", [])

    query_parts = [
        risk_level,
        predicted_class,
        "fraud investigation",
    ]

    for factor in factors:
        feature = factor.get("feature", "")
        if feature:
            query_parts.append(str(feature))

    policies = retrieve_policies(
        " ".join(query_parts),
        top_k=3,
    )

    if risk_level in {"HIGH", "CRITICAL"}:
        assessment = (
            "Prioritize this transaction for human review. "
            "The model classification is a risk signal, "
            "not proof of fraud."
        )
    elif risk_level == "MEDIUM":
        assessment = (
            "Review the available model evidence and "
            "apply appropriate transaction monitoring."
        )
    elif risk_level == "LOW":
        assessment = (
            "Continue applicable monitoring. A low-risk "
            "prediction does not guarantee legitimacy."
        )
    else:
        assessment = (
            "Risk level is unavailable or unrecognized. "
            "Verify the prediction before taking action."
        )

    evidence = [
        {
            "feature": factor.get("feature"),
            "shap_value": factor.get("shap_value"),
        }
        for factor in factors
    ]

    return {
        "prediction": predicted_class,
        "risk_level": risk_level,
        "fraud_probability": fraud_probability,
        "assessment": assessment,
        "model_evidence": evidence,
        "retrieved_policies": policies,
        "requires_human_review": (
            risk_level in {"HIGH", "CRITICAL"}
            or predicted_class == "FRAUD"
        ),
        "disclaimer": (
            "This report is decision support, not proof of "
            "fraud. Retrieved policies are sample development "
            "content and must be validated before production use."
        ),
    }
