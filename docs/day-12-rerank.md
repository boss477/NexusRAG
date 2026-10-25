# Day 12 — Cross-encoder reranking

Added a lazy Sentence Transformers cross-encoder over the fused candidate list. `max_candidates` bounds expensive pair scoring; `limit` controls returned top-k. Tests inject a fake scorer and do not download weights. Install `pip install -e ".[reranker]"` to run a real model.

Next: Day 13 LangGraph state.
