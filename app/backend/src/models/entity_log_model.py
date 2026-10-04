from datetime import datetime
from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, SourceEntityType


class EntityLog(Base):
    __tablename__ = "entity_log"
    __table_args__ = (
        CheckConstraint("confidence BETWEEN 0 AND 1", name="confidence_range"),
        Index("ix_entity_log_entity_checked", "entity_type", "entity_id", "checked_at"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    entity_type: Mapped[SourceEntityType | None] = mapped_column(nullable=True)
    # ID của place/message/itinerary/proposal/evaluation/offer/alert
    entity_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    # Ví dụ: opening_hours, price, weather, travel_time
    field_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(3,2), nullable=True)
    agent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)
    tool_call_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tool_calls.id"), index=True, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
