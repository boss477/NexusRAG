from __future__ import annotations

import hashlib
import math
from collections.abc import Sequence
from typing import Protocol


class EmbeddingProvider(Protocol):
    """Small contract shared by every embedding backend."""

    @property
    def dimension(self) -> int: ...

    @property
    def model_name(self) -> str: ...

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class HashEmbeddingProvider:
    """Deterministic, dependency-free provider for tests and local plumbing."""

    def __init__(self, dimension: int = 32, model_name: str = "hash-test") -> None:
        if dimension < 1:
            raise ValueError("dimension must be positive")
        self._dimension = dimension
        self._model_name = model_name

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def model_name(self) -> str:
        return self._model_name

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("text must not be empty")
        values = []
        for index in range(self._dimension):
            digest = hashlib.sha256(f"{index}:{text}".encode()).digest()
            values.append((int.from_bytes(digest[:4], "big") / 2**31) - 1)
        norm = math.sqrt(sum(value * value for value in values)) or 1
        return [value / norm for value in values]


class BGEEmbeddingProvider:
    """Lazy adapter for a local Sentence Transformers BGE-M3 model."""

    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        self._model_name = model_name
        self._model = None

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        self._load()
        return int(self._model.get_sentence_embedding_dimension())

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        self._validate(texts)
        self._load()
        return self._model.encode(list(texts), normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def _load(self) -> None:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError("Install sentence-transformers to use BGEEmbeddingProvider") from exc
            self._model = SentenceTransformer(self._model_name)

    @staticmethod
    def _validate(texts: Sequence[str]) -> None:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("texts must contain at least one non-empty string")


class OllamaEmbeddingProvider:
    """HTTP adapter for Ollama's local `/api/embed` endpoint."""

    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434") -> None:
        self._model_name = model_name
        self._base_url = base_url.rstrip("/")
        self._dimension: int | None = None

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            raise RuntimeError("dimension is available after the first embedding request")
        return self._dimension

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("texts must contain at least one non-empty string")
        try:
            import httpx
        except ImportError as exc:
            raise RuntimeError("Install httpx to use OllamaEmbeddingProvider") from exc
        response = httpx.post(
            f"{self._base_url}/api/embed",
            json={"model": self._model_name, "input": list(texts)},
            timeout=60,
        )
        response.raise_for_status()
        embeddings = response.json()["embeddings"]
        if not embeddings:
            raise RuntimeError("Ollama returned no embeddings")
        self._dimension = len(embeddings[0])
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


class GeminiEmbeddingProvider:
    """Google Gemini Embedding 2 text adapter using the Gemini REST API."""

    def __init__(self, api_key: str, model_name: str = "gemini-embedding-2", output_dimension: int = 1536, base_url: str = "https://generativelanguage.googleapis.com/v1beta") -> None:
        if not api_key:
            raise ValueError("api_key must not be empty")
        if output_dimension not in {768, 1536, 3072}:
            raise ValueError("output_dimension must be one of 768, 1536, or 3072")
        self._api_key = api_key
        self._model_name = model_name
        self._dimension = output_dimension
        self._base_url = base_url.rstrip("/")

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("texts must contain at least one non-empty string")
        try:
            import httpx
        except ImportError as exc:
            raise RuntimeError("Install httpx to use GeminiEmbeddingProvider") from exc
        embeddings = []
        for text in texts:
            response = httpx.post(
                f"{self._base_url}/models/{self._model_name}:embedContent",
                headers={"x-goog-api-key": self._api_key},
                json={"content": {"parts": [{"text": text}]}, "output_dimensionality": self._dimension},
                timeout=60,
            )
            response.raise_for_status()
            values = response.json().get("embedding", {}).get("values")
            if not values or len(values) != self._dimension:
                raise RuntimeError("Gemini returned an invalid embedding dimension")
            embeddings.append(values)
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

