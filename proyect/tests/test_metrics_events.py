from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


def test_create_and_list_metric():
    client = TestClient(app)

    payload = {
        "service": "api-gateway",
        "name": "http_latency_ms",
        "value": 123.4,
        "unit": "ms",
        "tags": {"env": "dev", "region": "eu"},
    }

    r = client.post("/v1/metrics", json=payload, headers={"X-API-Key": settings.write_api_key})
    assert r.status_code == 201
    """Codigo exitoso creado"""
    created = r.json()
    assert created["service"] == payload["service"]
    assert created["name"] == payload["name"]
    assert created["unit"] == "ms"
    assert created["tags"]["env"] == "dev"

    r2 = client.get(
        "/v1/metrics?service=api-gateway&name=http_latency_ms",
        headers={"X-API-Key": settings.read_api_key},
    )
    assert r2.status_code == 200
    data = r2.json()
    assert data["meta"]["count"] >= 1
    assert len(data["items"]) >= 1

#Crea lo mismo en caso error
def test_create_and_list_event_with_tag_filter():
    client = TestClient(app)

    payload = {
        "service": "auth-service",
        "level": "ERROR",
        "message": "database timeout",
        "tags": {"env": "dev", "region": "eu"},
    }

    r = client.post("/v1/events", json=payload, headers={"X-API-Key": settings.write_api_key})
    assert r.status_code == 201

    r2 = client.get(
        "/v1/events?service=auth-service&tag=env:dev&tag=region:eu",
        headers={"X-API-Key": settings.read_api_key},
    )
    assert r2.status_code == 200
    data = r2.json()
    assert data["meta"]["count"] >= 1
    assert any(item["service"] == "auth-service" for item in data["items"])


def test_metric_stats():
    client = TestClient(app)

    # Ensure at least one metric exists
    client.post(
        "/v1/metrics",
        json={"service": "s-stats", "name": "cpu", "value": 0.5, "unit": "%"},
        headers={"X-API-Key": settings.write_api_key},
    )

    r = client.get(
        "/v1/metrics/stats?service=s-stats&name=cpu",
        headers={"X-API-Key": settings.read_api_key},
    )
    assert r.status_code == 200
    stats = r.json()
    assert stats["name"] == "cpu"
    assert stats["count"] >= 1
    assert stats["min"] is not None
    assert stats["max"] is not None
    assert stats["avg"] is not None
