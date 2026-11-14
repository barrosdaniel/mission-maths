---
inclusion: always
---

# Mission Maths: Project Structure

Proposed layout; update as the repository takes shape.

```
app/
  api/            # FastAPI routers (sessions, assessments, progress, parent view)
  engine/
    generators/   # seeded question generators, one per skill
    mastery/      # pass rules, level checks, placement, repair missions
    review/       # retention and spaced review scheduling
  gamification/   # fuel, flight hours, badges, cosmetics (isolated from mastery)
  models/         # database models
  curriculum/     # loader and validators for curriculum data
curriculum/       # curriculum data files (levels, waypoints, thresholds, names)
web/              # front end, including the asteroid-field game
tests/
```

## Rules
- `engine/` must not import from `gamification/`
- One attempt log feeds every delivery mode (drill, level check, practice field, zone test, placement, repair mission)
- Terminology follows `business-rules.md` Section 10
