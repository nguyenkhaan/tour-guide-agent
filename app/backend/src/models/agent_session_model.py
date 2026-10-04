from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    AgentSessionStatus,
)


class AgentSession(Base):
    __tablename__ = "agent_session"
    __table_args__ = (
        Index("ix_agent_session_user_updated", "user_id", "updated_at"),
    )

    id: Mapped[UUIDValue] = uuid_primary_key()

    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    # A short summary about agent's session
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[AgentSessionStatus | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
    updated_at: Mapped[datetime] = updated_timestamp()
