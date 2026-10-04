from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    OperatorProposalStatus,
    OperatorProposalType,
)


class OperatorProposals(Base):
    __tablename__ = "operator_proposals"

    id: Mapped[UUIDValue] = uuid_primary_key()
    operator_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    proposal_type: Mapped[str | None] = mapped_column(OperatorProposalType, nullable=True)
    # Chỉ có khi kiến nghị cập nhật địa điểm
    target_place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    # Có thể có khi báo cáo thời tiết hoặc logic AI
    related_trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Nội dung thay đổi khác nhau theo proposal_type
    proposed_payload: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str | None] = mapped_column(OperatorProposalStatus, nullable=True)
    admin_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
