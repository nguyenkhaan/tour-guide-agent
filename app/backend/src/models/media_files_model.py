from datetime import datetime
from uuid import UUID as UUIDValue

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, MediaImage, uuid_primary_key, created_timestamp


class MediaFiles(Base):
    __tablename__ = "media_files"
    __table_args__ = (
        CheckConstraint("file_size_bytes >= 0", name="file_size_bytes_nonnegative"),
    )

    # Định danh tệp đa phương tiện
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Người sở hữu tải lên
    user_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=True)
    # Tin nhan upload len bang tin nhan nao
    message_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id"), index=True, nullable=True)
    # Đường dẫn file lưu trữ
    object_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Tên file gốc tải lên
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Dung lượng tệp
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    # Định dạng tệp
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Muc dich cua media

    purpose: Mapped[str | None] = mapped_column(MediaImage, nullable=True)
    # Thời điểm tải lên
    created_at: Mapped[datetime] = created_timestamp()
