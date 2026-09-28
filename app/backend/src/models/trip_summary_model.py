"""
Models: trip_summaries, trip_summary_places, trip_expenses, next_trip_suggestions

Tổng kết chuyến đi sau khi hoàn thành.
"""
import uuid
import datetime
import enum

from sqlalchemy import (
    Boolean, Date, Enum as SAEnum, ForeignKey, Index,
    Integer, Numeric, String, Text,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class TripSummaryStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"


class SummaryPlaceStatus(str, enum.Enum):
    VISITED = "VISITED"
    SKIPPED = "SKIPPED"
    UNPLANNED = "UNPLANNED"


class ExpenseCategory(str, enum.Enum):
    LODGING = "LODGING"
    TRANSPORT = "TRANSPORT"
    FOOD = "FOOD"
    TICKET = "TICKET"
    SHOPPING = "SHOPPING"
    OTHER = "OTHER"


class TripSummary(TimestampMixin, Base):
    """Bảng `trip_summaries` — tổng kết chuyến đi."""
    __tablename__ = "trip_summaries"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, unique=True)
    status: Mapped[TripSummaryStatus] = mapped_column(SAEnum(TripSummaryStatus, name="tripsummarystatus", create_type=True), nullable=False, default=TripSummaryStatus.DRAFT)
    overall_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    diary_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    confirmed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    places: Mapped[list["TripSummaryPlace"]] = relationship("TripSummaryPlace", back_populates="summary", cascade="all, delete-orphan", lazy="select")
    expenses: Mapped[list["TripExpense"]] = relationship("TripExpense", back_populates="summary", cascade="all, delete-orphan", lazy="select")
    suggestions: Mapped[list["NextTripSuggestion"]] = relationship("NextTripSuggestion", back_populates="summary", cascade="all, delete-orphan", lazy="select")

    def __repr__(self) -> str:
        return f"TripSummary(id={self.id}, status={self.status})"


class TripSummaryPlace(TimestampMixin, Base):
    """Bảng `trip_summary_places` — địa điểm thực tế trong tổng kết."""
    __tablename__ = "trip_summary_places"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_summary_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trip_summaries.id", ondelete="CASCADE"), nullable=False, index=True)
    place_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("places.id", ondelete="SET NULL"), nullable=True)
    place_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[SummaryPlaceStatus] = mapped_column(SAEnum(SummaryPlaceStatus, name="summaryplacestatus", create_type=True), nullable=False)
    confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    evidence: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_user_corrected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    summary: Mapped["TripSummary"] = relationship("TripSummary", back_populates="places")

    def __repr__(self) -> str:
        return f"TripSummaryPlace(id={self.id}, status={self.status})"


class TripExpense(TimestampMixin, Base):
    """Bảng `trip_expenses` — chi phí thực tế theo hạng mục."""
    __tablename__ = "trip_expenses"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_summary_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trip_summaries.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[ExpenseCategory] = mapped_column(SAEnum(ExpenseCategory, name="expensecategory", create_type=True), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="VND", server_default="VND")
    spent_on: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    summary: Mapped["TripSummary"] = relationship("TripSummary", back_populates="expenses")

    def __repr__(self) -> str:
        return f"TripExpense(id={self.id}, category={self.category})"


class NextTripSuggestion(Base):
    """Bảng `next_trip_suggestions` — gợi ý chuyến tiếp theo."""
    __tablename__ = "next_trip_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_summary_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trip_summaries.id", ondelete="CASCADE"), nullable=False, index=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_places: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    estimated_budget: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="VND", server_default="VND")
    started_agent_session_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")
    used_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    summary: Mapped["TripSummary"] = relationship("TripSummary", back_populates="suggestions")

    def __repr__(self) -> str:
        return f"NextTripSuggestion(id={self.id}, rank={self.rank})"
