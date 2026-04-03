from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware import RequestIdMiddleware


def _make_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(RequestIdMiddleware)

    @app.get("/ping")
    def ping():
        return {"ok": True}

    return app


def test_response_includes_request_id_header():
    client = TestClient(_make_app())

    response = client.get("/ping")

    assert response.status_code == 200
    request_id = response.headers.get("X-Request-ID")
    assert request_id is not None
    assert len(request_id) == 36


def test_client_provided_request_id_is_preserved():
    client = TestClient(_make_app())

    response = client.get("/ping", headers={"X-Request-ID": "custom-id-123"})

    assert response.headers["X-Request-ID"] == "custom-id-123"
