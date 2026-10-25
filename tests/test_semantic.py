from qdrant_client import QdrantClient

from app.embeddings import HashEmbeddingProvider
from app.retrieval import QdrantIndex
from app.schemas.documents import Document, DocumentChunk, Modality


def test_qdrant_index_upsert_and_search() -> None:
    document = Document(source="guide.txt", modality=Modality.TEXT, checksum="abc")
    chunk = DocumentChunk(
        document_id=document.document_id, text="hybrid search combines signals",
        source=document.source, modality=document.modality, ordinal=0,
    )
    index = QdrantIndex(QdrantClient(":memory:"), HashEmbeddingProvider(dimension=8))
    assert index.upsert(document, [chunk]) == 1
    assert index.upsert(document, [chunk]) == 1
    assert index.client.count(index.collection).count == 1
    hits = index.search(chunk.text)
    assert hits[0].chunk.text == chunk.text
    assert hits[0].chunk.source == "guide.txt"
    assert hits[0].score > 0.99


def test_qdrant_rejects_dimension_mismatch() -> None:
    client = QdrantClient(":memory:")
    QdrantIndex(client, HashEmbeddingProvider(dimension=8)).ensure_collection()
    try:
        QdrantIndex(client, HashEmbeddingProvider(dimension=16)).ensure_collection()
    except ValueError as exc:
        assert "dimension" in str(exc)
    else:
        raise AssertionError("dimension mismatch was accepted")
