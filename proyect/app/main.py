"""Application entrypoint for the Telemetry API."""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Telemetry API",
    version="0.1.0",
    description="Telemetry collector: metrics + events with tags, auth, stats, retention.",
)

app.include_router(router)
