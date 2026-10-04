from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, updated_timestamp


class Places(Base):
    __tablename__ = "places"
    __table_args__ = (
        CheckConstraint("min_price >= 0", name="min_price_range"),
        CheckConstraint("max_price >= 0", name="max_price_range"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="currency_format"),
        Index("ix_places_location", "location", postgresql_using="gist"),
        CheckConstraint("max_price >= min_price", name="price_order"),
    )

    # Định danh địa điểm
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Danh mục phân loại
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("place_categories.id"), index=True, nullable=True)
    # Tên địa điểm
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Slug nhận diện duy nhất
    slug: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    # Mô tả địa điểm
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Địa chỉ thực tế
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Tọa độ địa lý WGS84
    location: Mapped[WKBElement | None] = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False), nullable=True)
    # Tỉnh hoặc Thành phố
    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Giờ mở và đóng cửa
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Giá vé tối thiểu
    min_price: Mapped[Decimal | None] = mapped_column(Numeric(12,2), nullable=True)
    # Giá vé tối đa
    max_price: Mapped[Decimal | None] = mapped_column(Numeric(12,2), nullable=True)
    # Đơn vị tiền tệ
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    average_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    images: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Đặc điểm hình ảnh của địa điểm do Vision tool trích xuất
    visual_attributes: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Admin thêm địa điểm
    created_by: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Admin cập nhật gần nhất
    updated_by: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Thời điểm tạo
    created_at: Mapped[datetime] = created_timestamp()
    # Cập nhật gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
