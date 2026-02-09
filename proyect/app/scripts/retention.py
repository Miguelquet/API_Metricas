from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Event, Metric
from app.db.session import SessionLocal


def utc_now():
    return datetime.now(timezone.utc)


def run_retention(db: Session) -> dict:

    cutoff = utc_now() - timedelta(days=settings.retention_days)

    m_del = delete(Metric).where(Metric.timestamp < cutoff)
    e_del = delete(Event).where(Event.timestamp < cutoff)

    m_res = db.execute(m_del)
    e_res = db.execute(e_del)

    db.commit()

    return {
        "cutoff": cutoff.isoformat(),
        "metrics_deleted": m_res.rowcount or 0,
        "events_deleted": e_res.rowcount or 0,
    }


def main():
    db = SessionLocal()
    try:
        result = run_retention(db)
        print(result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
