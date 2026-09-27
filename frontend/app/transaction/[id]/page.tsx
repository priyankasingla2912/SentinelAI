"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

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

export default function TransactionDetailsPage() {
  const params = useParams();
  const id = params.id;

  const [transaction, setTransaction] =
    useState<Transaction | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTransaction = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/history/${id}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch transaction");
        }

        const data = await response.json();

        if (data.error) {
          throw new Error(data.error);
        }

        setTransaction(data);
      } catch (error) {
        console.error("Transaction details error:", error);

        setError(
          "Unable to load transaction details."
        );
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchTransaction();
    }
  }, [id]);

  const getRiskClass = (risk: string) => {
    switch (risk) {
      case "CRITICAL":
        return "bg-red-500/10 text-red-400 border-red-500/20";

      case "HIGH":
        return "bg-orange-500/10 text-orange-400 border-orange-500/20";

      case "MEDIUM":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20";

      default:
        return "bg-green-500/10 text-green-400 border-green-500/20";
    }
  };

  const getPredictionClass = (prediction: string) => {
    return prediction === "FRAUD"
      ? "text-red-400"
      : "text-green-400";
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 p-10 text-white">
        <div className="mx-auto max-w-6xl">
          <p className="text-slate-400">
            Loading transaction details...
          </p>
        </div>
      </main>
    );
  }

  if (error || !transaction) {
    return (
      <main className="min-h-screen bg-slate-950 p-10 text-white">
        <div className="mx-auto max-w-6xl">

          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-red-400">
            {error || "Transaction not found."}
          </div>

          <Link
            href="/history"
            className="mt-6 inline-block text-blue-400 hover:text-blue-300"
          >
            ← Back to History
          </Link>

        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 p-10 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Back Button */}
        <Link
          href="/history"
          className="mb-6 inline-block text-sm text-blue-400 hover:text-blue-300"
        >
          ← Back to History
        </Link>

        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Transaction #{transaction.id}
          </h1>

          <p className="mt-3 text-slate-400">
            Detailed fraud risk analysis and model explanation.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid gap-4 md:grid-cols-4">

          {/* Amount */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">
              Transaction Amount
            </p>

            <p className="mt-2 text-2xl font-bold">
              ${transaction.amount.toFixed(2)}
            </p>
          </div>

          {/* Fraud Probability */}
          
<div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
  <p className="text-sm text-slate-400">
    Fraud Probability
  </p>

  <p className="mt-2 text-2xl font-bold text-red-400">
    {(transaction.fraud_probability * 100).toFixed(1)}%
  </p>

  {/* Probability Bar */}
  <div className="mt-4">
    <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
      <div
        className="h-full rounded-full bg-red-500 transition-all"
        style={{
          width: `${transaction.fraud_probability * 100}%`,
        }}
      />
    </div>

    <div className="mt-2 flex justify-between text-xs text-slate-500">
      <span>0%</span>
      <span>100%</span>
    </div>
  </div>
</div>

{/* Prediction */}
<div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
  <p className="text-sm text-slate-400">
    Prediction
  </p>

  <p
    className={`mt-2 text-2xl font-bold ${getPredictionClass(
      transaction.prediction
    )}`}
  >
    {transaction.prediction}
  </p>
</div>

          {/* Risk Level */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">
              Risk Level
            </p>

            <span
              className={`mt-2 inline-block rounded-full border px-3 py-1 text-sm font-medium ${getRiskClass(
                transaction.risk_level
              )}`}
            >
              {transaction.risk_level}
            </span>
          </div>

        </div>

        {/* Recommended Action */}
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

          <h2 className="text-xl font-semibold">
            Recommended Action
          </h2>

          <p className="mt-3 text-slate-300">
            {transaction.recommended_action}
          </p>

        </div>

        {/* SHAP Explanation */}
        
<div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

  <h2 className="text-xl font-semibold">
    Top Risk Factors
  </h2>

  <p className="mt-2 text-sm text-slate-400">
    SHAP values explain how each feature influenced the fraud prediction.
  </p>

  {/* SHAP Legend */}
  <div className="mt-4 flex flex-wrap gap-4 text-sm">

    <div className="flex items-center gap-2">
      <span className="text-red-400 font-semibold">
        ↑
      </span>

      <span className="text-slate-400">
        Increased fraud risk
      </span>
    </div>

    <div className="flex items-center gap-2">
      <span className="text-blue-400 font-semibold">
        ↓
      </span>

      <span className="text-slate-400">
        Lowered fraud risk
      </span>
    </div>

  </div>

  {transaction.shap_factors &&
  transaction.shap_factors.length > 0 ? (

    <div className="mt-6">

      {/* Table Header */}
      <div className="grid grid-cols-3 border-b border-slate-800 px-4 pb-3 text-sm font-medium text-slate-400">

        <span>
          Feature
        </span>

        <span>
          Impact
        </span>

        <span className="text-right">
          SHAP Value
        </span>

      </div>

      {/* SHAP Rows */}
      <div className="divide-y divide-slate-800">

        {transaction.shap_factors.map(
          (factor, index) => {

            const increasedFraudRisk =
              factor.shap_value > 0;

            return (
              <div
                key={index}
                className="grid grid-cols-3 items-center px-4 py-4"
              >

                {/* Feature */}
                <div>
                  <p className="font-medium">
                    {factor.feature}
                  </p>
                </div>

                {/* Impact */}
                <div className="flex items-center gap-2">

                  <span
                    className={
                      increasedFraudRisk
                        ? "font-semibold text-red-400"
                        : "font-semibold text-blue-400"
                    }
                  >
                    {increasedFraudRisk ? "↑" : "↓"}
                  </span>

                  <span
                    className={
                      increasedFraudRisk
                        ? "text-sm text-red-400"
                        : "text-sm text-blue-400"
                    }
                  >
                    {increasedFraudRisk
                      ? "Increased fraud risk"
                      : "Lowered fraud risk"}
                  </span>

                </div>

                {/* SHAP Value */}
                <div className="text-right">

                  <span
                    className={
                      increasedFraudRisk
                        ? "font-mono font-semibold text-red-400"
                        : "font-mono font-semibold text-blue-400"
                    }
                  >
                    {increasedFraudRisk ? "+" : ""}
                    {factor.shap_value.toFixed(6)}
                  </span>

                </div>

              </div>
            );
          }
        )}

      </div>

    </div>

  ) : (

    <p className="mt-6 text-slate-500">
      SHAP explanation is not available for this transaction.
    </p>

  )}

</div>

        {/* Transaction Metadata */}
        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

          <h2 className="text-xl font-semibold">
            Transaction Information
          </h2>

          <div className="mt-4 grid gap-4 md:grid-cols-2">

            <div>
              <p className="text-sm text-slate-400">
                Model Threshold
              </p>

              <p className="mt-1 font-medium">
                {(transaction.threshold * 100).toFixed(0)}%
              </p>
            </div>

            <div>
              <p className="text-sm text-slate-400">
                Analyzed At
              </p>

              <p className="mt-1 font-medium">
                {new Date(
                  transaction.created_at
                ).toLocaleString()}
              </p>
            </div>

          </div>

        </div>

      </div>
    </main>
  );
}