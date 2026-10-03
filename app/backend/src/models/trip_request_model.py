"""
Models: trip_requests và trip_request_selected_places

trip_requests: yêu cầu chuyến đi từ người dùng.
trip_request_selected_places: địa điểm Agent gợi ý/chọn cho trip request.
"""
import uuid
import datetime
import enum

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import (
    Boolean, Date, Enum as SAEnum, ForeignKey, Index,
    Integer, Numeric, String, Text,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class TripRequestStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    PLANNING = "PLANNING"
    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"


class TripRequest(TimestampMixin, Base):
    """
    Bảng `trip_requests` — yêu cầu lập kế hoạch chuyến đi của người dùng.
    Hỗ trợ versioning qua parent_trip_request_id.
    """
    __tablename__ = "trip_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    parent_trip_request_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("trip_requests.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Liên kết phiên bản yêu cầu trước đó (versioning)",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    agent_session_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("agent_session.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )

    status: Mapped[TripRequestStatus] = mapped_column(
        SAEnum(TripRequestStatus, name="triprequeststatus", create_type=True),
        nullable=False,
        default=TripRequestStatus.DRAFT,
        server_default=TripRequestStatus.DRAFT.value,
    )

    version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        comment="Phiên bản của yêu cầu (tăng mỗi lần revise)",
    )

    origin_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    origin_location: Mapped[WKBElement | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
        comment="Tọa độ điểm xuất phát",
    )

    destination_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    start_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Currency convention
    budget: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default="VND", server_default="VND"
    )

    companions_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    companions_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    preferences: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    confirmed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    selected_places: Mapped[list["TripRequestSelectedPlace"]] = relationship(
        "TripRequestSelectedPlace",
        back_populates="trip_request",
        cascade="all, delete-orphan",
        lazy="select",
    )

    itineraries: Mapped[list["Itinerary"]] = relationship(
        "Itinerary",
        back_populates="trip_request",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (
        Index("ix_trip_requests_user_status", "user_id", "status"),
        Index("ix_trip_requests_origin_location", "origin_location", postgresql_using="gist"),
    )

    def __repr__(self) -> str:
        return f"TripRequest(id={self.id}, status={self.status})"


class TripRequestSelectedPlace(Base):
    """
    Bảng `trip_request_selected_places` — địa điểm Agent chọn cho một trip request.
    """
    __tablename__ = "trip_request_selected_places"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    trip_request_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("trip_requests.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    place_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("places.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    selection_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    selection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    trip_request: Mapped["TripRequest"] = relationship("TripRequest", back_populates="selected_places")

    def __repr__(self) -> str:
        return f"TripRequestSelectedPlace(trip={self.trip_request_id}, place={self.place_id})"


# Avoid circular imports
from src.models.itinerary_model import Itinerary  # noqa: E402
