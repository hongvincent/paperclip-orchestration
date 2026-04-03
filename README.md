# Paperclip Orchestration

FastAPI orchestration server that satisfies the `paperclip-dev-factory` client contract for:

- `POST /api/companies/{company_id}/approvals`
- `POST /api/companies/{company_id}/agent-hires`
- `GET /api/companies/{company_id}/dashboard`
## 역할

이 서버는 `paperclip-dev-factory`가 만든 청사진을 받아서 아래 상태를 관리합니다.

- approval 생성
- agent hire 요청 저장
- dashboard 집계 반환

클라이언트 계약은 고정이고, 이 저장소는 그 계약을 정확히 만족시키는 용도입니다.

## 다른 피시에서 함께 실행하기

### 1) 클론

```bash
git clone https://github.com/hongvincent/paperclip-orchestration.git
git clone https://github.com/hongvincent/paperclip-dev-factory.git
```

### 2) 서버 실행

터미널 A:
## Quick start

```bash
cd paperclip-orchestration
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
make run
```
이제 `http://localhost:3100/health` 와
`http://localhost:3100/health/ready` 를 확인할 수 있습니다.

### 3) Dev Factory와 연결

터미널 B에서 `paperclip-dev-factory`를 실행할 때 아래를 맞추면 됩니다.

```bash
PAPERCLIP_BASE_URL=http://localhost:3100
PAPERCLIP_COMPANY_ID=test-company-123
```

브라우저에서 Dev Factory에서 제출이 성공하면, 이 서버에는:

- approval 1건
- pending approval agent 3건

이 누적되고 `GET /api/companies/test-company-123/dashboard` 에 반영됩니다.

## 로컬 개발

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

## API 예시

### Approval 생성

```bash
curl -X POST http://localhost:3100/api/companies/test-company-123/approvals \
  -H 'Content-Type: application/json' \
  -d '{
    "details": {
      "title": "Build request: Ops Orbit",
      "description": "운영 요청을 자동 분류하는 서비스"
    }
  }'
```

### Agent hire 생성

```bash
curl -X POST http://localhost:3100/api/companies/test-company-123/agent-hires \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Blueprint Planner",
    "role": "planner",
    "capabilities": "청사진 설계와 승인 요청 생성",
    "desiredSkills": ["planning", "requirements"],
    "adapterType": "openai",
    "adapterConfig": {
      "cwd": "/tmp/project",
      "model": "gpt-5.4-mini",
      "promptTemplate": "You are the planner for Product. Your goal is: {goal}"
    }
  }'
```

### Dashboard 조회

```bash
curl http://localhost:3100/api/companies/test-company-123/dashboard
```

예상 응답 형태:

```json
{
  "taskCounts": {
    "todo": 1,
    "in_progress": 0,
    "completed": 0
  },
  "agentCounts": {
    "idle": 0,
    "working": 0,
    "pending_approval": 3
  }
}
```

## Verification
## Verification

```bash
make lint
make coverage
```
