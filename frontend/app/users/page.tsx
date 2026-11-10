"use client";

import { useCallback, useEffect, useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/lib/api";

type User = {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
};

export default function UsersPage() {
  const router = useRouter();

  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const loadUsers = useCallback(async () => {

    try {
      const response = await fetch(`${API_BASE_URL}/auth/users`, {
        cache: "no-store",
      });

      if (response.status === 401 || response.status === 403) {
        router.replace("/");
        return;
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to load users.");
      }

      setUsers(data.users || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load users.");
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    void Promise.resolve().then(() => loadUsers());
  }, [loadUsers]);

  async function createViewer(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/auth/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          email,
          password,
          role: "VIEWER",
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create account.");
      }

      setMessage("Viewer account created successfully.");
      setFullName("");
      setEmail("");
      setPassword("");
      await loadUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create account.");
    } finally {
      setSaving(false);
    }
  }

  async function toggleUser(user: User) {
    setError("");
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/auth/users/${user.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ is_active: !user.is_active }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to update account.");
      }

      setMessage(`Account ${user.is_active ? "deactivated" : "activated"}.`);
      await loadUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to update account.");
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-100">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">User Management</h1>
            <p className="mt-2 text-slate-400">
              Create and manage SentinelAI Viewer accounts.
            </p>
          </div>
          <button
            onClick={() => router.push("/")}
            className="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
          >
            Back to Dashboard
          </button>
        </div>

        {message && (
          <div role="status" className="mb-5 rounded-lg border border-green-800 bg-green-950/40 p-3 text-green-300">
            {message}
          </div>
        )}

        {error && (
          <div role="alert" className="mb-5 rounded-lg border border-red-800 bg-red-950/40 p-3 text-red-300">
            {error}
          </div>
        )}

        <section className="mb-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-5 text-xl font-semibold">Create Viewer Account</h2>

          <form onSubmit={createViewer} className="grid gap-4 md:grid-cols-2">
            <label className="text-sm text-slate-300">
              Full name
              <input
                required
                minLength={2}
                maxLength={150}
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-3 text-white"
                placeholder="Full name"
              />
            </label>

            <label className="text-sm text-slate-300">
              Email address
              <input
                required
                type="email"
                maxLength={255}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-3 text-white"
                placeholder="name@example.com"
              />
            </label>

            <label className="text-sm text-slate-300 md:col-span-2">
              Temporary password (minimum 12 characters)
              <input
                required
                type="password"
                minLength={12}
                maxLength={128}
                autoComplete="new-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-3 text-white"
                placeholder="Create a strong temporary password"
              />
            </label>

            <div className="md:col-span-2">
              <p className="mb-4 text-xs text-slate-400">
                New accounts receive Viewer permissions: read-only access to dashboards, history, and fraud cases.
              </p>
              <button
                type="submit"
                disabled={saving}
                className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-500 disabled:opacity-50"
              >
                {saving ? "Creating account..." : "Create Viewer Account"}
              </button>
            </div>
          </form>
        </section>

        <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-xl font-semibold">Registered Users</h2>
            <button
              onClick={() => void loadUsers()}
              disabled={loading}
              className="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800 disabled:opacity-50"
            >
              Refresh
            </button>
          </div>

          {loading ? (
            <p className="text-slate-400">Loading users...</p>
          ) : users.length === 0 ? (
            <p className="text-slate-400">No registered users found.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-700 text-slate-400">
                  <tr>
                    <th className="px-3 py-3">Name</th>
                    <th className="px-3 py-3">Email</th>
                    <th className="px-3 py-3">Role</th>
                    <th className="px-3 py-3">Status</th>
                    <th className="px-3 py-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b border-slate-800">
                      <td className="px-3 py-4">{user.full_name}</td>
                      <td className="px-3 py-4">{user.email}</td>
                      <td className="px-3 py-4">
                        {user.role.replaceAll("_", " ")}
                      </td>
                      <td className="px-3 py-4">
                        {user.is_active ? "Active" : "Inactive"}
                      </td>
                      <td className="px-3 py-4">
                        {user.role !== "ADMIN" && (
                          <button
                            onClick={() => void toggleUser(user)}
                            className="rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800"
                          >
                            {user.is_active ? "Deactivate" : "Activate"}
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
      </div>
    </main>
  );
}
