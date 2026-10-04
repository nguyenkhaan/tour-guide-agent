from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    AccountStatus,
    UserRole,
)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUIDValue] = uuid_primary_key()
    # required
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    password: Mapped[str | None] = mapped_column(String(200), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[AccountStatus | None] = mapped_column(nullable=True)
    role: Mapped[UserRole | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
