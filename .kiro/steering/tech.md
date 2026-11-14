---
inclusion: always
---

# Mission Maths: Technical Steering

This file is the source of truth for all technology decisions. When code, tooling or architecture decisions conflict with this file, raise the conflict rather than silently choosing. Update this file when a decision changes.

---

## 1. Language and runtime

- **Python 3.12+** throughout the back end and application layer.
- Type hints are required on all public functions and methods. Use `from __future__ import annotations` where needed for forward references.
- Prefer `pathlib` over `os.path`, dataclasses or Pydantic models over plain dicts for structured data.

---

## 2. Dependency and environment management

- **Poetry** for all dependency and virtual environment management.
- `pyproject.toml` is the single source of package metadata and dependencies.
- Never commit a manually created `requirements.txt`. If one is needed for deployment, generate it with `poetry export`.
- Pin direct dependencies; let Poetry resolve transitive pins. Commit `poetry.lock`.

---

## 3. Back end

### 3.1 Framework
- **FastAPI** for all HTTP and WebSocket endpoints.
- Organise routers by domain: `sessions`, `assessments`, `progress`, `curriculum`, `parent`, `admin`.
- Use FastAPI dependency injection for database sessions, authentication context, and shared services.
- All request and response bodies are **Pydantic v2 models**. No raw dicts crossing the API boundary.

### 3.2 Database
- **PostgreSQL** as the primary data store.
- **SQLAlchemy 2.x** (async, using `asyncpg` driver) for ORM and query layer.
- **Alembic** for schema migrations. Every schema change has a migration; never alter the database by hand.
- Curriculum data (levels, waypoints, thresholds, names) lives in the database, seeded from YAML/JSON files in `curriculum/`. It is never hard-coded in application logic.

### 3.3 Server authority
- Scoring, mastery decisions, and progression logic execute on the server from the event log.
- The server never trusts a client-supplied score, rank, or mastery state.
- The server validates that submitted answers correspond to the server-issued seeded question (by seed and question index) and that reported timings are plausible.

### 3.4 Async
- All I/O-bound code (database, external calls) uses `async`/`await`.
- CPU-bound work (if any) is offloaded with `asyncio.run_in_executor`.

---

## 4. Front end

### 4.1 Rendering model
NiceGUI is the application shell. Python holds state; the browser renders it via Vue and Quasar over a WebSocket. The following client-side bridges are available and should be used as described:

| Mechanism | When to use |
|---|---|
| `ui.run_javascript(...)` | One-off reads from the browser (e.g. `performance.now()`, DOM queries). Await the return value in Python when the result is needed. |
| `js_handler` on events | Handle an event entirely on the client with no server round trip, or capture and transform event data before emitting to Python. Use for all response-time capture. |
| `emitEvent(...)` / `ui.on(...)` | Send a batch of client-side results (e.g. end-of-round asteroid field data) back to Python. |
| Injected JS/CSS (`ui.add_head_html`) | Host the asteroid-field canvas module and any supporting game scripts inside a NiceGUI page. |
| Custom Vue components | Wrap reusable interactive elements that exceed what standard NiceGUI elements can express. Check current NiceGUI docs for registration. |

### 4.2 UI framework split

| Surface | Technology | Rationale |
|---|---|---|
| Parent dashboard, progress views, settings, login, admin | NiceGUI | CRUD and display; no tight timing; stays fully in Python |
| Daily drill screen | NiceGUI + `js_handler` for timing | Simple layout in NiceGUI; response time captured in browser via `performance.now()` to avoid network jitter |
| Level check | NiceGUI + `js_handler` for timing | Same as daily drill |
| Asteroid-field game | NiceGUI page shell + self-contained JS canvas module | 60 fps game loop must run entirely client-side; events batched and submitted to Python at round end via `emitEvent` |
| Journey map | NiceGUI (SVG or canvas via injected JS) | Static or lightly animated; no game loop required |

### 4.3 Response time capture rule
**Never measure response time on the server.** All response times are captured with `performance.now()` in the browser via a `js_handler` and submitted alongside the answer. The server records the submitted time and validates plausibility (floor: ~100 ms; ceiling: session timeout).

### 4.4 Asteroid-field module
- Implemented as a self-contained JavaScript module (plain JS or a minimal canvas library such as Konva or PixiJS — decide and record here when chosen).
- The server issues a seeded question set before the round starts. The JS module renders the round using that seed.
- Per-item events (answer given, time, outcome, pace in effect) are accumulated client-side and submitted as a batch to Python via `emitEvent` at round end.
- The server recomputes accuracy and speed from the batch. The client result is display-only.
- **No third-party game engine** (no Unity, no Godot, no Phaser) unless a specific need justifies the payload cost. Keep it small.

---

## 5. Testing

- **pytest** for all tests: unit, integration, and API.
- **pytest-asyncio** for async tests.
- **httpx** with FastAPI's `AsyncClient` for API-level tests.
- **pytest-cov** for coverage reporting.
- Test file convention: `tests/<module>/test_<name>.py` mirroring the `app/` structure.

