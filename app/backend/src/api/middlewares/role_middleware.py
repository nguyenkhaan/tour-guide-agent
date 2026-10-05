from collections.abc import Callable

from fastapi import Depends

from src.api.exceptions.error import ForbiddenException
from src.api.middlewares.auth_middleware import get_current_user
from src.models.base_model import UserRole
from src.models.users_model import Users


def require_role(*allowed_roles: UserRole) -> Callable:
    async def role_checker(
        current_user: Users = Depends(get_current_user),
    ) -> Users:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                message="You do not have permission to access this resource"
            )
        return current_user

    return role_checker
