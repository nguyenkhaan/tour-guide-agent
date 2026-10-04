from datetime import date, datetime
from uuid import UUID as UUIDValue

from sqlalchemy import Boolean, Date, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, updated_timestamp


class Trips(Base):
    __tablename__ = "trips"

    # Mã định danh chuyến đi
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Người thực hiện chuyến đi
    user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Yêu cầu chuyến đi ban đầu
    trip_request_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), index=True, nullable=True)
    # Lộ trình chốt cuối cùng
    finalized_itinerary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id"), index=True, nullable=True)
    # Trạng thái vòng đời
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Đồng ý chia sẻ GPS
    gps_consent: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Ngày bắt đầu thực tế
    actual_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Ngày kết thúc thực tế
    actual_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Thời điểm kích hoạt
    created_at: Mapped[datetime] = created_timestamp()
    # Cập nhật gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
