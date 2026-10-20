
from app.knowledge.retriever import retrieve_policies


def test_shap_query_returns_explainability_policy():
    results = retrieve_policies(
        "SHAP explanation risk factors",
        top_k=3,
    )

    assert results
    assert results[0]["id"] == "POL-002"
    assert "matched_terms" in results[0]
    assert results[0]["score"] > 0


def test_escalation_query_returns_escalation_policy():
    results = retrieve_policies(
        "suspicious transaction escalation investigation",
        top_k=3,
    )

    result_ids = [item["id"] for item in results]

    assert "POL-003" in result_ids


def test_empty_query_returns_no_results():
    assert retrieve_policies("") == []
    assert retrieve_policies("   ") == []


def test_top_k_limits_results():
    results = retrieve_policies(
        "fraud investigation risk review",
        top_k=2,
    )

    assert len(results) <= 2


def test_results_include_policy_evidence():
    results = retrieve_policies(
        "low risk monitoring",
        top_k=3,
    )

    assert results

    for result in results:
        assert result["id"]
        assert result["title"]
        assert result["content"]
        assert result["recommended_action"]
