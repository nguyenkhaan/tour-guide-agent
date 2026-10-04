from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, ToolCallStatus


class ToolCalls(Base):
    __tablename__ = "tool_calls"
    __table_args__ = (
        Index("ix_tool_calls_expires_at", "expires_at"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    agent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)
    tool_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Schema khác nhau theo từng tool
    arguments: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Kết quả đã loại bỏ secret và dữ liệu nhạy cảm không cần thiết
    result: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ToolCallStatus | None] = mapped_column(nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Lưu tối đa 7 ngày
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
