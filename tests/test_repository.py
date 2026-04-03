import sqlite3
from contextlib import closing
from pathlib import Path

from app.models import Agent, Approval
from app.repository import OrchestrationRepository


def test_repository_enables_wal_mode(tmp_path):
    db_path = Path(tmp_path / "test.db")
    OrchestrationRepository(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        mode = connection.execute("PRAGMA journal_mode").fetchone()[0]

    assert mode == "wal"


def test_dashboard_defaults_to_zero_counts_for_new_company(tmp_path):
    db_path = Path(tmp_path / "test.db")
    repository = OrchestrationRepository(db_path)

    dashboard = repository.get_dashboard("fresh-company")

    assert dashboard.taskCounts.todo == 0
    assert dashboard.agentCounts.pending_approval == 0


def test_repository_persists_approval_and_agent(tmp_path):
    db_path = Path(tmp_path / "test.db")
    repository = OrchestrationRepository(db_path)

    repository.create_approval(
        "company-123",
        Approval(title="Build request: Ops Orbit", description="desc"),
    )
    repository.create_agent(
        "company-123",
        Agent(name="Blueprint Planner", role="planner", capabilities="planning"),
        request_payload={
            "desiredSkills": ["planning"],
            "adapterType": "openai",
            "adapterConfig": {"cwd": "/tmp", "model": "gpt-5.4-mini", "promptTemplate": "plan"},
        },
    )

    dashboard = repository.get_dashboard("company-123")

    assert dashboard.taskCounts.todo == 1
    assert dashboard.agentCounts.pending_approval == 1
