from __future__ import annotations

from collections.abc import Sequence

from app.retrieval.semantic import SearchHit


def rrf_fuse(
    result_lists: Sequence[Sequence[SearchHit]], *, limit: int = 5, k: int = 60
) -> list[SearchHit]:
    """Fuse ranked result lists without comparing incompatible raw scores."""
    if limit < 1 or k < 1:
        raise ValueError("limit and k must be positive")
    scores: dict[str, float] = {}
    chunks = {}
    for results in result_lists:
        seen = set()
        for rank, hit in enumerate(results, start=1):
            chunk_id = str(hit.chunk.chunk_id)
            if chunk_id in seen:
                continue
            seen.add(chunk_id)
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1 / (k + rank)
            chunks[chunk_id] = hit.chunk
    ranked = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))[:limit]
    return [SearchHit(chunk=chunks[chunk_id], score=scores[chunk_id]) for chunk_id in ranked]
