import base64
import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.deps import get_voice_service
from app.schemas import VoiceSessionResponse
from app.voice.service import VoiceService

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/session", response_model=VoiceSessionResponse)
async def create_voice_session(voice_service: VoiceService = Depends(get_voice_service)) -> VoiceSessionResponse:
    return VoiceSessionResponse(session_id=voice_service.create_session())


@router.websocket("/stream/{session_id}")
async def voice_stream(websocket: WebSocket, session_id: str, voice_service: VoiceService = Depends(get_voice_service)):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            payload = json.loads(msg)
            audio_b64 = payload.get("audio_base64", "")
            audio_bytes = base64.b64decode(audio_b64) if audio_b64 else b""
            out = voice_service.process_chunk(session_id, audio_bytes)
            await websocket.send_text(json.dumps(out))
    except WebSocketDisconnect:
        return

