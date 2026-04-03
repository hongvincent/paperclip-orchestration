import structlog

from app.models import (
    Agent,
    AgentHireRequest,
    Approval,
    CreateAgentHireResponse,
    CreateApprovalRequest,
    CreateApprovalResponse,
    DashboardResponse,
)
from app.repository import OrchestrationRepository

logger = structlog.stdlib.get_logger("app.service")


class OrchestrationService:
    def __init__(self, repository: OrchestrationRepository) -> None:
        self.repository = repository

    def create_approval(
        self,
        company_id: str,
        request: CreateApprovalRequest,
    ) -> CreateApprovalResponse:
        approval = self.repository.create_approval(
            company_id,
            approval=Approval(
                title=request.details.title,
                description=request.details.description,
            ),
        )
        logger.info("approval_created", company_id=company_id, approval_id=approval.id)
        return CreateApprovalResponse(approval=approval)

    def hire_agent(
        self,
        company_id: str,
        request: AgentHireRequest,
    ) -> CreateAgentHireResponse:
        agent = Agent(
            name=request.name,
            role=request.role,
            capabilities=request.capabilities,
        )
        saved_agent = self.repository.create_agent(
            company_id,
            agent=agent,
            request_payload=request.model_dump(mode="json", by_alias=True),
        )
        logger.info(
            "agent_hired",
            company_id=company_id,
            agent_id=saved_agent.id,
            role=saved_agent.role,
        )
        return CreateAgentHireResponse(agent=saved_agent)

    def get_dashboard(self, company_id: str) -> DashboardResponse:
        dashboard = self.repository.get_dashboard(company_id)
        logger.info(
            "dashboard_requested",
            company_id=company_id,
            todo=dashboard.taskCounts.todo,
            pending_approval=dashboard.agentCounts.pending_approval,
        )
        return dashboard
