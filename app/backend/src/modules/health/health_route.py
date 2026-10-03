from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_db_session

health_router = APIRouter(
    prefix="/health", tags=["Health"]
)


@health_router.get("")
async def liveness():
    return {
        "status": "ok",
        "service": "Tour Guide Agent API",
    }


@health_router.get("/db")
async def db_health(db: AsyncSession = Depends(get_async_db_session)):
    """Kiểm tra kết nối Database trực tiếp qua AsyncSession và Transaction."""
    try:
        res = await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "check": res.scalar(),
        }
    except Exception as e:
        err_msg = str(e) if str(e).strip() else f"{type(e).__name__} (Database may be waking up from sleep)"
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": err_msg,
        }