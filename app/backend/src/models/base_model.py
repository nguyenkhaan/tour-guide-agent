"""
Postgres SQL command 
## Drop schema public -> reset database if failed qua roi 
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

## PostGIS extension CAST OFF
CREATE EXTENSION postgis;

"""
import datetime
from datetime import timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, MetaData, UUID, func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column


class AccountStatus(str, Enum):
    DISABLED = "DISABLED"
    BANNED = "BANNED"
    ACTIVE = "ACTIVE"


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class MediaImage(str, Enum):
    REQUEST_IMAGE = "REQUEST_IMAGE"
    REVIEW_PHOTO = "REVIEW_PHOTO"
    SUMMARY_PHOTO = "SUMMARY_PHOTO"


class AgentSessionStatus(str, Enum):
    ARCHIVED = "ARCHIVED"
    ACTIVE = "ACTIVE"


class TripRequestStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    PLANNING = "PLANNING"
    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"


class ItineraryStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEWING = "REVIEWING"
    SELECTED = "SELECTED"


class ItineraryProposalStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class BookingOfferType(str, Enum):
    HOTEL = "HOTEL"
    FLIGHT = "FLIGHT"
    TRANSPORT = "TRANSPORT"
    ACTIVITY = "ACTIVITY"


class BookingOfferStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class ReviewStatus(str, Enum):
    PRIVATE = "PRIVATE"
    PENDING = "PENDING"
    PUBLIC = "PUBLIC"
    REJECTED = "REJECTED"
    HIDDEN = "HIDDEN"


class VisitVerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class ReviewReportReason(str, Enum):
    SPAM = "SPAM"
    ABUSE = "ABUSE"
    IRRELEVANT = "IRRELEVANT"
    FALSE_INFORMATION = "FALSE_INFORMATION"
    OTHER = "OTHER"


class ReviewReportStatus(str, Enum):
    OPEN = "OPEN"
    REVIEWING = "REVIEWING"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class ModerationAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    HIDE = "HIDE"
    RESTORE = "RESTORE"


class ModeratorType(str, Enum):
    SYSTEM = "SYSTEM"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"


class TripSummaryStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"


class SummaryPlaceStatus(str, Enum):
    VISITED = "VISITED"
    SKIPPED = "SKIPPED"
    UNPLANNED = "UNPLANNED"


class ExpenseCategory(str, Enum):
    LODGING = "LODGING"
    TRANSPORT = "TRANSPORT"
    FOOD = "FOOD"
    TICKET = "TICKET"
    SHOPPING = "SHOPPING"
    OTHER = "OTHER"


class OperatorProposalType(str, Enum):
    PLACE_UPDATE = "PLACE_UPDATE"
    WEATHER_REPORT = "WEATHER_REPORT"
    AI_ISSUE = "AI_ISSUE"


class OperatorProposalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AgentType(str, Enum):
    PLANNER = "PLANNER"
    CRITIC = "CRITIC"
    BOOKING = "BOOKING"


class AgentRunTrigger(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    BACKGROUND_JOB = "BACKGROUND_JOB"


class AgentRunStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ToolCallStatus(str, Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class AgentMemoryScope(str, Enum):
    WORKING = "WORKING"
    TRIP = "TRIP"


class SourceEntityType(str, Enum):
    PLACE = "PLACE"
    MESSAGE = "MESSAGE"
    ITINERARY = "ITINERARY"
    ITINERARY_PROPOSAL = "ITINERARY_PROPOSAL"
    EVALUATION_RESULT = "EVALUATION_RESULT"
    BOOKING_OFFER = "BOOKING_OFFER"
    TRIP_ALERT = "TRIP_ALERT"


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
        AccountStatus: PgEnum(AccountStatus, name="account_status", validate_strings=True),
        UserRole: PgEnum(UserRole, name="user_role", validate_strings=True),
        MediaImage: PgEnum(MediaImage, name="media_image", validate_strings=True),
        AgentSessionStatus: PgEnum(AgentSessionStatus, name="agent_session_status", validate_strings=True),
        TripRequestStatus: PgEnum(TripRequestStatus, name="trip_request_status", validate_strings=True),
        ItineraryStatus: PgEnum(ItineraryStatus, name="itinerary_status", validate_strings=True),
        ItineraryProposalStatus: PgEnum(ItineraryProposalStatus, name="itinerary_proposal_status", validate_strings=True),
        BookingOfferType: PgEnum(BookingOfferType, name="booking_offer_type", validate_strings=True),
        BookingOfferStatus: PgEnum(BookingOfferStatus, name="booking_offer_status", validate_strings=True),
        ReviewStatus: PgEnum(ReviewStatus, name="review_status", validate_strings=True),
        VisitVerificationStatus: PgEnum(VisitVerificationStatus, name="visit_verification_status", validate_strings=True),
        ReviewReportReason: PgEnum(ReviewReportReason, name="review_report_reason", validate_strings=True),
        ReviewReportStatus: PgEnum(ReviewReportStatus, name="review_report_status", validate_strings=True),
        ModerationAction: PgEnum(ModerationAction, name="moderation_action", validate_strings=True),
        ModeratorType: PgEnum(ModeratorType, name="moderator_type", validate_strings=True),
        TripSummaryStatus: PgEnum(TripSummaryStatus, name="trip_summary_status", validate_strings=True),
        SummaryPlaceStatus: PgEnum(SummaryPlaceStatus, name="summary_place_status", validate_strings=True),
        ExpenseCategory: PgEnum(ExpenseCategory, name="expense_category", validate_strings=True),
        OperatorProposalType: PgEnum(OperatorProposalType, name="operator_proposal_type", validate_strings=True),
        OperatorProposalStatus: PgEnum(OperatorProposalStatus, name="operator_proposal_status", validate_strings=True),
        AgentType: PgEnum(AgentType, name="agent_type", validate_strings=True),
        AgentRunTrigger: PgEnum(AgentRunTrigger, name="agent_run_trigger", validate_strings=True),
        AgentRunStatus: PgEnum(AgentRunStatus, name="agent_run_status", validate_strings=True),
        ToolCallStatus: PgEnum(ToolCallStatus, name="tool_call_status", validate_strings=True),
        AgentMemoryScope: PgEnum(AgentMemoryScope, name="agent_memory_scope", validate_strings=True),
        SourceEntityType: PgEnum(SourceEntityType, name="source_entity_type", validate_strings=True),
    }
    metadata = MetaData(naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


def uuid_primary_key():
    from sqlalchemy import text
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                         server_default=text("gen_random_uuid()"))


def created_timestamp():
    return mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


def updated_timestamp():
    return mapped_column(DateTime(timezone=True), nullable=False,
                         server_default=func.now(), onupdate=func.now())


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(timezone.utc)


def as_utc(value: datetime.datetime) -> datetime.datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Datetime must include a timezone offset")
    return value.astimezone(timezone.utc)


def datetime_to_iso8601(value: datetime.datetime) -> str:
    return as_utc(value).isoformat().replace("+00:00", "Z")
