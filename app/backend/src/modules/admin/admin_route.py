from fastapi import APIRouter, Depends
from fastapi import Query 
from src.modules.admin.admin_dependency import get_admin_service
from src.modules.admin.admin_service import AdminService
from src.modules.admin.admin_dto import (
    GetAdminUserResponse, 
    PutAssignRoleRequest, 
    PutAssignRoleResponse,
    PutUserStatusRequest,
    PutUserStatusResponse
)
from typing import List 
from uuid import UUID
admin_router = APIRouter(
    prefix = "/admin", 
    tags = ["Admin"]
)

@admin_router.get("/users", response_model=List[GetAdminUserResponse] , summary="Get all users in system") 
async def get_admin_users_handler(
    limit: int = Query(default=10),
    offset: int = Query(default = 0),   
    service : AdminService = Depends(get_admin_service)
): 
    return (await service.get_admin_users(limit, offset))

@admin_router.put("/users/role/{user_id}" , response_model=PutAssignRoleResponse, summary="Update user role")
async def put_assign_role_handler(
    user_id: UUID,
    data : PutAssignRoleRequest, 
   service : AdminService = Depends(get_admin_service) 
): 
    return (await service.put_assign_role(user_id, data))

@admin_router.put("/users/status/{user_id}" , response_model = PutUserStatusResponse, summary = "Update user status")
async def put_user_status(
    user_id: UUID,
    data: PutUserStatusRequest,
    service : AdminService = Depends(get_admin_service) 
): 
    return (await service.put_user_status(user_id, data))
