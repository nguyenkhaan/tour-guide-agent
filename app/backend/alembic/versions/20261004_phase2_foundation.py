from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry, Geography

revision = "20261004_phase2"
down_revision = "58f3a357343b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE media_image AS ENUM ('REQUEST_IMAGE', 'REVIEW_PHOTO', 'SUMMARY_PHOTO')")
    op.execute("CREATE TYPE account_status AS ENUM ('DISABLED', 'BANNED', 'ACTIVE')")
    op.execute("CREATE TYPE agent_memory_scope AS ENUM ('WORKING', 'TRIP')")
    op.execute("CREATE TYPE agent_run_status AS ENUM ('RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'EXPIRED')")
    op.execute("CREATE TYPE agent_run_trigger AS ENUM ('USER', 'AGENT', 'BACKGROUND_JOB')")
    op.execute("CREATE TYPE agent_session_status AS ENUM ('ARCHIVED', 'ACTIVE')")
    op.execute("CREATE TYPE agent_type AS ENUM ('PLANNER', 'CRITIC', 'BOOKING')")
    op.execute("CREATE TYPE booking_offer_status AS ENUM ('AVAILABLE', 'STALE', 'UNAVAILABLE')")
    op.execute("CREATE TYPE booking_offer_type AS ENUM ('HOTEL', 'FLIGHT', 'TRANSPORT', 'ACTIVITY')")
    op.execute("CREATE TYPE expense_category AS ENUM ('LODGING', 'TRANSPORT', 'FOOD', 'TICKET', 'SHOPPING', 'OTHER')")
    op.execute("CREATE TYPE itinerary_proposal_status AS ENUM ('PENDING', 'ACCEPTED', 'REJECTED')")
    op.execute("CREATE TYPE itinerary_status AS ENUM ('DRAFT', 'REVIEWING', 'SELECTED')")
    op.execute("CREATE TYPE moderation_action AS ENUM ('APPROVE', 'REJECT', 'HIDE', 'RESTORE')")
    op.execute("CREATE TYPE moderator_type AS ENUM ('SYSTEM', 'OPERATOR', 'ADMIN')")
    op.execute("CREATE TYPE operator_proposal_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED')")
    op.execute("CREATE TYPE operator_proposal_type AS ENUM ('PLACE_UPDATE', 'WEATHER_REPORT', 'AI_ISSUE')")
    op.execute("CREATE TYPE review_report_reason AS ENUM ('SPAM', 'ABUSE', 'IRRELEVANT', 'FALSE_INFORMATION', 'OTHER')")
    op.execute("CREATE TYPE review_report_status AS ENUM ('OPEN', 'REVIEWING', 'RESOLVED', 'REJECTED')")
    op.execute("CREATE TYPE review_status AS ENUM ('PRIVATE', 'PENDING', 'PUBLIC', 'REJECTED', 'HIDDEN')")
    op.execute("CREATE TYPE source_entity_type AS ENUM ('PLACE', 'MESSAGE', 'ITINERARY', 'ITINERARY_PROPOSAL', 'EVALUATION_RESULT', 'BOOKING_OFFER', 'TRIP_ALERT')")
    op.execute("CREATE TYPE summary_place_status AS ENUM ('VISITED', 'SKIPPED', 'UNPLANNED')")
    op.execute("CREATE TYPE tool_call_status AS ENUM ('RUNNING', 'SUCCEEDED', 'FAILED')")
    op.execute("CREATE TYPE trip_request_status AS ENUM ('DRAFT', 'CONFIRMED', 'PLANNING', 'PLANNED', 'CANCELLED')")
    op.execute("CREATE TYPE trip_summary_status AS ENUM ('DRAFT', 'CONFIRMED')")
    op.execute("CREATE TYPE user_role AS ENUM ('USER', 'ADMIN', 'OPERATOR')")
    op.execute("CREATE TYPE visit_verification_status AS ENUM ('UNVERIFIED', 'VERIFIED')")

    op.create_table('agent_session',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('status', postgresql.ENUM('ARCHIVED', 'ACTIVE', name='agent_session_status', create_type=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_agent_session'))
    )
    op.create_index('ix_agent_session_user_updated', 'agent_session', ['user_id', 'updated_at'], unique=False)
    op.create_table('place_categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_place_categories'))
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('full_name', sa.String(length=200), nullable=True),
    sa.Column('status', postgresql.ENUM('DISABLED', 'BANNED', 'ACTIVE', name='account_status', create_type=False), nullable=True),
    sa.Column('role', postgresql.ENUM('USER', 'ADMIN', 'OPERATOR', name='user_role', create_type=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('system_configs',
    sa.Column('config_key', sa.String(length=100), nullable=False),
    sa.Column('config_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], name=op.f('fk_system_configs_updated_by_users')),
    sa.PrimaryKeyConstraint('config_key', name=op.f('pk_system_configs'))
    )
    op.create_index(op.f('ix_system_configs_updated_by'), 'system_configs', ['updated_by'], unique=False)
    op.create_table('trip_requests',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('parent_trip_request_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('agent_session_id', sa.UUID(), nullable=True),
    sa.Column('status', postgresql.ENUM('DRAFT', 'CONFIRMED', 'PLANNING', 'PLANNED', 'CANCELLED', name='trip_request_status', create_type=False), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('origin_name', sa.String(length=255), nullable=True),
    sa.Column('origin_location', Geometry(geometry_type="POINT", srid=4326, spatial_index=False), nullable=True),
    sa.Column('destination_text', sa.String(length=500), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('duration_days', sa.Integer(), nullable=True),
    sa.Column('budget', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('companions_count', sa.Integer(), nullable=True),
    sa.Column('companions_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name=op.f('ck_trip_requests_currency_format')),
    sa.CheckConstraint('budget >= 0', name=op.f('ck_trip_requests_budget_range')),
    sa.CheckConstraint('companions_count >= 0', name=op.f('ck_trip_requests_companions_count_nonnegative')),
    sa.CheckConstraint('duration_days > 0', name=op.f('ck_trip_requests_duration_days_positive')),
    sa.CheckConstraint('version > 0', name=op.f('ck_trip_requests_version_positive')),
    sa.ForeignKeyConstraint(['agent_session_id'], ['agent_session.id'], name=op.f('fk_trip_requests_agent_session_id_agent_session')),
    sa.ForeignKeyConstraint(['parent_trip_request_id'], ['trip_requests.id'], name=op.f('fk_trip_requests_parent_trip_request_id_trip_requests')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_trip_requests_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_requests'))
    )
    op.create_index(op.f('ix_trip_requests_agent_session_id'), 'trip_requests', ['agent_session_id'], unique=False)
    op.create_index('ix_trip_requests_origin_location', 'trip_requests', ['origin_location'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_trip_requests_parent_trip_request_id'), 'trip_requests', ['parent_trip_request_id'], unique=False)
    op.create_index(op.f('ix_trip_requests_user_id'), 'trip_requests', ['user_id'], unique=False)
    op.create_table('user_profile',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('travel_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('special_needs', sa.Text(), nullable=True),
    sa.Column('default_budget', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('preferred_currency', sa.String(length=3), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("preferred_currency ~ '^[A-Z]{3}$'", name=op.f('ck_user_profile_preferred_currency_format')),
    sa.CheckConstraint('default_budget > 0', name=op.f('ck_user_profile_default_budget_range')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_profile_user_id_users')),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user_profile'))
    )
    op.create_table('itineraries',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_request_id', sa.UUID(), nullable=True),
    sa.Column('option_index', sa.Integer(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('total_days', sa.Integer(), nullable=True),
    sa.Column('estimated_total_cost', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('cost_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('highlights', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('warnings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('trade_offs', sa.Text(), nullable=True),
    sa.Column('luggage_checklist', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('ranking_score', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('status', postgresql.ENUM('DRAFT', 'REVIEWING', 'SELECTED', name='itinerary_status', create_type=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name=op.f('ck_itineraries_currency_format')),
    sa.CheckConstraint('estimated_total_cost >= 0', name=op.f('ck_itineraries_estimated_total_cost_range')),
    sa.CheckConstraint('option_index >= 0', name=op.f('ck_itineraries_option_index_nonnegative')),
    sa.CheckConstraint('total_days > 0', name=op.f('ck_itineraries_total_days_positive')),
    sa.CheckConstraint('version > 0', name=op.f('ck_itineraries_version_positive')),
    sa.ForeignKeyConstraint(['trip_request_id'], ['trip_requests.id'], name=op.f('fk_itineraries_trip_request_id_trip_requests')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_itineraries'))
    )
    op.create_index(op.f('ix_itineraries_trip_request_id'), 'itineraries', ['trip_request_id'], unique=False)
    op.create_table('place_narrations',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('audio_object_key', sa.String(length=500), nullable=True),
    sa.Column('transcript', sa.Text(), nullable=True),
    sa.Column('duration_seconds', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('duration_seconds >= 0', name=op.f('ck_place_narrations_duration_seconds_nonnegative')),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], name=op.f('fk_place_narrations_created_by_users')),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_place_narrations_place_id_places')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_place_narrations'))
    )
    op.create_index(op.f('ix_place_narrations_created_by'), 'place_narrations', ['created_by'], unique=False)
    op.create_index(op.f('ix_place_narrations_place_id'), 'place_narrations', ['place_id'], unique=False)
    op.create_table('trip_request_selected_places',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_request_id', sa.UUID(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('selection_status', sa.String(length=20), nullable=True),
    sa.Column('selection_reason', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_trip_request_selected_places_place_id_places')),
    sa.ForeignKeyConstraint(['trip_request_id'], ['trip_requests.id'], name=op.f('fk_trip_request_selected_places_trip_request_id_trip_requests')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_request_selected_places'))
    )
    op.create_index(op.f('ix_trip_request_selected_places_place_id'), 'trip_request_selected_places', ['place_id'], unique=False)
    op.create_index(op.f('ix_trip_request_selected_places_trip_request_id'), 'trip_request_selected_places', ['trip_request_id'], unique=False)
    op.create_table('itinerary_days',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('itinerary_id', sa.UUID(), nullable=True),
    sa.Column('day_number', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('estimated_total_cost', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.CheckConstraint('day_number > 0', name=op.f('ck_itinerary_days_day_number_positive')),
    sa.CheckConstraint('estimated_total_cost >= 0', name=op.f('ck_itinerary_days_estimated_total_cost_range')),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], name=op.f('fk_itinerary_days_itinerary_id_itineraries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_itinerary_days'))
    )
    op.create_index(op.f('ix_itinerary_days_itinerary_id'), 'itinerary_days', ['itinerary_id'], unique=False)
    op.create_table('itinerary_proposals',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('itinerary_id', sa.UUID(), nullable=True),
    sa.Column('base_itinerary_id', sa.UUID(), nullable=True),
    sa.Column('target_version', sa.Integer(), nullable=True),
    sa.Column('proposed_by', sa.String(length=30), nullable=True),
    sa.Column('diff_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('rationale', sa.Text(), nullable=True),
    sa.Column('warnings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'ACCEPTED', 'REJECTED', name='itinerary_proposal_status', create_type=False), nullable=True),
    sa.Column('user_decision_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('target_version > 0', name=op.f('ck_itinerary_proposals_target_version_positive')),
    sa.ForeignKeyConstraint(['base_itinerary_id'], ['itineraries.id'], name=op.f('fk_itinerary_proposals_base_itinerary_id_itineraries')),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], name=op.f('fk_itinerary_proposals_itinerary_id_itineraries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_itinerary_proposals'))
    )
    op.create_index(op.f('ix_itinerary_proposals_base_itinerary_id'), 'itinerary_proposals', ['base_itinerary_id'], unique=False)
    op.create_index(op.f('ix_itinerary_proposals_itinerary_id'), 'itinerary_proposals', ['itinerary_id'], unique=False)
    op.create_table('trips',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('trip_request_id', sa.UUID(), nullable=True),
    sa.Column('finalized_itinerary_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('gps_consent', sa.Boolean(), nullable=True),
    sa.Column('actual_start_date', sa.Date(), nullable=True),
    sa.Column('actual_end_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['finalized_itinerary_id'], ['itineraries.id'], name=op.f('fk_trips_finalized_itinerary_id_itineraries')),
    sa.ForeignKeyConstraint(['trip_request_id'], ['trip_requests.id'], name=op.f('fk_trips_trip_request_id_trip_requests')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_trips_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trips'))
    )
    op.create_index(op.f('ix_trips_finalized_itinerary_id'), 'trips', ['finalized_itinerary_id'], unique=False)
    op.create_index(op.f('ix_trips_trip_request_id'), 'trips', ['trip_request_id'], unique=False)
    op.create_index(op.f('ix_trips_user_id'), 'trips', ['user_id'], unique=False)
    op.create_table('agent_memories',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('agent_session_id', sa.UUID(), nullable=True),
    sa.Column('trip_id', sa.UUID(), nullable=True),
    sa.Column('agent_type', postgresql.ENUM('PLANNER', 'CRITIC', 'BOOKING', name='agent_type', create_type=False), nullable=True),
    sa.Column('scope', postgresql.ENUM('WORKING', 'TRIP', name='agent_memory_scope', create_type=False), nullable=True),
    sa.Column('memory_key', sa.String(length=100), nullable=True),
    sa.Column('memory_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['agent_session_id'], ['agent_session.id'], name=op.f('fk_agent_memories_agent_session_id_agent_session')),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name=op.f('fk_agent_memories_trip_id_trips')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_agent_memories'))
    )
    op.create_index(op.f('ix_agent_memories_agent_session_id'), 'agent_memories', ['agent_session_id'], unique=False)
    op.create_index('ix_agent_memories_expires_at', 'agent_memories', ['expires_at'], unique=False)
    op.create_index(op.f('ix_agent_memories_trip_id'), 'agent_memories', ['trip_id'], unique=False)
    op.create_table('agent_runs',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('workflow_id', sa.UUID(), nullable=True),
    sa.Column('parent_run_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('agent_session_id', sa.UUID(), nullable=True),
    sa.Column('trip_request_id', sa.UUID(), nullable=True),
    sa.Column('trip_id', sa.UUID(), nullable=True),
    sa.Column('agent_type', postgresql.ENUM('PLANNER', 'CRITIC', 'BOOKING', name='agent_type', create_type=False), nullable=True),
    sa.Column('trigger_type', postgresql.ENUM('USER', 'AGENT', 'BACKGROUND_JOB', name='agent_run_trigger', create_type=False), nullable=True),
    sa.Column('status', postgresql.ENUM('RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'EXPIRED', name='agent_run_status', create_type=False), nullable=True),
    sa.Column('input_summary', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('output_summary', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('decision_summary', sa.Text(), nullable=True),
    sa.Column('error_code', sa.String(length=50), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['agent_session_id'], ['agent_session.id'], name=op.f('fk_agent_runs_agent_session_id_agent_session')),
    sa.ForeignKeyConstraint(['parent_run_id'], ['agent_runs.id'], name=op.f('fk_agent_runs_parent_run_id_agent_runs')),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name=op.f('fk_agent_runs_trip_id_trips')),
    sa.ForeignKeyConstraint(['trip_request_id'], ['trip_requests.id'], name=op.f('fk_agent_runs_trip_request_id_trip_requests')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_agent_runs_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_agent_runs'))
    )
    op.create_index(op.f('ix_agent_runs_agent_session_id'), 'agent_runs', ['agent_session_id'], unique=False)
    op.create_index('ix_agent_runs_expires_at', 'agent_runs', ['expires_at'], unique=False)
    op.create_index(op.f('ix_agent_runs_parent_run_id'), 'agent_runs', ['parent_run_id'], unique=False)
    op.create_index(op.f('ix_agent_runs_trip_id'), 'agent_runs', ['trip_id'], unique=False)
    op.create_index(op.f('ix_agent_runs_trip_request_id'), 'agent_runs', ['trip_request_id'], unique=False)
    op.create_index(op.f('ix_agent_runs_user_id'), 'agent_runs', ['user_id'], unique=False)
    op.create_index('ix_agent_runs_workflow_id', 'agent_runs', ['workflow_id'], unique=False)
    op.create_table('itinerary_activities',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('itinerary_day_id', sa.UUID(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('activity_type', sa.String(length=30), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.Column('estimated_cost', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('estimated_cost >= 0', name=op.f('ck_itinerary_activities_estimated_cost_range')),
    sa.CheckConstraint('order_index >= 0', name=op.f('ck_itinerary_activities_order_index_nonnegative')),
    sa.ForeignKeyConstraint(['itinerary_day_id'], ['itinerary_days.id'], name=op.f('fk_itinerary_activities_itinerary_day_id_itinerary_days')),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_itinerary_activities_place_id_places')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_itinerary_activities'))
    )
    op.create_index(op.f('ix_itinerary_activities_itinerary_day_id'), 'itinerary_activities', ['itinerary_day_id'], unique=False)
    op.create_index(op.f('ix_itinerary_activities_place_id'), 'itinerary_activities', ['place_id'], unique=False)
    op.create_table('operator_proposals',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('operator_id', sa.UUID(), nullable=True),
    sa.Column('proposal_type', postgresql.ENUM('PLACE_UPDATE', 'WEATHER_REPORT', 'AI_ISSUE', name='operator_proposal_type', create_type=False), nullable=True),
    sa.Column('target_place_id', sa.UUID(), nullable=True),
    sa.Column('related_trip_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('proposed_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='operator_proposal_status', create_type=False), nullable=True),
    sa.Column('admin_id', sa.UUID(), nullable=True),
    sa.Column('admin_note', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], name=op.f('fk_operator_proposals_admin_id_users')),
    sa.ForeignKeyConstraint(['operator_id'], ['users.id'], name=op.f('fk_operator_proposals_operator_id_users')),
    sa.ForeignKeyConstraint(['related_trip_id'], ['trips.id'], name=op.f('fk_operator_proposals_related_trip_id_trips')),
    sa.ForeignKeyConstraint(['target_place_id'], ['places.id'], name=op.f('fk_operator_proposals_target_place_id_places')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_operator_proposals'))
    )
    op.create_index(op.f('ix_operator_proposals_admin_id'), 'operator_proposals', ['admin_id'], unique=False)
    op.create_index(op.f('ix_operator_proposals_operator_id'), 'operator_proposals', ['operator_id'], unique=False)
    op.create_index(op.f('ix_operator_proposals_related_trip_id'), 'operator_proposals', ['related_trip_id'], unique=False)
    op.create_index(op.f('ix_operator_proposals_target_place_id'), 'operator_proposals', ['target_place_id'], unique=False)
    op.create_table('place_reviews',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('trip_id', sa.UUID(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('is_valid', sa.Boolean(), nullable=True),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('rating BETWEEN 1 AND 5', name=op.f('ck_place_reviews_rating_range')),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_place_reviews_place_id_places')),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name=op.f('fk_place_reviews_trip_id_trips')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_place_reviews_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_place_reviews'))
    )
    op.create_index(op.f('ix_place_reviews_place_id'), 'place_reviews', ['place_id'], unique=False)
    op.create_index(op.f('ix_place_reviews_trip_id'), 'place_reviews', ['trip_id'], unique=False)
    op.create_index(op.f('ix_place_reviews_user_id'), 'place_reviews', ['user_id'], unique=False)
    op.create_table('trip_summaries',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_id', sa.UUID(), nullable=True),
    sa.Column('status', postgresql.ENUM('DRAFT', 'CONFIRMED', name='trip_summary_status', create_type=False), nullable=True),
    sa.Column('overall_rating', sa.Integer(), nullable=True),
    sa.Column('diary_notes', sa.Text(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('overall_rating BETWEEN 1 AND 5', name=op.f('ck_trip_summaries_overall_rating_range')),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name=op.f('fk_trip_summaries_trip_id_trips')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_summaries'))
    )
    op.create_index(op.f('ix_trip_summaries_trip_id'), 'trip_summaries', ['trip_id'], unique=False)
    op.create_table('audit_access_logs',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('actor_id', sa.UUID(), nullable=True),
    sa.Column('target_user_id', sa.UUID(), nullable=True),
    sa.Column('agent_run_id', sa.UUID(), nullable=True),
    sa.Column('purpose', sa.Text(), nullable=True),
    sa.Column('ticket_id', sa.String(length=100), nullable=True),
    sa.Column('client_ip', sa.String(length=45), nullable=True),
    sa.Column('user_agent', sa.String(length=255), nullable=True),
    sa.Column('accessed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['users.id'], name=op.f('fk_audit_access_logs_actor_id_users')),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], name=op.f('fk_audit_access_logs_agent_run_id_agent_runs')),
    sa.ForeignKeyConstraint(['target_user_id'], ['users.id'], name=op.f('fk_audit_access_logs_target_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_audit_access_logs'))
    )
    op.create_index(op.f('ix_audit_access_logs_actor_id'), 'audit_access_logs', ['actor_id'], unique=False)
    op.create_index(op.f('ix_audit_access_logs_agent_run_id'), 'audit_access_logs', ['agent_run_id'], unique=False)
    op.create_index(op.f('ix_audit_access_logs_target_user_id'), 'audit_access_logs', ['target_user_id'], unique=False)
    op.create_table('evaluation_results',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('itinerary_id', sa.UUID(), nullable=True),
    sa.Column('proposal_id', sa.UUID(), nullable=True),
    sa.Column('agent_run_id', sa.UUID(), nullable=True),
    sa.Column('is_passed', sa.Boolean(), nullable=True),
    sa.Column('budget_status', sa.Boolean(), nullable=True),
    sa.Column('opening_hours_status', sa.Boolean(), nullable=True),
    sa.Column('travel_time_status', sa.Boolean(), nullable=True),
    sa.Column('safety_status', sa.Boolean(), nullable=True),
    sa.Column('hard_failures', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('soft_warnings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('evaluated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], name=op.f('fk_evaluation_results_agent_run_id_agent_runs')),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], name=op.f('fk_evaluation_results_itinerary_id_itineraries')),
    sa.ForeignKeyConstraint(['proposal_id'], ['itinerary_proposals.id'], name=op.f('fk_evaluation_results_proposal_id_itinerary_proposals')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_evaluation_results'))
    )
    op.create_index(op.f('ix_evaluation_results_agent_run_id'), 'evaluation_results', ['agent_run_id'], unique=False)
    op.create_index(op.f('ix_evaluation_results_itinerary_id'), 'evaluation_results', ['itinerary_id'], unique=False)
    op.create_index(op.f('ix_evaluation_results_proposal_id'), 'evaluation_results', ['proposal_id'], unique=False)
    op.create_table('itinerary_transits',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('itinerary_day_id', sa.UUID(), nullable=True),
    sa.Column('from_activity_id', sa.UUID(), nullable=True),
    sa.Column('to_activity_id', sa.UUID(), nullable=True),
    sa.Column('transport_mode', sa.String(length=30), nullable=True),
    sa.Column('estimated_duration_minutes', sa.Integer(), nullable=True),
    sa.Column('estimated_distance_km', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('estimated_cost', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('route_notes', sa.Text(), nullable=True),
    sa.CheckConstraint('estimated_cost >= 0', name=op.f('ck_itinerary_transits_estimated_cost_range')),
    sa.CheckConstraint('estimated_distance_km >= 0', name=op.f('ck_itinerary_transits_estimated_distance_km_range')),
    sa.CheckConstraint('estimated_duration_minutes >= 0', name=op.f('ck_itinerary_transits_estimated_duration_minutes_nonnegative')),
    sa.ForeignKeyConstraint(['from_activity_id'], ['itinerary_activities.id'], name=op.f('fk_itinerary_transits_from_activity_id_itinerary_activities')),
    sa.ForeignKeyConstraint(['itinerary_day_id'], ['itinerary_days.id'], name=op.f('fk_itinerary_transits_itinerary_day_id_itinerary_days')),
    sa.ForeignKeyConstraint(['to_activity_id'], ['itinerary_activities.id'], name=op.f('fk_itinerary_transits_to_activity_id_itinerary_activities')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_itinerary_transits'))
    )
    op.create_index(op.f('ix_itinerary_transits_from_activity_id'), 'itinerary_transits', ['from_activity_id'], unique=False)
    op.create_index(op.f('ix_itinerary_transits_itinerary_day_id'), 'itinerary_transits', ['itinerary_day_id'], unique=False)
    op.create_index(op.f('ix_itinerary_transits_to_activity_id'), 'itinerary_transits', ['to_activity_id'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('agent_session_id', sa.UUID(), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('sources', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('agent_run_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("role IN ('user', 'assistant')", name=op.f('ck_messages_role_values')),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], name=op.f('fk_messages_agent_run_id_agent_runs')),
    sa.ForeignKeyConstraint(['agent_session_id'], ['agent_session.id'], name=op.f('fk_messages_agent_session_id_agent_session')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    op.create_index(op.f('ix_messages_agent_run_id'), 'messages', ['agent_run_id'], unique=False)
    op.create_index(op.f('ix_messages_agent_session_id'), 'messages', ['agent_session_id'], unique=False)
    op.create_index('ix_messages_session_created', 'messages', ['agent_session_id', 'created_at'], unique=False)
    op.create_table('next_trip_suggestions',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_summary_id', sa.UUID(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('suggested_places', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('estimated_budget', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('started_agent_session_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name=op.f('ck_next_trip_suggestions_currency_format')),
    sa.CheckConstraint('estimated_budget >= 0', name=op.f('ck_next_trip_suggestions_estimated_budget_range')),
    sa.CheckConstraint('rank BETWEEN 1 AND 3', name=op.f('ck_next_trip_suggestions_rank_range')),
    sa.ForeignKeyConstraint(['started_agent_session_id'], ['agent_session.id'], name=op.f('fk_next_trip_suggestions_started_agent_session_id_agent_session')),
    sa.ForeignKeyConstraint(['trip_summary_id'], ['trip_summaries.id'], name=op.f('fk_next_trip_suggestions_trip_summary_id_trip_summaries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_next_trip_suggestions'))
    )
    op.create_index(op.f('ix_next_trip_suggestions_started_agent_session_id'), 'next_trip_suggestions', ['started_agent_session_id'], unique=False)
    op.create_index(op.f('ix_next_trip_suggestions_trip_summary_id'), 'next_trip_suggestions', ['trip_summary_id'], unique=False)
    op.create_table('review_moderation_logs',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('review_id', sa.UUID(), nullable=True),
    sa.Column('moderator_id', sa.UUID(), nullable=True),
    sa.Column('moderator_type', postgresql.ENUM('SYSTEM', 'OPERATOR', 'ADMIN', name='moderator_type', create_type=False), nullable=True),
    sa.Column('action', postgresql.ENUM('APPROVE', 'REJECT', 'HIDE', 'RESTORE', name='moderation_action', create_type=False), nullable=True),
    sa.Column('previous_status', postgresql.ENUM('PRIVATE', 'PENDING', 'PUBLIC', 'REJECTED', 'HIDDEN', name='review_status', create_type=False), nullable=True),
    sa.Column('new_status', postgresql.ENUM('PRIVATE', 'PENDING', 'PUBLIC', 'REJECTED', 'HIDDEN', name='review_status', create_type=False), nullable=True),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['moderator_id'], ['users.id'], name=op.f('fk_review_moderation_logs_moderator_id_users')),
    sa.ForeignKeyConstraint(['review_id'], ['place_reviews.id'], name=op.f('fk_review_moderation_logs_review_id_place_reviews')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_review_moderation_logs'))
    )
    op.create_index(op.f('ix_review_moderation_logs_moderator_id'), 'review_moderation_logs', ['moderator_id'], unique=False)
    op.create_index(op.f('ix_review_moderation_logs_review_id'), 'review_moderation_logs', ['review_id'], unique=False)
    op.create_table('review_reports',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('review_id', sa.UUID(), nullable=True),
    sa.Column('reporter_user_id', sa.UUID(), nullable=True),
    sa.Column('reason_code', postgresql.ENUM('SPAM', 'ABUSE', 'IRRELEVANT', 'FALSE_INFORMATION', 'OTHER', name='review_report_reason', create_type=False), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('status', postgresql.ENUM('OPEN', 'REVIEWING', 'RESOLVED', 'REJECTED', name='review_report_status', create_type=False), nullable=True),
    sa.Column('resolved_by', sa.UUID(), nullable=True),
    sa.Column('resolution', sa.Text(), nullable=True),
    sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['reporter_user_id'], ['users.id'], name=op.f('fk_review_reports_reporter_user_id_users')),
    sa.ForeignKeyConstraint(['resolved_by'], ['users.id'], name=op.f('fk_review_reports_resolved_by_users')),
    sa.ForeignKeyConstraint(['review_id'], ['place_reviews.id'], name=op.f('fk_review_reports_review_id_place_reviews')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_review_reports'))
    )
    op.create_index(op.f('ix_review_reports_reporter_user_id'), 'review_reports', ['reporter_user_id'], unique=False)
    op.create_index(op.f('ix_review_reports_resolved_by'), 'review_reports', ['resolved_by'], unique=False)
    op.create_index(op.f('ix_review_reports_review_id'), 'review_reports', ['review_id'], unique=False)
    op.create_table('tool_calls',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('agent_run_id', sa.UUID(), nullable=True),
    sa.Column('tool_name', sa.String(length=100), nullable=True),
    sa.Column('arguments', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', postgresql.ENUM('RUNNING', 'SUCCEEDED', 'FAILED', name='tool_call_status', create_type=False), nullable=True),
    sa.Column('error_code', sa.String(length=50), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], name=op.f('fk_tool_calls_agent_run_id_agent_runs')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tool_calls'))
    )
    op.create_index(op.f('ix_tool_calls_agent_run_id'), 'tool_calls', ['agent_run_id'], unique=False)
    op.create_index('ix_tool_calls_expires_at', 'tool_calls', ['expires_at'], unique=False)
    op.create_table('trip_alerts',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_id', sa.UUID(), nullable=True),
    sa.Column('alert_type', sa.String(length=30), nullable=True),
    sa.Column('severity', sa.String(length=20), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('source', sa.String(length=100), nullable=True),
    sa.Column('checked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('confidence', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('affected_activity_id', sa.UUID(), nullable=True),
    sa.Column('alternative_proposal_id', sa.UUID(), nullable=True),
    sa.Column('is_resolved', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('confidence BETWEEN 0 AND 1', name=op.f('ck_trip_alerts_confidence_range')),
    sa.ForeignKeyConstraint(['affected_activity_id'], ['itinerary_activities.id'], name=op.f('fk_trip_alerts_affected_activity_id_itinerary_activities')),
    sa.ForeignKeyConstraint(['alternative_proposal_id'], ['itinerary_proposals.id'], name=op.f('fk_trip_alerts_alternative_proposal_id_itinerary_proposals')),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], name=op.f('fk_trip_alerts_trip_id_trips')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_alerts'))
    )
    op.create_index(op.f('ix_trip_alerts_affected_activity_id'), 'trip_alerts', ['affected_activity_id'], unique=False)
    op.create_index(op.f('ix_trip_alerts_alternative_proposal_id'), 'trip_alerts', ['alternative_proposal_id'], unique=False)
    op.create_index(op.f('ix_trip_alerts_trip_id'), 'trip_alerts', ['trip_id'], unique=False)
    op.create_table('trip_expenses',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_summary_id', sa.UUID(), nullable=True),
    sa.Column('category', postgresql.ENUM('LODGING', 'TRANSPORT', 'FOOD', 'TICKET', 'SHOPPING', 'OTHER', name='expense_category', create_type=False), nullable=True),
    sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('spent_on', sa.Date(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name=op.f('ck_trip_expenses_currency_format')),
    sa.CheckConstraint('amount >= 0', name=op.f('ck_trip_expenses_amount_range')),
    sa.ForeignKeyConstraint(['trip_summary_id'], ['trip_summaries.id'], name=op.f('fk_trip_expenses_trip_summary_id_trip_summaries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_expenses'))
    )
    op.create_index(op.f('ix_trip_expenses_trip_summary_id'), 'trip_expenses', ['trip_summary_id'], unique=False)
    op.create_table('trip_summary_places',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trip_summary_id', sa.UUID(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('place_name', sa.String(length=255), nullable=True),
    sa.Column('status', postgresql.ENUM('VISITED', 'SKIPPED', 'UNPLANNED', name='summary_place_status', create_type=False), nullable=True),
    sa.Column('confidence', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('evidence', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_user_corrected', sa.Boolean(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('confidence BETWEEN 0 AND 1', name=op.f('ck_trip_summary_places_confidence_range')),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_trip_summary_places_place_id_places')),
    sa.ForeignKeyConstraint(['trip_summary_id'], ['trip_summaries.id'], name=op.f('fk_trip_summary_places_trip_summary_id_trip_summaries')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trip_summary_places'))
    )
    op.create_index(op.f('ix_trip_summary_places_place_id'), 'trip_summary_places', ['place_id'], unique=False)
    op.create_index(op.f('ix_trip_summary_places_trip_summary_id'), 'trip_summary_places', ['trip_summary_id'], unique=False)
    op.create_table('entity_log',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('entity_type', postgresql.ENUM('PLACE', 'MESSAGE', 'ITINERARY', 'ITINERARY_PROPOSAL', 'EVALUATION_RESULT', 'BOOKING_OFFER', 'TRIP_ALERT', name='source_entity_type', create_type=False), nullable=True),
    sa.Column('entity_id', sa.UUID(), nullable=True),
    sa.Column('field_name', sa.String(length=100), nullable=True),
    sa.Column('checked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('confidence', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('agent_run_id', sa.UUID(), nullable=True),
    sa.Column('tool_call_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('confidence BETWEEN 0 AND 1', name=op.f('ck_entity_log_confidence_range')),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], name=op.f('fk_entity_log_agent_run_id_agent_runs')),
    sa.ForeignKeyConstraint(['tool_call_id'], ['tool_calls.id'], name=op.f('fk_entity_log_tool_call_id_tool_calls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_entity_log'))
    )
    op.create_index(op.f('ix_entity_log_agent_run_id'), 'entity_log', ['agent_run_id'], unique=False)
    op.create_index('ix_entity_log_entity_checked', 'entity_log', ['entity_type', 'entity_id', 'checked_at'], unique=False)
    op.create_index(op.f('ix_entity_log_tool_call_id'), 'entity_log', ['tool_call_id'], unique=False)
    op.create_table('media_files',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('message_id', sa.UUID(), nullable=True),
    sa.Column('object_key', sa.String(length=500), nullable=True),
    sa.Column('file_name', sa.String(length=255), nullable=True),
    sa.Column('file_size_bytes', sa.BigInteger(), nullable=True),
    sa.Column('mime_type', sa.String(length=100), nullable=True),
    sa.Column('purpose', postgresql.ENUM('REQUEST_IMAGE', 'REVIEW_PHOTO', 'SUMMARY_PHOTO', name='media_image', create_type=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('file_size_bytes >= 0', name=op.f('ck_media_files_file_size_bytes_nonnegative')),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name=op.f('fk_media_files_message_id_messages')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_media_files_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_media_files'))
    )
    op.create_index(op.f('ix_media_files_message_id'), 'media_files', ['message_id'], unique=False)
    op.create_index(op.f('ix_media_files_user_id'), 'media_files', ['user_id'], unique=False)
    op.drop_index('idx_places_location', table_name='places')
    op.alter_column('places', 'name',
               existing_type=sa.String(),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('places', 'location',
               existing_type=Geography(geometry_type="POINT", srid=4326, spatial_index=False),
               type_=Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
               postgresql_using="location::geometry",
               nullable=True)
    op.alter_column('places', 'id',
               existing_type=sa.UUID(),
               server_default=sa.text("gen_random_uuid()"),
               existing_nullable=False)
    op.add_column('places', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('places', sa.Column('slug', sa.String(length=255), nullable=True))
    op.add_column('places', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('places', sa.Column('address', sa.String(length=500), nullable=True))
    op.add_column('places', sa.Column('province', sa.String(length=100), nullable=True))
    op.add_column('places', sa.Column('start_time', sa.DateTime(timezone=True), nullable=True))
    op.add_column('places', sa.Column('end_time', sa.DateTime(timezone=True), nullable=True))
    op.add_column('places', sa.Column('min_price', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('places', sa.Column('max_price', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('places', sa.Column('currency', sa.String(length=3), nullable=True))
    op.add_column('places', sa.Column('average_rating', sa.Float(), nullable=True))
    op.add_column('places', sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('places', sa.Column('visual_attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('places', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('places', sa.Column('created_by', sa.UUID(), nullable=True))
    op.add_column('places', sa.Column('updated_by', sa.UUID(), nullable=True))
    op.add_column('places', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('places', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_check_constraint(op.f('ck_places_currency_format'), 'places', "currency ~ '^[A-Z]{3}$'")
    op.create_check_constraint(op.f('ck_places_max_price_range'), 'places', 'max_price >= 0')
    op.create_check_constraint(op.f('ck_places_min_price_range'), 'places', 'min_price >= 0')
    op.create_check_constraint(op.f('ck_places_price_order'), 'places', 'max_price >= min_price')
    op.create_unique_constraint(op.f('uq_places_slug'), 'places', ['slug'])
    op.create_foreign_key(op.f('fk_places_category_id_place_categories'), 'places', 'place_categories', ['category_id'], ['id'])
    op.create_foreign_key(op.f('fk_places_created_by_users'), 'places', 'users', ['created_by'], ['id'])
    op.create_foreign_key(op.f('fk_places_updated_by_users'), 'places', 'users', ['updated_by'], ['id'])
    op.create_index(op.f('ix_places_category_id'), 'places', ['category_id'], unique=False)
    op.create_index(op.f('ix_places_created_by'), 'places', ['created_by'], unique=False)
    op.create_index('ix_places_location', 'places', ['location'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_places_updated_by'), 'places', ['updated_by'], unique=False)


def downgrade() -> None:

    op.execute("""DO $$ BEGIN
        IF EXISTS (SELECT 1 FROM places WHERE location IS NULL) THEN
            RAISE EXCEPTION 'Cannot downgrade: places.location contains NULL values';
        END IF;
    END $$""")

    op.drop_index(op.f('ix_places_category_id'), table_name='places')
    op.drop_index(op.f('ix_places_created_by'), table_name='places')
    op.drop_index('ix_places_location', table_name='places')
    op.drop_index(op.f('ix_places_updated_by'), table_name='places')
    op.drop_constraint(op.f('ck_places_currency_format'), 'places', type_='check')
    op.drop_constraint(op.f('ck_places_max_price_range'), 'places', type_='check')
    op.drop_constraint(op.f('ck_places_min_price_range'), 'places', type_='check')
    op.drop_constraint(op.f('ck_places_price_order'), 'places', type_='check')
    op.drop_constraint(op.f('uq_places_slug'), 'places', type_='unique')
    op.drop_constraint(op.f('fk_places_category_id_place_categories'), 'places', type_='foreignkey')
    op.drop_constraint(op.f('fk_places_created_by_users'), 'places', type_='foreignkey')
    op.drop_constraint(op.f('fk_places_updated_by_users'), 'places', type_='foreignkey')
    op.drop_column('places', 'updated_at')
    op.drop_column('places', 'created_at')
    op.drop_column('places', 'updated_by')
    op.drop_column('places', 'created_by')
    op.drop_column('places', 'is_active')
    op.drop_column('places', 'visual_attributes')
    op.drop_column('places', 'images')
    op.drop_column('places', 'average_rating')
    op.drop_column('places', 'currency')
    op.drop_column('places', 'max_price')
    op.drop_column('places', 'min_price')
    op.drop_column('places', 'end_time')
    op.drop_column('places', 'start_time')
    op.drop_column('places', 'province')
    op.drop_column('places', 'address')
    op.drop_column('places', 'description')
    op.drop_column('places', 'slug')
    op.drop_column('places', 'category_id')
    op.alter_column('places', 'name',
               existing_type=sa.String(length=255),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('places', 'location',
               existing_type=Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
               type_=Geography(geometry_type="POINT", srid=4326, spatial_index=False),
               postgresql_using="location::geography",
               nullable=False)
    op.alter_column('places', 'id',
               existing_type=sa.UUID(),
               server_default=None,
               existing_nullable=False)
    op.create_index('idx_places_location', 'places', ['location'], unique=False, postgresql_using='gist')
    op.drop_table('media_files')
    op.drop_table('entity_log')
    op.drop_table('trip_summary_places')
    op.drop_table('trip_expenses')
    op.drop_table('trip_alerts')
    op.drop_table('tool_calls')
    op.drop_table('review_reports')
    op.drop_table('review_moderation_logs')
    op.drop_table('next_trip_suggestions')
    op.drop_table('messages')
    op.drop_table('itinerary_transits')
    op.drop_table('evaluation_results')
    op.drop_table('audit_access_logs')
    op.drop_table('trip_summaries')
    op.drop_table('place_reviews')
    op.drop_table('operator_proposals')
    op.drop_table('itinerary_activities')
    op.drop_table('agent_runs')
    op.drop_table('agent_memories')
    op.drop_table('trips')
    op.drop_table('itinerary_proposals')
    op.drop_table('itinerary_days')
    op.drop_table('trip_request_selected_places')
    op.drop_table('place_narrations')
    op.drop_table('itineraries')
    op.drop_table('user_profile')
    op.drop_table('trip_requests')
    op.drop_table('system_configs')
    op.drop_table('users')
    op.drop_table('place_categories')
    op.drop_table('agent_session')

    op.execute("DROP TYPE visit_verification_status")
    op.execute("DROP TYPE user_role")
    op.execute("DROP TYPE trip_summary_status")
    op.execute("DROP TYPE trip_request_status")
    op.execute("DROP TYPE tool_call_status")
    op.execute("DROP TYPE summary_place_status")
    op.execute("DROP TYPE source_entity_type")
    op.execute("DROP TYPE review_status")
    op.execute("DROP TYPE review_report_status")
    op.execute("DROP TYPE review_report_reason")
    op.execute("DROP TYPE operator_proposal_type")
    op.execute("DROP TYPE operator_proposal_status")
    op.execute("DROP TYPE moderator_type")
    op.execute("DROP TYPE moderation_action")
    op.execute("DROP TYPE media_image")
    op.execute("DROP TYPE itinerary_status")
    op.execute("DROP TYPE itinerary_proposal_status")
    op.execute("DROP TYPE expense_category")
    op.execute("DROP TYPE booking_offer_type")
    op.execute("DROP TYPE booking_offer_status")
    op.execute("DROP TYPE agent_type")
    op.execute("DROP TYPE agent_session_status")
    op.execute("DROP TYPE agent_run_trigger")
    op.execute("DROP TYPE agent_run_status")
    op.execute("DROP TYPE agent_memory_scope")
    op.execute("DROP TYPE account_status")
