"""
Model: user_profile

Hồ sơ mở rộng của người dùng — quan hệ 1-1 với users.
user_id vừa là PK vừa là FK → users.id (shared primary key pattern).

Conventions:
- default_budget: NUMERIC(15,2) — tuân thủ quy tắc tiền tệ Phase 2
- preferred_currency: VARCHAR(3) ISO 4217 (VND, USD, EUR...)
- travel_preferences: JSONB — bán cấu trúc, dễ extend
"""
import uuid
import datetime

from sqlalchemy import String, Text, Numeric, ForeignKey, Index
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym

from src.models.base_model import Base, TimestampMixin


class UserProfile(TimestampMixin, Base):
    """
    Bảng `user_profile` — thông tin hồ sơ và sở thích người dùng.

    Primary key = user_id (cùng UUID với users.id) → 1-1 relationship.
    """
    __tablename__ = "user_profile"

    # user_id là PK và FK đồng thời — shared primary key pattern
    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        comment="PK = FK → users.id (1-1 relationship)",
    )

    # Alias user_id <-> id để tương thích 100% với ERD dbdiagram và code nghiệp vụ
    user_id = synonym("id")

    def __init__(self, *args, user_id: uuid.UUID | None = None, **kwargs):
        if user_id is not None:
            kwargs["id"] = user_id
        super().__init__(*args, **kwargs)

    travel_preferences: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Sở thích và phong cách du lịch (JSONB)",
    )

    special_needs: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Nhu cầu đặc biệt (dị ứng, khuyết tật, ...)",
    )

    # NUMERIC(15,2): đủ cho VND (tối đa 999_999_999_999_999.99)
    default_budget: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
        comment="Ngân sách mặc định — NUMERIC(15,2), luôn > 0 nếu có",
    )

    # ISO 4217: VND, USD, EUR...
    preferred_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="VND",
        server_default="VND",
        comment="Đơn vị tiền tệ mặc định — ISO 4217 (3 ký tự)",
    )

    # ── Relationship ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"UserProfile(user_id={self.id}, currency={self.preferred_currency})"


# Avoid circular import
from src.models.user_model import User  # noqa: E402
