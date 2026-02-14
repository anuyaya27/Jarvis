# Multiverse Copilot

Voice-driven parallel-reality decision engine for high-stakes business strategy using Amazon Nova (Nova 2 Sonic + Nova 2 Lite + Nova Multimodal Embeddings + optional Nova Act).

## Quickstart (no Docker)

1. Create and activate venv, then install backend:
   - macOS/Linux:
     - `python -m venv .venv`
     - `source .venv/bin/activate`
     - `pip install -e backend[dev]`
   - PowerShell:
     - `py -3 -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
     - `pip install -e backend[dev]`
2. Copy env file:
   - `Copy-Item .env.example .env` (PowerShell)
3. Start backend:
   - `uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000`
4. Start frontend in another terminal:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
5. Open:
   - `http://localhost:3000/voice`
   - `http://localhost:3000/kb`

## One-command backend bootstrap

- PowerShell: `./scripts/dev.ps1`
- Bash: `./scripts/dev.sh`

Both scripts:
- create `.venv` if missing
- install `backend[dev]`
- start backend via `uvicorn`
- print exact frontend command

## Modes

### Mock mode (default)

Set in `.env`:
- `USE_MOCK_PROVIDERS=true`

This mode runs without AWS credentials.

### Real Nova mode

Set in `.env`:
- `USE_MOCK_PROVIDERS=false`
- `AWS_REGION=us-east-1` (or your region)
- `AWS_PROFILE=your-profile` (optional)
- `BEDROCK_MODEL_ID_NOVA_LITE=amazon.nova-lite-v1:0`
- `NOVA_EMBEDDINGS_MODEL_ID=amazon.nova-multimodal-embeddings-v1:0`
- `NOVA_SONIC_MODEL_ID=amazon.nova-2-sonic-v1:0`

Backend behavior in real mode:
- Nova Lite uses Bedrock `converse(...)` first.
- Falls back to `invoke_model(...)` if Converse is unavailable.
- Extracts first valid JSON object from model text.
- If schema validation fails, retries once with a repair prompt.

## API Endpoints

- `GET /health`
- `POST /kb/upload`
- `POST /kb/query`
- `POST /decision/spec`
- `POST /simulate`
- `POST /voice/session`
- `WS /voice/stream/{session_id}`
- `POST /playbook/run`

## Curl examples

1. Upload a doc:

```bash
curl -s -X POST http://localhost:8000/kb/upload \
  -F "file=@./sample.txt"
```

2. Query KB:

```bash
curl -s -X POST http://localhost:8000/kb/query \
  -H "Content-Type: application/json" \
  -d '{"query":"acquisition recession risk","top_k":5}'
```

3. Simulate decision from plain text:

```bash
curl -s -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_text":"Simulate acquiring Competitor X under recession next quarter.",
    "constraints":{"timeframe":"next_quarter","max_branches":5}
  }'
```

## Voice Console behavior

- `Use Browser Mic (Web Speech)` is ON by default for demo reliability.
- If OFF, Sonic UI is intentionally disabled with a status message.
- Backend Sonic websocket endpoints are still present for future integration.

## Demo Script (90 seconds)

1. Open `http://localhost:3000/voice` and keep `Use Browser Mic (Web Speech)` ON.
2. Say this exact prompt:
   - `Simulate acquiring Competitor X under recession next quarter.`
3. Click `Run Simulation`.
4. Point out on screen:
   - `Executive Summary` card (concise board-ready narrative).
   - Branch grid showing `Final Stability` progress bars.
   - Risk chips normalized to consistent severities (`low/medium/high/critical`).
   - `Recommended Path` reasoning for the top branch.
5. Toggle `Show JSON` and highlight audit transparency fields:
   - `retry_count`
   - `used_repair_pass`
   - `used_mock`
   - `embedding_docs_used`
6. Optionally open `http://localhost:3000/kb`, upload one text/PDF file, rerun simulation, and show `embedding_docs_used` increases.

## Testing

- `cd backend && pytest -q`
