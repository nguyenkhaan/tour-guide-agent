from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    ReviewReportReason,
    ReviewReportStatus,
)


class ReviewReports(Base):
    __tablename__ = "review_reports"

    id: Mapped[UUIDValue] = uuid_primary_key()
    review_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("place_reviews.id"), index=True, nullable=True)
    reporter_user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    reason_code: Mapped[ReviewReportReason | None] = mapped_column(nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReviewReportStatus | None] = mapped_column(nullable=True)
    # Operator hoặc Admin xử lý
    resolved_by: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
