"""
src/models/__init__.py

Import tất cả models để Alembic autogenerate phát hiện được.
THỨ TỰ IMPORT QUAN TRỌNG — tránh circular import bằng cách import Base trước,
sau đó import theo thứ tự phụ thuộc (bảng cha trước bảng con).
"""

# 1. Base phải import đầu tiên
from src.models.base_model import Base, TimestampMixin, SoftDeleteMixin  # noqa: F401

# 2. Lookup / Independent tables
from src.models.place_model import PlaceCategory, Place, PlaceNarration  # noqa: F401

# 3. User tables (không phụ thuộc bảng nào khác)
from src.models.user_model import User, AccountStatus, UserRole  # noqa: F401
from src.models.user_profile_model import UserProfile  # noqa: F401

# 4. Session & messaging
from src.models.agent_session_model import AgentSession, AgentSessionStatus  # noqa: F401
from src.models.message_model import Message  # noqa: F401

# 5. Media
from src.models.media_file_model import MediaFile, MediaImage  # noqa: F401

# 6. Trip planning flow
from src.models.trip_request_model import (  # noqa: F401
    TripRequest, TripRequestStatus,
    TripRequestSelectedPlace,
)
from src.models.itinerary_model import (  # noqa: F401
    Itinerary, ItineraryStatus,
    ItineraryDay,
    ItineraryActivity,
    ItineraryTransit,
    ItineraryProposal, ItineraryProposalStatus,
    EvaluationResult,
)

# 7. Trip execution
from src.models.trip_model import Trip, GpsLocationEvent, TripAlert  # noqa: F401

# 8. Booking & reviews
from src.models.booking_review_model import (  # noqa: F401
    BookingOffer, BookingOfferType, BookingOfferStatus,
    PlaceReview, ReviewStatus, VisitVerificationStatus,
    ReviewReport, ReviewReportReason, ReviewReportStatus,
    ReviewModerationLog, ModerationAction, ModeratorType,
)

# 9. Trip summary
from src.models.trip_summary_model import (  # noqa: F401
    TripSummary, TripSummaryStatus,
    TripSummaryPlace, SummaryPlaceStatus,
    TripExpense, ExpenseCategory,
    NextTripSuggestion,
)

# 10. Operational / AI infrastructure
from src.models.operational_model import (  # noqa: F401
    OperatorProposal, OperatorProposalType, OperatorProposalStatus,
    AgentRun, AgentType, AgentRunTrigger, AgentRunStatus,
    ToolCall, ToolCallStatus,
    InformationSource, SourceEntityType,
    AuditAccessLog,
    AgentMemory, AgentMemoryScope,
    SystemConfig,
)

# 11. Legacy — giữ lại để không break migration cũ
from src.models.todo_model import Todo  # noqa: F401