# Day 7 — Gemini Embedding 2

## Completed

- Added `GeminiEmbeddingProvider` behind the shared embedding interface.
- Added configurable model name and output dimension.
- Added REST calls to Gemini's `embedContent` endpoint.
- Added API-key and response-dimension validation.
- Added environment settings for Gemini embeddings.
- Added a mocked provider test without requiring a live API key.

The adapter defaults to `gemini-embedding-2` with 1536 dimensions. Gemini recommends 768, 1536, or 3072 dimensions. Changing dimensions requires a new or re-indexed vector collection.

This day supports text inputs. Image, audio, video, and PDF payloads will be added with multimodal ingestion and local EmbeddingGemma work.

## Next day

Day 8: add the local EmbeddingGemma 2 adapter.
