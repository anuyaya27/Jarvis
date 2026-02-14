from functools import lru_cache

from app.core.config import get_settings
from app.kb.service import KBService
from app.providers.bedrock_nova_lite import NovaLiteClient
from app.providers.interfaces import AgentAutomationProvider, EmbeddingProvider, LLMProvider, SpeechProvider
from app.providers.mock_providers import MockEmbeddingProvider, MockLLMProvider, MockNovaActProvider, MockSpeechProvider
from app.providers.nova_act import NovaActClient
from app.providers.nova_embeddings import NovaEmbeddingsClient
from app.providers.nova_sonic import NovaSonicSpeechClient
from app.sim.service import SimulationService
from app.voice.service import VoiceService


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    return MockEmbeddingProvider() if settings.use_mock_providers else NovaEmbeddingsClient()


@lru_cache
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    return MockLLMProvider() if settings.use_mock_providers else NovaLiteClient()


@lru_cache
def get_speech_provider() -> SpeechProvider:
    settings = get_settings()
    return MockSpeechProvider() if settings.use_mock_providers else NovaSonicSpeechClient()


@lru_cache
def get_agent_provider() -> AgentAutomationProvider:
    settings = get_settings()
    return MockNovaActProvider() if settings.use_mock_providers else NovaActClient()


@lru_cache
def get_kb_service() -> KBService:
    return KBService(get_embedding_provider())


@lru_cache
def get_sim_service() -> SimulationService:
    return SimulationService(get_llm_provider(), get_kb_service())


@lru_cache
def get_voice_service() -> VoiceService:
    return VoiceService(get_speech_provider())

