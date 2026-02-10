
 from __future__ import annotations
 
 from datetime import datetime, timezone

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

