# Day 4 — Document Loaders

## Completed

- Added loaders for TXT, Markdown, PDF, and DOCX files.
- Added extension and file-existence validation.
- Added SHA-256 checksums for ingestion deduplication later.
- Added deterministic chunk ordinals.
- Preserved PDF page numbers in citation metadata.
- Emitted every loader result as the canonical `DocumentChunk` contract.
- Added loader tests for chunk identity, checksums, and invalid inputs.

## Design decision

Loaders are intentionally separate from embeddings and vector databases. They only parse and normalize source files. Indexing will consume `DocumentChunk` objects in a later day.

The current splitter is deliberately simple and deterministic. Semantic and sentence-aware chunking will replace or extend it after retrieval baselines exist.

## Next day

Day 5: improve chunking with paragraph/sentence boundaries, overlap, and configurable metadata.
