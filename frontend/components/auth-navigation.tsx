"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

type User = {
  id: number;
  email: string;
  full_name: string;
  role: string;
};

export default function AuthNavigation() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [loggingOut, setLoggingOut] = useState(false);

  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    const publicPaths = ["/login", "/register", "/forgot-password"];

if (publicPaths.includes(pathname)) {
  return;
}

    let active = true;

    async function loadSession() {
      try {
        const response = await fetch("/api/auth/me", {
          method: "GET",
          cache: "no-store",
        });

        if (!response.ok) {
          router.replace("/login");
          return;
        }

        const data = await response.json();

        if (active) {
          setUser(data);
        }
      } catch {
        router.replace("/login");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadSession();

    return () => {
      active = false;
    };
  }, [pathname, router]);

  async function handleLogout() {
    setLoggingOut(true);

    try {
      await fetch("/api/auth/logout", {
        method: "POST",
      });
    } finally {
      router.replace("/login");
      router.refresh();
    }
  }

  if (
  ["/login", "/register", "/forgot-password"].includes(pathname) ||
  loading ||
  !user
) {
    return null;
  }

  return (
    <nav className="border-b border-slate-800 bg-slate-900">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-xl font-bold tracking-tight">
          SentinelAI
        </Link>

        <div className="flex items-center gap-8">
          <Link
            href="/"
            className="text-sm font-medium text-slate-300 transition hover:text-white"
          >
            Dashboard
          </Link>

          {user.role === "ADMIN" && (
            <Link
              href="/analyze"
              className="text-sm font-medium text-slate-300 transition hover:text-white"
            >
              Analyze
            </Link>
          )}

          <Link
            href="/history"
            className="text-sm font-medium text-slate-300 transition hover:text-white"
          >
            History
          </Link>

          {user.role === "ADMIN" && (
            <Link
              href="/users"
              className="text-sm font-medium text-slate-300 transition hover:text-white"
            >
              Users
            </Link>
          )}

          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium text-white">
              {user.full_name}
            </p>
            <p className="text-xs text-slate-400">
              {user.role.replaceAll("_", " ")}
            </p>
          </div>

          <button
            onClick={handleLogout}
            disabled={loggingOut}
            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white disabled:opacity-50"
          >
            {loggingOut ? "Logging out..." : "Logout"}
          </button>

          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span className="h-2 w-2 rounded-full bg-green-400"></span>
            API Online
          </div>
        </div>
      </div>
    </nav>
  );
}
