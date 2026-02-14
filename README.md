# Multiverse Copilot

Voice-driven parallel-reality decision engine for high-stakes business strategy using Amazon Nova (Nova 2 Sonic + Nova 2 Lite + Nova Multimodal Embeddings + optional Nova Act).

## Monorepo layout

```text
.
├── .env.example
├── .gitignore
├── Makefile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── app
│   │   ├── main.py
│   │   ├── deps.py
│   │   ├── schemas.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── errors.py
│   │   │   └── logging.py
│   │   ├── api/routes
│   │   │   ├── health.py
│   │   │   ├── kb.py
│   │   │   ├── playbook.py
│   │   │   ├── simulate.py
│   │   │   └── voice.py
│   │   ├── kb
│   │   │   ├── chunker.py
│   │   │   ├── service.py
│   │   │   └── store.py
│   │   ├── sim
│   │   │   ├── prompt_builder.py
│   │   │   └── service.py
│   │   ├── voice/service.py
│   │   └── providers
│   │       ├── interfaces.py
│   │       ├── mock_providers.py
│   │       ├── bedrock_nova_lite.py
│   │       ├── nova_sonic.py
│   │       ├── nova_embeddings.py
│   │       └── nova_act.py
│   └── tests
│       ├── test_schema_validation.py
│       ├── test_branch_limiter.py
│       ├── test_kb_chunking.py
│       └── test_prompt_builder.py
├── frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── next-env.d.ts
│   └── app
│       ├── globals.css
│       ├── layout.tsx
│       ├── page.tsx
│       ├── voice/page.tsx
│       └── kb/page.tsx
├── infra
│   └── docker-compose.yml
└── scripts
    ├── dev.sh
    └── dev.ps1
```

## Core behavior

- `Nova 2 Lite`: `NovaLiteClient` uses Bedrock Converse API with retry/backoff and usage/latency capture.
- `Nova 2 Sonic`: websocket bridge endpoint accepts base64 audio chunks and returns partial/final transcript + audio payload.
- `Nova Multimodal Embeddings`: embeddings provider + local SQLite + Faiss KB store for retrieval-augmented simulation context.
- `Nova Act`: `NovaActClient` stub interface plus runnable mock playbook.
- Strict simulation JSON schema with Pydantic v2 validation.
- Prompt strategy implemented in code (`app/sim/prompt_builder.py`) with JSON-only instructions, branch diversity, and repair prompt support.

## Prerequisites

- Python 3.11+
- Node.js 20+
- Optional Docker + Docker Compose
- AWS account with Bedrock access to:
  - Nova Lite model
  - Nova Multimodal Embeddings model
  - Nova Sonic model (if enabling real speech path)

## Setup

1. Copy env file.
   - `cp .env.example .env` (Linux/macOS)
   - `Copy-Item .env.example .env` (PowerShell)
2. Install backend deps.
   - `cd backend && python -m pip install -e .[dev]`
3. Install frontend deps.
   - `cd frontend && npm install`

## Run locally (mock providers, no AWS required)

1. Ensure `.env` contains `USE_MOCK_PROVIDERS=true`.
2. Terminal 1:
   - `cd backend`
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
3. Terminal 2:
   - `cd frontend`
   - `npm run dev`
4. Open `http://localhost:3000/voice` and `http://localhost:3000/kb`.

## Run locally with real Amazon Nova

1. Set `.env`:
   - `USE_MOCK_PROVIDERS=false`
   - `AWS_REGION=...`
   - `AWS_PROFILE=...` (optional)
   - `BEDROCK_MODEL_ID_NOVA_LITE=...`
   - `NOVA_EMBEDDINGS_MODEL_ID=...`
   - `NOVA_SONIC_MODEL_ID=...`
2. Configure AWS credentials (`aws configure` or profile-based auth).
3. Start backend/frontend as above.

## API endpoints

- `GET /health`
- `POST /kb/upload` (multipart file)
- `POST /kb/query`
- `POST /voice/session`
- `WS /voice/stream/{session_id}`
- `POST /simulate`
- `POST /playbook/run` (Nova Act demo stub)

## Sample curl

```bash
curl -s http://localhost:8000/health
```

```bash
curl -s -X POST http://localhost:8000/kb/upload \
  -F "file=@./sample.txt"
```

```bash
curl -s -X POST http://localhost:8000/kb/query \
  -H "Content-Type: application/json" \
  -d '{"query":"acquisition recession risk", "top_k":5}'
```

```bash
curl -s -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_text":"Simulate acquiring Competitor X under recession next quarter.",
    "constraints":{"timeframe":"next_quarter","max_branches":5}
  }'
```

```bash
curl -s -X POST http://localhost:8000/playbook/run \
  -H "Content-Type: application/json" \
  -d '{"name":"collect_competitor_pricing","payload":{"url":"https://example.com"}}'
```

## Docker

- `cd infra && docker compose up --build`
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

## Tests

- `cd backend && pytest -q`

## Deployment notes

- Backend deploy target: ECS/Fargate, EKS, or App Runner.
- Frontend deploy target: Vercel, Amplify Hosting, or container-based service.
- Set CORS allowlist in production.
- Route logs to CloudWatch/ELK and keep request IDs end-to-end.
- Switch mock providers off and validate model access per AWS account/region.
# Jarvis
