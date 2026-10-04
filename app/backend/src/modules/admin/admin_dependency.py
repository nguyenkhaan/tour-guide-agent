
from src.modules.admin.admin_service import AdminService
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import Depends
from src.db import get_async_db_session
def get_admin_service(
    db : AsyncSession = Depends(get_async_db_session)
) -> AdminService: 
    return AdminService(db)