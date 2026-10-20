# Day 3 — Canonical Document Contracts

## Completed

- Added shared `Document` and `DocumentChunk` Pydantic models.
- Added modalities for text, PDF, DOCX, image, audio, video, table, and web data.
- Added stable document and chunk UUIDs.
- Added source, ordinal, checksum, and ingestion metadata.
- Added citation locations for pages, timestamps, and bounding boxes.
- Added validation for non-empty content and valid media timestamps.
- Added tests covering metadata preservation and invalid input.

## Design decision

All ingestion adapters must produce `DocumentChunk` records before indexing. This keeps loaders independent from Qdrant, BM25, embedding providers, and agent logic.

Citation metadata is part of the chunk contract so final answers can render citations from source data instead of asking the language model to invent them.

## Next day

Day 4: implement PDF, DOCX, Markdown, and text loaders that emit these canonical records.
