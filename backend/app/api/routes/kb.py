from fastapi import APIRouter, Depends, File, UploadFile

from app.deps import get_kb_service
from app.kb.service import KBService
from app.schemas import KBQueryRequest, KBQueryResponse, KBUploadResponse

router = APIRouter(prefix="/kb", tags=["knowledge-base"])


@router.post("/upload", response_model=KBUploadResponse)
async def upload_doc(file: UploadFile = File(...), kb_service: KBService = Depends(get_kb_service)) -> KBUploadResponse:
    data = await file.read()
    doc_id, chunks = kb_service.upload_document(file.filename, data)
    return KBUploadResponse(doc_id=doc_id, chunks=chunks)


@router.post("/query", response_model=KBQueryResponse)
async def query_kb(req: KBQueryRequest, kb_service: KBService = Depends(get_kb_service)) -> KBQueryResponse:
    matches = kb_service.query(req.query, req.top_k)
    return KBQueryResponse(matches=matches)

