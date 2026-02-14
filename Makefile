PY=python

.PHONY: backend-install backend-dev backend-test frontend-install frontend-dev dev docker-up

backend-install:
	cd backend && $(PY) -m pip install -e .[dev]

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-test:
	cd backend && pytest -q

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

dev:
	@echo "Run backend and frontend in separate terminals:"
	@echo "make backend-dev"
	@echo "make frontend-dev"

docker-up:
	cd infra && docker compose up --build

