"""
FastAPI application entrypoint.

Lifespan: kiểm tra kết nối DB khi startup, dispose engine khi shutdown.
Routers: tất cả API modules được mount vào /api prefix.
"""
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from sqlalchemy import text

from src.db import engine
from src.api.settings.config import DATABASE_URL, APP_ENV

# ── Module routers ────────────────────────────────────────────────────────────
from src.modules.health.health_route import health_router


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: verify DB connection.
    Shutdown: dispose connection pool gracefully.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print(f"[{APP_ENV}] ✅ PostgreSQL connected")
    except Exception as e:
        print(f"[{APP_ENV}] ❌ PostgreSQL connection failed: {e}")
        raise

    yield

    await engine.dispose()
    print(f"[{APP_ENV}] 🔌 PostgreSQL disconnected")


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Tour Guide Agent API",
    description="Backend API for AI-powered tour guide agent",
    version="0.1.0",
    lifespan=lifespan,
)

# ── API Router ─────────────────────────────────────────────────────────────────
api_router = APIRouter(prefix="/api")

# Health check (always first)
api_router.include_router(health_router)

app.include_router(api_router)