from datetime import datetime

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base, created_timestamp


class PlaceCategories(Base):
    __tablename__ = "place_categories"

    # Mã danh mục tự tăng
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Tên phân loại địa điểm
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Chuỗi định danh URL
    slug: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Mô tả chi tiết phân loại
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = created_timestamp()
