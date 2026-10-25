# Day 10 — Keyword retrieval

Added a persistent SQLite FTS5 index for chunk text with BM25 ranking. Upserts replace an existing chunk ID, so repeat indexing is idempotent. Searches tokenize and quote terms before passing them to FTS5, avoiding raw query syntax injection. Tests cover rare-token lookup, repeat indexing, and malformed input.

Next: Day 11 RRF hybrid fusion.
