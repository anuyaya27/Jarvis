#!/usr/bin/env bash
set -euo pipefail

echo "Start backend:"
echo "  cd backend && uvicorn app.main:app --reload --port 8000"
echo "Start frontend:"
echo "  cd frontend && npm run dev"

