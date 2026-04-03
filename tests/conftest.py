import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "orchestration.db"))
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    return TestClient(create_app())


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    yield
    os.environ.pop("DATABASE_PATH", None)
    os.environ.pop("LOG_LEVEL", None)
