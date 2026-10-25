# Day 11 — Hybrid retrieval

Added Reciprocal Rank Fusion to combine dense and sparse ranked lists. Ranking uses positions rather than incomparable Qdrant/FTS scores, deduplicates by chunk ID, and returns fused scores. Tests cover cross-retriever promotion and duplicate removal.

Next: Day 12 cross-encoder reranking.
