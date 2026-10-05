from uuid import UUID

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions.error import (
    BadRequestException,
    ForbiddenException,
    UnauthenticatedException,
)
from src.bases.enums.jwt_token_type import TokenType
from src.models.base_model import AccountStatus, UserRole
from src.models.users_model import Users
from src.modules.auth.auth_dto import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)
from src.services.jwt_service import create_jwt_token

password_hash = PasswordHash((BcryptHasher(),))


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)

    async def register_user(self, req: RegisterRequest) -> RegisterResponse:
        stmt = select(Users).where(Users.email == req.email)
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            raise BadRequestException(message="This email is already registered")

        hashed_pwd = self.hash_password(req.password)
        new_user = Users(
            email=req.email,
            password=hashed_pwd,
            full_name=req.full_name,
            status=AccountStatus.ACTIVE, # Thuc hien verify lai sau bang cach gui email chua ma xac thuc den tai khoan email do
            role=UserRole.USER,
        )

        self.db.add(new_user)
        await self.db.commit()
        return RegisterResponse(
            message="User registered successfully",
            path="/auth/login",
        )

    async def login_user(self, req: LoginRequest) -> TokenResponse:
        stmt = select(Users).where(Users.email == req.email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if (
            user is None
            or user.password is None
            or not self.verify_password(req.password, user.password)
        ):
            raise UnauthenticatedException(message="Incorrect email or password")

        if user.status == AccountStatus.BANNED:
            raise ForbiddenException(message="Your account has been banned")
        if user.status == AccountStatus.DISABLED:
            raise ForbiddenException(message="Your account has been disabled")

        token_payload = {"sub": str(user.id)}
        access_token = create_jwt_token(token_payload, TokenType.ACCESS_TOKEN)
        refresh_token = create_jwt_token(token_payload, TokenType.REFRESH_TOKEN)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        user = await self.db.get(Users, user_id)
        if user is None:
            raise UnauthenticatedException(message="User information was not found")
        return UserResponse.model_validate(user)
