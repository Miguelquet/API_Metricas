
from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_write_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    if not x_api_key or x_api_key != settings.write_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key") #401 UNAUTHORISED ERROR
    return x_api_key


def require_read_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    # Allow either the read key or the write key for read operations
    if not x_api_key or x_api_key not in {settings.read_api_key, settings.write_api_key}:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
    return x_api_key
