
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from app.core.config import settings

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class MetricIn(BaseModel):
    service: str = Field(..., min_length=1, max_length=120)
    name: str = Field(..., min_length=1, max_length=200)
    value: float
    unit: str | None = Field(default=None, max_length=40)
    timestamp: datetime | None = None
    tags: dict[str, str] = Field(default_factory=dict)

    @field_validator("timestamp", mode="before")
    @classmethod
    #Acepta ISO strings o datetimes, si faltan se ponen posteriormente en route
    def normalize_timestamp(cls, v):
        return v
    #cls: la clase del modelo
    #v: el valor que llega para ese campo
    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: dict[str, str]) -> dict[str, str]:
        if tags is None:
            return {}
        if len(tags) > settings.max_tags:
            raise ValueError(f"Too many tags (max {settings.max_tags})")
        for k, val in tags.items():
            if not isinstance(k, str) or not isinstance(val, str):
                raise ValueError("Tags must be string:string")
            if len(k) == 0 or len(k) > settings.max_tag_key_len:
                raise ValueError(f"Tag key length must be 1..{settings.max_tag_key_len}")
            if len(val) > settings.max_tag_value_len:
                raise ValueError(f"Tag value length must be <= {settings.max_tag_value_len}")
        return tags


    id: int
    service: str
    name: str
    value: float
    unit: str | None
    timestamp: datetime
    tags: dict[str, str]

    model_config = {"from_attributes": True}


class EventLevel(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class EventIn(BaseModel):
    service: str = Field(..., min_length=1, max_length=120)
    level: EventLevel
    message: str = Field(..., min_length=1, max_length=10_000)
    timestamp: datetime | None = None
    tags: dict[str, str] = Field(default_factory=dict)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: dict[str, str]) -> dict[str, str]:
        if tags is None:
            return {}
        if len(tags) > settings.max_tags:
            raise ValueError(f"Too many tags (max {settings.max_tags})")
        for k, val in tags.items():
            if not isinstance(k, str) or not isinstance(val, str):
                raise ValueError("Tags must be string:string")
            if len(k) == 0 or len(k) > settings.max_tag_key_len:
                raise ValueError(f"Tag key length must be 1..{settings.max_tag_key_len}")
            if len(val) > settings.max_tag_value_len:
                raise ValueError(f"Tag value length must be <= {settings.max_tag_value_len}")
        return tags


class EventOut(BaseModel):
    id: int
    service: str
    level: str
    message: str
    timestamp: datetime
    tags: dict[str, str]

    model_config = {"from_attributes": True}


class PageMeta(BaseModel):
    limit: int
    offset: int
    count: int


class MetricListOut(BaseModel):
    meta: PageMeta
    items: list[MetricOut]


class EventListOut(BaseModel):
    meta: PageMeta
    items: list[EventOut]


class MetricStatsOut(BaseModel):
    service: str | None
    name: str
    from_ts: datetime | None
    to_ts: datetime | None
    count: int
    min: float | None
    max: float | None
    avg: float | None
