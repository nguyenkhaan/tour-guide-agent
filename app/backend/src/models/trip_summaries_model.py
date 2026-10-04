from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    TripSummaryStatus,
)


class TripSummaries(Base):
    __tablename__ = "trip_summaries"
    __table_args__ = (
        CheckConstraint("overall_rating BETWEEN 1 AND 5", name="overall_rating_range"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    status: Mapped[TripSummaryStatus | None] = mapped_column(nullable=True)
    overall_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    diary_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
