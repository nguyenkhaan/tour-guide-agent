from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_db_session
from src.modules.auth.auth_service import AuthService


def get_auth_service(
    db: AsyncSession = Depends(get_async_db_session),
) -> AuthService:
    return AuthService(db)
