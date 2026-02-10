diff --git a/proyect/app/api/routes.py b/proyect/app/api/routes.py
index f397d90eddb4169bf80b2611cc6d4e5ffe814486..75ab15ba3dc85f2c94c3410da0e7da10b22de651 100644
--- a/proyect/app/api/routes.py
+++ b/proyect/app/api/routes.py
@@ -1,30 +1,28 @@
 from __future__ import annotations
 
 from datetime import datetime, timezone
-from typing import Annotated
-
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

