# Day 6 — Embedding Provider Interface

## Completed

- Added the provider-neutral `EmbeddingProvider` protocol.
- Added a deterministic hash provider for tests and local plumbing.
- Added a lazy BGE-M3 adapter using Sentence Transformers.
- Added an Ollama adapter using the local `/api/embed` endpoint.
- Added dimension and model identity properties.
- Added normalized-vector and empty-input tests.

## Design decision

Retrieval and indexing code will depend on `EmbeddingProvider`, not on Google, OpenAI, BGE, or Ollama directly. This allows NexusRAG to compare providers and migrate collections deliberately.

Gemini Embedding 2 remains a separate Day 7 adapter because it also introduces multimodal inputs and production dimension configuration.

## Next day

Day 7: add the Gemini Embedding 2 adapter and configuration.
