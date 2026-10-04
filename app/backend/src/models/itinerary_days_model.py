from datetime import datetime
from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class ItineraryDays(Base):
    __tablename__ = "itinerary_days"
    __table_args__ = (
        CheckConstraint("day_number > 0", name="day_number_positive"),
        CheckConstraint("estimated_total_cost >= 0", name="estimated_total_cost_range"),
    )

    # Định danh ngày
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc lộ trình nào
    itinerary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id"), index=True, nullable=True)
    # Ngày thứ mấy trong chuyến đi
    day_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Ngay da len ke hoach
    created_at: Mapped[datetime] = created_timestamp()
    # Tiêu đề ngày
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Mô tả trải nghiệm chính
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Dự trù chi phí ngày
    estimated_total_cost: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
