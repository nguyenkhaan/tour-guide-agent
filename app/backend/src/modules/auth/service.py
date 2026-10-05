from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.error import (
    BadRequestException,
    ForbiddenException,
    UnauthenticatedException,
)
from src.api.settings.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)
from src.models.base_model import AccountStatus
from src.models.users_model import Users
from src.modules.auth.dto import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

password_hash = PasswordHash.recommended()

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": now,
        })
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthenticatedException(message="Token đã hết hạn, vui lòng đăng nhập lại")
        except jwt.PyJWTError:
            raise UnauthenticatedException(message="Token không hợp lệ")

    @classmethod
    async def register_user(cls, session: AsyncSession, req: RegisterRequest) -> TokenResponse:
        stmt = select(Users).where(Users.email == req.email)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            raise BadRequestException(message="Email này đã được đăng ký tài khoản")

        hashed_pwd = cls.hash_password(req.password)
        new_user = Users(
            email=req.email,
            password=hashed_pwd,
            full_name=req.full_name,
            status=AccountStatus.ACTIVE,
            role=req.role,
        )

        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)

        token_payload = {
            "sub": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role.value if new_user.role else "USER",
        }
        access_token = cls.create_access_token(token_payload)

        user_dto = UserResponse.model_validate(new_user)
        return TokenResponse(access_token=access_token, user=user_dto)

    @classmethod
    async def login_user(cls, session: AsyncSession, req: LoginRequest) -> TokenResponse:
        stmt = select(Users).where(Users.email == req.email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or user.password is None or not cls.verify_password(req.password, user.password):
            raise UnauthenticatedException(message="Email hoặc mật khẩu không chính xác")

        if user.status == AccountStatus.BANNED:
            raise ForbiddenException(message="Tài khoản của bạn đã bị khóa")
        if user.status == AccountStatus.DISABLED:
            raise ForbiddenException(message="Tài khoản của bạn đã bị vô hiệu hóa")

        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value if user.role else "USER",
        }
        access_token = cls.create_access_token(token_payload)

        user_dto = UserResponse.model_validate(user)
        return TokenResponse(access_token=access_token, user=user_dto)

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: UUID) -> UserResponse:
        user = await session.get(Users, user_id)
        if user is None:
            raise UnauthenticatedException(message="Không tìm thấy thông tin người dùng")
        return UserResponse.model_validate(user)