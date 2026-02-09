
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, Float, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    service: Mapped[str] = mapped_column(String(120), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    tags: Mapped[dict[str, str]] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_metrics_service_name_time", Metric.service, Metric.name, Metric.timestamp)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    service: Mapped[str] = mapped_column(String(120), index=True)
    level: Mapped[str] = mapped_column(String(10), index=True)  # INFO/WARN/ERROR
    message: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    tags: Mapped[dict[str, str]] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_events_service_level_time", Event.service, Event.level, Event.timestamp)
