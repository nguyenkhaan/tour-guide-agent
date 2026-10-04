from datetime import date, datetime
from decimal import Decimal
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    ExpenseCategory,
)


class TripExpenses(Base):
    __tablename__ = "trip_expenses"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="amount_range"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="currency_format"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    trip_summary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_summaries.id"), index=True, nullable=True)
    category: Mapped[ExpenseCategory | None] = mapped_column(nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    spent_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
