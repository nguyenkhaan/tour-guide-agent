from src.models.base_model import AccountStatus, UserRole
from pydantic import BaseModel
from datetime import datetime 
from uuid import UUID
class AdminBase(BaseModel): 
    message: str 
    path: str # Dung de dinh huong nguoi dung den route lay thong tin chi tiet ve nguoi dung do 

class GetAdminUserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str | None
    status: AccountStatus | None
    role: UserRole | None
    created_at : datetime
    updated_at: datetime 

class PutAssignRoleRequest(BaseModel): 
    role : UserRole 

class PutAssignRoleResponse(AdminBase): 
    """
        Update user's role 
    """

class PutUserStatusRequest(BaseModel): 
    status: AccountStatus 

class PutUserStatusResponse(AdminBase): 
    """
        Update user's status 
        Code tay chu meo phai AI code nhe may con ga 
    """
