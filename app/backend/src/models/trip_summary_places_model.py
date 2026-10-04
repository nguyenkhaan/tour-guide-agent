from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    SummaryPlaceStatus,
)


class TripSummaryPlaces(Base):
    __tablename__ = "trip_summary_places"
    __table_args__ = (
        CheckConstraint("confidence BETWEEN 0 AND 1", name="confidence_range"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    trip_summary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_summaries.id"), index=True, nullable=True)
    # Có thể null nếu địa điểm không có bản ghi tương ứng trong places
    place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    # Tên địa điểm, dùng khi place_id là null
    place_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str | None] = mapped_column(SummaryPlaceStatus, nullable=True)
    # Độ tin cậy khi hệ thống tự phân loại
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(3,2), nullable=True)
    # GPS, tương tác hoặc xác nhận dùng để phân loại
    evidence: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    is_user_corrected: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
