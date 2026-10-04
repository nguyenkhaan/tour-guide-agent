from datetime import datetime
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import ForeignKey, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, updated_timestamp


class SystemConfigs(Base):
    __tablename__ = "system_configs"

    config_key: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False)
    config_value: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_by: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    updated_at: Mapped[datetime] = updated_timestamp()
