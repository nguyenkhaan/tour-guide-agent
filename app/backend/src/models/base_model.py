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
from uuid import uuid4

from sqlalchemy import DateTime, MetaData, UUID, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    type_annotation_map = {datetime.datetime: DateTime(timezone=True)}
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

AccountStatus = ENUM('DISABLED', 'BANNED', 'ACTIVE', name="account_status", validate_strings=True)
UserRole = ENUM('USER', 'ADMIN', 'OPERATOR', name="user_role", validate_strings=True)
MediaImage = ENUM('REQUEST_IMAGE', 'REVIEW_PHOTO', 'SUMMARY_PHOTO', name="media_image", validate_strings=True)
AgentSessionStatus = ENUM('ARCHIVED', 'ACTIVE', name="agent_session_status", validate_strings=True)
TripRequestStatus = ENUM('DRAFT', 'CONFIRMED', 'PLANNING', 'PLANNED', 'CANCELLED', name="trip_request_status", validate_strings=True)
ItineraryStatus = ENUM('DRAFT', 'REVIEWING', 'SELECTED', name="itinerary_status", validate_strings=True)
ItineraryProposalStatus = ENUM('PENDING', 'ACCEPTED', 'REJECTED', name="itinerary_proposal_status", validate_strings=True)
BookingOfferType = ENUM('HOTEL', 'FLIGHT', 'TRANSPORT', 'ACTIVITY', name="booking_offer_type", validate_strings=True)
BookingOfferStatus = ENUM('AVAILABLE', 'STALE', 'UNAVAILABLE', name="booking_offer_status", validate_strings=True)
ReviewStatus = ENUM('PRIVATE', 'PENDING', 'PUBLIC', 'REJECTED', 'HIDDEN', name="review_status", validate_strings=True)
VisitVerificationStatus = ENUM('UNVERIFIED', 'VERIFIED', name="visit_verification_status", validate_strings=True)
ReviewReportReason = ENUM('SPAM', 'ABUSE', 'IRRELEVANT', 'FALSE_INFORMATION', 'OTHER', name="review_report_reason", validate_strings=True)
ReviewReportStatus = ENUM('OPEN', 'REVIEWING', 'RESOLVED', 'REJECTED', name="review_report_status", validate_strings=True)
ModerationAction = ENUM('APPROVE', 'REJECT', 'HIDE', 'RESTORE', name="moderation_action", validate_strings=True)
ModeratorType = ENUM('SYSTEM', 'OPERATOR', 'ADMIN', name="moderator_type", validate_strings=True)
TripSummaryStatus = ENUM('DRAFT', 'CONFIRMED', name="trip_summary_status", validate_strings=True)
SummaryPlaceStatus = ENUM('VISITED', 'SKIPPED', 'UNPLANNED', name="summary_place_status", validate_strings=True)
ExpenseCategory = ENUM('LODGING', 'TRANSPORT', 'FOOD', 'TICKET', 'SHOPPING', 'OTHER', name="expense_category", validate_strings=True)
OperatorProposalType = ENUM('PLACE_UPDATE', 'WEATHER_REPORT', 'AI_ISSUE', name="operator_proposal_type", validate_strings=True)
OperatorProposalStatus = ENUM('PENDING', 'APPROVED', 'REJECTED', name="operator_proposal_status", validate_strings=True)
AgentType = ENUM('PLANNER', 'CRITIC', 'BOOKING', name="agent_type", validate_strings=True)
AgentRunTrigger = ENUM('USER', 'AGENT', 'BACKGROUND_JOB', name="agent_run_trigger", validate_strings=True)
AgentRunStatus = ENUM('RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'EXPIRED', name="agent_run_status", validate_strings=True)
ToolCallStatus = ENUM('RUNNING', 'SUCCEEDED', 'FAILED', name="tool_call_status", validate_strings=True)
AgentMemoryScope = ENUM('WORKING', 'TRIP', name="agent_memory_scope", validate_strings=True)
SourceEntityType = ENUM('PLACE', 'MESSAGE', 'ITINERARY', 'ITINERARY_PROPOSAL', 'EVALUATION_RESULT', 'BOOKING_OFFER', 'TRIP_ALERT', name="source_entity_type", validate_strings=True)
