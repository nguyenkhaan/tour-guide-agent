"""
Base SQLAlchemy model and reusable mixins for all Phase 2 migrations.

== Phase 2 Migration Conventions ==

1. PRIMARY KEY
   - UUID v4 (uuid.uuid4) cho tất cả bảng chính.
   - SERIAL (Integer auto-increment) chỉ cho lookup/category tables (place_categories, system_configs).

2. DATETIME / TIMESTAMP
   - Tất cả datetime lưu dạng TIMESTAMPTZ (DateTime(timezone=True)) — UTC trong database.
   - Hiển thị ra ngoài theo APP_TIMEZONE (Asia/Ho_Chi_Minh).
   - Dùng func.now() làm server_default cho created_at, updated_at.
   - Không bao giờ dùng datetime.datetime.utcnow() — deprecated.
   - Với soft-delete: thêm cột deleted_at TIMESTAMPTZ nullable.

3. TIỀN TỆ (Currency)
   - Mọi giá tiền: NUMERIC(15,2) — đủ cho VND và ngoại tệ, không mất precision.
   - Luôn đi kèm cột currency VARCHAR(3) chứa ISO 4217 code (VND, USD, EUR...).
   - Default currency: VND.

4. INDEX
   - FK columns luôn có index (Index hoặc mapped_column(index=True)).
   - Geospatial columns dùng GiST index (PostgreSQL).
   - Unique constraints dùng UniqueConstraint hoặc unique=True trong mapped_column.
   - Index naming convention: ix_<table>_<column>.

5. SOFT DELETE
   - Dùng cột deleted_at TIMESTAMPTZ nullable thay vì xóa cứng.
   - Query lọc: WHERE deleted_at IS NULL.

6. JSONB
   - Dùng cho dữ liệu bán cấu trúc: preferences, metadata, cost_breakdown...
   - Không dùng JSON (text) — dùng JSONB để hỗ trợ index và query operators.

7. NAMING CONVENTION (Alembic auto-name constraints)
   - ix: ix_%(column_0_label)s
   - uq: uq_%(table_name)s_%(column_0_name)s
   - ck: ck_%(table_name)s_`%(constraint_name)s`
   - fk: fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s
   - pk: pk_%(table_name)s

== Postgres setup commands (nếu cần reset) ==
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    CREATE EXTENSION IF NOT EXISTS postgis;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""
import datetime
import uuid

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy import UUID as SA_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for ALL SQLAlchemy models.
    - Provides UUID primary key.
    - Maps Python datetime → TIMESTAMPTZ (PostgreSQL timezone-aware).
    - Enforces constraint naming conventions for Alembic autogenerate.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    # All datetime fields in models will map to TIMESTAMPTZ automatically.
    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }

    # Default UUID primary key for all tables.
    id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )


class TimestampMixin:
    """
    Mixin cung cấp created_at và updated_at.
    Dùng server_default=func.now() để DB tự set — không phụ thuộc app clock.

    Usage:
        class MyModel(TimestampMixin, Base):
            ...
    """
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Thời điểm tạo bản ghi (UTC, server clock)",
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Thời điểm cập nhật gần nhất (UTC, server clock)",
    )


class SoftDeleteMixin:
    """
    Mixin soft-delete: thêm cột deleted_at TIMESTAMPTZ.
    Để query dữ liệu chưa xóa: WHERE deleted_at IS NULL.

    Usage:
        class MyModel(SoftDeleteMixin, TimestampMixin, Base):
            ...
    """
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Soft-delete: NULL = chưa xóa; có giá trị = đã xóa lúc đó (UTC)",
    )