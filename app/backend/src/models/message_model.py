"""
Model: messages

Tin nhắn trong một agent_session — có thể từ user hoặc assistant (AI).
"""
import uuid
import datetime

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base


class Message(Base):
    """
    Bảng `messages` — từng tin nhắn trong một phiên hội thoại.

    - role: 'user' | 'assistant'
    - agent_run_id: liên kết assistant message với lần Agent tạo ra nó
    - metadata: JSONB cho context bổ sung (file attachments, tool hints...)
    - created_at: immutable — messages không được chỉnh sửa
    """
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )

    agent_session_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("agent_session.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="FK → agent_session.id",
    )

    role: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Vai trò gửi tin: 'user' | 'assistant'",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Nội dung tin nhắn",
    )

    message_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="Metadata bổ sung: file ids, tool hints, ... (JSONB)",
    )

    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        nullable=True,
        index=True,
        comment="FK → agent_runs.id (chỉ có với assistant messages)",
    )

    # Immutable — messages không updated
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        server_default="now()",
        comment="Thời điểm gửi tin nhắn (UTC)",
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    agent_session: Mapped["AgentSession"] = relationship(
        "AgentSession",
        back_populates="messages",
        lazy="select",
    )

    __table_args__ = (
        Index("ix_messages_session_created", "agent_session_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"Message(id={self.id}, role={self.role})"


from src.models.agent_session_model import AgentSession  # noqa: E402
