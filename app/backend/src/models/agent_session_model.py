"""
Model: agent_session

Phiên làm việc giữa người dùng và AI Agent.
Một session chứa nhiều messages, trip_requests, và agent_runs.
"""
import uuid
import enum

from sqlalchemy import String, Text, Enum as SAEnum, ForeignKey, Index
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class AgentSessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class AgentSession(TimestampMixin, Base):
    """
    Bảng `agent_session` — một phiên hội thoại của người dùng với AI Agent.

    Mỗi session có thể sinh ra nhiều trip_requests và messages.
    Status ARCHIVED khi người dùng kết thúc hoặc timeout sau 30 ngày.
    """
    __tablename__ = "agent_session"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="FK → users.id — chủ sở hữu phiên",
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Tiêu đề phiên (người dùng đặt hoặc AI tự generate)",
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Tóm tắt nội dung phiên do Agent tạo ra",
    )

    status: Mapped[AgentSessionStatus] = mapped_column(
        SAEnum(AgentSessionStatus, name="agentsessionstatus", create_type=True),
        nullable=False,
        default=AgentSessionStatus.ACTIVE,
        server_default=AgentSessionStatus.ACTIVE.value,
        comment="Trạng thái phiên: ACTIVE | ARCHIVED",
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(
        "User",
        back_populates="agent_sessions",
        lazy="select",
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="agent_session",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
        lazy="select",
    )

    # ── Table-level indexes ────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_agent_session_user_id_status", "user_id", "status"),
    )

    def __repr__(self) -> str:
        return f"AgentSession(id={self.id}, user_id={self.user_id}, status={self.status})"


# Avoid circular import
from src.models.user_model import User  # noqa: E402
from src.models.message_model import Message  # noqa: E402
