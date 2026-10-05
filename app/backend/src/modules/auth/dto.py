from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.models.base_model import AccountStatus, UserRole

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Địa chỉ email người dùng")
    password: str = Field(..., min_length=6, max_length=100, description="Mật khẩu (tối thiểu 6 ký tự)")
    full_name: str | None = Field(default=None, max_length=200, description="Họ và tên người dùng")
    role: UserRole = Field(default=UserRole.USER, description="Vai trò (USER, OPERATOR, ADMIN)")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Địa chỉ email người dùng")
    password: str = Field(..., description="Mật khẩu người dùng")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    full_name: str | None = None
    status: AccountStatus = AccountStatus.ACTIVE
    role: UserRole = UserRole.USER
    created_at: datetime
    updated_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
