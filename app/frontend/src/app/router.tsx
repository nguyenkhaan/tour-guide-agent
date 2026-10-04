import { useEffect, useState } from "react";
import AdminUsersPage from "@/features/admin-user/AdminUsersPage";

export type RoutePath = "/admin/users" | "/";

export function useRouter() {
  const [currentPath, setCurrentPath] = useState<string>(() => {
    return typeof window !== "undefined" ? window.location.pathname : "/admin/users";
  });

  useEffect(() => {
    const handlePopState = () => {
      setCurrentPath(window.location.pathname);
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const navigate = (path: string) => {
    if (typeof window !== "undefined") {
      window.history.pushState({}, "", path);
      setCurrentPath(path);
    }
  };

  return { currentPath, navigate };
}

export function AppRouter() {
  const { currentPath } = useRouter();

  // If path is root or /admin/users, render AdminUsersPage (SCR-28)
  if (currentPath === "/admin/users" || currentPath === "/" || currentPath.startsWith("/admin")) {
    return <AdminUsersPage />;
  }

  // Fallback to AdminUsersPage as default active screen
  return <AdminUsersPage />;
}
