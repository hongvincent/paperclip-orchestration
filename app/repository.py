import json
import sqlite3
from contextlib import closing
from pathlib import Path

from app.models import Agent, AgentCounts, Approval, DashboardResponse, TaskCounts


class OrchestrationRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def create_approval(self, company_id: str, approval: Approval) -> Approval:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute(
                """
                INSERT INTO approvals (id, company_id, status, title, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    approval.id,
                    company_id,
                    approval.status,
                    approval.title,
                    approval.description,
                    approval.created_at.isoformat(),
                ),
            )
            connection.commit()
        return approval

    def create_agent(self, company_id: str, agent: Agent, request_payload: dict) -> Agent:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute(
                """
                INSERT INTO agent_hires (
                    id,
                    company_id,
                    name,
                    role,
                    status,
                    capabilities,
                    desired_skills_json,
                    adapter_type,
                    adapter_config_json,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    agent.id,
                    company_id,
                    agent.name,
                    agent.role,
                    agent.status,
                    agent.capabilities,
                    json.dumps(request_payload["desiredSkills"], ensure_ascii=False),
                    request_payload["adapterType"],
                    json.dumps(request_payload["adapterConfig"], ensure_ascii=False),
                    agent.created_at.isoformat(),
                ),
            )
            connection.commit()
        return agent

    def get_dashboard(self, company_id: str) -> DashboardResponse:
        with closing(sqlite3.connect(self.database_path)) as connection:
            todo = self._count(
                connection,
                "SELECT COUNT(*) FROM approvals WHERE company_id = ?",
                (company_id,),
            )
            idle = self._count(
                connection,
                "SELECT COUNT(*) FROM agent_hires WHERE company_id = ? AND status = 'idle'",
                (company_id,),
            )
            working = self._count(
                connection,
                "SELECT COUNT(*) FROM agent_hires WHERE company_id = ? AND status = 'working'",
                (company_id,),
            )
            pending_approval = self._count(
                connection,
                """
                SELECT COUNT(*)
                FROM agent_hires
                WHERE company_id = ? AND status = 'pending_approval'
                """,
                (company_id,),
            )
        return DashboardResponse(
            taskCounts=TaskCounts(todo=todo, in_progress=working, completed=0),
            agentCounts=AgentCounts(
                idle=idle,
                working=working,
                pending_approval=pending_approval,
            ),
        )

    def _initialize(self) -> None:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS approvals (
                    id TEXT PRIMARY KEY,
                    company_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_hires (
                    id TEXT PRIMARY KEY,
                    company_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL,
                    capabilities TEXT NOT NULL,
                    desired_skills_json TEXT NOT NULL,
                    adapter_type TEXT NOT NULL,
                    adapter_config_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    @staticmethod
    def _count(connection: sqlite3.Connection, query: str, params: tuple[object, ...]) -> int:
        return int(connection.execute(query, params).fetchone()[0])
