import pytest

from app.ingestion.chunking import chunk_text


def test_chunking_prefers_sentence_boundaries() -> None:
    chunks = chunk_text("First sentence. Second sentence. Third sentence.", max_chars=32, overlap=0)
    assert chunks == ["First sentence. Second sentence.", "Third sentence."]


def test_chunking_adds_overlap() -> None:
    chunks = chunk_text("One. Two. Three. Four.", max_chars=12, overlap=4)
    assert len(chunks) > 1
    assert any(set(left.split()) & set(right.split()) for left, right in zip(chunks, chunks[1:]))


def test_chunking_validates_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("text", max_chars=10, overlap=10)

