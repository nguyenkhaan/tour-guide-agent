from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key


class ItineraryTransits(Base):
    __tablename__ = "itinerary_transits"
    __table_args__ = (
        CheckConstraint("estimated_duration_minutes >= 0", name="estimated_duration_minutes_nonnegative"),
        CheckConstraint("estimated_distance_km >= 0", name="estimated_distance_km_range"),
        CheckConstraint("estimated_cost >= 0", name="estimated_cost_range"),
    )

    # Định danh chặng di chuyển
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc ngày nào
    itinerary_day_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_days.id"), index=True, nullable=True)
    # Hoạt động xuất phát
    from_activity_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_activities.id"), index=True, nullable=True)
    # Hoạt động đích đến
    to_activity_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_activities.id"), index=True, nullable=True)
    # Phương tiện đề xuất
    transport_mode: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Thời gian di chuyển ước tính
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Cự ly ước tính
    estimated_distance_km: Mapped[Decimal | None] = mapped_column(Numeric(8,2), nullable=True)
    # Chi phí dự trù
    estimated_cost: Mapped[Decimal | None] = mapped_column(Numeric(12,2), nullable=True)
    # Ghi chú cung đường
    route_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
