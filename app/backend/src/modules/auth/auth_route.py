from fastapi import APIRouter, Depends, status

from src.api.middlewares.auth_middleware import get_current_user
from src.models.users_model import Users
from src.modules.auth.auth_dependency import get_auth_service
from src.modules.auth.auth_dto import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)
from src.modules.auth.auth_service import AuthService

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(
    req: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> RegisterResponse:
    return await service.register_user(req)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Log in to an account",
)
async def login(
    req: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await service.login_user(req)


@auth_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the current user's information",
)
async def get_me(
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Log out of the system",
)
async def logout(
    current_user: Users = Depends(get_current_user),
) -> dict[str, str]:
    return {"message": "Logged out successfully"}
