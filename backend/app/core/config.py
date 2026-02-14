from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multiverse Copilot"
    environment: str = "dev"
    use_mock_providers: bool = True
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    aws_region: str = "us-east-1"
    aws_profile: str | None = None
    bedrock_model_id_nova_lite: str = "amazon.nova-lite-v1:0"
    nova_embeddings_model_id: str = "amazon.nova-multimodal-embeddings-v1:0"
    nova_sonic_model_id: str = "amazon.nova-2-sonic-v1:0"

    kb_db_path: str = "data/kb.sqlite3"
    kb_index_path: str = "data/kb.faiss"
    kb_chunk_size: int = 800
    kb_chunk_overlap: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def ensure_dirs(self) -> None:
        Path("data").mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
