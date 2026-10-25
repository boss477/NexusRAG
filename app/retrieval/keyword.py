from __future__ import annotations

import json
import re
import sqlite3

from app.retrieval.semantic import SearchHit
from app.schemas.documents import DocumentChunk


class KeywordIndex:
    """Incremental, persistent SQLite FTS5 keyword index."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5("
            "chunk_id UNINDEXED, payload UNINDEXED, text)"
        )

    def upsert(self, chunks: list[DocumentChunk]) -> int:
        with self.connection:
            for chunk in chunks:
                chunk_id = str(chunk.chunk_id)
                self.connection.execute("DELETE FROM chunks_fts WHERE chunk_id = ?", (chunk_id,))
                self.connection.execute(
                    "INSERT INTO chunks_fts (chunk_id, payload, text) VALUES (?, ?, ?)",
                    (chunk_id, chunk.model_dump_json(), chunk.text),
                )
        return len(chunks)

    def search(self, query: str, limit: int = 5) -> list[SearchHit]:
        if limit < 1:
            raise ValueError("limit must be positive")
        terms = re.findall(r"\w+", query, flags=re.UNICODE)
        if not terms:
            return []
        expression = " OR ".join(f'"{term}"' for term in terms)
        rows = self.connection.execute(
            "SELECT payload, -bm25(chunks_fts) FROM chunks_fts "
            "WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT ?",
            (expression, limit),
        ).fetchall()
        return [
            SearchHit(chunk=DocumentChunk.model_validate(json.loads(payload)), score=score)
            for payload, score in rows
        ]