### 5.1 What must be tested
| Component | Test approach |
|---|---|
| Question generators | Unit tests: determinism from seed, full output range, boundary inputs, property-style tests over sampled seeds |
| Mastery pass rules | Unit tests: accuracy just below and just above threshold, speed just below and just above, consecutive-session counting, mixed pass/fail streaks |
| Promotion logic | Unit tests: level check pass/fail, zone test pass/fail, no-loss invariant |
| Event log processing | Unit tests: error pattern detection, fluency trend calculation |
| Repair mission selection | Unit tests: correct skills targeted from error log |
| FastAPI routers | Integration tests via `AsyncClient`: happy paths and error cases |
| Asteroid-field server validation | Unit tests: plausibility checks on submitted timings and answer-to-seed correspondence |

### 5.2 Testing rules
- Generators must be tested for determinism: the same seed always produces the same question sequence.
- Mastery and progression tests must cover boundary cases explicitly (at-threshold, one below, one above).
- Gamification code must be tested independently of mastery code; no shared fixtures that couple them.
- Tests never hit a live database; use `pytest-postgresql` or an in-memory SQLite override for unit tests, and a test-scoped PostgreSQL instance for integration tests.

---

## 6. Architecture principles

### 6.1 Clean architecture boundaries

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
  schemas/        # Pydantic request/response models.
  curriculum/     # Curriculum data loader and validators.
curriculum/       # Curriculum data files (YAML/JSON). Not application code.
web/              # NiceGUI pages and the asteroid-field JS module.
tests/
```

**Dependency rule:** inner layers never import from outer layers.
- `engine/` has no imports from `api/`, `services/`, `models/`, or `gamification/`.
- `gamification/` has no imports from `engine/`.
- `api/` calls `services/`, never `engine/` or `models/` directly.

### 6.2 SOLID

| Principle | How it applies |
|---|---|
| **Single responsibility** | Each module, class and function does one thing. Routers route. Generators generate. Mastery logic decides pass/fail. Services orchestrate. |
| **Open/closed** | Question generators and mastery rules are open to new curriculum data without changing existing logic. Add a new level by adding data, not by editing a switch statement. |
| **Liskov substitution** | Concrete generator classes implement a common `QuestionGenerator` protocol. Any generator can replace any other wherever the protocol is expected. |
| **Interface segregation** | Define narrow protocols (`QuestionGenerator`, `MasteryEvaluator`, `ReviewScheduler`) rather than large base classes. |
| **Dependency inversion** | Services depend on protocols, not concrete implementations. Inject dependencies via FastAPI's `Depends` or constructor injection. |

### 6.3 DRY
- One mastery engine. Daily drills, level checks, placement, repair missions and asteroid fields all write to the same attempt log and run through the same pass-rule logic. Delivery mode is a parameter, not a code branch.
- One question-generation interface. The asteroid field and the daily drill call the same generators with the same seed contract.
- Curriculum thresholds and target times are read from data once, cached in memory, and passed to the engine. They are never duplicated in code.

### 6.4 Pure functions in the engine
- All functions in `engine/generators/` and `engine/mastery/` are **pure**: same inputs, same outputs, no side effects, no I/O.
- This makes them trivially testable and reproducible.
- I/O (database reads/writes) lives in `services/` and is injected.

### 6.5 Immutable event log
- The attempt log is append-only. Rows are never updated or deleted.
- Mastery state is derived from the log on demand (or cached and invalidated). It is never stored as a mutable flag.

---

## 7. Code style and conventions

- **PEP-8** is the baseline style standard for all Python code. Follow it unless a rule below explicitly overrides it.
- **Ruff** for linting and import sorting. Config in `pyproject.toml`. Ruff enforces PEP-8 rules automatically; treat any Ruff violation as a PEP-8 violation.
- **Ruff formatter** for code formatting. Do not use Black.
- Maximum line length: 100 characters (a deliberate PEP-8 override; 79 is too narrow for modern screens).
- Naming follows PEP-8: `snake_case` for functions, variables and modules; `PascalCase` for classes; `UPPER_SNAKE_CASE` for module-level constants; `_leading_underscore` for internal/private names.
- Imports are grouped in PEP-8 order: standard library, third-party, local. Ruff enforces this automatically.
- No bare `except:`. Catch specific exceptions.
- No mutable default arguments.
- All public functions have a docstring if their purpose is not obvious from the name and signature alone.

---

## 8. Configuration and secrets

- Application configuration via **Pydantic `BaseSettings`**, reading from environment variables and a `.env` file (never committed).
- Secrets (database URL, secret keys) are never hard-coded or committed.
- Provide a `.env.example` with all required keys and placeholder values, committed to the repository.

---

## 9. Open decisions (record here when settled)

| Decision | Status | Notes |
|---|---|---|
| Canvas library for asteroid field | Undecided | Plain JS, Konva, or PixiJS. Evaluate against payload size and animation smoothness. |
| Code formatter | **Ruff formatter** | Black is not used |
| Spaced repetition algorithm | Undecided | Leitner or SM-2. Must be documented once chosen (business-rules.md §8). |
| Deployment target | Undecided | — |
| Monetisation model | Undecided | Affects auth and account model (business-rules.md §16) |
| Auth library | Undecided | FastAPI-Users or custom JWT implementation |
