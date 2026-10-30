"use client";

import { useState } from "react";
import { API_BASE_URL } from "@/lib/api";


interface RiskFactor {
  feature: string;
  shap_value: number;
}

interface PredictionResult {
  prediction_id: number;
  case_id: number | null;
  amount: number;
  fraud_probability: number;
  threshold: number;
  prediction: string;
  risk_level: string;
  top_risk_factors: RiskFactor[];
  recommended_action: string;
}

interface ModelEvidence {
  feature?: string;
  shap_value: number;
}

interface RetrievedPolicy {
  id?: string | number;
  title?: string;
  category?: string;
  content?: string;
  recommended_action?: string;
  matched_terms?: string[];
}

interface InvestigationResult {
  assessment: string;
  requires_human_review: boolean;
  model_evidence: ModelEvidence[];
  retrieved_policies: RetrievedPolicy[];
  disclaimer?: string;
}


export default function AnalyzePage() {
  const [amount, setAmount] = useState("");
  const [time, setTime] = useState("");
  const [features, setFeatures] = useState<Record<string, string>>(
    Object.fromEntries(Array.from({ length: 28 }, (_, i) => [`V${i + 1}`, "0"]))
  );
  const [showAdvancedFeatures, setShowAdvancedFeatures] = useState(false);

  const [result, setResult] = useState<PredictionResult | null>(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

const [investigation, setInvestigation] =
  useState<InvestigationResult | null>(null);
const [investigating, setInvestigating] = useState(false);
const [investigationError, setInvestigationError] = useState("");

  const featureNames = Array.from({ length: 28 }, (_, i) => `V${i + 1}`);
  
const legitimateSample = {
  Time: 0,
  Amount: 149.62,
  V1: -1.3598071336738,
  V2: -0.0727811733098497,
  V3: 2.53634673796914,
  V4: 1.37815522427443,
  V5: -0.338320769942518,
  V6: 0.462387777762292,
  V7: 0.239598554061257,
  V8: 0.0986979012610507,
  V9: 0.363786969978931,
  V10: 0.0907941719789316,
  V11: -0.551599533260813,
  V12: -0.617800855762348,
  V13: -0.991389847235408,
  V14: -0.311169353699879,
  V15: 1.46817697209427,
  V16: -0.470400525259478,
  V17: 0.207971241929242,
  V18: 0.0257905801985591,
  V19: 0.403992960255733,
  V20: 0.251412098239705,
  V21: -0.018306777944153,
  V22: 0.277837575558899,
  V23: -0.110473910188767,
  V24: 0.0669280749146731,
  V25: 0.128539358273528,
  V26: -0.189114843888824,
  V27: 0.133558376740387,
  V28: -0.0210530534538215,
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
  setInvestigation(null);
setInvestigationError("");
};
  
const handleSubmit = async (event: React.FormEvent) => {
  event.preventDefault();

  // Validate transaction amount and time
  if (amount.trim() === "" || time.trim() === "") {
    setError("Please enter both the transaction amount and transaction time.");
    return;
  }

  if (
    !Number.isFinite(Number(amount)) ||
    Number(amount) < 0 ||
    !Number.isFinite(Number(time)) ||
    Number(time) < 0
  ) {
    setError("Please enter valid, non-negative numbers for amount and time.");
    return;
  }

  // Validate all 28 model features
  const invalidFeature = featureNames.find((feature) => {
    const value = features[feature];

    return (
      value === undefined ||
      value.trim() === "" ||
      !Number.isFinite(Number(value))
    );
  });

  if (invalidFeature) {
    setError(`Please enter a valid numeric value for ${invalidFeature}.`);
    return;
  }


  setLoading(true);
  setError("");
  setResult(null);
  setInvestigation(null);
  setInvestigationError("");

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
      `${API_BASE_URL}/predict`,
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

const handleInvestigate = async () => {
  if (!result) {
    setInvestigationError("Analyze a transaction first.");
    return;
  }

  setInvestigating(true);
  setInvestigationError("");
  setInvestigation(null);

  try {
    const payload = {
      prediction: result.prediction,
      risk_level: result.risk_level,
      fraud_probability: result.fraud_probability,
      top_risk_factors: result.top_risk_factors ?? [],
    };

    const response = await fetch(
      `${API_BASE_URL}/investigate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "The investigation request failed."
      );
    }

    setInvestigation(data);
  } catch (err) {
    console.error("Investigation error:", err);
    setInvestigationError(
      err instanceof Error
        ? err.message
        : "Unable to generate the investigation report."
    );
  } finally {
    setInvestigating(false);
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

<div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/10 p-4">
  <p className="text-sm font-semibold text-amber-300">
    Demo and data-quality notice
  </p>
  <p className="mt-2 text-sm leading-6 text-slate-300">
    For meaningful predictions, provide transaction features prepared
    using the same preprocessing as the model's training data.
    The default V1–V28 values are placeholders, not real transaction
    evidence. Use the sample buttons to explore the demo. Do not use
    placeholder-based predictions to make real financial decisions.
  </p>
</div>



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
                    (factor: RiskFactor, index: number) => {

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
            {/* AI Investigation */}
<div className="mt-6 rounded-lg border border-blue-500/30 bg-slate-950 p-5">
  <h3 className="text-lg font-semibold">
    AI Fraud Investigation
  </h3>

  <p className="mt-2 text-sm text-slate-400">
    Generate an investigation report using model evidence
    and the platform&apos;s sample fraud policies.
  </p>

  <button
    type="button"
    onClick={handleInvestigate}
    disabled={investigating}
    className="mt-4 rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
  >
    {investigating ? "Investigating..." : "Investigate Transaction"}
  </button>

  {investigationError && (
    <p className="mt-4 text-sm text-red-400">
      {investigationError}
    </p>
  )}

  {investigation && (
    <div className="mt-6 space-y-5">
      <div>
        <h4 className="font-semibold">Investigation Assessment</h4>
        <p className="mt-2 text-slate-300">
          {investigation.assessment}
        </p>
      </div>

      <div>
        <h4 className="font-semibold">Human Review Required</h4>
        <p className="mt-2 text-slate-300">
          {investigation.requires_human_review
            ? "Yes — human review is required."
            : "No — human review was not flagged by the system."}
        </p>
      </div>

<div>
  <h4 className="font-semibold">Model Evidence</h4>
  <p className="mt-2 text-sm text-slate-400">
    Features and their contributions to the model output.
  </p>

  {Array.isArray(investigation.model_evidence) &&
  investigation.model_evidence.length > 0 ? (
    <div className="mt-3 overflow-x-auto rounded-lg border border-slate-800">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-900 text-slate-400">
          <tr>
            <th className="px-4 py-3">Feature</th>
            <th className="px-4 py-3">SHAP Contribution</th>
            <th className="px-4 py-3">Direction</th>
          </tr>
        </thead>
        <tbody>
          {investigation.model_evidence.map(
            (item: ModelEvidence, index: number) => {
              const value = Number(item.shap_value);
              const positive = value > 0;

              return (
                <tr
                  key={`${item.feature ?? "feature"}-${index}`}
                  className="border-t border-slate-800"
                >
                  <td className="px-4 py-3 font-medium">
                    {item.feature ?? "Unknown"}
                  </td>
                  <td className="px-4 py-3 font-mono">
                    {Number.isFinite(value)
                      ? value.toFixed(6)
                      : "N/A"}
                  </td>
                  <td
                    className={`px-4 py-3 ${
                      positive
                        ? "text-red-400"
                        : value < 0
                        ? "text-blue-400"
                        : "text-slate-400"
                    }`}
                  >
                    {value > 0
                      ? "Positive contribution"
                      : value < 0
                      ? "Negative contribution"
                      : "No contribution"}
                  </td>
                </tr>
              );
            }
          )}
        </tbody>
      </table>
    </div>
  ) : (
    <pre className="mt-2 whitespace-pre-wrap break-words rounded-lg bg-slate-900 p-4 text-sm text-slate-300">
      {JSON.stringify(investigation.model_evidence, null, 2)}
    </pre>
  )}
</div>




<div>
  <h4 className="text-lg font-semibold">Retrieved Sample Policies</h4>
  <p className="mt-2 text-sm text-slate-400">
    Sample development policies relevant to this investigation.
  </p>

  {Array.isArray(investigation.retrieved_policies) &&
  investigation.retrieved_policies.length > 0 ? (
    <div className="mt-4 space-y-4">
      {investigation.retrieved_policies.map(
        (policy: RetrievedPolicy, index: number) => (
          <div
            key={policy.id ?? index}
            className="rounded-lg border border-slate-800 bg-slate-900 p-5"
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-blue-400">
                  {policy.id ?? "Policy"}
                </p>
                <h5 className="mt-1 font-semibold text-white">
                  {policy.title ?? "Untitled policy"}
                </h5>
              </div>

              {policy.category && (
                <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300">
                  {policy.category}
                </span>
              )}
            </div>

            {policy.content && (
              <p className="mt-3 text-sm leading-6 text-slate-300">
                {policy.content}
              </p>
            )}

            {policy.recommended_action && (
              <div className="mt-4 rounded-md border border-blue-500/20 bg-blue-500/5 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-blue-300">
                  Recommended Action
                </p>
                <p className="mt-1 text-sm text-slate-200">
                  {policy.recommended_action}
                </p>
              </div>
            )}

            {Array.isArray(policy.matched_terms) &&
              policy.matched_terms.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {policy.matched_terms.map(
                    (term: string, termIndex: number) => (
                      <span
                        key={`${term}-${termIndex}`}
                        className="rounded bg-slate-800 px-2 py-1 text-xs text-slate-400"
                      >
                        {term}
                      </span>
                    )
                  )}
                </div>
              )}
          </div>
        )
      )}
    </div>
  ) : (
    <p className="mt-3 text-sm text-slate-400">
      No sample policies were returned for this investigation.
    </p>
  )}
</div>
{investigation.disclaimer && (
        <p className="border-t border-slate-800 pt-4 text-xs text-slate-500">
          {investigation.disclaimer}
        </p>
      )}
    </div>
  )}
</div>

          </div>
        )}

      </div>
    </main>
  );
}
