from datetime import datetime, time
from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, Text, Time, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, updated_timestamp


class ItineraryActivities(Base):
    __tablename__ = "itinerary_activities"
    __table_args__ = (
        CheckConstraint("order_index >= 0", name="order_index_nonnegative"),
        CheckConstraint("estimated_cost >= 0", name="estimated_cost_range"),
    )

    # Định danh hoạt động
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc ngày nào
    itinerary_day_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_days.id"), index=True, nullable=True)
    # Tham chiếu đến places.id
    place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    # Thứ tự thực hiện
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Tên hoạt động
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Phân loại hoạt động
    activity_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Mô tả chi tiết
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Giờ bắt đầu dự kiến
    start_time: Mapped[time | None] = mapped_column(Time(timezone=False), nullable=True)
    # Giờ kết thúc dự kiến
    end_time: Mapped[time | None] = mapped_column(Time(timezone=False), nullable=True)
    # Chi phí dự trù hoạt động
    estimated_cost: Mapped[Decimal | None] = mapped_column(Numeric(12,2), nullable=True)
    # Thời điểm tạo
    created_at: Mapped[datetime] = created_timestamp()
    # Cập nhật gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
