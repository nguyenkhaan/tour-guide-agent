from fastapi import APIRouter, Depends

from src.api.exceptions.error import NotFoundException
from src.api.middlewares.auth_middleware import get_current_user
from src.api.middlewares.role_middleware import require_role
from src.models.base_model import UserRole
from src.models.users_model import Users

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("")
async def liveness() -> str:
    return "Hello world. Build with Cloudian 💙 Cloud"


@health_router.get("/auth-test", summary="Test access-token authentication")
async def authentication_test(
    current_user: Users = Depends(get_current_user),
) -> dict[str, str]:
    return {
        "message": "Authentication succeeded",
        "user_id": str(current_user.id),
    }


@health_router.get("/role-test", summary="Test admin role authorization")
async def role_authorization_test(
    current_user: Users = Depends(require_role(UserRole.ADMIN)),
) -> dict[str, str]:
    return {
        "message": "Admin role authorization succeeded",
        "user_id": str(current_user.id),
    }


@health_router.get("/exception-test", summary="Test the not-found exception response")
async def exception_test() -> None:
    raise NotFoundException(
        message="This endpoint intentionally raises a not-found exception"
    )
