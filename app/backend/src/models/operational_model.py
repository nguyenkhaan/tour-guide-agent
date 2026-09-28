"""
Models: operator_proposals, agent_runs, tool_calls, information_sources,
        audit_access_logs, agent_memories, system_configs

Bảng vận hành, audit và AI infrastructure.
"""
import uuid
import datetime
import enum

from sqlalchemy import (
    Boolean, Enum as SAEnum, ForeignKey, Index,
    Integer, Numeric, String, Text,
)
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base


# ── Enums ─────────────────────────────────────────────────────────────────────

class OperatorProposalType(str, enum.Enum):
    PLACE_UPDATE = "PLACE_UPDATE"
    WEATHER_REPORT = "WEATHER_REPORT"
    AI_ISSUE = "AI_ISSUE"


class OperatorProposalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AgentType(str, enum.Enum):
    PLANNER = "PLANNER"
    CRITIC = "CRITIC"
    BOOKING = "BOOKING"


class AgentRunTrigger(str, enum.Enum):
    USER = "USER"
    AGENT = "AGENT"
    BACKGROUND_JOB = "BACKGROUND_JOB"


class AgentRunStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ToolCallStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class AgentMemoryScope(str, enum.Enum):
    WORKING = "WORKING"
    TRIP = "TRIP"


class SourceEntityType(str, enum.Enum):
    PLACE = "PLACE"
    MESSAGE = "MESSAGE"
    ITINERARY = "ITINERARY"
    ITINERARY_PROPOSAL = "ITINERARY_PROPOSAL"
    EVALUATION_RESULT = "EVALUATION_RESULT"
    BOOKING_OFFER = "BOOKING_OFFER"
    TRIP_ALERT = "TRIP_ALERT"


# ── Models ────────────────────────────────────────────────────────────────────

class OperatorProposal(Base):
    """Bảng `operator_proposals` — Maker-Checker: operator đề xuất, admin duyệt."""
    __tablename__ = "operator_proposals"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    proposal_type: Mapped[OperatorProposalType] = mapped_column(SAEnum(OperatorProposalType, name="operatorproposaltype", create_type=True), nullable=False)
    target_place_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("places.id", ondelete="SET NULL"), nullable=True)
    related_trip_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    proposed_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[OperatorProposalStatus] = mapped_column(SAEnum(OperatorProposalStatus, name="operatorproposalstatus", create_type=True), nullable=False, default=OperatorProposalStatus.PENDING)
    admin_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")
    reviewed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"OperatorProposal(id={self.id}, type={self.proposal_type})"


class AgentRun(Base):
    """
    Bảng `agent_runs` — một lần thực thi Agent (Planner/Critic/Booking).
    Hỗ trợ workflow_id để nhóm nhiều lần chạy trong cùng luồng.
    Có TTL: expires_at — log kỹ thuật lưu tối đa 7 ngày.
    """
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True, index=True)
    parent_run_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    agent_session_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("agent_session.id", ondelete="SET NULL"), nullable=True)
    trip_request_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trip_requests.id", ondelete="SET NULL"), nullable=True)
    trip_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trips.id", ondelete="SET NULL"), nullable=True)
    agent_type: Mapped[AgentType] = mapped_column(SAEnum(AgentType, name="agenttype", create_type=True), nullable=False)
    trigger_type: Mapped[AgentRunTrigger] = mapped_column(SAEnum(AgentRunTrigger, name="agentrun_trigger", create_type=True), nullable=False)
    status: Mapped[AgentRunStatus] = mapped_column(SAEnum(AgentRunStatus, name="agentrunstatus", create_type=True), nullable=False, default=AgentRunStatus.RUNNING)
    agent_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    input_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    decision_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")
    completed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True, comment="Log kỹ thuật lưu tối đa 7 ngày")

    __table_args__ = (
        Index("ix_agent_runs_session_status", "agent_session_id", "status"),
        Index("ix_agent_runs_workflow", "workflow_id"),
    )

    def __repr__(self) -> str:
        return f"AgentRun(id={self.id}, type={self.agent_type}, status={self.status})"


class ToolCall(Base):
    """Bảng `tool_calls` — từng tool call trong một agent_run."""
    __tablename__ = "tool_calls"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tool_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    arguments: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ToolCallStatus] = mapped_column(SAEnum(ToolCallStatus, name="toolcallstatus", create_type=True), nullable=False, default=ToolCallStatus.RUNNING)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")
    completed_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True, comment="Lưu tối đa 7 ngày")

    def __repr__(self) -> str:
        return f"ToolCall(id={self.id}, tool={self.tool_name}, status={self.status})"


class InformationSource(Base):
    """Bảng `information_sources` — nguồn thông tin biến động của từng entity."""
    __tablename__ = "information_sources"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[SourceEntityType] = mapped_column(SAEnum(SourceEntityType, name="sourceentitytype", create_type=True), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), nullable=False)
    field_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    checked_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    tool_call_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    __table_args__ = (
        Index("ix_information_sources_entity", "entity_type", "entity_id"),
    )

    def __repr__(self) -> str:
        return f"InformationSource(id={self.id}, entity={self.entity_type})"


class AuditAccessLog(Base):
    """Bảng `audit_access_logs` — giám sát truy cập log kỹ thuật."""
    __tablename__ = "audit_access_logs"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    target_user_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True, index=True)
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    ticket_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    client_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    accessed_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    def __repr__(self) -> str:
        return f"AuditAccessLog(id={self.id})"


class AgentMemory(Base):
    """
    Bảng `agent_memories` — bộ nhớ tạm của Agent.
    Scope WORKING/TRIP, TTL 7 ngày.
    """
    __tablename__ = "agent_memories"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_session_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("agent_session.id", ondelete="CASCADE"), nullable=True, index=True)
    trip_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    agent_type: Mapped[AgentType] = mapped_column(SAEnum(AgentType, name="agenttype", create_type=False), nullable=False)
    scope: Mapped[AgentMemoryScope] = mapped_column(SAEnum(AgentMemoryScope, name="agentmemoryscope", create_type=True), nullable=False)
    memory_key: Mapped[str] = mapped_column(String(100), nullable=False)
    memory_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True, comment="Working/trip memory lưu tối đa 7 ngày")
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    __table_args__ = (
        Index("ix_agent_memories_session_key", "agent_session_id", "memory_key"),
    )

    def __repr__(self) -> str:
        return f"AgentMemory(id={self.id}, key={self.memory_key})"


class SystemConfig(Base):
    """
    Bảng `system_configs` — cấu hình tham số toàn cục.
    PK là config_key (VARCHAR), không dùng UUID.
    """
    __tablename__ = "system_configs"

    # Override: PK là string key, không dùng UUID
    id: Mapped[str] = mapped_column(  # type: ignore[assignment]
        String(100),
        primary_key=True,
        name="config_key",
        comment="Config key — chuỗi định danh tham số",
    )

    config_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    updated_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True, onupdate=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"SystemConfig(key={self.id})"
