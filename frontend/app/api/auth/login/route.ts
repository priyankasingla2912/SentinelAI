import { NextResponse } from "next/server";

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"
).replace(/\/+$/, "");

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { email, password } = body;

    if (
      typeof email !== "string" ||
      typeof password !== "string" ||
      !email.trim() ||
      !password
    ) {
      return NextResponse.json(
        { detail: "Email and password are required." },
        { status: 400 }
      );
    }

    const backendResponse = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
      cache: "no-store",
    });

    const result = await backendResponse.json().catch(() => ({}));

    if (!backendResponse.ok) {
      return NextResponse.json(
        { detail: result.detail || "Login failed." },
        { status: backendResponse.status }
      );
    }

    if (typeof result.access_token !== "string" || !result.user) {
      return NextResponse.json(
        { detail: "The authentication server returned an invalid response." },
        { status: 502 }
      );
    }

    const response = NextResponse.json({ user: result.user });

    response.cookies.set("sentinelai_access_token", result.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 30 * 60,
    });

    return response;
  } catch {
    return NextResponse.json(
      { detail: "Unable to connect to the authentication server." },
      { status: 502 }
    );
  }
}
