from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.base_model import AccountStatus, UserRole


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password (minimum 6 characters)",
    )
    full_name: str | None = Field(
        default=None,
        max_length=200,
        description="User's full name",
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class RegisterResponse(BaseModel):
    message: str
    path: str


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
    refresh_token: str
