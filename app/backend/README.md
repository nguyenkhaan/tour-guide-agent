# Tour Guide Agent Backend

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1%2B-D71F00?logo=sqlalchemy&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)

Backend API for the Tour Guide Agent.

## Folder structure

```text
backend/
├── .env.example          # Environment variable template
├── alembic/              # Database migrations
├── main.py               # Local development entry point
├── net.http              # API request examples
├── pyproject.toml        # Python dependencies and project settings
└── src/
    ├── api/
    │   ├── exceptions/   # Application error types
    │   ├── https/        # Exception handlers and API helpers
    │   ├── middlewares/  # Request ID, authentication, and role checks
    │   └── settings/     # Environment configuration
    ├── bases/
    │   └── enums/        # Shared enums
    ├── models/           # SQLAlchemy database models
    ├── modules/          # Feature modules
    │   ├── admin/
    │   ├── auth/
    │   ├── health/
    │   └── .../
    ├── services/         # Shared services, including JWT handling
    ├── test/             # Unit tests
    ├── app.py            # FastAPI application
    └── db.py             # Database engine and sessions
```

## How to setup

Install [uv](https://docs.astral.sh/uv/) if it is not already available, then run the commands from the backend folder.

```bash
cd app/backend
cp .env.example .env
uv sync
uv run main.py
```

Update `.env` with your PostgreSQL connection string and separate JWT secrets before starting the API.

The server runs at <http://localhost:4000>. Open <http://localhost:4000/docs> for Swagger UI.

Use [`net.http`](net.http) to send example requests from an HTTP client extension such as VS Code REST Client.
