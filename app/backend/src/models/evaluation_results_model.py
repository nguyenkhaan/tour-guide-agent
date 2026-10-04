from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import Boolean, DateTime, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key


class EvaluationResults(Base):
    __tablename__ = "evaluation_results"

    # Định danh kết quả đánh giá
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Lộ trình kiểm tra
    itinerary_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id"), index=True, nullable=True)
    # Đề xuất chỉnh sửa tương ứng
    proposal_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("itinerary_proposals.id"), index=True, nullable=True)
    agent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)
    # Đạt điều kiện khả thi
    is_passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Đánh giá ngân sách
    budget_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Đánh giá giờ mở cửa
    opening_hours_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Đánh giá thời gian di chuyển
    travel_time_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Đánh giá rủi ro an toàn
    safety_status: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Lỗi bất khả thi
    hard_failures: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Cảnh báo mềm
    soft_warnings: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Thời điểm thẩm định
    evaluated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
