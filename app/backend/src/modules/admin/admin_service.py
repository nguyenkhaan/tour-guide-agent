import datetime

from src.modules.admin.admin_dto import GetAdminUserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.models.base_model import AccountStatus, UserRole
class AdminService: 
    def __init__(self, db: AsyncSession): 
        self.db = db
    async def get_admin_users(self) -> List[GetAdminUserResponse]: 
        return [
            GetAdminUserResponse(
                email="nguyenkhaan2006@gmail.com",
                full_name="Cloudian", 
                status = AccountStatus.ACTIVE,
                role = UserRole.ADMIN,
                created_at=datetime.datetime.now(), 
                updated_at=datetime.datetime.now()
            ), 
            GetAdminUserResponse(
                email="nguyenkhaan2006@gmail.com",
                full_name="Cloudian", 
                status = AccountStatus.ACTIVE,
                role = UserRole.ADMIN,
                created_at=datetime.datetime.now(), 
                updated_at=datetime.datetime.now()
            )
        ]