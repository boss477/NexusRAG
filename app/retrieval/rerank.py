from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Protocol

from app.retrieval.semantic import SearchHit


class PairScorer(Protocol):
    def predict(self, pairs: list[tuple[str, str]]) -> Sequence[float]: ...


class CrossEncoderReranker:
    """Bounded reranker; loads its local model only on first use."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L6-v2",
        max_candidates: int = 30,
        scorer: PairScorer | None = None,
    ) -> None:
        if max_candidates < 1:
            raise ValueError("max_candidates must be positive")
        self.model_name = model_name
        self.max_candidates = max_candidates
        self._scorer = scorer

    def rerank(self, query: str, hits: Sequence[SearchHit], limit: int = 5) -> list[SearchHit]:
        if not query.strip() or limit < 1:
            raise ValueError("query must be non-empty and limit must be positive")
        candidates = list(hits[: self.max_candidates])
        if not candidates:
            return []
        if self._scorer is None:
            try:
                from sentence_transformers import CrossEncoder
            except ImportError as exc:
                raise RuntimeError("Install the reranker extra to use CrossEncoderReranker") from exc
            self._scorer = CrossEncoder(self.model_name)
        scores = self._scorer.predict([(query, hit.chunk.text) for hit in candidates])
        if len(scores) != len(candidates) or any(not math.isfinite(float(s)) for s in scores):
            raise RuntimeError("reranker returned invalid scores")
        ranked = sorted(
            (SearchHit(hit.chunk, float(score)) for hit, score in zip(candidates, scores, strict=True)),
            key=lambda hit: hit.score,
            reverse=True,
        )
        return ranked[:limit]
