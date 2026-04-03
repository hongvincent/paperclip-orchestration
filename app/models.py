from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def approval_id() -> str:
    return f"approval-{uuid4()}"


def agent_id() -> str:
    return f"agent-{uuid4()}"


class ApprovalDetails(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=5000)


class CreateApprovalRequest(BaseModel):
    details: ApprovalDetails


class Approval(BaseModel):
    id: str = Field(default_factory=approval_id)
    status: Literal["pending"] = "pending"
    title: str
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CreateApprovalResponse(BaseModel):
    approval: Approval


class AdapterConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cwd: str = Field(min_length=1)
    model: str = Field(min_length=1)
    prompt_template: str = Field(alias="promptTemplate", min_length=1)


class AgentHireRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=100)
    capabilities: str = Field(min_length=1, max_length=5000)
    desired_skills: list[str] = Field(alias="desiredSkills", min_length=1, max_length=20)
    adapter_type: str = Field(alias="adapterType", min_length=1, max_length=100)
    adapter_config: AdapterConfig = Field(alias="adapterConfig")


class Agent(BaseModel):
    id: str = Field(default_factory=agent_id)
    name: str
    role: str
    status: Literal["pending_approval", "idle", "working"] = "pending_approval"
    capabilities: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CreateAgentHireResponse(BaseModel):
    agent: Agent


class TaskCounts(BaseModel):
    todo: int = 0
    in_progress: int = 0
    completed: int = 0


class AgentCounts(BaseModel):
    idle: int = 0
    working: int = 0
    pending_approval: int = 0


class DashboardResponse(BaseModel):
    taskCounts: TaskCounts
    agentCounts: AgentCounts
