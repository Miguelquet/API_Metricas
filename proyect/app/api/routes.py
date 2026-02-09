from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import require_read_api_key, require_write_api_key
from app.db.models import Event, Metric
from app.db.session import SessionLocal
from app.schemas import (
    EventIn,
    EventListOut,
    EventOut,
    MetricIn,
    MetricListOut,
    MetricOut,
    MetricStatsOut,
    PageMeta,
)

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_tags(tag_params: list[str] | None) -> dict[str, str]:
    if not tag_params:
        return {}
    tags: dict[str, str] = {}
    for raw in tag_params:
        if ":" not in raw:
            raise HTTPException(status_code=400, detail="Invalid tag format. Use tag=key:value")
        k, v = raw.split(":", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise HTTPException(status_code=400, detail="Invalid tag key")
        tags[k] = v
    if len(tags) > settings.max_tags:
        raise HTTPException(status_code=400, detail=f"Too many tags (max {settings.max_tags})")
    return tags


def clamp_pagination(limit: int, offset: int) -> tuple[int, int]:
    if limit < 1:
        limit = 1
    if limit > settings.max_page_size:
        limit = settings.max_page_size
    if offset < 0:
        offset = 0
    return limit, offset

#Hardcodeado porque si no llega a hacerlo es que esta muerto el servidor igualmente
@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="Not ready")
    return {"status": "ready"}


@router.post(
    "/v1/metrics",
    status_code=status.HTTP_201_CREATED,
    response_model=MetricOut,
    dependencies=[Depends(require_write_api_key)],
)
def create_metric(payload: MetricIn, db: Session = Depends(get_db)) -> Metric:
    ts = payload.timestamp or utc_now()

    metric = Metric(
        service=payload.service,
        name=payload.name,
        value=float(payload.value),
        unit=payload.unit,
        timestamp=ts,
        tags=payload.tags or {},
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


@router.post(
    "/v1/events",
    status_code=status.HTTP_201_CREATED,
    response_model=EventOut,
    dependencies=[Depends(require_write_api_key)],
)
def create_event(payload: EventIn, db: Session = Depends(get_db)) -> Event:
    ts = payload.timestamp or utc_now()

    ev = Event(
        service=payload.service,
        level=payload.level.value,
        message=payload.message,
        timestamp=ts,
        tags=payload.tags or {},
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.get(
    "/v1/metrics",
    response_model=MetricListOut,
    dependencies=[Depends(require_read_api_key)],
)
def list_metrics(
    db: Session = Depends(get_db),
    service: str | None = Query(default=None),
    name: str | None = Query(default=None),
    from_ts: datetime | None = Query(default=None),
    to_ts: datetime | None = Query(default=None),
    tag: list[str] | None = Query(default=None),
    limit: int = Query(default=100),
    offset: int = Query(default=0),
) -> MetricListOut:
    tags = parse_tags(tag)
    limit, offset = clamp_pagination(limit, offset)

    conditions = []
    if service:
        conditions.append(Metric.service == service)
    if name:
        conditions.append(Metric.name == name)
    if from_ts:
        conditions.append(Metric.timestamp >= from_ts)
    if to_ts:
        conditions.append(Metric.timestamp <= to_ts)
    if tags:
        conditions.append(Metric.tags.contains(tags))  

    where_clause = and_(*conditions) if conditions else None

    total_stmt = select(func.count()).select_from(Metric)
    if where_clause is not None:
        total_stmt = total_stmt.where(where_clause)
    count = db.execute(total_stmt).scalar_one()

    stmt = select(Metric).order_by(Metric.timestamp.desc()).limit(limit).offset(offset)
    if where_clause is not None:
        stmt = stmt.where(where_clause)

    items = db.execute(stmt).scalars().all()
    return MetricListOut(meta=PageMeta(limit=limit, offset=offset, count=count), items=items)


@router.get(
    "/v1/events",
    response_model=EventListOut,
    dependencies=[Depends(require_read_api_key)],
)
def list_events(
    db: Session = Depends(get_db),
    service: str | None = Query(default=None),
    level: str | None = Query(default=None, description="INFO|WARN|ERROR"),
    from_ts: datetime | None = Query(default=None),
    to_ts: datetime | None = Query(default=None),
    tag: list[str] | None = Query(default=None),
    limit: int = Query(default=100),
    offset: int = Query(default=0),
) -> EventListOut:
    tags = parse_tags(tag)
    limit, offset = clamp_pagination(limit, offset)

    conditions = []
    if service:
        conditions.append(Event.service == service)
    if level:
        conditions.append(Event.level == level)
    if from_ts:
        conditions.append(Event.timestamp >= from_ts)
    if to_ts:
        conditions.append(Event.timestamp <= to_ts)
    if tags:
        conditions.append(Event.tags.contains(tags))

    where_clause = and_(*conditions) if conditions else None

    total_stmt = select(func.count()).select_from(Event)
    if where_clause is not None:
        total_stmt = total_stmt.where(where_clause)
    count = db.execute(total_stmt).scalar_one()

    stmt = select(Event).order_by(Event.timestamp.desc()).limit(limit).offset(offset)
    if where_clause is not None:
        stmt = stmt.where(where_clause)

    items = db.execute(stmt).scalars().all()
    return EventListOut(meta=PageMeta(limit=limit, offset=offset, count=count), items=items)


@router.get(
    "/v1/metrics/stats",
    response_model=MetricStatsOut,
    dependencies=[Depends(require_read_api_key)],
)
def metric_stats(
    db: Session = Depends(get_db),
    name: str = Query(..., min_length=1, max_length=200),
    service: str | None = Query(default=None),
    from_ts: datetime | None = Query(default=None),
    to_ts: datetime | None = Query(default=None),
    tag: list[str] | None = Query(default=None),
) -> MetricStatsOut:
    tags = parse_tags(tag)

    conditions = [Metric.name == name]
    if service:
        conditions.append(Metric.service == service)
    if from_ts:
        conditions.append(Metric.timestamp >= from_ts)
    if to_ts:
        conditions.append(Metric.timestamp <= to_ts)
    if tags:
        conditions.append(Metric.tags.contains(tags))

    stmt = (
        select(
            func.count(Metric.id),
            func.min(Metric.value),
            func.max(Metric.value),
            func.avg(Metric.value),
        )
        .where(and_(*conditions))
    )

    count, vmin, vmax, vavg = db.execute(stmt).one()

    return MetricStatsOut(
        service=service,
        name=name,
        from_ts=from_ts,
        to_ts=to_ts,
        count=int(count),
        min=float(vmin) if vmin is not None else None,
        max=float(vmax) if vmax is not None else None,
        avg=float(vavg) if vavg is not None else None,
    )
