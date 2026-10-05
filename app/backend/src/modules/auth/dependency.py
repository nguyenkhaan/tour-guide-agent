from typing import Callable
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.error import ForbiddenException, UnauthenticatedException
from src.db import get_async_db_session
from src.models.base_model import AccountStatus, UserRole
from src.models.users_model import Users
from src.modules.auth.service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_db_session),
) -> Users:
    if not token:
        raise UnauthenticatedException(message="Chưa cung cấp token xác thực")

    payload = AuthService.decode_access_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthenticatedException(message="Payload token không hợp lệ")

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise UnauthenticatedException(message="User ID trong token không đúng định dạng UUID")

    user = await session.get(Users, user_id)
    if user is None:
        raise UnauthenticatedException(message="Tài khoản không tồn tại trong hệ thống")

    if user.status == AccountStatus.BANNED:
        raise ForbiddenException(message="Tài khoản của bạn đã bị khóa")
    if user.status == AccountStatus.DISABLED:
        raise ForbiddenException(message="Tài khoản của bạn đã bị vô hiệu hóa")

    return user


def require_roles(*allowed_roles: UserRole) -> Callable:
    async def role_checker(current_user: Users = Depends(get_current_user)) -> Users:
        if current_user.role not in allowed_roles:
            role_names = ", ".join([r.value for r in allowed_roles])
            raise ForbiddenException(
                message=f"Bạn không có quyền truy cập. Yêu cầu quyền: {role_names}"
            )
        return current_user

    return role_checker
