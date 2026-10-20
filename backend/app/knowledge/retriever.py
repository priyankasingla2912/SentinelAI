
import json
import re
from pathlib import Path
from typing import Any


POLICY_FILE = Path(__file__).resolve().parent / "fraud_policies.json"


def load_policies() -> list[dict[str, Any]]:
    """Load the sample fraud investigation policies."""
    with POLICY_FILE.open("r", encoding="utf-8") as file:
        policies = json.load(file)

    if not isinstance(policies, list):
        raise ValueError("Policy file must contain a JSON list.")

    return policies


def tokenize(text: str) -> set[str]:
    """Normalize text into searchable terms."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve_policies(
    query: str,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Return policies ranked by keyword overlap."""
    if not query.strip():
        return []

    if top_k < 1:
        return []

    query_terms = tokenize(query)
    results = []

    for policy in load_policies():
        searchable_text = " ".join(
            [
                policy.get("title", ""),
                policy.get("category", ""),
                " ".join(policy.get("keywords", [])),
                policy.get("content", ""),
            ]
        )

        policy_terms = tokenize(searchable_text)
        matched_terms = sorted(query_terms & policy_terms)

        if not matched_terms:
            continue

        results.append(
            {
                "id": policy["id"],
                "title": policy["title"],
                "category": policy["category"],
                "content": policy["content"],
                "recommended_action": policy["recommended_action"],
                "matched_terms": matched_terms,
                "score": len(matched_terms),
            }
        )

    results.sort(
        key=lambda item: (-item["score"], item["id"])
    )

    return results[:top_k]
