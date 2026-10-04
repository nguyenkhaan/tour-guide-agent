from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, uuid_primary_key, created_timestamp


class PlaceNarrations(Base):
    __tablename__ = "place_narrations"
    __table_args__ = (
        CheckConstraint("duration_seconds >= 0", name="duration_seconds_nonnegative"),
    )

    # Định danh bài thuyết minh
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Thuộc địa điểm nào
    place_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("places.id"), index=True, nullable=True)
    # Tiêu đề nội dung thuyết minh
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Đường dẫn file TTS
    audio_object_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Văn bản lời bình
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Thời lượng phát
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Trạng thái kích hoạt
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Admin tải lên hoặc cập nhật
    created_by: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Thời điểm tạo
    created_at: Mapped[datetime] = created_timestamp()
