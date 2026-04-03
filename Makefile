PYTHON ?= python3

.PHONY: install lint test coverage run docker-build docker-run

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/ -v --tb=short

coverage:
	PYTHONPATH=. $(PYTHON) -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=95

run:
	PYTHONPATH=. $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 3100

docker-build:
	docker build -t paperclip-orchestration .

docker-run:
	docker compose up --build
