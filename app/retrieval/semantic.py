from __future__ import annotations

import hashlib
from dataclasses import dataclass
from uuid import NAMESPACE_URL, uuid5

from app.embeddings import EmbeddingProvider
from app.schemas.documents import Document, DocumentChunk


@dataclass(frozen=True)
class SearchHit:
    chunk: DocumentChunk
    score: float


class QdrantIndex:
    """Index and search text chunks in one dimension-checked Qdrant collection."""

    def __init__(self, client: object, embeddings: EmbeddingProvider, collection: str = "documents") -> None:
        self.client = client
        self.embeddings = embeddings
        self.collection = collection

    def ensure_collection(self) -> None:
        from qdrant_client import models

        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(
                    size=self.embeddings.dimension, distance=models.Distance.COSINE
                ),
            )
        config = self.client.get_collection(self.collection).config.params.vectors
        if config.size != self.embeddings.dimension:
            raise ValueError("Qdrant collection dimension does not match embedding provider")

    def upsert(self, document: Document, chunks: list[DocumentChunk]) -> int:
        from qdrant_client import models

        if any(chunk.document_id != document.document_id for chunk in chunks):
            raise ValueError("chunk document_id does not match document")
        self.ensure_collection()
        if not chunks:
            return 0
        vectors = self.embeddings.embed_documents([chunk.text for chunk in chunks])
        if len(vectors) != len(chunks) or any(len(v) != self.embeddings.dimension for v in vectors):
            raise RuntimeError("embedding provider returned invalid vectors")
        checksum = document.checksum or hashlib.sha256(
            "\n".join(chunk.text for chunk in chunks).encode()
        ).hexdigest()
        points = [
            models.PointStruct(
                id=str(uuid5(NAMESPACE_URL, f"{document.source}:{checksum}:{chunk.ordinal}")),
                vector=vector,
                payload={"chunk": chunk.model_dump(mode="json"), "checksum": checksum},
            )
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        self.client.upsert(collection_name=self.collection, points=points, wait=True)
        return len(points)

    def search(self, query: str, limit: int = 5) -> list[SearchHit]:
        if not query.strip() or limit < 1:
            raise ValueError("query must be non-empty and limit must be positive")
        self.ensure_collection()
        vector = self.embeddings.embed_query(query)
        if len(vector) != self.embeddings.dimension:
            raise RuntimeError("embedding provider returned invalid query dimension")
        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        return [
            SearchHit(chunk=DocumentChunk.model_validate(point.payload["chunk"]), score=point.score)
            for point in response.points
        ]
