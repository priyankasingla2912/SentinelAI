# Investigation Workflow & AI Agent Validation

**Project:** SentinelAI – AI-Powered Fraud & Risk Intelligence Platform  
**Validation status:** Completed  
**Date:** November 6, 2026

## 1. Objective

Validate the existing fraud investigation workflow, explainability integration,
policy retrieval, case management, role-based permissions, and backend test suite.

## 2. Architecture Reviewed

The current investigation workflow uses LangGraph with two sequential nodes:

1. `assess_risk` – prepares a risk assessment from prediction output.
2. `prepare_report` – retrieves relevant policy content and creates an investigation report.

The workflow is a linear two-node pipeline. It should not currently be described
as five independent autonomous agents.

## 3. Investigation Workflow

The `run_investigation()` function was executed successfully using a sample
high-risk fraud prediction.

The returned report included:
- Prediction and risk level.
- Fraud probability.
- Top model risk factors.
- Retrieved policy references.
- Human-review recommendation.
- Development-policy disclaimer.

High-risk and fraud predictions are flagged for human review.

## 4. Explainability (SHAP)

SHAP execution was verified separately using the Random Forest model.

The investigation report preserves the supplied feature names and SHAP values
as model evidence.

The workflow therefore demonstrates explainability data flowing into the
investigation report.

## 5. Policy Retrieval

The retriever loads sample policies from `fraud_policies.json`.

It uses keyword overlap across policy titles, categories, keywords, and content.

Current limitations:
- Retrieval is keyword-based, not embedding-based semantic search.
- The policy collection contains sample development content.
- Policies must be reviewed and validated before any real banking use.

## 6. Case Management and Permissions

Existing API implementation and tests cover:
- Case creation and retrieval.
- Administrator case updates.
- Assigned analyst updates.
- Restrictions on analysts updating other analysts' cases.
- Restrictions on analyst reassignment.
- Viewer update restrictions.
- Invalid case status rejection.

The supported case statuses include NEW, IN_PROGRESS, and RESOLVED.

## 7. Automated Test Results

Full backend test suite:

**82 passed, 3 warnings**

The inspected test suites also reported:
- `tests/test_api.py`: 19 passed.
- `tests/test_roles.py`: 42 passed.
- Remaining backend tests: 21 passed.

The three warnings are non-fatal SHAP/Matplotlib deprecation warnings.

No test failures were reported.

## 8. Known Gaps and Production Considerations

1. A dedicated automated API test for the `/investigate` endpoint was not
   identified during this review.
2. The current LangGraph workflow is a two-node sequential pipeline.
3. Policy retrieval uses keyword matching rather than semantic retrieval.
4. The policy content is illustrative development material, not verified
   institutional banking policy.
5. Human review remains necessary; model output is not proof of fraud.
6. Further end-to-end testing with realistic, approved test scenarios is
   recommended before production deployment.

## 9. Conclusion

The existing investigation workflow executed successfully in a direct test.
SHAP execution was verified, investigation reports preserved model evidence,
and the complete backend automated test suite passed.

The validation confirms the current development implementation is functioning
within the tested scope. It does not establish production readiness or
regulatory compliance.

**Milestone result: Validation completed with documented limitations.**
