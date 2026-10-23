import pytest

from app.embeddings import HashEmbeddingProvider


def test_embedding_provider_returns_normalized_vectors() -> None:
    provider = HashEmbeddingProvider(dimension=8)
    vectors = provider.embed_documents(["alpha", "beta"])

    assert len(vectors) == 2
    assert all(len(vector) == 8 for vector in vectors)
    assert sum(value * value for value in vectors[0]) == pytest.approx(1.0)
    assert provider.dimension == 8


def test_embedding_provider_is_deterministic() -> None:
    provider = HashEmbeddingProvider(dimension=4)
    assert provider.embed_query("same") == provider.embed_query("same")


def test_embedding_provider_rejects_empty_text() -> None:
    provider = HashEmbeddingProvider()
    with pytest.raises(ValueError, match="must not be empty"):
        provider.embed_query("  ")

