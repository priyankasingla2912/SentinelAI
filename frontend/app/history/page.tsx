"use client";

import { useEffect, useState } from "react";

type Transaction = {
  id: number;
  amount: number;
  fraud_probability: number;
  threshold: number;
  prediction: string;
  risk_level: string;
  recommended_action: string;
  created_at: string;
};

export default function HistoryPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedRisk, setSelectedRisk] = useState("ALL");
  const [selectedPrediction, setSelectedPrediction] = useState("ALL");

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/history?limit=50"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch transaction history");
        }

        const data = await response.json();

        setTransactions(data.predictions);
      } catch (error) {
        console.error("History error:", error);

        setError(
          "Unable to load transaction history. Please make sure the backend is running."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

    useEffect(() => {
    setCurrentPage(1);
  }, [selectedRisk, selectedPrediction]);

const filteredTransactions = transactions.filter((transaction) => {
    const riskMatches =
      selectedRisk === "ALL" ||
      transaction.risk_level === selectedRisk;

    const predictionMatches =
      selectedPrediction === "ALL" ||
      transaction.prediction === selectedPrediction;

    return riskMatches && predictionMatches;
  });

  const totalPages = Math.ceil(
  filteredTransactions.length / itemsPerPage
);

const startIndex = (currentPage - 1) * itemsPerPage;

const paginatedTransactions = filteredTransactions.slice(
  startIndex,
  startIndex + itemsPerPage
);

  
  const getRiskClass = (risk: string) => {
    switch (risk) {
      case "CRITICAL":
        return "bg-red-500/10 text-red-400";
      case "HIGH":
        return "bg-orange-500/10 text-orange-400";
      case "MEDIUM":
        return "bg-yellow-500/10 text-yellow-400";
      default:
        return "bg-green-500/10 text-green-400";
    }
  };

  const getPredictionClass = (prediction: string) => {
    return prediction === "FRAUD"
      ? "text-red-400"
      : "text-green-400";
  };

  return (
    <main className="min-h-screen bg-slate-950 p-10 text-white">
      <div className="mx-auto max-w-7xl">

        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Transaction History
          </h1>

          <p className="mt-3 text-slate-400">
            View transactions previously analyzed by SentinelAI.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 rounded-xl border border-red-500/30 bg-red-500/10 p-5 text-red-400">
            {error}
          </div>
        )}

        {/* History Table */}
        <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">

          <div className="border-b border-slate-800 p-6">
            <h2 className="text-xl font-semibold">
              Analyzed Transactions
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Latest transactions are shown first.
            </p>
            <div className="mt-5 flex flex-wrap gap-2">
  {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map(
    (risk) => (
      <button
        key={risk}
        type="button"
        onClick={() => setSelectedRisk(risk)}
        className={`rounded-lg px-3 py-2 text-xs font-medium transition ${
          selectedRisk === risk
            ? "bg-blue-600 text-white"
            : "border border-slate-700 text-slate-400 hover:bg-slate-800"
        }`}
      >
        {risk === "ALL"
          ? "All Risks"
          : risk.charAt(0) + risk.slice(1).toLowerCase()}
      </button>
    )
  )}
</div>

<div className="mt-3 flex flex-wrap gap-2">
  {["ALL", "FRAUD", "LEGITIMATE"].map(
    (prediction) => (
      <button
        key={prediction}
        type="button"
        onClick={() => setSelectedPrediction(prediction)}
        className={`rounded-lg px-3 py-2 text-xs font-medium transition ${
          selectedPrediction === prediction
            ? "bg-blue-600 text-white"
            : "border border-slate-700 text-slate-400 hover:bg-slate-800"
        }`}
      >
        {prediction === "ALL"
          ? "All Predictions"
          : prediction.charAt(0) +
            prediction.slice(1).toLowerCase()}
      </button>
    )
  )}
</div>
<div className="mt-4">
  <button
    type="button"
    onClick={() => {
      setSelectedRisk("ALL");
      setSelectedPrediction("ALL");
      setCurrentPage(1);
    }}
    className="rounded-lg border border-slate-700 px-3 py-2 text-xs font-medium text-slate-400 transition hover:bg-slate-800 hover:text-white"
  >
    Clear Filters
  </button>
</div>
          </div>

          {loading ? (
            <div className="p-10 text-center text-slate-400">
              Loading transaction history...
            </div>
          ) : transactions.length === 0 ? (
            <div className="p-10 text-center text-slate-400">
              No transactions have been analyzed yet.
            </div>
            ) : filteredTransactions.length === 0 ? (
  <div className="p-10 text-center text-slate-400">
    No transactions match the selected filters.
  </div>
          ) : (
            <div className="overflow-x-auto">

              <table className="w-full text-left">

                <thead className="border-b border-slate-800 bg-slate-950/50">
                  <tr>
                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      ID
                    </th>

                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      Amount
                    </th>

                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      Probability
                    </th>

                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      Prediction
                    </th>

                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      Risk
                    </th>

                    <th className="px-6 py-4 text-sm font-medium text-slate-400">
                      Date
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {paginatedTransactions.map((transaction) => (
                    <tr
                      key={transaction.id}
                      onClick={() =>
                        (window.location.href = `/transaction/${transaction.id}`)
    }
                      className="cursor-pointer border-b border-slate-800 transition hover:bg-slate-800/60"
                    >

                      <td className="px-6 py-4 font-medium">
                        #{transaction.id}
                      </td>

                      <td className="px-6 py-4">
                        ${transaction.amount.toFixed(2)}
                      </td>

                      <td className="px-6 py-4">
                        {(transaction.fraud_probability * 100).toFixed(1)}%
                      </td>

                      <td
                        className={`px-6 py-4 font-medium ${getPredictionClass(
                          transaction.prediction
                        )}`}
                      >
                        {transaction.prediction}
                      </td>

                      <td className="px-6 py-4">
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${getRiskClass(
                            transaction.risk_level
                          )}`}
                        >
                          {transaction.risk_level}
                        </span>
                      </td>

                      <td className="px-6 py-4 text-sm text-slate-400">
                        {new Date(
                          transaction.created_at
                        ).toLocaleString()}
                      </td>

                    </tr>
                  ))}
                </tbody>

              </table>
              {/* Pagination Controls */}
              <div className="flex items-center justify-between border-t border-slate-800 px-6 py-4">

                <button
                  type="button"
                  onClick={() => setCurrentPage((page) => page - 1)}
                  disabled={currentPage === 1}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Previous
                </button>

                <span className="text-sm text-slate-400">
                  Page {currentPage} of {totalPages}
                </span>

                <button
                  type="button"
                  onClick={() => setCurrentPage((page) => page + 1)}
                  disabled={currentPage === totalPages}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Next
                </button>

              </div>

            </div>
          )}
          </div>

      </div>
    </main>
  );
}