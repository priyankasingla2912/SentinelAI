"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [step, setStep] = useState<"request" | "reset">("request");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRequest(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Unable to request a reset code.");
        return;
      }

      setMessage(data.message || "If an active account exists, a reset code will be sent.");
      setStep("reset");
    } catch {
      setError("Unable to connect. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleReset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          otp,
          new_password: newPassword,
        }),
      });
      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Password reset failed.");
        return;
      }

      setMessage(data.message || "Password reset successful. Please sign in.");
      setTimeout(() => router.push("/login"), 1800);
    } catch {
      setError("Unable to connect. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500";

  return (
    <main className="flex flex-1 items-center justify-center px-6 py-16">
      <section className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">
        <h1 className="text-center text-3xl font-bold text-white">SentinelAI</h1>
        <h2 className="mt-8 text-center text-2xl font-semibold text-white">
          {step === "request" ? "Forgot Password" : "Reset Password"}
        </h2>

        {step === "request" ? (
          <form onSubmit={handleRequest} className="mt-8 space-y-5">
            <label className="block text-sm text-slate-300">
              Email address
              <input
                className={`${inputClass} mt-2`}
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                placeholder="Enter your registered email"
              />
            </label>
            <button disabled={loading} className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-500 disabled:opacity-60">
              {loading ? "Sending..." : "Send reset code"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleReset} className="mt-8 space-y-5">
            <p className="text-sm text-slate-400">
              Enter the six-digit code sent to {email}.
            </p>
            <label className="block text-sm text-slate-300">
              Verification code
              <input
                className={`${inputClass} mt-2 text-center text-xl tracking-[0.5em]`}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                inputMode="numeric"
                pattern="[0-9]{6}"
                maxLength={6}
                required
                placeholder="000000"
              />
            </label>
            <label className="block text-sm text-slate-300">
              New password (minimum 12 characters)
              <input
                className={`${inputClass} mt-2`}
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                minLength={12}
                maxLength={128}
                required
                autoComplete="new-password"
                placeholder="Create a new password"
              />
            </label>
            <button disabled={loading || otp.length !== 6} className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-500 disabled:opacity-60">
              {loading ? "Resetting..." : "Reset password"}
            </button>
          </form>
        )}

        {error && <p role="alert" className="mt-5 rounded-lg bg-red-950/50 p-3 text-sm text-red-300">{error}</p>}
        {message && <p role="status" className="mt-5 rounded-lg bg-green-950/50 p-3 text-sm text-green-300">{message}</p>}

        <p className="mt-6 text-center text-sm text-slate-400">
          <a href="/login" className="text-blue-400 hover:text-blue-300">Back to sign in</a>
        </p>
      </section>
    </main>
  );
}
