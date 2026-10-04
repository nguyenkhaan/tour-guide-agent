from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import DateTime, ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key


class AuditAccessLogs(Base):
    __tablename__ = "audit_access_logs"

    id: Mapped[UUIDValue] = uuid_primary_key()
    # Operator hoặc Admin truy cập
    actor_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    target_user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    agent_run_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_runs.id"), index=True, nullable=True)

    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    ticket_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    client_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    accessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
