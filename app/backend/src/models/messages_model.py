from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class Messages(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_session_created", "agent_session_id", "created_at"),
        CheckConstraint("role IN ('user', 'assistant')", name="role_values"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    agent_session_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_session.id"), index=True, nullable=True)
    # user or assistant
    role: Mapped[str | None] = mapped_column(String(10), nullable=True)
    sources: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    message_metadata: Mapped[Any | None] = mapped_column("metadata", JSONB, nullable=True)
    # Liên kết assistant message với lần chạy Agent tạo ra nó
    agent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
