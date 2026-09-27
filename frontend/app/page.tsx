"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
export default function Home() {
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [stats, setStats] = useState({
    
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
  });
  const [transactions, setTransactions] = useState<
  {
    id: number;
    amount: number;
    fraud_probability: number;
    threshold: number;
    prediction: string;
    risk_level: string;
    recommended_action: string;
    created_at: string;
  }[]
>([]);
const [selectedRisk, setSelectedRisk] = useState("ALL");

  const fetchDashboardData = async () => {
    try {
      setApiStatus("Checking...");

      // Fetch dashboard statistics
      const statsResponse = await fetch(
        "http://127.0.0.1:8000/stats"
      );

      if (!statsResponse.ok) {
        throw new Error("Failed to fetch dashboard statistics");
      }

      const statsData = await statsResponse.json();

      setStats(statsData);

      // Fetch recent transactions
      const historyResponse = await fetch(
        "http://127.0.0.1:8000/history?limit=5"
      );

      if (!historyResponse.ok) {
        throw new Error("Failed to fetch transaction history");
      }

      const historyData = await historyResponse.json();

      setTransactions(historyData.predictions);

      setApiStatus("Online");
    } catch (error) {
      console.error("Dashboard error:", error);
      setApiStatus("Offline");
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);
  const filteredTransactions =
    selectedRisk === "ALL"
      ? transactions
      : transactions.filter(
          (transaction) =>
            transaction.risk_level === selectedRisk
        );

 


  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              SentinelAI
            </h1>

            <p className="text-sm text-slate-400">
              Fraud & Risk Intelligence Platform
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
></div>

<span className="text-sm text-slate-300">
  API {apiStatus}
</span>
            
          </div>

        </div>
      </header>


      {/* Dashboard */}
      <section className="mx-auto max-w-7xl px-6 py-8">

        {/* Dashboard Header */}
        <div className="mb-8">

          <h2 className="text-3xl font-bold">
            Fraud Intelligence Dashboard
          </h2>

          <p className="mt-2 text-slate-400">
            Monitor transaction risk and AI-powered fraud detection.
          </p>

        </div>


        {/* KPI Cards */}
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">

          {/* Total Transactions */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

            <p className="text-sm text-slate-400">
              Total Transactions
            </p>

            <p className="mt-3 text-3xl font-bold">
              {stats.total_transactions}
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Transactions analyzed
            </p>

          </div>


          {/* Fraud Detected */}
          <div className="rounded-xl border border-red-900/50 bg-slate-900 p-6">

            <p className="text-sm text-slate-400">
              Fraud Detected
            </p>

            <p className="mt-3 text-3xl font-bold text-red-400">
              {stats.fraud_transactions}
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Flagged transactions
            </p>

          </div>


          {/* Fraud Rate */}
          <div className="rounded-xl border border-amber-900/50 bg-slate-900 p-6">

            <p className="text-sm text-slate-400">
              Fraud Rate
            </p>

            <p className="mt-3 text-3xl font-bold text-amber-400">
              {stats.fraud_rate}%
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Based on analyzed transactions
            </p>

          </div>


          {/* Critical Risk */}
          <div className="rounded-xl border border-purple-900/50 bg-slate-900 p-6">

            <p className="text-sm text-slate-400">
              Critical Risk
            </p>

            <p className="mt-3 text-3xl font-bold text-purple-400">
              {stats.risk_distribution.CRITICAL}
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Require immediate review
            </p>

          </div>

        </div>


        {/* Main Dashboard */}
        <div className="mt-8 grid gap-6 lg:grid-cols-3">


          {/* Risk Distribution */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-1">

            <h3 className="text-lg font-semibold">
              Risk Distribution
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              Current transaction risk levels
            </p>


            <div className="mt-6 space-y-5">


              {/* Critical */}
              <div>

                <div className="mb-2 flex justify-between text-sm">

                  <span>
                    Critical
                  </span>

                  <span className="text-red-400">
                    {stats.risk_distribution.CRITICAL}
                  </span>

                </div>


                <div className="h-2 rounded-full bg-slate-800">

                  <div
                    className="h-2 rounded-full bg-red-500"
                    style={{
                      width: `${
                        stats.total_transactions > 0
                          ? (stats.risk_distribution.CRITICAL /
                              stats.total_transactions) *
                            100
                          : 0
                      }%`,
                    }}
                  ></div>

                </div>

              </div>


              {/* High */}
              <div>

                <div className="mb-2 flex justify-between text-sm">

                  <span>
                    High
                  </span>

                  <span className="text-orange-400">
                    {stats.risk_distribution.HIGH}
                  </span>

                </div>


                <div className="h-2 rounded-full bg-slate-800">

                  <div
                    className="h-2 rounded-full bg-orange-500"
                    style={{
                      width: `${
                        stats.total_transactions > 0
                          ? (stats.risk_distribution.HIGH /
                              stats.total_transactions) *
                            100
                          : 0
                      }%`,
                    }}
                  ></div>

                </div>

              </div>


              {/* Medium */}
              <div>

                <div className="mb-2 flex justify-between text-sm">

                  <span>
                    Medium
                  </span>

                  <span className="text-yellow-400">
                    {stats.risk_distribution.MEDIUM}
                  </span>

                </div>


                <div className="h-2 rounded-full bg-slate-800">

                  <div
                    className="h-2 rounded-full bg-yellow-500"
                    style={{
                      width: `${
                        stats.total_transactions > 0
                          ? (stats.risk_distribution.MEDIUM /
                              stats.total_transactions) *
                            100
                          : 0
                      }%`,
                    }}
                  ></div>

                </div>

              </div>


              {/* Low */}
              <div>

                <div className="mb-2 flex justify-between text-sm">

                  <span>
                    Low
                  </span>

                  <span className="text-green-400">
                    {stats.risk_distribution.LOW}
                  </span>

                </div>


                <div className="h-2 rounded-full bg-slate-800">

                  <div
                    className="h-2 rounded-full bg-green-500"
                    style={{
                      width: `${
                        stats.total_transactions > 0
                          ? (stats.risk_distribution.LOW /
                              stats.total_transactions) *
                            100
                          : 0
                      }%`,
                    }}
                  ></div>

                </div>

              </div>


            </div>

          </div>


          {/* Recent Transactions */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-2">

            <div className="flex items-center justify-between">

  <div>

    <h3 className="text-lg font-semibold">
      Recent Transactions
    </h3>

    <p className="mt-1 text-sm text-slate-400">
      Latest AI fraud predictions
    </p>

  </div>

  <div className="flex items-center gap-2">

    <button
      type="button"
      onClick={fetchDashboardData}
      className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800"
    >
      Refresh
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
          ? "All"
          : risk.charAt(0) + risk.slice(1).toLowerCase()}
      </button>
    )
  )}
</div>


            <div className="mt-6 overflow-x-auto">

              <table className="w-full text-left text-sm">

                <thead className="border-b border-slate-800 text-slate-400">

                  <tr>

                    <th className="px-3 py-3">
                      ID
                    </th>

                    <th className="px-3 py-3">
                      Amount
                    </th>

                    <th className="px-3 py-3">
                      Probability
                    </th>

                    <th className="px-3 py-3">
                      Prediction
                    </th>

                    <th className="px-3 py-3">
                      Risk
                    </th>

                  </tr>

                </thead>


                <tbody>
  {filteredTransactions.map((transaction) => (
    <tr
      key={transaction.id}
      onClick={() =>
        (window.location.href = `/transaction/${transaction.id}`)
}
       className="cursor-pointer border-b border-slate-800 transition hover:bg-slate-800/60"
    >

      <td className="px-3 py-4">
        #{transaction.id}
      </td>

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
          className={`rounded-full px-3 py-1 text-xs ${
            transaction.risk_level === "CRITICAL"
              ? "bg-red-500/10 text-red-400"
              : transaction.risk_level === "HIGH"
              ? "bg-orange-500/10 text-orange-400"
              : transaction.risk_level === "MEDIUM"
              ? "bg-yellow-500/10 text-yellow-400"
              : "bg-green-500/10 text-green-400"
          }`}
        >
          {transaction.risk_level}
        </span>

      </td>

    </tr>
  ))}
</tbody>

              </table>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}