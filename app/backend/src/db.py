"""
Database engine, session factory, and transaction helpers.

Convention (Phase 2):
- Sử dụng asyncpg driver qua SQLAlchemy async engine.
- Mọi DB interaction đều qua AsyncSession — không dùng sync engine.
- Transaction: dùng context manager `get_async_db_session` (auto commit/rollback).
- Pool: NullPool cho alembic migrations, QueuePool cho app runtime.
"""
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from src.api.settings.config import DATABASE_URL, APP_DEBUG

# ── Engine ────────────────────────────────────────────────────────────────────
engine = create_async_engine(
    DATABASE_URL,
    echo=APP_DEBUG,          # SQL logging only in dev/debug mode
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,      # Verify connection liveness before use
    pool_recycle=3600,       # Recycle connections every 1 hour
)

# ── Session factory ───────────────────────────────────────────────────────────
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Avoid lazy-load errors after commit in async context
    autoflush=False,         # Explicit flush for predictable behavior
)


# ── FastAPI dependency: auto-commit or rollback ───────────────────────────────
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a DB session.
    - Auto-commits on success.
    - Auto-rolls back on any exception.
    Usage:
        @router.get("/")
        async def handler(db: AsyncSession = Depends(get_async_db_session)):
            ...
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Standalone transaction context manager ────────────────────────────────────
@asynccontextmanager
async def get_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """
    Standalone async context manager for use outside FastAPI dependency injection
    (e.g., background jobs, startup tasks, scripts).

    Usage:
        async with get_db_transaction() as session:
            session.add(some_model)
            # commit happens automatically on exit
    """
    async with async_session_maker() as session:
        async with session.begin():
            yield session