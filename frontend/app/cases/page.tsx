
"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8001";

type FraudCase = {
  case_id: number;
  prediction_id: number;
  status: string;
  analyst: string | null;
  investigation_notes: string | null;
  created_at: string;
  updated_at: string;
};

export default function CasesPage() {
  const [cases, setCases] = useState<FraudCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editAnalyst, setEditAnalyst] = useState("");
  const [editNotes, setEditNotes] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");


  const loadCases = useCallback(async () => {
    try {
      setError("");

      const response = await fetch(`${API_URL}/cases`);

      if (!response.ok) {
        throw new Error(`Unable to load cases (${response.status})`);
      }

      const data = await response.json();
      setCases(data.cases);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to SentinelAI."
      );
    } finally {
      setLoading(false);
    }
  }, []);

 useEffect(() => {
  const controller = new AbortController();

  async function fetchInitialCases() {
    try {
      const response = await fetch(`${API_URL}/cases`, {
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Unable to load cases (${response.status})`);
      }

      const data = await response.json();
      setCases(data.cases);
      setError("");
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

  void fetchInitialCases();

  return () => controller.abort();
}, []);

  async function updateStatus(
    fraudCase: FraudCase,
    newStatus: string
  ) {
    setUpdatingId(fraudCase.case_id);
    setMessage("");
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/cases/${fraudCase.case_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: newStatus,
            analyst: fraudCase.analyst,
            investigation_notes: fraudCase.investigation_notes,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update the case."
        );
      }

      setMessage(`Case #${fraudCase.case_id} updated successfully.`);
      await loadCases();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to update the case."
      );
    } finally {
      setUpdatingId(null);
    }
  }

async function saveCaseDetails(fraudCase: FraudCase) {
  setUpdatingId(fraudCase.case_id);
  setMessage("");
  setError("");

  try {
    const response = await fetch(
      `${API_URL}/cases/${fraudCase.case_id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          analyst: editAnalyst.trim() || null,
          investigation_notes: editNotes.trim() || null,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Unable to save case details.");
    }

    setMessage(`Case #${fraudCase.case_id} details saved successfully.`);
    setEditingId(null);
    await loadCases();
  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "Unable to save case details."
    );
  } finally {
    setUpdatingId(null);
  }
}


const filteredCases = cases.filter((fraudCase) => {
  const query = searchTerm.trim().toLowerCase();

  const matchesSearch =
    query === "" ||
    String(fraudCase.case_id).includes(query) ||
    String(fraudCase.prediction_id).includes(query) ||
    (fraudCase.analyst || "").toLowerCase().includes(query) ||
    (fraudCase.investigation_notes || "").toLowerCase().includes(query);

  const matchesStatus =
    statusFilter === "ALL" || fraudCase.status === statusFilter;

  return matchesSearch && matchesStatus;
});

  const openCases = cases.filter(
    (item) => item.status !== "RESOLVED"
  ).length;

  const inProgressCases = cases.filter(
    (item) => item.status === "IN_PROGRESS"
  ).length;

  const resolvedCases = cases.filter(
    (item) => item.status === "RESOLVED"
  ).length;

  return (
    <main className="cases-page">
      <div className="cases-header">
        <div>
          <p className="cases-eyebrow">SENTINELAI / OPERATIONS</p>
          <h1>Fraud Case Management</h1>
          <p className="cases-subtitle">
            Review investigations, monitor case status, and manage analyst workflows.
          </p>
        </div>

        <button
          className="cases-refresh"
          onClick={() => void loadCases()}
          disabled={loading}
        >
          Refresh cases
        </button>
      </div>

      <section className="cases-metrics">
        <article className="cases-metric">
          <span>Total cases</span>
          <strong>{cases.length}</strong>
        </article>

        <article className="cases-metric">
          <span>Open cases</span>
          <strong>{openCases}</strong>
        </article>

        <article className="cases-metric">
          <span>In progress</span>
          <strong>{inProgressCases}</strong>
        </article>

        <article className="cases-metric">
          <span>Resolved</span>
          <strong>{resolvedCases}</strong>
        </article>
      </section>

      {message && (
        <div className="cases-success" role="status">
          {message}
        </div>
      )}

      {error && (
        <div className="cases-error" role="alert">
          {error}
        </div>
      )}

      <section className="cases-table-section">
        <div className="cases-table-header">
          <div>
            <h2>Investigation queue</h2>
            <p>Cases returned by the SentinelAI API</p>
          </div>


<div className="cases-filters">
  <input
    type="text"
    value={searchTerm}
    onChange={(event) => setSearchTerm(event.target.value)}
    placeholder="Search case, transaction, analyst..."
    aria-label="Search fraud cases"
  />

  <select
    value={statusFilter}
    onChange={(event) => setStatusFilter(event.target.value)}
    aria-label="Filter cases by status"
  >
    <option value="ALL">All statuses</option>
    <option value="NEW">New</option>
    <option value="IN_PROGRESS">In progress</option>
    <option value="RESOLVED">Resolved</option>
  </select>
</div>

          <span className="cases-count">
            {filteredCases.length} records
          </span>
        </div>

        {loading ? (
          <p className="cases-state">Loading fraud cases...</p>
        ) : error && cases.length === 0 ? (
          <p className="cases-state">
            Check that your FastAPI backend is running at port 8000.
          </p>
        
) : cases.length === 0 ? (
  <p className="cases-state">
    No cases found. Create a test case through the API first.
  </p>
) : filteredCases.length === 0 ? (
  <p className="cases-state">
    No cases match your search or selected status. Try changing your filters.
  </p>
) : (

          <div className="cases-table-wrapper">
            <table className="cases-table">
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Transaction</th>
                  <th>Analyst</th>
                  <th>Status</th>
                  <th>Investigation notes</th>
                  <th>Last updated</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredCases.map((fraudCase) => (
                  <tr key={fraudCase.case_id}>
                    <td>
                      <strong>#{fraudCase.case_id}</strong>
                    </td>
                    <td>
  <Link
    href={`/transaction/${fraudCase.prediction_id}`}
    className="cases-transaction-link"
  >
    #{fraudCase.prediction_id}
  </Link>
</td>
                    
                    
<td>
  {editingId === fraudCase.case_id ? (
    <input
      aria-label={`Analyst for case ${fraudCase.case_id}`}
      value={editAnalyst}
      onChange={(event) => setEditAnalyst(event.target.value)}
      placeholder="Enter analyst name"
    />
  ) : (
    fraudCase.analyst || "Unassigned"
  )}
</td>
                    
                    
                    
<td>
                      <span
                        className={`case-status case-status-${fraudCase.status.toLowerCase()}`}
                      >
                        {fraudCase.status.replace("_", " ")}
                      </span>
                    </td>
                   <td className="cases-notes">
  {editingId === fraudCase.case_id ? (
    <textarea
      aria-label={`Investigation notes for case ${fraudCase.case_id}`}
      value={editNotes}
      onChange={(event) => setEditNotes(event.target.value)}
      placeholder="Enter investigation notes"
      rows={3}
    />
  ) : (
    fraudCase.investigation_notes || "No notes added"
  )}
</td>
                    <td>{fraudCase.updated_at}</td>
                    <td>
                      <select
                        aria-label={`Update status for case ${fraudCase.case_id}`}
                        value={fraudCase.status}
                        disabled={updatingId === fraudCase.case_id}
                        onChange={(event) =>
                          void updateStatus(fraudCase, event.target.value)
                        }
                      >
                        <option value="NEW">New</option>
                        <option value="IN_PROGRESS">In progress</option>
                        <option value="RESOLVED">Resolved</option>
                      </select>

                      {updatingId === fraudCase.case_id && (
                        <small>Saving...</small>
                      )}
                      {editingId === fraudCase.case_id ? (
  <div className="cases-edit-actions">
    <button
      disabled={updatingId === fraudCase.case_id}
      onClick={() => void saveCaseDetails(fraudCase)}
    >
      Save details
    </button>

    <button
      disabled={updatingId === fraudCase.case_id}
      onClick={() => {
        setEditingId(null);
        setEditAnalyst("");
        setEditNotes("");
      }}
    >
      Cancel
    </button>
  </div>
) : (
  <button
    disabled={updatingId === fraudCase.case_id}
    onClick={() => {
      setEditingId(fraudCase.case_id);
      setEditAnalyst(fraudCase.analyst || "");
      setEditNotes(fraudCase.investigation_notes || "");
    }}
  >
    Edit details
  </button>
)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <p className="cases-footer">
        SentinelAI • AI-powered Fraud &amp; Risk Intelligence
      </p>
    </main>
  );
}
