import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SentinelAI | Fraud Intelligence Platform",
  description:
    "AI-powered fraud detection and risk intelligence platform",
};

export default function RootLayout({
  children,
}: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-950 text-white">

        {/* Navigation Bar */}
        <nav className="border-b border-slate-800 bg-slate-900">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

            {/* Logo */}
            <Link
              href="/"
              className="text-xl font-bold tracking-tight"
            >
              SentinelAI
            </Link>

            {/* Navigation Links */}
            <div className="flex items-center gap-8">

              <Link
                href="/"
                className="text-sm font-medium text-slate-300 transition hover:text-white"
              >
                Dashboard
              </Link>

              <Link
                href="/analyze"
                className="text-sm font-medium text-slate-300 transition hover:text-white"
              >
                Analyze
              </Link>

              <Link
                href="/history"
                className="text-sm font-medium text-slate-300 transition hover:text-white"
              >
                History
              </Link>

              {/* API Status */}
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <span className="h-2 w-2 rounded-full bg-green-400"></span>
                API Online
              </div>

            </div>
          </div>
        </nav>

        {/* Page Content */}
        <div className="flex-1">
          {children}
        </div>

      </body>
    </html>
  );
}