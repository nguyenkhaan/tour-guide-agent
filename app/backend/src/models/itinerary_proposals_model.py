from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, ItineraryProposalStatus


class ItineraryProposals(Base):
    __tablename__ = "itinerary_proposals"
    __table_args__ = (
        CheckConstraint("target_version > 0", name="target_version_positive"),
    )

    # Định danh đề xuất
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Lộ trình đang sửa
    itinerary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id"), index=True, nullable=True)
    # Phiên bản gốc
    base_itinerary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id"), index=True, nullable=True)
    # Phiên bản sau khi duyệt
    target_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Tác nhân đề xuất
    proposed_by: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Chi tiết thay đổi
    diff_payload: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Lý do thay đổi
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Cảnh báo phát sinh
    warnings: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Trạng thái phê duyệt
    status: Mapped[ItineraryProposalStatus | None] = mapped_column(nullable=True)
    # Thời điểm người dùng duyệt
    user_decision_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Thời điểm tạo đề xuất
    created_at: Mapped[datetime] = created_timestamp()
