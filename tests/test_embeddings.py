import pytest

from app.embeddings import EmbeddingGemmaProvider, GeminiEmbeddingProvider, HashEmbeddingProvider


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


def test_gemini_provider_uses_configured_dimension(monkeypatch) -> None:
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"embedding": {"values": [0.1] * 768}}

    def fake_post(*args, **kwargs):
        assert kwargs["json"]["output_dimensionality"] == 768
        return Response()

    monkeypatch.setattr("httpx.post", fake_post)
    provider = GeminiEmbeddingProvider("key", output_dimension=768)
    assert len(provider.embed_query("hello")) == 768


def test_embeddinggemma_prompts_truncates_and_normalizes() -> None:
    calls = []

    class FakeModel:
        def encode(self, value, **kwargs):
            calls.append((value, kwargs))
            vector = [3.0, 4.0] + [0.0] * 126
            return [vector] * len(value) if isinstance(value, list) else vector

    provider = EmbeddingGemmaProvider(dimension=128)
    provider._model = FakeModel()
    assert provider.embed_query("query")[:2] == pytest.approx([0.6, 0.8])
    assert provider.embed_documents(["document"])[0][:2] == pytest.approx([0.6, 0.8])
    assert calls[0] == (
        "query",
        {"prompt_name": "SearchQuery", "truncate_dim": 128, "normalize_embeddings": True},
    )
    assert calls[1][1]["prompt_name"] == "Document"


def test_embeddinggemma_media_uses_enabled_encoder() -> None:
    class FakeModel:
        def encode(self, value, **kwargs):
            assert value == {"image": "photo.png"}
            assert "prompt_name" not in kwargs
            return [1.0] + [0.0] * 767

    provider = EmbeddingGemmaProvider(load_vision=True)
    provider._model = FakeModel()
    assert len(provider.embed_media({"image": "photo.png"})) == 768
    with pytest.raises(ValueError, match="audio encoder is disabled"):
        provider.embed_media({"audio": "speech.wav"})


def test_embeddinggemma_rejects_invalid_dimension_and_output() -> None:
    with pytest.raises(ValueError, match="dimension"):
        EmbeddingGemmaProvider(dimension=1536)

    class FakeModel:
        def encode(self, value, **kwargs):
            return [float("nan")] * 768

    provider = EmbeddingGemmaProvider()
    provider._model = FakeModel()
    with pytest.raises(RuntimeError, match="invalid embedding"):
        provider.embed_query("query")


def test_embeddinggemma_loads_only_selected_encoders(monkeypatch) -> None:
    import sys
    from types import SimpleNamespace

    captured = {}

    def fake_sentence_transformer(name, **kwargs):
        captured.update({"name": name, **kwargs})
        return object()

    fake_cuda = SimpleNamespace(is_available=lambda: False, is_bf16_supported=lambda: False)
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(cuda=fake_cuda, float32="float32"))
    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=fake_sentence_transformer),
    )
    EmbeddingGemmaProvider(load_vision=True)._load()
    assert captured["config_kwargs"] == {"audio_config": None}
    assert captured["model_kwargs"] == {"torch_dtype": "float32"}

