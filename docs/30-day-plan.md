# NexusRAG — 30-Day Implementation Plan

## Final architecture

NexusRAG combines:

- FastAPI + LangGraph as the application and orchestration layer
- Qdrant for semantic document retrieval
- BM25/SQLite FTS5 for keyword retrieval
- Laya for fast text decisions
- Vega for long-context and multimodal decisions
- Gemini Embedding 2 for multimodal embeddings
- Unlimited-OCR for difficult scanned documents
- Corrective RAG for evidence filtering and sentence refinement
- Two memory features: duplicate detection and sleep-phase consolidation
- RAGAS and LangSmith for quality evaluation and observability

```text
FastAPI
  ↓
LangGraph Agentic RAG
  ↓
Router: Laya/Vega
  ↓
Adaptive retrieval
  ├── Qdrant semantic search
  ├── BM25/SQLite FTS5 keyword search
  ├── SQL search
  ├── multimodal search
  ├── memory recall
  └── Tavily web fallback
  ↓
RRF fusion → cross-encoder reranking
  ↓
Corrective grading → sentence filtering
  ↓
LLM generation
  ↓
Reflection → grounding → cited response

Background:
  duplicate detection → sleep-phase consolidation
```

## Completed

### Day 1 — Repository foundation

- Created the NexusRAG repository.
- Added FastAPI application and health endpoint.
- Added typed settings and local Qdrant/Redis services.
- Added pytest and development configuration.

### Day 2 — Foundation hardening

- Added settings validation.
- Added structured JSON logging.
- Added request ID propagation.
- Added `/ready` infrastructure readiness endpoint.

### Day 3 — Canonical document contracts

- Added `Document`, `DocumentChunk`, `CitationLocation`, and `Modality` schemas.
- Added page, timestamp, and bounding-box citation metadata.
- Added UUIDs, checksums, and validation tests.

### Day 4 — Document loaders

- Added TXT, Markdown, PDF, and DOCX loaders.
- Preserved PDF page citations.
- Added deterministic chunk ordering and loader tests.

## Core RAG foundation

### Day 5 — Chunking

- Add paragraph and sentence-aware splitting.
- Add configurable chunk size and overlap.
- Preserve section headings and source metadata.

### Day 6 — Embedding provider interface

- Define a provider-neutral embedding interface.
- Add local BGE-M3 and Ollama adapters.
- Add embedding dimension validation.

### Day 7 — Gemini Embedding 2

- Add Gemini Embedding 2 adapter.
- Support text, image, audio, video, and PDF inputs.
- Add configurable output dimensions.
- Document re-indexing requirements when dimensions change.

### Day 8 — Qdrant indexing

- Create collections with dimension checks.
- Index `DocumentChunk` records.
- Add idempotent upserts using document checksums.
- Add collection and index tests.

### Day 9 — Semantic retrieval

- Embed user queries.
- Retrieve top-k chunks from Qdrant.
- Return scores and citation metadata.
- Add semantic-search evaluation cases.

### Day 10 — Keyword retrieval

- Add SQLite FTS5/BM25 index.
- Support incremental indexing.
- Add keyword-sensitive retrieval tests.

### Day 11 — Hybrid retrieval

- Implement Reciprocal Rank Fusion.
- Deduplicate results across semantic and keyword search.
- Add retrieval score normalization.

### Day 12 — Cross-encoder reranking

- Add cross-encoder reranker interface.
- Rerank fused candidates.
- Add top-k and latency configuration.

## Agentic and corrective RAG

### Day 13 — LangGraph state

- Define the graph state and typed transitions.
- Add bounded retry counters.
- Add traceable node outputs.

### Day 14 — Router Agent

- Route queries to document, SQL, web, multimodal, or memory retrieval.
- Add rule-based baseline before model routing.

### Day 15 — Laya decision adapter

- Add optional Laya provider.
- Use it for fast text routing and typed decisions.
- Add abstention and confidence handling.

### Day 16 — Vega decision adapter

- Add optional Vega provider.
- Use it for long-context and multimodal decisions.
- Compare Vega and Laya on routing and sufficiency tasks.

### Day 17 — Corrective grading

- Grade retrieved chunks as relevant, ambiguous, or irrelevant.
- Add threshold configuration.
- Use Laya/Vega when appropriate and LLM fallback when needed.

### Day 18 — Sentence-level correction

- Split ambiguous chunks into sentences.
- Remove unsupported sentences.
- Preserve a safe full-chunk fallback.

### Day 19 — Query rewriting and retry

- Rewrite failed queries.
- Enforce a maximum retry budget.
- Add Tavily fallback for insufficient evidence.

### Day 20 — Generation and grounding

- Add generation agent.
- Restrict answers to verified context.
- Generate citations from metadata, never from model guesses.

### Day 21 — Reflection loop

- Add groundedness and contradiction checks.
- Re-retrieve when confidence is low.
- Abstain when evidence remains insufficient.

## Multimodal and memory

### Day 22 — OCR and visual documents

- Add Unlimited-OCR as an optional GPU-backed parser.
- Add OCR text, layout, table, formula, and bounding-box metadata.
- Keep standard PDF extraction as fallback.

### Day 23 — Audio and video

- Add Whisper transcripts.
- Preserve timestamps.
- Add video frame metadata and sampled-frame OCR.
- Index multimodal chunks through the same contract.

### Day 24 — SQL and tabular retrieval

- Add CSV/XLSX ingestion to SQLite.
- Route aggregations to SQL instead of embeddings.
- Add SQL citation metadata.

### Day 25 — Memory storage and recall

- Add HippocampAI-inspired memory records.
- Store user/agent facts, preferences, events, and summaries.
- Add semantic and keyword memory recall.
- Keep memory separate from authoritative documents.

### Day 26 — Duplicate detection

- Detect exact duplicates with checksums.
- Detect near-duplicates with embeddings.
- Prevent duplicate memories and repeated indexing.
- Add dry-run cleanup mode.

### Day 27 — Sleep-phase consolidation

- Add background consolidation worker.
- Merge related memories.
- Summarize old sessions.
- Update importance and recency.
- Detect contradictions without blocking live queries.

## Evaluation and production

### Day 28 — RAGAS and LangSmith

- Create a representative evaluation dataset.
- Track faithfulness, answer relevancy, context precision, and context recall.
- Add LangSmith traces for every graph run.
- Compare Laya, Vega, and LLM judges.

### Day 29 — Reliability and operations

- Add Prometheus metrics and Grafana dashboards.
- Add timeouts, rate limits, caching, and structured errors.
- Test provider failures, empty retrieval, OCR failures, and retry exhaustion.

### Day 30 — Release

- Run end-to-end integration tests.
- Validate Docker deployment.
- Document configuration and model choices.
- Record benchmark results and known limitations.
- Tag the first NexusRAG release.

## Scope rule

We borrow architecture and focused components from the selected projects. We do not merge entire repositories or duplicate their frontends and SaaS platforms. Every new feature must have a provider boundary, tests, and an evaluation path.

