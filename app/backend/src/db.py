import datetime
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.api.settings.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)  

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session_maker() as session:
        yield session