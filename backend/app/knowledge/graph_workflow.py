
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.knowledge.investigator import investigate_transaction


class InvestigationState(TypedDict, total=False):
    prediction: dict[str, Any]
    risk_assessment: dict[str, Any]
    investigation_report: dict[str, Any]


def assess_risk(state: InvestigationState) -> dict:
    """Preserve the existing model prediction as evidence."""
    prediction = state["prediction"]

    return {
        "risk_assessment": {
            "prediction": prediction.get("prediction", "UNKNOWN"),
            "risk_level": prediction.get("risk_level", "UNKNOWN"),
            "fraud_probability": prediction.get("fraud_probability"),
            "top_risk_factors": prediction.get(
                "top_risk_factors", []
            ),
        }
    }


def retrieve_and_prepare_report(
    state: InvestigationState,
) -> dict:
    """Retrieve policies and assemble the investigation report."""
    report = investigate_transaction(state["risk_assessment"])

    return {"investigation_report": report}


def build_investigation_graph():
    """Build and compile the SentinelAI investigation workflow."""
    workflow = StateGraph(InvestigationState)

    workflow.add_node("assess_risk", assess_risk)
    workflow.add_node(
        "prepare_report",
        retrieve_and_prepare_report,
    )

    workflow.add_edge(START, "assess_risk")
    workflow.add_edge("assess_risk", "prepare_report")
    workflow.add_edge("prepare_report", END)

    return workflow.compile()


investigation_graph = build_investigation_graph()


def run_investigation(
    prediction: dict[str, Any],
) -> dict[str, Any]:
    """Run the workflow for an existing prediction result."""
    result = investigation_graph.invoke(
        {"prediction": prediction}
    )

    return result["investigation_report"]
