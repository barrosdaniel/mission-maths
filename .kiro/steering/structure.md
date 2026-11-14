---
inclusion: always
---

# Mission Maths: Project Structure

```
app/
  api/            # FastAPI routers — HTTP/WebSocket boundary only. No business logic.
  engine/
    generators/   # Seeded question generators. Pure functions. No I/O.
    mastery/      # Pass rules, level checks, placement, repair missions. No I/O.
    review/       # Retention scheduling. No I/O.
  gamification/   # Fuel, flight hours, badges, cosmetics. Isolated from engine/.
  services/       # Orchestration layer. Calls engine + persistence. Owns transactions.
  models/         # SQLAlchemy ORM models.
  schemas/        # Pydantic request/response models. No SQLAlchemy imports.
  curriculum/     # Curriculum data loader and validators.
  config.py       # Pydantic BaseSettings — application configuration.
  database.py     # Async engine, session factory, declarative Base.
  main.py         # FastAPI app entry point — mounts routers and middleware.
curriculum/       # Curriculum data files (YAML/JSON). Not application code.
web/              # NiceGUI pages and the asteroid-field JS canvas module.
tests/            # Mirrors app/ structure.
alembic/          # Database migration scripts.
```

## Dependency rules

- `engine/` must not import from `api/`, `services/`, `models/`, or `gamification/`.
- `gamification/` must not import from `engine/`.
- `api/` calls `services/` only — never `engine/` or `models/` directly.
- One attempt log feeds every delivery mode: drill, level check, practice field, zone test, placement, repair mission.

## Terminology

Follows `business-rules.md` Section 10. Use those terms in code identifiers, comments, and UI copy.
