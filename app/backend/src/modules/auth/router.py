from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_db_session
from src.models.users_model import Users
from src.modules.auth.dependency import get_current_user
from src.modules.auth.dto import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from src.modules.auth.service import AuthService

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản người dùng mới",
)
async def register(
    req: RegisterRequest,
    session: AsyncSession = Depends(get_async_db_session),
) -> TokenResponse:
    return await AuthService.register_user(session, req)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập tài khoản",
)
async def login(
    req: LoginRequest,
    session: AsyncSession = Depends(get_async_db_session),
) -> TokenResponse:
    return await AuthService.login_user(session, req)


@auth_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin người dùng đang đăng nhập",
)
async def get_me(
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Đăng xuất khỏi hệ thống",
)
async def logout(
    current_user: Users = Depends(get_current_user),
) -> dict[str, str]:
    return {"message": "Đăng xuất thành công"}
