from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.health import router


def _make_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_health_endpoint_returns_ok():
    client = TestClient(_make_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}


def test_readiness_checks_database():
    client = TestClient(_make_app())

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] in ("ready", "degraded")
    assert "database" in response.json()["checks"]
