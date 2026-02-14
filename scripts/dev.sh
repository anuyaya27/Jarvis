#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  python -m venv .venv
fi

source .venv/bin/activate
python -m pip install -e "backend[dev]"

echo "Frontend command:"
echo "  cd frontend && npm install && npm run dev"
echo
echo "Starting backend on http://localhost:8000 ..."
exec uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
