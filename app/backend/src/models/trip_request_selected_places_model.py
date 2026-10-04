from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class TripRequestSelectedPlaces(Base):
    __tablename__ = "trip_request_selected_places"

    # Khóa chính bảng nối
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc yêu cầu chuyến đi
    trip_request_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), index=True, nullable=True)
    # Địa điểm được chọn
    place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    # Trạng thái lựa chọn
    selection_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Lý do hoặc ghi chú
    selection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Thời điểm tương tác
    created_at: Mapped[datetime] = created_timestamp()
