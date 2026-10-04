from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    TripRequestStatus,
)


class TripRequests(Base):
    __tablename__ = "trip_requests"
    __table_args__ = (
        CheckConstraint("version > 0", name="version_positive"),
        CheckConstraint("duration_days > 0", name="duration_days_positive"),
        CheckConstraint("budget >= 0", name="budget_range"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="currency_format"),
        CheckConstraint("companions_count >= 0", name="companions_count_nonnegative"),
        Index("ix_trip_requests_origin_location", "origin_location", postgresql_using="gist"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    # Liên kết phiên bản yêu cầu trước đó
    parent_trip_request_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), index=True, nullable=True)
    user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    agent_session_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_session.id"), index=True, nullable=True)
    status: Mapped[str | None] = mapped_column(TripRequestStatus, nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Tên địa điểm xuất phát
    origin_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Tọa độ điểm xuất phát
    origin_location: Mapped[WKBElement | None] = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False), nullable=True)
    # Điểm đến hoặc khu vực người dùng mong muốn
    destination_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Ngày khởi hành
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Thời lượng chuyến đi
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Tổng mức ngân sách dự kiến
    budget: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
    # Đơn vị tiền tệ
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    # Số lượng người đi cùng
    companions_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Thông tin người đi cùng
    companions_info: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Sở thích riêng chỉ định
    preferences: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Thời điểm xác nhận chốt tóm tắt
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Thời điểm tạo yêu cầu
    created_at: Mapped[datetime] = created_timestamp()
    # Cập nhật gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
