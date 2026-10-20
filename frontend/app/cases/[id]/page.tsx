"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";

const API_URL = "http://127.0.0.1:8001";

type FraudCase = {
  case_id: number;
  prediction_id: number;
  status: "NEW" | "IN_PROGRESS" | "RESOLVED" | string;
  analyst: string | null;
  investigation_notes: string | null;
  created_at: string;
  updated_at: string;
};

type ShapFactor = {
  feature: string;
  shap_value: number;
};

type Transaction = {
  id: number;
  amount: number;
  fraud_probability: number;
  threshold: number;
  prediction: string;
  risk_level: string;
  recommended_action: string;
  shap_factors: ShapFactor[] | null;
  created_at: string;
};

const panelClass =
  "rounded-xl border border-slate-800 bg-slate-900 p-6";

const fieldClass =
  "mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500";

const buttonClass =
  "rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50";

function statusClass(status: string) {
  switch (status) {
    case "RESOLVED":
      return "border-green-500/30 bg-green-500/10 text-green-400";
    case "IN_PROGRESS":
      return "border-blue-500/30 bg-blue-500/10 text-blue-400";
    default:
      return "border-amber-500/30 bg-amber-500/10 text-amber-400";
  }
}

function riskClass(risk: string) {
  switch (risk.toUpperCase()) {
    case "CRITICAL":
      return "border-red-500/30 bg-red-500/10 text-red-400";
    case "HIGH":
      return "border-orange-500/30 bg-orange-500/10 text-orange-400";
    case "MEDIUM":
      return "border-yellow-500/30 bg-yellow-500/10 text-yellow-400";
    default:
      return "border-green-500/30 bg-green-500/10 text-green-400";
  }
}

export default function FraudCaseDetailsPage() {
  const params = useParams<{ id: string }>();
  const caseId = Number(params.id);

  const [fraudCase, setFraudCase] = useState<FraudCase | null>(null);
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [status, setStatus] = useState("NEW");
  const [analyst, setAnalyst] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadCase = useCallback(async () => {
    if (!Number.isInteger(caseId) || caseId < 1) {
      setError("Invalid case ID in the URL.");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const caseResponse = await fetch(`${API_URL}/cases/${caseId}`);
      const caseData = await caseResponse.json();

      if (!caseResponse.ok) {
        throw new Error(
          caseData.detail || "Unable to load this fraud case."
        );
      }

      const loadedCase = caseData as FraudCase;

      setFraudCase(loadedCase);
      setStatus(loadedCase.status);
      setAnalyst(loadedCase.analyst ?? "");
      setNotes(loadedCase.investigation_notes ?? "");

      // A case ID and a prediction ID are different.
      // Use prediction_id to load the linked transaction.
      const transactionResponse = await fetch(
        `${API_URL}/history/${loadedCase.prediction_id}`
      );

      const transactionData = await transactionResponse.json();

      if (!transactionResponse.ok) {
        throw new Error(
          transactionData.detail ||
            "The case loaded, but its linked transaction could not be loaded."
        );
      }

      setTransaction(transactionData as Transaction);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to SentinelAI."
      );
    } finally {
      setLoading(false);
    }
  }, [caseId]);


