from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from app.core.config import get_settings
from app.kb.chunker import chunk_text
from app.kb.store import KBStore
from app.providers.interfaces import EmbeddingProvider


class KBService:
    def __init__(self, embedding_provider: EmbeddingProvider):
        settings = get_settings()
        self._store = KBStore(settings.kb_db_path, settings.kb_index_path)
        self._embedder = embedding_provider
        self._chunk_size = settings.kb_chunk_size
        self._chunk_overlap = settings.kb_chunk_overlap

    def upload_document(self, filename: str, data: bytes) -> tuple[str, int]:
        text = self._extract_text(filename, data)
        chunks = chunk_text(text, chunk_size=self._chunk_size, overlap=self._chunk_overlap)
        embeddings = self._embedder.embed_texts(chunks) if chunks else []
        return self._store.add_chunks(source=filename, chunks=chunks, embeddings=embeddings)

    def query(self, query: str, top_k: int) -> list[dict]:
        q = self._embedder.embed_query(query)
        return self._store.search(q, top_k)

    def context_for_docs(self, doc_ids: list[str]) -> list[str]:
        return self._store.fetch_context_by_doc_ids(doc_ids)

    @staticmethod
    def _extract_text(filename: str, data: bytes) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix == ".pdf":
            reader = PdfReader(BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        return data.decode("utf-8", errors="ignore")
