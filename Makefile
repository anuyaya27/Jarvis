PY=python

.PHONY: setup backend-install backend-dev backend-test frontend-install frontend-dev dev

setup:
	$(PY) -m venv .venv
	. .venv/bin/activate && pip install -e backend[dev]
	cd frontend && npm install

backend-install:
	$(PY) -m pip install -e backend[dev]

backend-dev:
	uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000

backend-test:
	cd backend && pytest -q

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

dev:
	@echo "Run backend:"
	@echo ". .venv/bin/activate && uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000"
	@echo "Run frontend in another terminal:"
	@echo "cd frontend && npm run dev"
