import sqlite3
from contextlib import closing

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])

VERSION = "0.1.0"


@router.get("/health")
def health() -> dict:
    return {"status": "healthy", "version": VERSION}


@router.get("/health/ready")
def readiness() -> dict:
    checks = {"database": _check_database()}
    is_ready = all(check["ok"] for check in checks.values())
    return {
        "status": "ready" if is_ready else "degraded",
        "checks": checks,
    }


def _check_database() -> dict:
    settings = get_settings()
    try:
        with closing(sqlite3.connect(settings.database_path)) as connection:
            connection.execute("SELECT 1")
        return {"ok": True}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
