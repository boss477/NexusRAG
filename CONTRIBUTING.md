# Contributing to NexusRAG

Thanks for helping. NexusRAG grows one tested vertical slice at a time, and every new feature needs
a provider boundary, tests and an evaluation path.

## Ground rules

- Be kind. This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
- Open an issue before a large change so it can fit the [30-day plan](docs/30-day-plan.md).
- Keep pull requests to one slice: one change, one reason, with its tests.
- Never commit `.env`. Copy `.env.example` instead.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev,qdrant]"
cp .env.example .env               # Windows: copy .env.example .env
docker compose up -d               # Qdrant and Redis
uvicorn app.main:app --reload
```

## Before you open a pull request

- `pytest` passes.
- New behaviour has a test, and a `docs/day-NN-*.md` note if it is a slice of the plan.
