import datetime
from uuid import UUID

from fastapi import HTTPException
from models.users_model import Users
from sqlalchemy import select

from src.modules.admin.admin_dto import (
    GetAdminUserResponse,
    PutAssignRoleRequest,
    PutAssignRoleResponse,
    PutUserStatusRequest,
    PutUserStatusResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.models.base_model import AccountStatus, UserRole
class AdminService: 
    def __init__(self, db: AsyncSession): 
        self.db = db
    async def get_admin_users(self, limit: int, offset: int) -> List[GetAdminUserResponse]: 
        stmt = select(Users).order_by(Users.created_at.desc()).limit(limit).offset(offset) 
        user_lists = (await self.db.execute(stmt)).scalars().all() 
        return [
            GetAdminUserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                status=user.status,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in user_lists
        ]
    async def put_assign_role(self, user_id : UUID, data : PutAssignRoleRequest) -> PutAssignRoleResponse: 
        try: 
            user = await self.db.get(Users, user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            user.role = data.role
            await self.db.commit()
            return PutAssignRoleResponse(
                message="User role updated successfully",
                path=f"/api/user/{user_id}",
            )
        except Exception as e: 
            await self.db.rollback() 
            raise e 
    async def put_user_status(self, user_id: UUID, data : PutUserStatusRequest) -> PutUserStatusResponse: 
        try: 
            user = await self.db.get(Users, user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            user.status = data.status
            await self.db.commit()
            return PutUserStatusResponse(
                message="User status updated successfully",
                path=f"/api/user/{user_id}",
            )
        except Exception as e: 
            await self.db.rollback() 
            raise e 
