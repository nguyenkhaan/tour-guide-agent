"""
Models: media_files

Bảng lưu trữ file đa phương tiện tải lên (ảnh, ...).
Tham chiếu đến object storage (MinIO/S3) qua object_key.
"""
import uuid
import datetime
import enum

from sqlalchemy import BigInteger, Enum as SAEnum, ForeignKey, Index, String
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base


class MediaImage(str, enum.Enum):
    REQUEST_IMAGE = "REQUEST_IMAGE"
    REVIEW_PHOTO = "REVIEW_PHOTO"
    SUMMARY_PHOTO = "SUMMARY_PHOTO"


class MediaFile(Base):
    """
    Bảng `media_files` — metadata của file tải lên.
    File thực tế lưu trong MinIO/S3, ở đây chỉ lưu object_key.
    """
    __tablename__ = "media_files"

    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    message_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Tin nhắn upload lên bằng tin nhắn nào",
    )

    object_key: Mapped[str] = mapped_column(
        String(500), nullable=False,
        comment="Đường dẫn file trong object storage (MinIO key)",
    )

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    purpose: Mapped[MediaImage] = mapped_column(
        SAEnum(MediaImage, name="mediaimage", create_type=True),
        nullable=False,
        comment="Mục đích sử dụng file",
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default="now()"
    )

    def __repr__(self) -> str:
        return f"MediaFile(id={self.id}, purpose={self.purpose})"
