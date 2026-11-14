---
inclusion: always
---

# Mission Maths: Technical Stack

Proposed defaults; edit as decisions are made.

- **Language (back end):** Python 3.12+
- **Web framework:** FastAPI
- **Database:** PostgreSQL
- **Front end:** undecided (a thin client is enough: number pad, timer, canvas for asteroid fields). Record the decision here.
- **Game rendering:** HTML canvas (plain JS or a small framework)
- **Testing:** pytest, with property-style tests for question generators and boundary tests for mastery rules

## Conventions
- Type hints on all public functions
- Question generators are pure and deterministic from a seed
- Scoring and mastery decisions happen server-side from the event log; never trust client scores
- Gamification code and tables are separate from mastery code and tables
- Curriculum is data (see `curriculum.md`), never hard-coded in logic
