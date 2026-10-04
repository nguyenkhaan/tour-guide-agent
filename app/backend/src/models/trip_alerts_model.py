from datetime import datetime
from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UUID,
)
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class TripAlerts(Base):
    __tablename__ = "trip_alerts"
    __table_args__ = (
        CheckConstraint("confidence BETWEEN 0 AND 1", name="confidence_range"),
    )

    # Định danh cảnh báo
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc chuyến đi nào
    trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    # Loại sự cố
    alert_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Mức độ nghiêm trọng
    severity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Tiêu đề cảnh báo
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Nội dung chi tiết
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Nguồn dữ liệu kiểm tra
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Thời điểm kiểm tra thông tin
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Mức độ tin cậy thông tin
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(3,2), nullable=True)
    # Hoạt động bị ảnh hưởng bởi cảnh báo
    affected_activity_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_activities.id"), index=True, nullable=True)
    # Phương án thay thế nếu có
    alternative_proposal_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_proposals.id"), index=True, nullable=True)
    # Trạng thái đã xử lý hoặc xem
    is_resolved: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Thời điểm tạo cảnh báo
    created_at: Mapped[datetime] = created_timestamp()
