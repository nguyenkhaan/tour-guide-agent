from fastapi import APIRouter, Depends
from src.modules.admin.admin_dependency import get_admin_service
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dto import GetAdminUserResponse
from typing import List 
admin_router = APIRouter(
    prefix = "/admin"
)

@admin_router.get("/users", response_model=List[GetAdminUserResponse]) 
async def getAdminUsers(
    service : AdminService = Depends(get_admin_service)
): 
    return (await service.get_admin_users())