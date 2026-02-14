if (-not (Test-Path .venv)) {
  py -3 -m venv .venv
}

$python = Join-Path ".venv" "Scripts\\python.exe"
& $python -m pip install -e "backend[dev]"

Write-Host "Frontend command:"
Write-Host "  cd frontend; npm install; npm run dev"
Write-Host ""
Write-Host "Starting backend on http://localhost:8000 ..."
& ".venv\\Scripts\\uvicorn.exe" app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
