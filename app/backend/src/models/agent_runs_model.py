from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, AgentRunStatus, AgentRunTrigger, AgentType


class AgentRuns(Base):
    __tablename__ = "agent_runs"
    __table_args__ = (
        Index("ix_agent_runs_workflow_id", "workflow_id"),
        Index("ix_agent_runs_expires_at", "expires_at"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    # Nhóm các lần Planner -> Critic -> Planner trong cùng luồng
    workflow_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    # Lần chạy đã bàn giao hoặc kích hoạt lần chạy này
    parent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)
    user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    agent_session_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_session.id"), index=True, nullable=True)
    trip_request_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), index=True, nullable=True)
    trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    agent_type: Mapped[AgentType | None] = mapped_column(nullable=True)
    trigger_type: Mapped[AgentRunTrigger | None] = mapped_column(nullable=True)
    status: Mapped[AgentRunStatus | None] = mapped_column(nullable=True)
    # Input đã rút gọn và loại bỏ secret
    input_summary: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Output có cấu trúc, không lưu chain-of-thought
    output_summary: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Lý do quyết định ngắn gọn cho người dùng và vận hành
    decision_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Log kỹ thuật chi tiết lưu tối đa 7 ngày
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
