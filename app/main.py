from fastapi import FastAPI, status

from app.config import get_settings
from app.health import router as health_router
from app.logging_config import configure_logging
from app.middleware import RequestIdMiddleware
from app.models import (
    AgentHireRequest,
    CreateAgentHireResponse,
    CreateApprovalRequest,
    CreateApprovalResponse,
    DashboardResponse,
)
from app.repository import OrchestrationRepository
from app.service import OrchestrationService


def create_app(service: OrchestrationService | None = None) -> FastAPI:
    settings = get_settings()
    configure_logging(log_level=settings.log_level)
    settings.log_startup_info()

    app = FastAPI(title=settings.app_name)
    app.add_middleware(RequestIdMiddleware)
    app.include_router(health_router)
    app.state.service = service or OrchestrationService(
        OrchestrationRepository(settings.database_path)
    )

    @app.post(
        "/api/companies/{company_id}/approvals",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateApprovalResponse,
    )
    def create_approval(
        company_id: str,
        request_body: CreateApprovalRequest,
    ) -> CreateApprovalResponse:
        return app.state.service.create_approval(company_id, request_body)

    @app.post(
        "/api/companies/{company_id}/agent-hires",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateAgentHireResponse,
    )
    def hire_agent(company_id: str, request_body: AgentHireRequest) -> CreateAgentHireResponse:
        return app.state.service.hire_agent(company_id, request_body)

    @app.get(
        "/api/companies/{company_id}/dashboard",
        response_model=DashboardResponse,
    )
    def dashboard(company_id: str) -> DashboardResponse:
        return app.state.service.get_dashboard(company_id)

    return app


app = create_app()
