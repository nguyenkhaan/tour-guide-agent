"""
Models: booking_offers, place_reviews, review_reports, review_moderation_logs

Đặt chỗ (chỉ redirect, không lưu payment), đánh giá địa điểm và kiểm duyệt.
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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base, TimestampMixin


class BookingOfferType(str, enum.Enum):
    HOTEL = "HOTEL"
    FLIGHT = "FLIGHT"
    TRANSPORT = "TRANSPORT"
    ACTIVITY = "ACTIVITY"


class BookingOfferStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class ReviewStatus(str, enum.Enum):
    PRIVATE = "PRIVATE"
    PENDING = "PENDING"
    PUBLIC = "PUBLIC"
    REJECTED = "REJECTED"
    HIDDEN = "HIDDEN"


class VisitVerificationStatus(str, enum.Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class ReviewReportReason(str, enum.Enum):
    SPAM = "SPAM"
    ABUSE = "ABUSE"
    IRRELEVANT = "IRRELEVANT"
    FALSE_INFORMATION = "FALSE_INFORMATION"
    OTHER = "OTHER"


class ReviewReportStatus(str, enum.Enum):
    OPEN = "OPEN"
    REVIEWING = "REVIEWING"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class ModerationAction(str, enum.Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    HIDE = "HIDE"
    RESTORE = "RESTORE"


class ModeratorType(str, enum.Enum):
    SYSTEM = "SYSTEM"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"


class BookingOffer(Base):
    """
    Bảng `booking_offers` — tra cứu và so sánh dịch vụ đối tác.
    Chỉ lưu metadata + redirect_url, không xử lý payment.
    """
    __tablename__ = "booking_offers"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="SET NULL"), nullable=True, index=True)
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    offer_type: Mapped[BookingOfferType] = mapped_column(SAEnum(BookingOfferType, name="bookingoffertype", create_type=True), nullable=False)
    status: Mapped[BookingOfferStatus] = mapped_column(SAEnum(BookingOfferStatus, name="bookingofferstatus", create_type=True), nullable=False, default=BookingOfferStatus.AVAILABLE)
    provider_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provider_offer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    match_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    final_price: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="VND", server_default="VND")
    cancellation_policy: Mapped[str | None] = mapped_column(Text, nullable=True)
    redirect_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    checked_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    def __repr__(self) -> str:
        return f"BookingOffer(id={self.id}, type={self.offer_type})"


class PlaceReview(TimestampMixin, Base):
    """Bảng `place_reviews` — đánh giá địa điểm sau chuyến đi."""
    __tablename__ = "place_reviews"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("places.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("trips.id", ondelete="SET NULL"), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReviewStatus] = mapped_column(SAEnum(ReviewStatus, name="reviewstatus", create_type=True), nullable=False, default=ReviewStatus.PRIVATE, server_default="PRIVATE")
    visit_status: Mapped[VisitVerificationStatus] = mapped_column(SAEnum(VisitVerificationStatus, name="visitverificationstatus", create_type=True), nullable=False, default=VisitVerificationStatus.UNVERIFIED)
    published_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)

    reports: Mapped[list["ReviewReport"]] = relationship("ReviewReport", back_populates="review", cascade="all, delete-orphan", lazy="select")
    moderation_logs: Mapped[list["ReviewModerationLog"]] = relationship("ReviewModerationLog", back_populates="review", cascade="all, delete-orphan", lazy="select")

    __table_args__ = (Index("ix_place_reviews_place_status", "place_id", "status"),)

    def __repr__(self) -> str:
        return f"PlaceReview(id={self.id}, rating={self.rating})"


class ReviewReport(Base):
    """Bảng `review_reports` — báo cáo đánh giá vi phạm."""
    __tablename__ = "review_reports"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("place_reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    reporter_user_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason_code: Mapped[ReviewReportReason] = mapped_column(SAEnum(ReviewReportReason, name="reviewreportreason", create_type=True), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReviewReportStatus] = mapped_column(SAEnum(ReviewReportStatus, name="reviewreportstatus", create_type=True), nullable=False, default=ReviewReportStatus.OPEN)
    resolved_by: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    review: Mapped["PlaceReview"] = relationship("PlaceReview", back_populates="reports")

    def __repr__(self) -> str:
        return f"ReviewReport(id={self.id}, status={self.status})"


class ReviewModerationLog(Base):
    """Bảng `review_moderation_logs` — lịch sử kiểm duyệt đánh giá."""
    __tablename__ = "review_moderation_logs"

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), ForeignKey("place_reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    moderator_id: Mapped[uuid.UUID | None] = mapped_column(SA_UUID(as_uuid=True), nullable=True)
    moderator_type: Mapped[ModeratorType] = mapped_column(SAEnum(ModeratorType, name="moderatortype", create_type=True), nullable=False)
    action: Mapped[ModerationAction] = mapped_column(SAEnum(ModerationAction, name="moderationaction", create_type=True), nullable=False)
    previous_status: Mapped[ReviewStatus | None] = mapped_column(SAEnum(ReviewStatus, name="reviewstatus", create_type=False), nullable=True)
    new_status: Mapped[ReviewStatus] = mapped_column(SAEnum(ReviewStatus, name="reviewstatus", create_type=False), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default="now()")

    review: Mapped["PlaceReview"] = relationship("PlaceReview", back_populates="moderation_logs")

    def __repr__(self) -> str:
        return f"ReviewModerationLog(id={self.id}, action={self.action})"
