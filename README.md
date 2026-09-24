# Tour Guide Agent

## Overview

Tour Guide Agent is a Vietnamese travel-planning application for independent travelers in Vietnam. It helps users describe a trip in natural language, discover destinations, compare feasible itineraries, receive booking guidance, use an in-trip companion, and complete a trip summary.

The product is a modular monolith:

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, and Bun.
- **Backend:** Python, FastAPI, AI orchestration, PostgreSQL/PostGIS, and Object Storage.
- **AI Agents:** Planner, Critic/Evaluator, and Booking & Logistics only.

The system never books or pays for services on the user's behalf. GPS, original media, temporary AI memory, and detailed technical logs expire after at most seven days.

## Backend Folder Structure

```text
app/backend/
├── main.py                 # Current runnable backend entry point
├── pyproject.toml          # Python and uv project configuration
├── src/
│   ├── api/                # Shared HTTP, SSE, middleware, and error handling
│   ├── module/             # Feature modules: auth, trip, itinerary, review, etc.
│   └── ai/                 # Agents and external-provider adapters
└── uv.lock
```

`api/` is the HTTP boundary. Feature business logic belongs in `module/`; AI-specific logic belongs in `ai/`.

## Frontend Folder Structure

```text
app/frontend/
├── src/
│   ├── app/                # React entry point and application shell
│   ├── features/           # Feature-first pages and API adapters
│   └── shared/             # Shared API, UI, utility, and style code
├── tests/e2e/              # End-to-end tests
├── package.json
├── vite.config.ts
├── tsconfig.json
└── bun.lock
```

Each frontend feature maps to a backend module and is delivered as a vertical slice: UI, API contract, backend logic, and tests move together.

## How to Start the Frontend

Requirements: [Bun](https://bun.sh/) 1.3 or later.

```bash
cd app/frontend
bun install
bun run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`.

For a production build:

```bash
cd app/frontend
bun run build
bun run preview
```

## How to Start the Backend

Requirements: Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
cd app/backend
uv sync
uv run main.py
```
