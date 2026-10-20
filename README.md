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

1. Repository foundation and health endpoint
2. Configuration and environment validation
3. Document ingestion contracts
4. PDF, DOCX, and Markdown loading
5. Chunking and metadata
6. Embedding provider
7. Qdrant indexing
8. Dense retrieval
9. BM25 sparse retrieval
10. Hybrid fusion with RRF
11. Cross-encoder reranking
12. Query router agent
13. Retrieval agent
14. Corrective chunk scoring
15. Sentence-level refinement
16. Tavily web fallback
17. Generation agent
18. Citation grounding
19. Reflection and retry loop
20. LangGraph state machine
21. Streaming API responses
22. Redis-backed state and caching
23. LangSmith tracing
24. RAGAS evaluation dataset
25. Automated evaluation runner
26. Authentication and request limits
27. Docker Compose deployment
28. Observability with Prometheus/Grafana
29. Integration and failure testing
30. Production hardening and release

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

Day 1–3 are complete: project foundation, settings/logging/readiness hardening, and canonical document schemas are in place.

Decisions are recorded in [docs/](docs/).

