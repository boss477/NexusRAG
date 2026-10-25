# NexusRAG

Production agentic corrective multimodal RAG.

NexusRAG is a 30-day implementation project for a production-oriented RAG system combining:

- LangGraph multi-agent orchestration
- Corrective retrieval with relevance thresholds and sentence filtering
- Hybrid dense + sparse retrieval
- Qdrant vector search
- FastAPI backend
- RAGAS evaluation
- LangSmith tracing and observability

The project is intentionally starting small. Each day will add one tested vertical slice.

## Planned architecture

```text
Query -> Router -> Hybrid Retrieval -> Correction -> Generation
                                      ^              |
                                      |              v
                              Web fallback <- Reflection -> Grounding
```

## 30-day roadmap

The detailed plan is in [docs/30-day-plan.md](docs/30-day-plan.md). Days 1–11 are complete locally; only Days 1–8 are published so far.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/macOS
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Current status

Days 1–11 are complete locally: ingestion, embeddings, semantic and keyword retrieval, and RRF fusion. Day 11 is documented in [docs/day-11-hybrid.md](docs/day-11-hybrid.md).

Decisions are recorded in [docs/](docs/).

