from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.kb import router as kb_router
from app.api.routes.playbook import router as playbook_router
from app.api.routes.simulate import router as simulate_router
from app.api.routes.voice import router as voice_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import RequestIdMiddleware, configure_logging

configure_logging()
settings = get_settings()
app = FastAPI(title="Multiverse Copilot API", version="0.1.0")

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
app.include_router(health_router)
app.include_router(kb_router)
app.include_router(playbook_router)
app.include_router(simulate_router)
app.include_router(voice_router)
