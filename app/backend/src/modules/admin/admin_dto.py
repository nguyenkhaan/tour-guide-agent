from src.models.base_model import AccountStatus, UserRole
from pydantic import BaseModel
from datetime import datetime 
class GetAdminUserResponse(BaseModel):
    email: str
    full_name: str
    status: AccountStatus
    role: UserRole
    created_at : datetime
    updated_at: datetime 
