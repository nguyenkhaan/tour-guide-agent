from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, created_timestamp, updated_timestamp


class UserProfile(Base):
    __tablename__ = "user_profile"
    __table_args__ = (
        CheckConstraint("default_budget > 0", name="default_budget_range"),
        CheckConstraint("preferred_currency ~ '^[A-Z]{3}$'", name="preferred_currency_format"),
    )

    # Khóa chính và ngoại liên kết 1-1 với người dùng
    user_id: Mapped[UUIDValue] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    # Sở thích và phong cách du lịch
    travel_preferences: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Nhu cầu đặc biệt của người dùng
    special_needs: Mapped[str | None] = mapped_column(Text, nullable=True)
    # > 0
    default_budget: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
    # Đơn vị tiền tệ mặc định
    preferred_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    # Thời điểm cập nhật hồ sơ gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
