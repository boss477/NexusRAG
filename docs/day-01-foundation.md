# Day 1 — Foundation

## Project name

**NexusRAG**: the nexus between multimodal evidence, agentic retrieval, and grounded answers.

## Goal

Create a small, testable service foundation that future ingestion, retrieval, agents, evaluation, and observability work can build on.

## Completed

- Python package configuration with `pyproject.toml`
- FastAPI application entrypoint
- Typed environment settings using Pydantic Settings
- `/` and `/health` endpoints
- Qdrant and Redis local services in Docker Compose
- Development dependencies and pytest configuration
- Initial health endpoint test
- Repository-wide ignore rules and environment template

## Design decisions

- FastAPI is the external API boundary.
- Settings are read from environment variables and `.env`, never hardcoded secrets.
- Qdrant and Redis run as local infrastructure services.
- Application features will be added behind interfaces rather than coupled directly to providers.
- Every future day must add tests with the feature.

## Definition of done

```text
python -m pytest       -> passing
uvicorn app.main:app  -> starts successfully
GET /health            -> {"status": "ok", ...}
```

## Day 2 follow-up

Completed in the next increment: configuration validation, structured logging, request IDs, and a readiness endpoint that reports infrastructure DNS availability.

