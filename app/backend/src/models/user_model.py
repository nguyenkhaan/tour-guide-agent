"""
Model: users

Bảng tài khoản người dùng — lưu thông tin xác thực và phân quyền.
Quan hệ:
  - 1-1 với user_profile (profile mở rộng)
  - 1-N với agent_session (các phiên hội thoại với agent)
  - 1-N với trip_requests, trips, place_reviews...
"""
import datetime
import uuid
import enum

from sqlalchemy import String, Enum as SAEnum, Index
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin, SoftDeleteMixin


class AccountStatus(str, enum.Enum):
    DISABLED = "DISABLED"
    BANNED = "BANNED"
    ACTIVE = "ACTIVE"


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class User(SoftDeleteMixin, TimestampMixin, Base):
    """
    Bảng `users` — tài khoản người dùng hệ thống.

    Conventions:
    - email: unique, case-insensitive (nên lowercase trước khi lưu)
    - password: bcrypt hash (không lưu plaintext)
    - status: soft-disable thay vì xóa cứng
    """
    __tablename__ = "users"

    # Override id để giữ tính nhất quán (UUID từ Base)
    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Email đăng nhập — unique, lowercase",
    )

    password: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,                  # Nullable cho OAuth users (Google, Apple...)
        comment="Bcrypt hash của mật khẩu; NULL nếu đăng nhập qua OAuth",
    )

    full_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="Họ tên đầy đủ",
    )

    status: Mapped[AccountStatus] = mapped_column(
        SAEnum(AccountStatus, name="accountstatus", create_type=True),
        nullable=False,
        default=AccountStatus.ACTIVE,
        server_default=AccountStatus.ACTIVE.value,
        comment="Trạng thái tài khoản",
    )

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="userrole", create_type=True),
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        comment="Phân quyền người dùng",
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",
    )

    agent_sessions: Mapped[list["AgentSession"]] = relationship(
        "AgentSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # ── Table-level indexes ────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_users_status", "status"),
        Index("ix_users_role", "role"),
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, role={self.role})"


# Avoid circular import — import here at bottom
from src.models.user_profile_model import UserProfile  # noqa: E402
from src.models.agent_session_model import AgentSession  # noqa: E402
