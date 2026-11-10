"use client";

import { useEffect, useState, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";

const publicPaths = ["/login", "/register", "/forgot-password"];

export default function AuthGuard({
  children,
}: {
  children: ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const isPublic = publicPaths.includes(pathname);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (isPublic) {
      return;
    }

    let active = true;
    

    async function checkAuthentication() {
      try {
        const response = await fetch("/api/auth/me", {
          method: "GET",
          cache: "no-store",
        });

        if (!response.ok) {
          if (active) {
            router.replace("/login");
          }
          return;
        }

        if (active) {
          setAuthorized(true);
        }
      } catch {
        if (active) {
          router.replace("/login");
        }
      }
    }

    checkAuthentication();

    return () => {
      active = false;
    };
  }, [pathname, router, isPublic]);

  if (isPublic) {
  return <>{children}</>;
}

if (!authorized) {
  return null;
}

  return <>{children}</>;
}