from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.settings.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL, echo=False, hide_parameters=True, pool_pre_ping=True,
    connect_args={"server_settings": {"timezone": "UTC"}, "timeout": 10},
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@event.listens_for(engine.sync_engine, "begin")
def set_transaction_timezone(connection) -> None:
    connection.exec_driver_sql("SET LOCAL TIME ZONE 'UTC'")


async def check_database_connection() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def get_async_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def transaction() -> AsyncIterator[AsyncSession]:
    async with async_session_maker.begin() as session:
        yield session
