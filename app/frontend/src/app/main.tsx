//Generate contract api: bunx openapi-typescript http://localhost:4000/openapi.json -o src/types/api-contract.ts
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "@/app/App";
import "@/shared/styles/global.css";

const queryClient = new QueryClient();

const root = document.getElementById("root");

if (!root) {
  throw new Error("Không tìm thấy phần tử #root.");
}

createRoot(root).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
);
