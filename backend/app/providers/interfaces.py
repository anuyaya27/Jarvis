from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.schemas import SimulationResult


@dataclass
class LLMResponse:
    content: str
    model_id: str
    latency_ms: int
    tokens_input: int | None = None
    tokens_output: int | None = None
    retry_count: int = 0


class LLMProvider(ABC):
    @abstractmethod
    def simulate_decision(self, prompt: str, context: list[str], constraints: dict[str, Any]) -> SimulationResult:
        raise NotImplementedError

    @abstractmethod
    def generate_json(self, prompt: str) -> LLMResponse:
        raise NotImplementedError


class SpeechProvider(ABC):
    @abstractmethod
    def create_session(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def process_audio_chunk(self, session_id: str, audio_chunk: bytes) -> dict[str, Any]:
        raise NotImplementedError


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError


class AgentAutomationProvider(ABC):
    @abstractmethod
    def run_playbook(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
