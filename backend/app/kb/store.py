import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

import faiss
import numpy as np


class KBStore:
    def __init__(self, db_path: str, index_path: str):
        self._db_path = db_path
        self._index_path = index_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._index, self._id_map = self._load_or_create_index()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL,
                source TEXT NOT NULL,
                text TEXT NOT NULL,
                metadata TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def _load_or_create_index(self) -> tuple[faiss.IndexFlatIP | None, list[str]]:
        if Path(self._index_path).exists() and Path(f"{self._index_path}.ids").exists():
            index = faiss.read_index(self._index_path)
            ids = json.loads(Path(f"{self._index_path}.ids").read_text(encoding="utf-8"))
            return index, ids
        return None, []

    def add_chunks(self, source: str, chunks: list[str], embeddings: list[list[float]]) -> tuple[str, int]:
        doc_id = str(uuid.uuid4())
        conn = sqlite3.connect(self._db_path)
        for text, emb in zip(chunks, embeddings):
            chunk_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO chunks (chunk_id, doc_id, source, text, metadata) VALUES (?, ?, ?, ?, ?)",
                (chunk_id, doc_id, source, text, json.dumps({"dim": len(emb)})),
            )
            self._id_map.append(chunk_id)
            vec = np.array([emb], dtype=np.float32)
            if self._index is None:
                self._index = faiss.IndexFlatIP(vec.shape[1])
            faiss.normalize_L2(vec)
            self._index.add(vec)
        conn.commit()
        conn.close()
        self._persist_index()
        return doc_id, len(chunks)

    def search(self, query_vec: list[float], top_k: int) -> list[dict[str, Any]]:
        if self._index is None or self._index.ntotal == 0:
            return []
        q = np.array([query_vec], dtype=np.float32)
        faiss.normalize_L2(q)
        scores, idxs = self._index.search(q, top_k)
        conn = sqlite3.connect(self._db_path)
        matches: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0 or idx >= len(self._id_map):
                continue
            chunk_id = self._id_map[idx]
            row = conn.execute("SELECT source, text FROM chunks WHERE chunk_id = ?", (chunk_id,)).fetchone()
            if not row:
                continue
            matches.append({"source": row[0], "text": row[1], "score": float(score)})
        conn.close()
        return matches

    def fetch_context_by_doc_ids(self, doc_ids: list[str], limit: int = 8) -> list[str]:
        if not doc_ids:
            return []
        conn = sqlite3.connect(self._db_path)
        placeholders = ",".join("?" for _ in doc_ids)
        rows = conn.execute(
            f"SELECT text FROM chunks WHERE doc_id IN ({placeholders}) LIMIT ?",
            (*doc_ids, limit),
        ).fetchall()
        conn.close()
        return [r[0] for r in rows]

    def _persist_index(self) -> None:
        if self._index is None:
            return
        faiss.write_index(self._index, self._index_path)
        Path(f"{self._index_path}.ids").write_text(json.dumps(self._id_map), encoding="utf-8")

