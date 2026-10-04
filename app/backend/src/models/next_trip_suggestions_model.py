from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class NextTripSuggestions(Base):
    __tablename__ = "next_trip_suggestions"
    __table_args__ = (
        CheckConstraint("rank BETWEEN 1 AND 3", name="rank_range"),
        CheckConstraint("estimated_budget >= 0", name="estimated_budget_range"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="currency_format"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    trip_summary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_summaries.id"), index=True, nullable=True)
    # Thứ tự từ 1 đến 3
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Danh sách nhỏ chỉ dùng để hiển thị một suggestion card
    suggested_places: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    estimated_budget: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    # Phiên hội thoại được tạo từ gợi ý
    started_agent_session_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_session.id"), index=True, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
