"""
Models: trips, gps_location_events, trip_alerts

Bảng chuyến đi thực tế, GPS tracking, và cảnh báo thời gian thực.
"""
import uuid
import datetime

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import (
    Boolean, Enum as SAEnum, ForeignKey, Index,
    Numeric, String, Text,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class Trip(TimestampMixin, Base):
    """
    Bảng `trips` — chuyến đi thực tế đang hoặc đã thực hiện.
    Liên kết với itinerary được chốt cuối cùng.
    """
    __tablename__ = "trips"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    trip_request_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("trip_requests.id", ondelete="SET NULL"), nullable=True, index=True
    )
    finalized_itinerary_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    gps_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    actual_start_date: Mapped[datetime.date | None] = mapped_column(nullable=True)
    actual_end_date: Mapped[datetime.date | None] = mapped_column(nullable=True)

    gps_events: Mapped[list["GpsLocationEvent"]] = relationship(
        "GpsLocationEvent", back_populates="trip", cascade="all, delete-orphan", lazy="select"
    )
    alerts: Mapped[list["TripAlert"]] = relationship(
        "TripAlert", back_populates="trip", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"Trip(id={self.id}, status={self.status})"


class GpsLocationEvent(Base):
    """
    Bảng `gps_location_events` — tọa độ GPS ghi nhận trong chuyến đi.
    Tự động expire sau 7 ngày (expires_at + is_expired flag).
    """
    __tablename__ = "gps_location_events"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    location: Mapped[WKBElement] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    accuracy_meters: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    recorded_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")
    expires_at: Mapped[datetime.datetime | None] = mapped_column(
        nullable=True, comment="Hạn lưu trữ tối đa 7 ngày"
    )
    is_expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    trip: Mapped["Trip"] = relationship("Trip", back_populates="gps_events")

    __table_args__ = (
        Index("ix_gps_location_events_trip_recorded", "trip_id", "recorded_at"),
        Index("ix_gps_location_events_location", "location", postgresql_using="gist"),
    )

    def __repr__(self) -> str:
        return f"GpsLocationEvent(id={self.id}, trip={self.trip_id})"


class TripAlert(Base):
    """Bảng `trip_alerts` — cảnh báo thời gian thực từ Weather Monitor."""
    __tablename__ = "trip_alerts"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    alert_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    checked_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    affected_activity_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    alternative_proposal_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    is_resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    trip: Mapped["Trip"] = relationship("Trip", back_populates="alerts")

    def __repr__(self) -> str:
        return f"TripAlert(id={self.id}, type={self.alert_type})"
