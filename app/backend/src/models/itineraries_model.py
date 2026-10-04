from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID as UUIDValue

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import (
    Base,
    uuid_primary_key,
    created_timestamp,
    updated_timestamp,
    ItineraryStatus,
)


class Itineraries(Base):
    __tablename__ = "itineraries"
    __table_args__ = (
        CheckConstraint("option_index >= 0", name="option_index_nonnegative"),
        CheckConstraint("version > 0", name="version_positive"),
        CheckConstraint("total_days > 0", name="total_days_positive"),
        CheckConstraint("estimated_total_cost >= 0", name="estimated_total_cost_range"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="currency_format"),
    )

    # Định danh lộ trình
    id: Mapped[UUIDValue] = uuid_primary_key()
    # Yêu cầu chuyến đi gốc
    trip_request_id: Mapped[UUIDValue | None] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), index=True, nullable=True)
    # Thứ tự phương án
    option_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Số hiệu phiên bản lộ trình
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Tên phương án lộ trình
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Tóm tắt tổng quan
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Tổng số ngày
    total_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Dự trù kinh phí
    estimated_total_cost: Mapped[Decimal | None] = mapped_column(Numeric(15,2), nullable=True)
    # Be nho thoing tin ve kinh phi
    cost_breakdown: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Đơn vị tiền tệ
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    # Điểm nổi bật nhất
    highlights: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Cảnh báo mềm
    warnings: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Đánh đổi khi chọn
    trade_offs: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Danh sách vật dụng gợi ý
    luggage_checklist: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
    # Điểm xếp hạng đề xuất
    ranking_score: Mapped[Decimal | None] = mapped_column(Numeric(5,2), nullable=True)
    # Trạng thái vòng đời lộ trình
    status: Mapped[str | None] = mapped_column(ItineraryStatus, nullable=True)
    # Thời điểm tạo
    created_at: Mapped[datetime] = created_timestamp()
    # Cập nhật gần nhất
    updated_at: Mapped[datetime] = updated_timestamp()
