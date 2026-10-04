from fastapi import APIRouter, Depends
from src.modules.admin.admin_dependency import get_admin_service
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dto import GetAdminUserResponse
from typing import List 
admin_router = APIRouter(
    prefix = "/admin", 
    tags = ["Admin"]
)

@admin_router.get("/users", response_model=List[GetAdminUserResponse] , summary="Get all users in system") 
async def get_admin_users_handler(
    service : AdminService = Depends(get_admin_service)
): 
    return (await service.get_admin_users_handler())