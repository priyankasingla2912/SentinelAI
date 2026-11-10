import { NextResponse } from "next/server";
import { cookies } from "next/headers";

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"
).replace(/\/+$/, "");

export async function GET() {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get("sentinelai_access_token")?.value;

    if (!token) {
      return NextResponse.json(
        { detail: "Not authenticated." },
        { status: 401 }
      );
    }

    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    const result = await response.json().catch(() => ({}));

    return NextResponse.json(result, { status: response.status });
  } catch {
    return NextResponse.json(
      { detail: "Unable to verify the current session." },
      { status: 502 }
    );
  }
}
