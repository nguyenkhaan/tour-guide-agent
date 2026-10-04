from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import ForeignKey, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    ModerationAction,
    ModeratorType,
    ReviewStatus,
)


class ReviewModerationLogs(Base):
    __tablename__ = "review_moderation_logs"

    id: Mapped[UUIDValue] = uuid_primary_key()
    review_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("place_reviews.id"), index=True, nullable=True)
    # Null nếu hệ thống tự động kiểm duyệt
    moderator_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    moderator_type: Mapped[ModeratorType | None] = mapped_column(nullable=True)
    action: Mapped[ModerationAction | None] = mapped_column(nullable=True)
    previous_status: Mapped[ReviewStatus | None] = mapped_column(nullable=True)
    new_status: Mapped[ReviewStatus | None] = mapped_column(nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Kết quả kiểm tra spam, policy, relevance
    details: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
