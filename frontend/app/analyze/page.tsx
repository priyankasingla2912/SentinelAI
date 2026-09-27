"use client";

import { useState } from "react";

export default function AnalyzePage() {
  const [amount, setAmount] = useState("");
  const [time, setTime] = useState("");
  const [features, setFeatures] = useState<Record<string, string>>({});
  const [showAdvancedFeatures, setShowAdvancedFeatures] = useState(false);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error,setError] = useState("");

  const featureNames = Array.from({ length: 28 }, (_, i) => `V${i + 1}`);
  const legitimateSample = {
  Time: 50000,
  Amount: 100,
  V1: 0,
  V2: 0,
  V3: 0,
  V4: 0,
  V5: 0,
  V6: 0,
  V7: 0,
  V8: 0,
  V9: 0,
  V10: 0,
  V11: 0,
  V12: 0,
  V13: 0,
  V14: 0,
  V15: 0,
  V16: 0,
  V17: 0,
  V18: 0,
  V19: 0,
  V20: 0,
  V21: 0,
  V22: 0,
  V23: 0,
  V24: 0,
  V25: 0,
  V26: 0,
  V27: 0,
  V28: 0,
};

const fraudSample = {
  Time: 4462,
  Amount: 239.93,
  V1: -2.30334956758553,
  V2: 1.759247460267,
  V3: -0.359744743330052,
  V4: 2.33024305053917,
  V5: -0.821628328375422,
  V6: -0.0757875706194599,
  V7: 0.562319782266954,
  V8: -0.399146578487216,
  V9: -0.238253367661746,
  V10: -1.52541162656194,
  V11: 2.03291215755072,
  V12: -6.56012429505962,
  V13: 0.0229373234890961,
  V14: -1.47010153611197,
  V15: -0.698826068579047,
  V16: -2.28219382856251,
  V17: -4.78183085597533,
  V18: -2.61566494476124,
  V19: -1.33444106667307,
  V20: -0.430021867171611,
  V21: -0.294166317554753,
  V22: -0.932391057274991,
  V23: 0.172726295799422,
  V24: -0.0873295379700724,
  V25: -0.156114264651172,
  V26: -0.542627889040196,
  V27: 0.0395659889264757,
  V28: -0.153028796529788,
};

  const handleFeatureChange = (feature: string, value: string) => {
    setFeatures((previous) => ({
      ...previous,
      [feature]: value,
    }));
  };

  const loadSample = (
  sample: typeof legitimateSample
) => {
  setAmount(String(sample.Amount));
  setTime(String(sample.Time));

  const sampleFeatures: Record<string, string> = {};

  featureNames.forEach((feature) => {
    sampleFeatures[feature] = String(
      sample[feature as keyof typeof sample]
    );
  });

  setFeatures(sampleFeatures);
  setResult(null);
  setError("");
};
  const handleSubmit = async (event: React.FormEvent) => {
  event.preventDefault();

  setLoading(true);
  setError("");
  setResult(null);

  try {
    const transactionData = {
      Time: Number(time),
      Amount: Number(amount),
      ...Object.fromEntries(
        Object.entries(features).map(([key, value]) => [
          key,
          Number(value),
        ])
      ),
    };
    console.log("Sending transaction:",transactionData);

    const response = await fetch(
      "http://127.0.0.1:8000/predict",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(transactionData),
      }
    );

    if (!response.ok) {
      throw new Error("Prediction request failed");
    }

    const data = await response.json();
    console.log("Prediction result:",data);

    setResult(data);
  } catch (error) {
    console.error("Prediction error:", error);
    setError(
      "Unable to analyze the transaction. Please make sure the backend is running."
    );
  } finally {
    setLoading(false);
}
};

  return (
    <main className="min-h-screen bg-slate-950 text-white p-10">
      <div className="mx-auto max-w-6xl">

        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Transaction Analyzer
          </h1>

          <p className="mt-3 text-slate-400">
            Analyze a transaction for fraud risk using SentinelAI.
          </p>
        </div>

        {/* Transaction Form */}
        <form onSubmit={handleSubmit}>

          {/* Basic Transaction Information */}
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              Transaction Details
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Enter the basic transaction information below.
            </p>
            

            <div className="mt-6 grid gap-6 md:grid-cols-2">

              {/* Amount */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  Transaction Amount
                </label>

                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={amount}
                  onChange={(event) => setAmount(event.target.value)}
                  placeholder="e.g. 125.50"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                  required
                />
              </div>

              {/* Time */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  Transaction Time
                </label>

                <input
                  type="number"
                  step="0.01"
                  value={time}
                  onChange={(event) => setTime(event.target.value)}
                  placeholder="e.g. 50000"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                  required
                />
              </div>

            </div>
          </div>

          {/* Advanced Features */}
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

         <button
  type="button"
  onClick={() =>
    setShowAdvancedFeatures((previous) => !previous)
  }
  className="flex w-full items-center justify-between text-left"
>
  <div>
    <h2 className="text-xl font-semibold">
      Advanced Model Features
    </h2>

    <p className="mt-2 text-sm text-slate-400">
      V1–V28 are anonymized transaction features used by the fraud detection model.
    </p>

    <p className="mt-2 text-xs text-slate-500">
      These features come from the transformed input data used during model training.
    </p>
  </div>

  <span className="ml-4 text-xl text-slate-400">
    {showAdvancedFeatures ? "▲" : "▼"}
  </span>
</button>

        {showAdvancedFeatures &&(
            <div className="mt-6 grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">

              {featureNames.map((feature) => (
                <div key={feature}>

                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {feature}
                  </label>

                  <input
                    type="number"
                    step="any"
                    value={features[feature] || ""}
                    onChange={(event) =>
                      handleFeatureChange(feature, event.target.value)
                    }
                    placeholder="0.00"
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-white outline-none focus:border-blue-500"
                    required
                  />

                </div>
              ))}

            </div>
        )}
          </div>
          <div className="mt-5 flex flex-wrap gap-3">

  <button
    type="button"
    onClick={() => loadSample(legitimateSample)}
    className="rounded-lg border border-green-500/30 bg-green-500/10 px-4 py-2 text-sm font-medium text-green-400 transition hover:bg-green-500/20"
  >
    Load Legitimate Sample
  </button>

  <button
    type="button"
    onClick={() => loadSample(fraudSample)}
    className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
  >
    Load Fraud Sample
  </button>

</div>

          {/* Submit Button */}
          <div className="mt-6 flex justify-end">

            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze Transaction"}
            </button>

          </div>

        </form>
         {/* Error Message */}
        {error && (
          <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-5 text-red-400">
            {error}
          </div>
        )}

                {/* Prediction Results */}
        {result && (
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-2xl font-bold">
              Analysis Results
            </h2>

            {/* Summary Cards */}
            <div className="mt-6 grid gap-4 md:grid-cols-3">

              {/* Fraud Probability */}
              <div className="rounded-lg bg-slate-950 p-5">

                <p className="text-sm text-slate-400">
                  Fraud Probability
                </p>

                <p className="mt-2 text-3xl font-bold text-red-400">
                  {(result.fraud_probability * 100).toFixed(1)}%
                </p>

                {/* Probability Bar */}
                <div className="mt-4">

                  <div className="relative h-3 w-full rounded-full bg-slate-800">

                    <div
                      className="h-3 rounded-full bg-red-500 transition-all"
                      style={{
                        width: `${result.fraud_probability * 100}%`,
                      }}
                    />

                    <div
                      className="absolute top-[-5px] h-5 w-0.5 bg-yellow-400"
                      style={{
                        left: `${result.threshold * 100}%`,
                      }}
                    />

                  </div>

                  <div className="mt-2 flex justify-between text-xs text-slate-500">

                    <span>0%</span>

                    <span>
                      Threshold: {(result.threshold * 100).toFixed(0)}%
                    </span>

                    <span>100%</span>

                  </div>

                </div>

              </div>

              {/* Prediction */}
              <div className="rounded-lg bg-slate-950 p-5">

                <p className="text-sm text-slate-400">
                  Prediction
                </p>

                <p
                  className={`mt-2 text-2xl font-bold ${
                    result.prediction === "FRAUD"
                      ? "text-red-400"
                      : "text-green-400"
                  }`}
                >
                  {result.prediction}
                </p>

              </div>

              {/* Risk Level */}
              <div className="rounded-lg bg-slate-950 p-5">

                <p className="text-sm text-slate-400">
                  Risk Level
                </p>

                <p
                  className={`mt-2 text-2xl font-bold ${
                    result.risk_level === "CRITICAL"
                      ? "text-red-400"
                      : result.risk_level === "HIGH"
                      ? "text-orange-400"
                      : result.risk_level === "MEDIUM"
                      ? "text-yellow-400"
                      : "text-green-400"
                  }`}
                >
                  {result.risk_level}
                </p>

              </div>

            </div>

            {/* Recommended Action */}
            <div className="mt-6 rounded-lg bg-slate-950 p-5">

              <p className="text-sm text-slate-400">
                Recommended Action
              </p>

              <p className="mt-2 text-lg text-white">
                {result.recommended_action}
              </p>

            </div>

            {/* SHAP Factors */}
            <div className="mt-6 rounded-lg bg-slate-950 p-5">

              <h3 className="text-lg font-semibold">
                Top Risk Factors
              </h3>

              <p className="mt-2 text-sm text-slate-400">
                SHAP values explain how each feature influenced the fraud prediction.
              </p>

              {/* Legend */}
              <div className="mt-4 flex flex-wrap gap-5 text-sm">

                <span className="text-red-400">
                  ↑ Increased fraud risk
                </span>

                <span className="text-blue-400">
                  ↓ Lowered fraud risk
                </span>

              </div>

              {/* SHAP Factors */}
              <div className="mt-5 space-y-3">

                {result.top_risk_factors?.length > 0 ? (
                  result.top_risk_factors.map(
                    (factor: any, index: number) => {

                      const shapValue = Number(factor.shap_value);
                      const increasedRisk = shapValue > 0;

                      return (
                        <div
                          key={index}
                          className="flex items-center justify-between border-b border-slate-800 pb-3"
                        >

                          {/* Feature */}
                          <span className="font-medium">
                            {factor.feature}
                          </span>

                          {/* Impact */}
                          <span
                            className={
                              increasedRisk
                                ? "text-red-400"
                                : "text-blue-400"
                            }
                          >
                            {increasedRisk
                              ? "↑ Increased fraud risk"
                              : "↓ Lowered fraud risk"}
                          </span>

                          {/* SHAP Value */}
                          <span
                            className={
                              increasedRisk
                                ? "font-mono text-red-400"
                                : "font-mono text-blue-400"
                            }
                          >
                            {shapValue > 0 ? "+" : ""}
                            {shapValue.toFixed(4)}
                          </span>

                        </div>
                      );
                    }
                  )
                ) : (
                  <p className="text-sm text-slate-500">
                    No SHAP risk factors are available for this transaction.
                  </p>
                )}

              </div>

            </div>

          </div>
        )}

      </div>
    </main>
  );
}