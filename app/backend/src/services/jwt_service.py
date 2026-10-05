from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.api.exceptions.error import UnauthenticatedException
from src.api.settings.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ACCESS_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from src.bases.enums.jwt_token_type import TokenType

_TOKEN_SETTINGS = {
    TokenType.ACCESS_TOKEN: (
        JWT_ACCESS_SECRET_KEY,
        ACCESS_TOKEN_EXPIRE_MINUTES,
    ),
    TokenType.REFRESH_TOKEN: (
        JWT_REFRESH_SECRET_KEY,
        REFRESH_TOKEN_EXPIRE_MINUTES,
    ),
}


def create_jwt_token(payload: dict[str, Any], token_type: TokenType) -> str:
    secret_key, expire_minutes = _TOKEN_SETTINGS[token_type]
    now = datetime.now(timezone.utc)
    token_payload = {
        "sub": payload["sub"],
        "purpose": token_type.value,
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }
    return jwt.encode(token_payload, secret_key, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str, token_type: TokenType) -> dict[str, Any]:
    secret_key, _ = _TOKEN_SETTINGS[token_type]
    try:
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthenticatedException(
            message="Token has expired. Please log in again"
        )
    except jwt.PyJWTError:
        raise UnauthenticatedException(message="Invalid token")

    if payload.get("purpose") != token_type.value or not payload.get("sub"):
        raise UnauthenticatedException(message="Invalid token purpose")
    return payload
