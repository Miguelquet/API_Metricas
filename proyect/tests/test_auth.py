
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


def test_write_requires_key():
    client = TestClient(app)
    r = client.post("/v1/metrics", json={"service": "s1", "name": "m1", "value": 1.0})
    assert r.status_code == 401


def test_read_requires_key():
    client = TestClient(app)
    r = client.get("/v1/metrics")
    assert r.status_code == 401


def test_read_accepts_read_key():
    client = TestClient(app)
    r = client.get("/v1/metrics", headers={"X-API-Key": settings.read_api_key})
    assert r.status_code == 200


def test_read_accepts_write_key():
    client = TestClient(app)
    r = client.get("/v1/metrics", headers={"X-API-Key": settings.write_api_key})
    assert r.status_code == 200
