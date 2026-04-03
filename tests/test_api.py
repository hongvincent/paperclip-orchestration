from fastapi.testclient import TestClient


def test_create_approval_returns_expected_contract(client: TestClient):
    response = client.post(
        "/api/companies/test-company-123/approvals",
        json={
            "details": {
                "title": "Build request: Ops Orbit",
                "description": "운영 요청을 자동 분류하는 서비스",
            }
        },
    )

    assert response.status_code == 201
    body = response.json()

    assert body["approval"]["id"].startswith("approval-")
    assert body["approval"]["status"] == "pending"
    assert body["approval"]["title"] == "Build request: Ops Orbit"
    assert body["approval"]["description"] == "운영 요청을 자동 분류하는 서비스"
    assert body["approval"]["created_at"].endswith("Z")


def test_hire_agent_returns_expected_contract(client: TestClient):
    response = client.post(
        "/api/companies/test-company-123/agent-hires",
        json={
            "name": "Blueprint Planner",
            "role": "planner",
            "capabilities": "청사진 설계와 승인 요청 생성",
            "desiredSkills": ["planning", "requirements"],
            "adapterType": "openai",
            "adapterConfig": {
                "cwd": "/tmp/project",
                "model": "gpt-5.4-mini",
                "promptTemplate": "You are the planner for Product. Your goal is: {goal}",
            },
        },
    )

    assert response.status_code == 201
    body = response.json()

    assert body["agent"]["id"].startswith("agent-")
    assert body["agent"]["name"] == "Blueprint Planner"
    assert body["agent"]["role"] == "planner"
    assert body["agent"]["status"] == "pending_approval"
    assert body["agent"]["capabilities"] == "청사진 설계와 승인 요청 생성"
    assert body["agent"]["created_at"].endswith("Z")


def test_dashboard_reflects_created_approvals_and_pending_agents(client: TestClient):
    client.post(
        "/api/companies/test-company-123/approvals",
        json={
            "details": {
                "title": "Build request: Ops Orbit",
                "description": "운영 요청을 자동 분류하는 서비스",
            }
        },
    )
    for role in ("planner", "builder", "qa"):
        client.post(
            "/api/companies/test-company-123/agent-hires",
            json={
                "name": role,
                "role": role,
                "capabilities": f"{role} capabilities",
                "desiredSkills": [role],
                "adapterType": "openai",
                "adapterConfig": {
                    "cwd": "/tmp/project",
                    "model": "gpt-5.4-mini",
                    "promptTemplate": f"{role} prompt",
                },
            },
        )

    response = client.get("/api/companies/test-company-123/dashboard")

    assert response.status_code == 200
    assert response.json() == {
        "taskCounts": {
            "todo": 1,
            "in_progress": 0,
            "completed": 0,
        },
        "agentCounts": {
            "idle": 0,
            "working": 0,
            "pending_approval": 3,
        },
    }


def test_dashboard_is_isolated_by_company(client: TestClient):
    client.post(
        "/api/companies/company-a/approvals",
        json={
            "details": {
                "title": "Build request: A",
                "description": "A desc",
            }
        },
    )

    response = client.get("/api/companies/company-b/dashboard")

    assert response.status_code == 200
    assert response.json()["taskCounts"]["todo"] == 0
    assert response.json()["agentCounts"]["pending_approval"] == 0
