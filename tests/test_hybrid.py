from uuid import uuid4

from app.retrieval import SearchHit, rrf_fuse
from app.schemas.documents import DocumentChunk, Modality


def test_rrf_deduplicates_and_rewards_cross_retriever_hits() -> None:
    def hit(text: str, score: float) -> SearchHit:
        return SearchHit(
            DocumentChunk(document_id=uuid4(), text=text, source="x", modality=Modality.TEXT, ordinal=0),
            score,
        )

    shared = hit("shared", 0.1)
    semantic = hit("semantic", 0.99)
    keyword = hit("keyword", 100.0)
    fused = rrf_fuse([[shared, semantic], [keyword, shared]], limit=3)
    assert [item.chunk.text for item in fused][0] == "shared"
    assert len({item.chunk.chunk_id for item in fused}) == 3
    assert all(item.score <= 2 / 61 for item in fused)


def test_rrf_validates_parameters() -> None:
    try:
        rrf_fuse([], k=0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid k was accepted")
