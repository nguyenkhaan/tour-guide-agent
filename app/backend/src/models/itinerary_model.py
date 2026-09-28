"""
Models: itineraries, itinerary_days, itinerary_activities, itinerary_transits,
        itinerary_proposals, evaluation_results

Lộ trình và các thành phần chi tiết của lộ trình.
"""
import uuid
import datetime
import enum

from sqlalchemy import (
    Boolean, Date, Enum as SAEnum, ForeignKey, Index,
    Integer, Numeric, String, Text, Time,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class ItineraryStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    REVIEWING = "REVIEWING"
    SELECTED = "SELECTED"


class ItineraryProposalStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Itinerary(TimestampMixin, Base):
    """
    Bảng `itineraries` — một phương án lộ trình được Agent tạo ra.
    """
    __tablename__ = "itineraries"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    trip_request_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("trip_requests.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    option_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_days: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Currency convention
    estimated_total_cost: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    cost_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="VND", server_default="VND")

    highlights: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    trade_offs: Mapped[str | None] = mapped_column(Text, nullable=True)
    luggage_checklist: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    ranking_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    status: Mapped[ItineraryStatus] = mapped_column(
        SAEnum(ItineraryStatus, name="itinerarystatus", create_type=True),
        nullable=False, default=ItineraryStatus.DRAFT, server_default=ItineraryStatus.DRAFT.value,
    )

    trip_request: Mapped["TripRequest"] = relationship("TripRequest", back_populates="itineraries")
    days: Mapped[list["ItineraryDay"]] = relationship(
        "ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan",
        order_by="ItineraryDay.day_number", lazy="select",
    )
    proposals: Mapped[list["ItineraryProposal"]] = relationship(
        "ItineraryProposal", back_populates="itinerary", cascade="all, delete-orphan", lazy="select"
    )
    evaluation_results: Mapped[list["EvaluationResult"]] = relationship(
        "EvaluationResult", back_populates="itinerary", cascade="all, delete-orphan", lazy="select"
    )

    __table_args__ = (
        Index("ix_itineraries_trip_request_status", "trip_request_id", "status"),
    )

    def __repr__(self) -> str:
        return f"Itinerary(id={self.id}, status={self.status})"


class ItineraryDay(Base):
    """Bảng `itinerary_days` — từng ngày trong lộ trình."""
    __tablename__ = "itinerary_days"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    planned_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_total_cost: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)

    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="days")
    activities: Mapped[list["ItineraryActivity"]] = relationship(
        "ItineraryActivity", back_populates="day", cascade="all, delete-orphan",
        order_by="ItineraryActivity.order_index", lazy="select",
    )
    transits: Mapped[list["ItineraryTransit"]] = relationship(
        "ItineraryTransit", back_populates="day", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self) -> str:
        return f"ItineraryDay(id={self.id}, day={self.day_number})"


class ItineraryActivity(TimestampMixin, Base):
    """Bảng `itinerary_activities` — hoạt động trong ngày."""
    __tablename__ = "itinerary_activities"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_day_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itinerary_days.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    place_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("places.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )

    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    activity_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime.time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[datetime.time | None] = mapped_column(Time, nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    day: Mapped["ItineraryDay"] = relationship("ItineraryDay", back_populates="activities")

    def __repr__(self) -> str:
        return f"ItineraryActivity(id={self.id}, title={self.title})"


class ItineraryTransit(Base):
    """Bảng `itinerary_transits` — di chuyển giữa hai hoạt động."""
    __tablename__ = "itinerary_transits"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_day_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itinerary_days.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    from_activity_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("itinerary_activities.id", ondelete="SET NULL"), nullable=True)
    to_activity_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("itinerary_activities.id", ondelete="SET NULL"), nullable=True)
    transport_mode: Mapped[str | None] = mapped_column(String(30), nullable=True)
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_distance_km: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    route_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    day: Mapped["ItineraryDay"] = relationship("ItineraryDay", back_populates="transits")

    def __repr__(self) -> str:
        return f"ItineraryTransit(id={self.id}, mode={self.transport_mode})"


class ItineraryProposal(Base):
    """Bảng `itinerary_proposals` — đề xuất chỉnh sửa lộ trình từ Agent."""
    __tablename__ = "itinerary_proposals"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    base_itinerary_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    target_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proposed_by: Mapped[str | None] = mapped_column(String(30), nullable=True)
    diff_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ItineraryProposalStatus] = mapped_column(
        SAEnum(ItineraryProposalStatus, name="itineraryproposalstatus", create_type=True),
        nullable=False, default=ItineraryProposalStatus.PENDING, server_default="PENDING",
    )
    user_decision_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="proposals")

    def __repr__(self) -> str:
        return f"ItineraryProposal(id={self.id}, status={self.status})"


class EvaluationResult(Base):
    """Bảng `evaluation_results` — kết quả thẩm định từ Critic Agent."""
    __tablename__ = "evaluation_results"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    proposal_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    is_passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    budget_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    opening_hours_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    travel_time_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    safety_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    hard_failures: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    soft_warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    evaluated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="evaluation_results")

    def __repr__(self) -> str:
        return f"EvaluationResult(id={self.id}, passed={self.is_passed})"


from src.models.trip_request_model import TripRequest  # noqa: E402