useEffect(() => {
  const controller = new AbortController();

  async function fetchCase() {
    if (!Number.isInteger(caseId) || caseId < 1) {
      setError("Invalid case ID in the URL.");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const caseResponse = await fetch(`${API_URL}/cases/${caseId}`, {
        signal: controller.signal,
      });
      const caseData = await caseResponse.json();

      if (!caseResponse.ok) {
        throw new Error(
          caseData.detail || "Unable to load this fraud case."
        );
      }

      const loadedCase = caseData as FraudCase;

      setFraudCase(loadedCase);
      setStatus(loadedCase.status);
      setAnalyst(loadedCase.analyst ?? "");
      setNotes(loadedCase.investigation_notes ?? "");

      const transactionResponse = await fetch(
        `${API_URL}/history/${loadedCase.prediction_id}`,
        { signal: controller.signal }
      );
      const transactionData = await transactionResponse.json();

      if (!transactionResponse.ok) {
        throw new Error(
          transactionData.detail ||
            "The case loaded, but its linked transaction could not be loaded."
        );
      }

      setTransaction(transactionData as Transaction);
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") {
        return;
      }

      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to SentinelAI."
      );
    } finally {
      if (!controller.signal.aborted) {
        setLoading(false);
      }
    }
  }

  void fetchCase();

  return () => controller.abort();
}, [caseId]);


  async function saveCase() {
    if (!fraudCase) return;

    setSaving(true);
    setError("");
    setMessage("");

    try {
      const response = await fetch(
        `${API_URL}/cases/${fraudCase.case_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status,
            analyst: analyst.trim() || null,
            investigation_notes: notes.trim() || null,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to save case changes."
        );
      }

      setFraudCase(data as FraudCase);
      setStatus(data.status);
      setAnalyst(data.analyst ?? "");
      setNotes(data.investigation_notes ?? "");
      setMessage("Case changes saved successfully.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to save case changes."
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 p-6 text-white md:p-10">
        <div className="mx-auto max-w-6xl text-slate-400">
          Loading fraud case...
        </div>
      </main>
    );
  }

  if (error && !fraudCase) {
    return (
      <main className="min-h-screen bg-slate-950 p-6 text-white md:p-10">
        <div className="mx-auto max-w-6xl">
          <Link
            href="/cases"
            className="text-sm text-blue-400 hover:text-blue-300"
          >
            ← Back to Fraud Cases
          </Link>

          <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-5 text-red-300">
            {error}
          </div>
        </div>
      </main>
    );
  }

  if (!fraudCase) return null;

  const shapFactors = transaction?.shap_factors ?? [];

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-8 text-white md:px-8 md:py-10">
      <div className="mx-auto max-w-6xl">

        {/* Navigation */}
        <div className="mb-7 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap gap-4 text-sm">
            <Link
              href="/cases"
              className="text-blue-400 hover:text-blue-300"
            >
              ← Back to Fraud Cases
            </Link>

            <Link
              href={`/transaction/${fraudCase.prediction_id}`}
              className="text-blue-400 hover:text-blue-300"
            >
              Open transaction #{fraudCase.prediction_id} →
            </Link>
          </div>

          <button
            className={buttonClass}
            onClick={() => void loadCase()}
          >
            Refresh case
          </button>
        </div>

        {/* Page Header */}
        <header className="mb-8">
          <p className="text-xs font-semibold tracking-[0.2em] text-blue-400">
            SENTINELAI / INVESTIGATION WORKSPACE
          </p>

          <div className="mt-3 flex flex-wrap items-center gap-3">
            <h1 className="text-3xl font-bold md:text-4xl">
              Fraud Case #{fraudCase.case_id}
            </h1>

            <span
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${statusClass(
                fraudCase.status
              )}`}
            >
              {fraudCase.status.replace("_", " ")}
            </span>
          </div>

          <p className="mt-3 text-slate-400">
            Review the linked prediction, understand model factors, and record
            investigation progress.
          </p>
        </header>

        {/* Notifications */}
        {error && (
          <div
            role="alert"
            className="mb-5 rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300"
          >
            {error}
          </div>
        )}

        {message && (
          <div
            role="status"
            className="mb-5 rounded-lg border border-green-500/30 bg-green-500/10 p-4 text-green-300"
          >
            {message}
          </div>
        )}

        {/* Summary Cards */}
        <section className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article className={panelClass}>
            <p className="text-sm text-slate-400">Case ID</p>
            <p className="mt-2 text-2xl font-bold">
              #{fraudCase.case_id}
            </p>
          </article>

          <article className={panelClass}>
            <p className="text-sm text-slate-400">Linked prediction</p>
            <p className="mt-2 text-2xl font-bold">
              #{fraudCase.prediction_id}
            </p>
          </article>

          <article className={panelClass}>
            <p className="text-sm text-slate-400">Fraud probability</p>
            <p className="mt-2 text-2xl font-bold text-red-400">
              {transaction
                ? `${(transaction.fraud_probability * 100).toFixed(1)}%`
                : "Unavailable"}
            </p>
          </article>

          <article className={panelClass}>
            <p className="text-sm text-slate-400">Risk level</p>

            {transaction ? (
              <span
                className={`mt-2 inline-block rounded-full border px-3 py-1 text-sm font-semibold ${riskClass(
                  transaction.risk_level
                )}`}
              >
                {transaction.risk_level}
              </span>
            ) : (
              <p className="mt-2 text-slate-400">Unavailable</p>
            )}
          </article>
        </section>

        <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">

          {/* Investigation Form */}
          <section className={panelClass}>
            <h2 className="text-xl font-semibold">
              Investigation details
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Changes are saved to the local SentinelAI database.
            </p>

            <label
              className="mt-6 block text-sm font-medium text-slate-300"
              htmlFor="case-status"
            >
              Case status
            </label>

            <select
              id="case-status"
              className={fieldClass}
              value={status}
              onChange={(event) => setStatus(event.target.value)}
            >
              <option value="NEW">New</option>
              <option value="IN_PROGRESS">In progress</option>
              <option value="RESOLVED">Resolved</option>
            </select>

            <label
              className="mt-5 block text-sm font-medium text-slate-300"
              htmlFor="case-analyst"
            >
              Assigned analyst
            </label>

            <input
              id="case-analyst"
              className={fieldClass}
              value={analyst}
              maxLength={100}
              onChange={(event) => setAnalyst(event.target.value)}
              placeholder="Enter analyst name"
            />

            <label
              className="mt-5 block text-sm font-medium text-slate-300"
              htmlFor="case-notes"
            >
              Investigation notes
            </label>

            <textarea
              id="case-notes"
              className={fieldClass}
              value={notes}
              maxLength={2000}
              rows={6}
              onChange={(event) => setNotes(event.target.value)}
              placeholder="Record what was reviewed, evidence found, and next steps..."
            />

            <p className="mt-1 text-right text-xs text-slate-500">
              {notes.length}/2000 characters
            </p>

            <button
              className="mt-5 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              onClick={() => void saveCase()}
              disabled={saving}
            >
              {saving ? "Saving..." : "Save case changes"}
            </button>

            {/* Timestamps */}
            <div className="mt-6 grid gap-3 border-t border-slate-800 pt-5 text-sm sm:grid-cols-2">
              <div>
                <p className="text-slate-500">Created</p>
                <p className="mt-1 text-slate-300">
                  {new Date(fraudCase.created_at).toLocaleString()}
                </p>
              </div>

              <div>
                <p className="text-slate-500">Last updated</p>
                <p className="mt-1 text-slate-300">
                  {new Date(fraudCase.updated_at).toLocaleString()}
                </p>
              </div>
            </div>
          </section>

          {/* Transaction and SHAP Details */}
          <div className="space-y-6">

            <section className={panelClass}>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h2 className="text-xl font-semibold">
                  Transaction assessment
                </h2>

                {transaction && (
                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-semibold ${riskClass(
                      transaction.risk_level
                    )}`}
                  >
                    {transaction.prediction}
                  </span>
                )}
              </div>

              {transaction ? (
                <>
                  <div className="mt-5 grid grid-cols-2 gap-4">
                    <div className="rounded-lg bg-slate-950 p-4">
                      <p className="text-sm text-slate-400">Amount</p>
                      <p className="mt-1 text-xl font-semibold">
                        ${transaction.amount.toFixed(2)}
                      </p>
                    </div>

                    <div className="rounded-lg bg-slate-950 p-4">
                      <p className="text-sm text-slate-400">
                        Model threshold
                      </p>
                      <p className="mt-1 text-xl font-semibold">
                        {(transaction.threshold * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>

                  <h3 className="mt-5 text-sm font-semibold text-slate-300">
                    Recommended action
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-slate-400">
                    {transaction.recommended_action}
                  </p>

                  <Link
                    href={`/transaction/${fraudCase.prediction_id}`}
                    className="mt-5 inline-flex text-sm font-medium text-blue-400 hover:text-blue-300"
                  >
                    View full transaction analysis →
                  </Link>
                </>
              ) : (
                <p className="mt-4 text-sm text-slate-400">
                  The case is available, but transaction details could not be
                  loaded. Open the transaction page to investigate further.
                </p>
              )}
            </section>

            <section className={panelClass}>
              <h2 className="text-xl font-semibold">
                AI explanation · SHAP
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                SHAP values show how individual model features contributed to
                this prediction. Positive values are displayed as increasing
                fraud risk and negative values as lowering fraud risk,
                following the existing transaction page&apos;s convention.
              </p>

              {shapFactors.length > 0 ? (
                <div className="mt-5 space-y-3">
                  {shapFactors.map((factor, index) => {
                    const positive = factor.shap_value > 0;

                    return (
                      <div
                        key={`${factor.feature}-${index}`}
                        className="rounded-lg border border-slate-800 bg-slate-950 p-3"
                      >
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className="font-medium">
                            {factor.feature}
                          </span>

                          <span
                            className={`font-mono text-sm ${
                              positive ? "text-red-400" : "text-blue-400"
                            }`}
                          >
                            {positive ? "+" : ""}
                            {factor.shap_value.toFixed(6)}
                          </span>
                        </div>

                        <p
                          className={`mt-1 text-xs ${
                            positive ? "text-red-400" : "text-blue-400"
                          }`}
                        >
                          {positive
                            ? "↑ Increased fraud risk"
                            : "↓ Lowered fraud risk"}
                        </p>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="mt-5 rounded-lg bg-slate-950 p-4 text-sm text-slate-500">
                  SHAP explanation is not available for this transaction.
                </p>
              )}

              <p className="mt-4 text-xs leading-5 text-slate-500">
                Model explanations are decision-support information, not proof
                of fraud. Review the transaction and supporting evidence before
                resolving a case.
              </p>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
