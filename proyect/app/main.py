"""Application entrypoint for the Telemetry API."""
 
 from fastapi import FastAPI
 
 from app.api.routes import router
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)
 
 app = FastAPI(
     title="Telemetry API",
     version="0.1.0",
     description="Telemetry collector: metrics + events with tags, auth, stats, retention.",
 )
 
 app.include_router(router)

 
EOF
)
