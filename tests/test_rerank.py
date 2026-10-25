from uuid import uuid4

from app.retrieval import CrossEncoderReranker, SearchHit
from app.schemas.documents import DocumentChunk, Modality


def test_reranker_rescores_bounded_candidates() -> None:
    class FakeScorer:
        def predict(self, pairs):
            assert len(pairs) == 2
            return [0.1, 0.9]

    hits = [
        SearchHit(
            DocumentChunk(document_id=uuid4(), text=text, source="x", modality=Modality.TEXT, ordinal=i),
            score=1 / (i + 1),
        )
        for i, text in enumerate(["first", "second", "third"])
    ]
    result = CrossEncoderReranker(max_candidates=2, scorer=FakeScorer()).rerank("query", hits)
    assert [hit.chunk.text for hit in result] == ["second", "first"]
    assert result[0].score == 0.9
