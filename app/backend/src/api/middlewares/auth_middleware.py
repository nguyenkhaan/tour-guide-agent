from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.exceptions.error import ForbiddenException, UnauthenticatedException
from src.bases.enums.jwt_token_type import TokenType
from src.models.base_model import AccountStatus
from src.models.users_model import Users
from src.modules.auth.auth_dependency import get_auth_service
from src.modules.auth.auth_service import AuthService
from src.services.jwt_service import verify_jwt_token

access_token_scheme = HTTPBearer(
    scheme_name="Access Token",
    bearerFormat="JWT",
    auto_error=False,
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(access_token_scheme),
    service: AuthService = Depends(get_auth_service),
) -> Users:
    if credentials is None:
        raise UnauthenticatedException(message="Authentication token was not provided")

    payload = verify_jwt_token(credentials.credentials, TokenType.ACCESS_TOKEN)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthenticatedException(message="Invalid token payload")

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise UnauthenticatedException(
            message="The user ID in the token is not a valid UUID"
        )

    user = await service.db.get(Users, user_id)
    if user is None:
        raise UnauthenticatedException(message="User account does not exist")

    if user.status == AccountStatus.BANNED:
        raise ForbiddenException(message="Your account has been banned")
    if user.status == AccountStatus.DISABLED:
        raise ForbiddenException(message="Your account has been disabled")

    return user
