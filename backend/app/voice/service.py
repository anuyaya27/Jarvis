from app.providers.interfaces import SpeechProvider


class VoiceService:
    def __init__(self, speech_provider: SpeechProvider):
        self._speech_provider = speech_provider

    def create_session(self) -> str:
        return self._speech_provider.create_session()

    def process_chunk(self, session_id: str, audio_bytes: bytes) -> dict:
        return self._speech_provider.process_audio_chunk(session_id, audio_bytes)

