# Day 9 — Qdrant indexing and semantic retrieval

- Added dimension-checked collection creation, chunk upserts, and top-k semantic search.
- Preserved source and citation metadata in each Qdrant payload.
- Used document checksum, source, and chunk ordinal for stable point IDs across repeated ingestion.
- Tested against Qdrant's in-memory client; no server or network is needed for the test.

Install `pip install -e ".[qdrant]"`. Use one embedding model and dimension per collection; changed models require a fresh collection/reindex. The local tests are not a production Qdrant server benchmark.

Next: Day 10 keyword retrieval.
