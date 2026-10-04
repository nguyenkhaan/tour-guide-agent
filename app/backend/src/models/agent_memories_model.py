from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, Index, String, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp, AgentMemoryScope, AgentType


class AgentMemories(Base):
    __tablename__ = "agent_memories"
    __table_args__ = (
        Index("ix_agent_memories_expires_at", "expires_at"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()
    agent_session_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_session.id"), index=True, nullable=True)
    trip_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), index=True, nullable=True)
    agent_type: Mapped[AgentType | None] = mapped_column(nullable=True)
    scope: Mapped[AgentMemoryScope | None] = mapped_column(nullable=True)
    memory_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    memory_value: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Working/trip memory lưu tối đa 7 ngày
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
