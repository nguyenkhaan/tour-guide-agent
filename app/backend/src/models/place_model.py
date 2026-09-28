"""
Models: place_categories và places (refactored)

Cập nhật places để khớp với schema đã chốt trong DATABASE_AFTER_FIX.txt.
place_categories: SERIAL PK (lookup table), không dùng UUID.
places: UUID PK, có full-text slug, pricing NUMERIC(15,2), GiST spatial index.
"""
import uuid
import datetime

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import (
    Boolean, Float, ForeignKey, Index, Integer, Numeric,
    String, Text,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class PlaceCategory(TimestampMixin, Base):
    """
    Bảng `place_categories` — danh mục phân loại địa điểm.

    SERIAL PK (Integer auto-increment) vì đây là lookup table nhỏ,
    không cần UUID.
    """
    __tablename__ = "place_categories"

    # Override UUID PK → SERIAL (Integer)
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="SERIAL PK — lookup table",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Tên phân loại địa điểm",
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="URL-friendly identifier",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Mô tả chi tiết phân loại",
    )

    # created_at from TimestampMixin (no updated_at needed for category)
    updated_at: Mapped[datetime.datetime | None] = mapped_column(  # type: ignore[assignment]
        nullable=True,
        default=None,
        comment="Cập nhật gần nhất",
    )

    places: Mapped[list["Place"]] = relationship(
        "Place",
        back_populates="category",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"PlaceCategory(id={self.id}, slug={self.slug})"


class Place(TimestampMixin, Base):
    """
    Bảng `places` — catalog địa điểm du lịch.

    - location: GEOGRAPHY(Point, 4326) với GiST index.
    - min_price/max_price: NUMERIC(15,2) theo convention tiền tệ Phase 2.
    - images/opening_hours/visual_attributes: JSONB.
    """
    __tablename__ = "places"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )

    category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("place_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="FK → place_categories.id",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Tên địa điểm",
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="Slug nhận diện duy nhất — URL safe",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Mô tả địa điểm",
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Địa chỉ thực tế",
    )

    location: Mapped[WKBElement] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False,
        comment="Tọa độ địa lý WGS84 — GiST index",
    )

    province: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="Tỉnh hoặc Thành phố",
    )

    opening_hours: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Giờ mở/đóng cửa theo ngày trong tuần (JSONB)",
    )

    # Currency convention: NUMERIC(15,2) + VARCHAR(3)
    min_price: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
        comment="Giá vé tối thiểu — NUMERIC(15,2)",
    )

    max_price: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
        comment="Giá vé tối đa — NUMERIC(15,2)",
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="VND",
        server_default="VND",
        comment="Đơn vị tiền tệ — ISO 4217",
    )

    average_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Điểm trung bình đánh giá",
    )

    images: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Danh sách ảnh (object_key, alt...) — JSONB",
    )

    visual_attributes: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Đặc điểm ảnh do Vision tool trích xuất (JSONB)",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Địa điểm có đang hoạt động không",
    )

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        nullable=True,
        comment="UUID admin tạo địa điểm",
    )

    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        nullable=True,
        comment="UUID admin cập nhật gần nhất",
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    category: Mapped["PlaceCategory"] = relationship(
        "PlaceCategory",
        back_populates="places",
        lazy="select",
    )

    narrations: Mapped[list["PlaceNarration"]] = relationship(
        "PlaceNarration",
        back_populates="place",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # ── Table-level indexes ────────────────────────────────────────────────────
    __table_args__ = (
        # GiST spatial index — required for PostGIS operators
        Index(
            "ix_places_location",
            "location",
            postgresql_using="gist",
        ),
        Index("ix_places_is_active", "is_active"),
        Index("ix_places_province", "province"),
    )

    def __repr__(self) -> str:
        return f"Place(id={self.id}, name={self.name})"


class PlaceNarration(Base):
    """
    Bảng `place_narrations` — bài thuyết minh audio cho địa điểm.
    """
    __tablename__ = "place_narrations"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    place_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("places.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    audio_object_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    created_by: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    place: Mapped["Place"] = relationship("Place", back_populates="narrations", lazy="select")

    def __repr__(self) -> str:
        return f"PlaceNarration(id={self.id}, place_id={self.place_id})"