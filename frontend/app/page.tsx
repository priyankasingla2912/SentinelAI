"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

type DashboardStats = {
  total_transactions: number;
  fraud_transactions: number;
  legitimate_transactions: number;
  fraud_rate: number;
  risk_distribution: Record<RiskLevel, number>;
};

type TransactionRecord = {
  id: number;
  amount: number;
  fraud_probability: number;
  threshold: number;
  prediction: string;
  risk_level: RiskLevel;
  recommended_action: string;
  created_at: string;
};

type FraudCase = {
  case_id: number;
  prediction_id: number;
  status: string;
  analyst: string | null;
  investigation_notes: string | null;
  created_at: string;
  updated_at: string;
};

const API_BASE_URL = "http://127.0.0.1:8001";

const initialStats: DashboardStats = {
  total_transactions: 0,
  fraud_transactions: 0,
  legitimate_transactions: 0,
  fraud_rate: 0,
  risk_distribution: {
    LOW: 0,
    MEDIUM: 0,
    HIGH: 0,
    CRITICAL: 0,
  },
};

export default function Home() {
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [stats, setStats] = useState<DashboardStats>(initialStats);
  const [transactions, setTransactions] = useState<TransactionRecord[]>([]);
  const [chartTransactions, setChartTransactions] = useState<TransactionRecord[]>([]);
  const [selectedRisk, setSelectedRisk] = useState("ALL");
  const [fraudCases, setFraudCases] = useState<FraudCase[]>([]);
  const [casesError, setCasesError] = useState("");
  const [dashboardError, setDashboardError] = useState("");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchDashboardData = useCallback(async () => {
    setApiStatus("Checking...");
    setDashboardError("");
    setIsRefreshing(true);

    // Load dashboard statistics and transaction history.
    try {
      const [statsResponse, historyResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/stats`),
        fetch(`${API_BASE_URL}/history?limit=100`),
      ]);

      if (!statsResponse.ok) {
        throw new Error("Failed to fetch dashboard statistics");
      }

      if (!historyResponse.ok) {
        throw new Error("Failed to fetch transaction history");
      }

      const statsData: DashboardStats = await statsResponse.json();
      const historyData: { count: number; predictions: TransactionRecord[] } =
        await historyResponse.json();

      setStats(statsData);
      setTransactions(historyData.predictions.slice(0, 5));
      setChartTransactions(historyData.predictions);
      setApiStatus("Online");
    } catch (error) {
      console.error("Dashboard error:", error);
      setApiStatus("Offline");
      setDashboardError(
        "Unable to load dashboard data. Check that the FastAPI backend is running."
      );
    }

    // Load cases separately so a cases request failure does not mark the
    // otherwise-working statistics/history API as offline.
    try {
      const casesResponse = await fetch(`${API_BASE_URL}/cases?limit=5`);

      if (!casesResponse.ok) {
        throw new Error("Failed to fetch fraud cases");
      }

      const casesData: { count: number; cases: FraudCase[] } =
        await casesResponse.json();

      setFraudCases(casesData.cases);
      setCasesError("");
    } catch (error) {
      console.error("Fraud cases error:", error);
      setCasesError("Unable to load fraud cases. Please try again.");
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void fetchDashboardData();
  }, [fetchDashboardData]);


  const chartWidth = 760;
  const chartHeight = 320;
  const chartPadding = { top: 20, right: 25, bottom: 55, left: 65 };

  const plotWidth = chartWidth - chartPadding.left - chartPadding.right;
  const plotHeight = chartHeight - chartPadding.top - chartPadding.bottom;

  const maxAmount = Math.max(
    100,
    ...chartTransactions.map((transaction) => transaction.amount)
  );

  const amountAxisMax = Math.ceil(maxAmount / 100) * 100;

  const getPointX = (amount: number) =>
    chartPadding.left + (amount / amountAxisMax) * plotWidth;

  const getPointY = (probability: number) =>
    chartPadding.top + (1 - probability) * plotHeight;

  const fraudCount = chartTransactions.filter(
    (transaction) => transaction.prediction === "FRAUD"
  ).length;

  const legitimateCount = chartTransactions.length - fraudCount;

  const filteredTransactions =
    selectedRisk === "ALL"
      ? transactions
      : transactions.filter(
          (transaction) => transaction.risk_level === selectedRisk
        );

  const riskLevels = [
    {
      key: "CRITICAL" as RiskLevel,
      label: "Critical",
      countClass: "text-red-400",
      barClass: "bg-red-500",
    },
    {
      key: "HIGH" as RiskLevel,
      label: "High",
      countClass: "text-orange-400",
      barClass: "bg-orange-500",
    },
    {
      key: "MEDIUM" as RiskLevel,
      label: "Medium",
      countClass: "text-yellow-400",
      barClass: "bg-yellow-500",
    },
    {
      key: "LOW" as RiskLevel,
      label: "Low",
      countClass: "text-green-400",
      barClass: "bg-green-500",
    },
  ];

  const riskBadgeClass = (risk: string) => {
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

  const caseStatusClass = (status: string) => {
    switch (status) {
      case "RESOLVED":
        return "bg-green-500/10 text-green-400";
      case "IN_PROGRESS":
        return "bg-blue-500/10 text-blue-300";
      default:
        return "bg-amber-500/10 text-amber-300";
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">SentinelAI</h1>
            <p className="text-sm text-slate-400">
              Fraud &amp; Risk Intelligence Platform
            </p>
          </div>

          <div className="flex items-center gap-2">
            <div
              className={`h-2.5 w-2.5 rounded-full ${
                apiStatus === "Online"
                  ? "bg-green-400"
                  : apiStatus === "Offline"
                    ? "bg-red-400"
                    : "bg-yellow-400"
              }`}
            />
            <span className="text-sm text-slate-300">API {apiStatus}</span>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Fraud Intelligence Dashboard</h2>
          <p className="mt-2 text-slate-400">
            Monitor transaction risk and AI-powered fraud detection.
          </p>
        </div>

        {dashboardError && (
          <div
            role="alert"
            className="mb-6 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300"
          >
            {dashboardError}
          </div>
        )}

        {/* KPI cards */}
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">Total Transactions</p>
            <p className="mt-3 text-3xl font-bold">
              {stats.total_transactions}
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Transactions analyzed
            </p>
          </div>

          <div className="rounded-xl border border-red-900/50 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">Fraud Detected</p>
            <p className="mt-3 text-3xl font-bold text-red-400">
              {stats.fraud_transactions}
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Flagged transactions
            </p>
          </div>

          <div className="rounded-xl border border-amber-900/50 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">Fraud Rate</p>
            <p className="mt-3 text-3xl font-bold text-amber-400">
              {stats.fraud_rate}%
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Based on analyzed transactions
            </p>
          </div>

          <div className="rounded-xl border border-purple-900/50 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">Critical Risk</p>
            <p className="mt-3 text-3xl font-bold text-purple-400">
              {stats.risk_distribution.CRITICAL}
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Require immediate review
            </p>
          </div>
        </div>

        {/* Risk distribution and recent transactions */}

        {/* Transaction Amount vs Fraud Probability */}
        <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h3 className="text-lg font-semibold">
                Transaction Risk Analysis
              </h3>
              <p className="mt-1 text-sm text-slate-400">
                Transaction amount compared with predicted fraud probability
              </p>
            </div>

            <div className="flex flex-wrap gap-4 text-sm">
              <span className="flex items-center gap-2 text-slate-300">
                <span className="h-3 w-3 rounded-full bg-red-400" />
                Fraud ({fraudCount})
              </span>
              <span className="flex items-center gap-2 text-slate-300">
                <span className="h-3 w-3 rounded-full bg-green-400" />
                Legitimate ({legitimateCount})
              </span>
            </div>
          </div>

          {chartTransactions.length === 0 ? (
            <p className="py-12 text-center text-sm text-slate-400">
              No transaction data available for the chart.
            </p>
          ) : (
            <div className="mt-6 w-full overflow-x-auto">
              <svg
                viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                role="img"
                aria-label="Scatter plot of transaction amount against fraud probability"
                className="w-full min-w-[520px]"
              >
                {[0, 25, 50, 75, 100].map((value) => {
                  const y = getPointY(value / 100);

                  return (
                    <g key={value}>
                      <line
                        x1={chartPadding.left}
                        y1={y}
                        x2={chartWidth - chartPadding.right}
                        y2={y}
                        stroke="#334155"
                        strokeDasharray="4 4"
                      />
                      <text
                        x={chartPadding.left - 12}
                        y={y + 4}
                        textAnchor="end"
                        fill="#94a3b8"
                        fontSize="12"
                      >
                        {value}%
                      </text>
                    </g>
                  );
                })}

                {[0, 0.25, 0.5, 0.75, 1].map((fraction) => {
                  const amount = amountAxisMax * fraction;
                  const x = getPointX(amount);

                  return (
                    <g key={fraction}>
                      <line
                        x1={x}
                        y1={chartPadding.top}
                        x2={x}
                        y2={chartHeight - chartPadding.bottom}
                        stroke="#1e293b"
                      />
                      <text
                        x={x}
                        y={chartHeight - chartPadding.bottom + 22}
                        textAnchor="middle"
                        fill="#94a3b8"
                        fontSize="12"
                      >
                        ${Math.round(amount)}
                      </text>
                    </g>
                  );
                })}

                <line
                  x1={chartPadding.left}
                  y1={chartPadding.top}
                  x2={chartPadding.left}
                  y2={chartHeight - chartPadding.bottom}
                  stroke="#64748b"
                />

                <line
                  x1={chartPadding.left}
                  y1={chartHeight - chartPadding.bottom}
                  x2={chartWidth - chartPadding.right}
                  y2={chartHeight - chartPadding.bottom}
                  stroke="#64748b"
                />

                <text
                  x={chartPadding.left + plotWidth / 2}
                  y={chartHeight - 8}
                  textAnchor="middle"
                  fill="#cbd5e1"
                  fontSize="13"
                >
                  Transaction Amount ($)
                </text>

                <text
                  transform={`translate(18 ${
                    chartPadding.top + plotHeight / 2
                  }) rotate(-90)`}
                  textAnchor="middle"
                  fill="#cbd5e1"
                  fontSize="13"
                >
                  Fraud Probability
                </text>

                {chartTransactions.map((transaction) => (
                  <circle
                    key={transaction.id}
                    cx={getPointX(transaction.amount)}
                    cy={getPointY(transaction.fraud_probability)}
                    r={5}
                    fill={
                      transaction.prediction === "FRAUD"
                        ? "#f87171"
                        : "#4ade80"
                    }
                    fillOpacity={0.85}
                    stroke="#0f172a"
                    strokeWidth={1}
                  >
                    <title>
                      {`Transaction #${transaction.id} | Amount: $${transaction.amount.toFixed(
                        2
                      )} | Fraud probability: ${(
                        transaction.fraud_probability * 100
                      ).toFixed(1)}% | Prediction: ${transaction.prediction}`}
                    </title>
                  </circle>
                ))}
              </svg>
            </div>
          )}

          <p className="mt-3 text-xs text-slate-500">
            Each dot represents one saved prediction. Hover over a dot to see
            its transaction details. The chart displays up to 100 recent
            predictions.
          </p>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-1">
            <h3 className="text-lg font-semibold">Risk Distribution</h3>
            <p className="mt-1 text-sm text-slate-400">
              Current transaction risk levels
            </p>

            <div className="mt-6 space-y-5">
              {riskLevels.map((risk) => {
                const count = stats.risk_distribution[risk.key] ?? 0;
                const percentage =
                  stats.total_transactions > 0
                    ? Math.min(
                        100,
                        (count / stats.total_transactions) * 100
                      )
                    : 0;

                return (
                  <div key={risk.key}>
                    <div className="mb-2 flex justify-between text-sm">
                      <span>{risk.label}</span>
                      <span className={risk.countClass}>{count}</span>
                    </div>
                    <div
                      className="h-2 rounded-full bg-slate-800"
                      role="progressbar"
                      aria-label={`${risk.label} risk distribution`}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-valuenow={Math.round(percentage)}
                    >
                      <div
                        className={`h-2 rounded-full ${risk.barClass}`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-2">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold">Recent Transactions</h3>
                <p className="mt-1 text-sm text-slate-400">
                  Latest AI fraud predictions
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => void fetchDashboardData()}
                  disabled={isRefreshing}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isRefreshing ? "Refreshing..." : "Refresh"}
                </button>
                <Link
                  href="/history"
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800"
                >
                  View All
                </Link>
              </div>
            </div>

            <div className="mt-5 flex flex-wrap gap-2">
              {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map((risk) => (
                <button
                  key={risk}
                  type="button"
                  onClick={() => setSelectedRisk(risk)}
                  aria-pressed={selectedRisk === risk}
                  className={`rounded-lg px-3 py-2 text-xs font-medium transition ${
                    selectedRisk === risk
                      ? "bg-blue-600 text-white"
                      : "border border-slate-700 text-slate-400 hover:bg-slate-800"
                  }`}
                >
                  {risk === "ALL"
                    ? "All"
                    : risk.charAt(0) + risk.slice(1).toLowerCase()}
                </button>
              ))}
            </div>

            <div className="mt-6 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-800 text-slate-400">
                  <tr>
                    <th scope="col" className="px-3 py-3">ID</th>
                    <th scope="col" className="px-3 py-3">Amount</th>
                    <th scope="col" className="px-3 py-3">Probability</th>
                    <th scope="col" className="px-3 py-3">Prediction</th>
                    <th scope="col" className="px-3 py-3">Risk</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTransactions.map((transaction) => (
                    <tr
                      key={transaction.id}
                      onClick={() => {
                        window.location.href = `/transaction/${transaction.id}`;
                      }}
                      onKeyDown={(event) => {
                        if (event.key === "Enter") {
                          window.location.href = `/transaction/${transaction.id}`;
                        }
                      }}
                      tabIndex={0}
                      className="cursor-pointer border-b border-slate-800 transition hover:bg-slate-800/60 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <td className="px-3 py-4">#{transaction.id}</td>
                      <td className="px-3 py-4">
                        ${transaction.amount.toFixed(2)}
                      </td>
                      <td className="px-3 py-4">
                        {(transaction.fraud_probability * 100).toFixed(0)}%
                      </td>
                      <td
                        className={`px-3 py-4 ${
                          transaction.prediction === "FRAUD"
                            ? "text-red-400"
                            : "text-green-400"
                        }`}
                      >
                        {transaction.prediction}
                      </td>
                      <td className="px-3 py-4">
                        <span
                          className={`rounded-full px-3 py-1 text-xs ${riskBadgeClass(
                            transaction.risk_level
                          )}`}
                        >
                          {transaction.risk_level}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {filteredTransactions.length === 0 && (
                    <tr>
                      <td
                        colSpan={5}
                        className="px-3 py-8 text-center text-slate-400"
                      >
                        No transactions found for this risk level.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Recent fraud cases */}
        <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-5">
            <h3 className="text-lg font-semibold">Recent Fraud Cases</h3>
            <p className="mt-1 text-sm text-slate-400">
              Review flagged transactions and investigation progress.
            </p>
          </div>
          {casesError ? (
  <div role="alert" className="text-sm text-red-400">
    {casesError}
  </div>
) : fraudCases.length === 0 ? (
  <p className="text-sm text-slate-400">
    No fraud cases found.
  </p>
) : (
  <div className="overflow-x-auto">
    <table className="w-full text-left text-sm">
      <thead className="border-b border-slate-800 text-slate-400">
        <tr>
          <th scope="col" className="px-3 py-3">
            Case ID
          </th>
          <th scope="col" className="px-3 py-3">
            Prediction ID
          </th>
          <th scope="col" className="px-3 py-3">
            Status
          </th>
          <th scope="col" className="px-3 py-3">
            Analyst
          </th>
          <th scope="col" className="px-3 py-3">
            Investigation Notes
          </th>
          <th scope="col" className="px-3 py-3">
            Action
          </th>
        </tr>
      </thead>

      <tbody>
        {fraudCases.map((fraudCase) => (
          <tr
            key={fraudCase.case_id}
            className="border-b border-slate-800 align-top"
          >
            <td className="px-3 py-4">
              <Link
                href={`/cases/${fraudCase.case_id}`}
                className="font-semibold text-blue-400 hover:text-blue-300 hover:underline"
              >
                #{fraudCase.case_id}
              </Link>
            </td>

            <td className="px-3 py-4">
              #{fraudCase.prediction_id}
            </td>

            <td className="px-3 py-4">
              <span
                className={`rounded-full px-3 py-1 text-xs ${caseStatusClass(
                  fraudCase.status
                )}`}
              >
                {fraudCase.status.replaceAll("_", " ")}
              </span>
            </td>

            <td className="px-3 py-4">
              {fraudCase.analyst || "Unassigned"}
            </td>

            <td className="max-w-sm whitespace-pre-wrap px-3 py-4 text-slate-400">
              {fraudCase.investigation_notes || "No notes"}
            </td>

            <td className="px-3 py-4">
              <Link
                href={`/cases/${fraudCase.case_id}`}
                className="inline-flex whitespace-nowrap rounded-lg border border-blue-500/40 px-3 py-2 text-xs font-medium text-blue-400 transition hover:bg-blue-500/10"
              >
                Investigate →
              </Link>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
        </div>
      </section>
    </main>
  );
}