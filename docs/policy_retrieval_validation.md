# SentinelAI — Policy Retrieval Validation

**Validation Day:** Day 3  
**Status:** Completed  
**Scope:** Policy quality, keyword retrieval, edge cases, and JSON integrity

## 1. Objective

Evaluate the existing fraud policy knowledge base and keyword-based retrieval implementation without modifying application code or production data.

## 2. Policy Inventory

Four sample policies were reviewed:

| Policy ID | Title | Purpose |
|---|---|---|
| POL-001 | High-Risk Transaction Review | Human review of high and critical risk transactions |
| POL-002 | Explainable Fraud Investigation | Interpretation and limitations of SHAP explanations |
| POL-003 | Suspicious Transaction Escalation | Documentation and analyst escalation |
| POL-004 | Low-Risk Transaction Monitoring | Monitoring and awareness of false negatives |

These policies are development guidance and have not been validated as official banking policies.

## 3. Retrieval Implementation

The existing retriever in `backend/app/knowledge/retriever.py`:

- Loads policies from `fraud_policies.json`.
- Normalizes text using lowercase alphanumeric tokenization.
- Compares unique query terms with policy titles, categories, keywords, and content.
- Scores policies by the number of matching unique terms.
- Sorts by descending score, then policy ID.
- Returns up to the requested `top_k` results.

This is keyword-overlap retrieval, not embedding-based semantic search.

## 4. Retrieval Relevance Tests

Four representative queries were tested.

| Scenario | Expected policy | Actual top result | Result |
|---|---|---|---|
| High/critical risk review | POL-001 | POL-001 | Pass |
| SHAP explanation | POL-002 | POL-002 | Pass |
| Suspicious transaction escalation | POL-003 | POL-003 | Pass |
| Low-risk monitoring | POL-004 | POL-004 | Pass |

The expected policy ranked first in all four tested scenarios.

### Observed limitations

- Generic terms such as `risk`, `review`, and `transaction` can produce less relevant additional results.
- SHAP-specific feature names such as V14 and V10 are not matched by the current sample policies.
- Ranking is based on term overlap, not semantic relevance or calibrated confidence.

## 5. Edge-Case Tests

| Input | Expected behavior | Result |
|---|---|---|
| Empty query | Empty result list | Pass |
| Unmatched query | Empty result list | Pass |
| `top_k = 0` | Empty result list | Pass |
| `high risk`, `top_k = 1` | One matching result | Pass |

All four tests passed without errors.

## 6. Policy File Integrity

The JSON integrity check confirmed:

- Policy count: 4
- Policy IDs are unique.
- No required fields are missing.
- All keyword fields are lists.
- JSON parsing succeeds.

Required fields checked: `id`, `title`, `category`, `keywords`, `content`, and `recommended_action`.

## 7. Findings

### Strengths

- All four representative scenarios ranked their expected policy first.
- Empty and unmatched queries are handled safely.
- The retriever respects the requested result limit.
- Policy records have consistent required fields.
- The sample policies include human-review and model-limitation guidance.

### Limitations

- Retrieval uses keyword overlap rather than semantic search.
- Generic term overlap can introduce irrelevant results.
- There is no relevance confidence threshold.
- The knowledge base contains only four sample policies.
- Policy content has not been approved or validated by a bank or compliance team.

## 8. Recommendations

1. Retain the current implementation for the validated prototype.
2. Consider semantic retrieval as a future enhancement, with a measured relevance evaluation.
3. Expand policy coverage using institution-approved policy documents.
4. Introduce policy versioning and ownership before production use.
5. Keep human review central to consequential fraud decisions.
6. Evaluate retrieval quality using a larger, labeled test set before claiming production readiness.

## 9. Validation Conclusion

The current keyword-based policy retriever passed all four representative relevance tests and all four edge-case tests. The policy JSON passed its structural integrity checks.

The implementation is suitable as a basic prototype retrieval component within the tested scope. It is not a production-grade banking policy engine or semantic RAG system.

**No application code or production database was modified during this validation.**
