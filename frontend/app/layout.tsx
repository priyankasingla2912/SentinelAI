import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import AuthNavigation from "../components/auth-navigation";
import AuthGuard from "../components/auth-guard";
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
        <AuthNavigation />

        <div className="flex-1">
          <AuthGuard>{children}</AuthGuard>
        </div>
      </body>
    </html>
  );
}