from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, updated_timestamp


class PlaceReviews(Base):
    __tablename__ = "place_reviews"
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="rating_range"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Chuyến đi dùng để xác minh lượt ghé thăm
    trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Kiểm duyệt review của người dùng
    is_valid: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
