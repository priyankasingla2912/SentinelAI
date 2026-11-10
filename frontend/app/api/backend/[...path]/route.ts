import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"
).replace(/\/+$/, "");

type RouteContext = {
  params: Promise<{ path: string[] }>;
};

async function proxyRequest(
  request: NextRequest,
  context: RouteContext
) {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get("sentinelai_access_token")?.value;

    if (!token) {
      return NextResponse.json(
        { detail: "Authentication required." },
        { status: 401 }
      );
    }

    const { path } = await context.params;
    const backendPath = path.map(encodeURIComponent).join("/");
    const query = request.nextUrl.search;

    const headers = new Headers();
    headers.set("Authorization", `Bearer ${token}`);

    const contentType = request.headers.get("content-type");
    if (contentType) {
      headers.set("Content-Type", contentType);
    }

    const method = request.method;
    const body =
      method === "GET" || method === "HEAD"
        ? undefined
        : await request.arrayBuffer();

    const backendResponse = await fetch(
      `${API_BASE_URL}/${backendPath}${query}`,
      {
        method,
        headers,
        body,
        cache: "no-store",
      }
    );

    return new NextResponse(backendResponse.body, {
      status: backendResponse.status,
      headers: {
        "Content-Type":
          backendResponse.headers.get("content-type") ||
          "application/json",
      },
    });
  } catch {
    return NextResponse.json(
      { detail: "Unable to connect to the backend service." },
      { status: 502 }
    );
  }
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const PATCH = proxyRequest;
export const DELETE = proxyRequest;
