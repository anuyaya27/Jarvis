from typing import Any
from uuid import uuid4

from app.providers.interfaces import SpeechProvider


class NovaSonicSpeechClient(SpeechProvider):
    """
    Placeholder adapter for Nova 2 Sonic bidirectional streaming.

    TODO:
    - Replace with AWS SDK event-stream/WebSocket client once the runtime endpoint
      configuration is finalized for your account setup.
    - Map browser PCM/audio chunks to Nova Sonic input stream frames.
    - Forward Nova Sonic audio + partial/final transcript frames back to the client.
    """

    def create_session(self) -> str:
        return str(uuid4())

    def process_audio_chunk(self, session_id: str, audio_chunk: bytes) -> dict[str, Any]:
        _ = session_id, audio_chunk
        return {
            "partial_transcript": "",
            "final_transcript": "",
            "audio_base64": "",
            "note": "Nova Sonic real-time bridge TODO",
        }

