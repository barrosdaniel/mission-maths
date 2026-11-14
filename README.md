# Mission Maths

A mastery-based maths fluency platform for children, built with a Kumon-inspired method: tiny steps, mastery before progression, short daily repetition, and self-correction.

Learners are trainee astronauts on a mission to a distant planet. Fleet Academy ranks recognise progress. Asteroid-field games are the periodic zone assessments.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Backend | FastAPI + Uvicorn |
| Database | PostgreSQL (async via SQLAlchemy 2 + asyncpg) |
| Migrations | Alembic |
| Frontend | NiceGUI (application shell) + self-contained JS canvas module (asteroid field) |
| Config | Pydantic BaseSettings |
| Testing | pytest + pytest-asyncio + httpx |
| Linting / formatting | Ruff |
| Dependency management | Poetry |

---

## Getting started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- PostgreSQL running locally (or via Docker)

### Install dependencies

```bash
poetry install
```

### Configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### Run the development server

```bash
poetry run uvicorn app.main:fastapi_app --reload
```

API docs available at http://localhost:8000/docs.

### Run database migrations

```bash
poetry run alembic upgrade head
```

### Run tests

```bash
poetry run pytest
```

### Lint and format

```bash
# Check
poetry run ruff check .
# Format
poetry run ruff format .
```

---

## Project structure

```
app/
  api/            # FastAPI routers — HTTP/WebSocket boundary only
  engine/
    generators/   # Seeded question generators (pure functions)
    mastery/      # Pass rules, level checks, placement, repair missions
    review/       # Retention and spaced repetition scheduling
  gamification/   # Fuel, flight hours, badges — isolated from engine/
  services/       # Orchestration layer (calls engine + persistence)
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic request/response models
  curriculum/     # Curriculum data loader and validators
  config.py       # Pydantic BaseSettings
  database.py     # Async engine, session factory, declarative Base
  main.py         # FastAPI app entry point
curriculum/       # Curriculum data files (YAML/JSON) — not application code
web/              # NiceGUI pages and asteroid-field JS module
tests/            # Mirrors app/ structure
alembic/          # Database migration scripts
```

---

## Steering documents

Product and engineering decisions live in `.kiro/steering/`:

| File | Contents |
|---|---|
| `product.md` | Product summary and audience |
| `business-rules.md` | Full product rules — read before changing any behaviour |
| `curriculum.md` | Maths programme: levels, waypoints, thresholds (loaded on demand) |
| `tech.md` | Technology decisions, architecture principles, code style |
| `structure.md` | Project folder layout |
