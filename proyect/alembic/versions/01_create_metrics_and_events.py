"""create metrics and events tables

Revision ID: 0001_create_metrics_events
Revises:
Create Date: 2026-02-10 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_metrics_events"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "metrics",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("service", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=40), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_metrics_service", "metrics", ["service"])
    op.create_index("ix_metrics_name", "metrics", ["name"])
    op.create_index("ix_metrics_timestamp", "metrics", ["timestamp"])
    op.create_index("ix_metrics_service_name_time", "metrics", ["service", "name", "timestamp"])

    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("service", sa.String(length=120), nullable=False),
        sa.Column("level", sa.String(length=10), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_events_service", "events", ["service"])
    op.create_index("ix_events_level", "events", ["level"])
    op.create_index("ix_events_timestamp", "events", ["timestamp"])
    op.create_index("ix_events_service_level_time", "events", ["service", "level", "timestamp"])


def downgrade() -> None:
    op.drop_index("ix_events_service_level_time", table_name="events")
    op.drop_index("ix_events_timestamp", table_name="events")
    op.drop_index("ix_events_level", table_name="events")
    op.drop_index("ix_events_service", table_name="events")
    op.drop_table("events")

    op.drop_index("ix_metrics_service_name_time", table_name="metrics")
    op.drop_index("ix_metrics_timestamp", table_name="metrics")
    op.drop_index("ix_metrics_name", table_name="metrics")
    op.drop_index("ix_metrics_service", table_name="metrics")
    op.drop_table("metrics")
