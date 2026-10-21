# Day 5 — Sentence-Aware Chunking

## Completed

- Replaced raw character slicing with paragraph and sentence-aware chunking.
- Added configurable `max_chars` and overlap settings.
- Added hard-split fallback for individual units longer than the configured limit.
- Preserved deterministic chunk ordinals and source citation metadata.
- Added validation for invalid chunk sizes and overlap values.
- Added chunking and loader tests.

## Design decision

Chunking is deterministic and provider-independent. It runs before embeddings and indexing, so retrieval providers receive the same canonical chunks and can be compared fairly.

The overlap is intentionally bounded and configurable. Later retrieval benchmarks will tune it against context recall and storage cost.

## Next day

Day 6: define and implement the provider-neutral embedding interface.
