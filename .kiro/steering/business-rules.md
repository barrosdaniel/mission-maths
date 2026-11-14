---
inclusion: always
---

# Mission Maths: Business Rules

This file describes **what Mission Maths is and the rules it must obey**. It is the source of truth for product behaviour. When code, tests or design decisions conflict with this file, raise the conflict rather than silently choosing.

**Related files**
- `.kiro/steering/curriculum.md`: the maths programme, levels, waypoints, question types and pass thresholds per level. This file deliberately does **not** define curriculum content. Always read `.kiro/steering/curriculum.md` before implementing or changing any level, generator or threshold.

Where this file says "configurable", the value lives in configuration or curriculum data, never hard-coded in logic.

---

## 1. Product summary

Mission Maths is a web platform that teaches **basic mathematical operations to fluency and automaticity** using a Kumon-inspired methodology: tiny steps, mastery before progression, short daily repetition, and self-correction.

The learner is a trainee astronaut on a **mission to a distant planet**. A **Fleet Academy** rank system recognises progress. **Asteroid-field games** act as the periodic assessments along the journey.

The theme is a skin over a learning engine. The engine's rules (Sections 3 to 8) take precedence over theme and gamification (Sections 9 to 10).

**Do not use or imply any affiliation with Kumon or its trademarks** in code, UI copy, assets or documentation visible to users. "Kumon-inspired" may appear in internal documents only.

---

## 2. Users and roles

| Role | Description | Key capabilities |
|---|---|---|
| **Learner** | A child (primary audience), possibly older learners | Do daily sessions, take level checks and asteroid fields, view own journey |
| **Parent / guardian** | Owns the account and one or more learner profiles | Create and manage learner profiles, view progress and time practised, see where a learner is stuck, adjust accessibility settings |
| **Teacher** (future) | Manages a class of learners | Read-only class progress view; out of scope for MVP unless stated |
| **Admin** | Platform operator | Manage curriculum data, content, accounts, support |

Rules:
- Learners never see other learners' data. There are **no public leaderboards** and no learner-to-learner messaging.
- A parent account can hold multiple learner profiles. A learner profile belongs to exactly one parent account.
- Child data is sensitive. Collect the minimum needed; see Section 11.

---

## 3. Learning model

### 3.1 Hierarchy

| Layer | Name in product | Meaning |
|---|---|---|
| Smallest unit | **Waypoint** | One worksheet-sized step within a level |
| Skill stage | **Level** | A tightly scoped skill made up of ordered waypoints. About 20 levels in the programme |
| Group of levels | **Zone** | A set of consecutive levels (about 4) ending in an asteroid-field test |
| Recognition | **Rank** and **pip** | Pips are earned per level, ranks per zone |

The exact levels, waypoints, groupings and names are defined in `.kiro/steering/curriculum.md`. Never hard-code level numbers, counts or content in application logic.

### 3.2 Core principles that must hold in every feature

1. **Tiny steps.** Each waypoint adds at most one small new difficulty.
2. **Mastery before progression.** A learner advances only when both accuracy and speed criteria are met. Neither alone is enough.
3. **Repetition to automaticity.** The goal is fast, effortless recall, not just correctness.
4. **Short, regular sessions.** Daily practice is the intended habit; sessions are short (target 10 to 15 minutes).
5. **Self-correction.** A wrong answer is not simply marked wrong; the learner must see it and redo it until correct (see 5.4).
6. **Right starting point.** New learners are placed at the correct level, not always at the beginning.
7. **Retention.** Mastered skills are periodically reviewed on an expanding schedule.

---

## 4. Progression rules

### 4.1 Passing a waypoint or level
- Pass requires **both** an accuracy threshold and a speed (median response time) threshold, achieved over a required number of **consecutive** qualifying sessions.
- All thresholds and counts are defined per level in `.kiro/steering/curriculum.md` (configurable). There must be sensible global defaults, but level-specific values override them.
- Fast but inaccurate, or accurate but slow, does **not** pass.

### 4.2 Level check
- A plain timed drill at the end of each level, equivalent to a unit test.
- Passing it completes the level, awards a **pip**, and unlocks the next level.
- Failing it does not lose progress: the learner repeats the final waypoints and retries.

### 4.3 Zone test (asteroid field)
- After the last level of a zone, the learner must pass that zone's asteroid-field game (Section 6).
- Passing awards the **next rank** and advances the journey to the next zone.
- Failing triggers a **repair mission** (4.4), not a repeat of the whole zone.

### 4.4 Repair missions
- On a failed zone test, use the event log to identify which skills and levels produced the errors or slow responses.
- Assign a short, targeted set of waypoints covering only those weaknesses, then allow a retry.
- A learner must never be forced to redo entire levels because of one weak skill.

### 4.5 Placement
- A new learner takes an **adaptive placement assessment** that climbs the level ladder.
- Start the learner **just below** the point where errors begin, so early sessions are confidence-building.
- Levels below the placement point are marked as skipped-by-placement (not "mastered by practice") and are eligible for retention review.
- Placement can be re-run by a parent. It never lowers an already-earned rank.

### 4.6 Regression and ranks
- **Ranks and pips are never taken away.** Faded skills trigger a refresher (Section 8), not a demotion.
- A learner may be stepped back to an earlier waypoint **within the current level** after repeated failure, as a teaching aid, not a penalty.

### 4.7 Frustration protection
- If accuracy drops sharply mid-session, ease to an easier set and end the session on a success.
- Never end a session on a failure screen.

---

## 5. Daily sessions ("flight simulator")

### 5.1 Purpose
The main learning activity. Calm, plain, timed drills. **No game complexity** in daily sessions.

### 5.2 Structure
- A fixed-size set of questions (size configurable, roughly 20 to 30).
- Mixes **new material** (current waypoint) with **review items** (Section 8).
- Questions come from deterministic, seeded generators so sessions are reproducible and testable.

### 5.3 Timing
- Each question has a **target response time** defined per level in `.kiro/steering/curriculum.md`.
- Response time is captured on the client and the answer is validated on the server.
- Exceeding target time is recorded; it does not block the learner from answering.

### 5.4 Self-correction
- A wrong answer is shown with the correct answer, and the same item (or an equivalent) is re-presented later in the session until answered correctly.
- Both the original error and the correction are logged.

### 5.5 Streaks and daily rhythm
- A day counts as practised when a minimum session is completed (threshold configurable).
- Missing a day reduces bonuses (Section 9) but never affects rank, pips or mastery state.

---

## 6. Asteroid-field assessments

### 6.1 Role
Asteroid fields are the **zone tests**. The game must be a valid measure of the same skills and thresholds as the plain drills. The game is the test, not decoration.

### 6.2 Core rules
- **Travel time equals target response time.** An asteroid's travel time is derived from the target response time of the skill it carries. An asteroid reaching the base means "too slow for automaticity".
- **Motor skill must not confound maths skill.** Do not require ship steering or precise aiming. Selection by tap or click on the asteroid, or by key, is sufficient.
- **No lives-based game over** in assessment rounds. A round always runs to completion so a full data set is collected.
- **Pass rule** is the same shape as everywhere else: accuracy threshold and median-time threshold, over the configured number of rounds, defined in `.kiro/steering/curriculum.md`.
- Errors include: wrong answer chosen or typed, shooting a correct asteroid in spot-the-error mode, failing to shoot an incorrect asteroid, and an asteroid reaching the base.
- Pace may adapt (speed up after streaks, ease after misses) but the **pace in effect must be recorded** with every event so results stay comparable.
- Each field includes a few **review items from earlier zones**.

### 6.3 Modes and escalation
Game modes increase in demand across zones (exact mapping in `.kiro/steering/curriculum.md`):
1. **Answer-asteroids**: the question is shown and asteroids carry candidate answers. Recognition.
2. **Answer-asteroids with diagnostic distractors**: distractors are drawn from the learner's own common wrong answers.
3. **Spot-the-error**: asteroids show equations, the learner shoots the incorrect ones.
4. **Typed answer**: each asteroid shows a question and the learner types the answer to destroy it. Recall.
5. **Final field**: fully typed, mixed operations, larger asteroids that split into smaller ones, with review items from all zones.

Recognition modes are easier than recall. Later zones must rely progressively on recall.

### 6.4 Practice field
- A **non-gated practice field** is available from early in the journey so the mechanic is familiar before any zone test.
- Practice results never affect progression.

### 6.5 Integrity
- The client reports per-item events; the **server recomputes** accuracy and speed from the event log and never trusts a client-side score.
- Validate that submitted answers correspond to the server-issued seeded questions and that timings are plausible. Light validation is sufficient; this is a learning tool, not a competitive one.

---

## 7. Event logging and analytics (required by the rules above)

Every attempt must be logged with at least:
- learner, question identifier and seed, level and waypoint
- the question presented, the answer given, correctness
- response time and the target time in effect
- mode (daily drill, level check, practice field, zone test, placement, repair mission)
- game pace in effect (for asteroid modes)
- timestamp

Uses:
- **Error patterns**: track repeated specific wrong answers (for example a consistent wrong product for the same fact). These drive diagnostic distractors and targeted repair missions.
- **Fluency tracking**: median response time per skill over time; automaticity appears as time dropping and stabilising.
- **Parent progress view** (Section 12).

---

## 8. Retention and review

- Mastered levels and skills resurface on an **expanding schedule** (Leitner or SM-2 style; the exact algorithm is an implementation choice but must be documented).
- Review items appear in daily sessions and as review asteroids in zone tests.
- If a reviewed skill has faded, assign a short **refresher mission**. Never remove a rank or pip.
- Skills skipped by placement are scheduled for review early to verify them.

---

## 9. Gamification and motivation

**Golden rule: rank is earned by mastery only, never by points.** Gamification state must never influence promotion logic. Keep gamification data in separate tables and separate code paths from mastery state.

| Element | Rule |
|---|---|
| **Rank** | Earned by passing a zone test. Never lost |
| **Pip** | Earned by passing a level check. Never lost |
| **Fuel (streaks)** | Charged by daily practice. A missed day lowers bonuses only |
| **Flight hours / XP** | Cosmetic currency for unlocking ship skins, cockpit panels, laser effects and uniform patches. Cannot buy progression |
| **Badges** | For habits and milestones (personal-best time, perfect round, consecutive days) |
| **Journey map** | Visible route across the solar system showing the ship's position |
| **Mission log** | Short story beat after each zone |

Design constraints:
- No public leaderboards, no learner-to-learner competition. Personal bests and streaks only.
- No loss-based mechanics (no losing ranks, items or streak-linked punishments).
- Do not use dark patterns (artificial scarcity, guilt messaging, manipulative timers) aimed at children or parents.
- Story and narration must stay light. Daily drills prioritise speed of access over story.

---

## 10. Theme and terminology

Use these terms consistently in UI, copy and code identifiers where user-facing:

| Concept | Term |
|---|---|
| Smallest step | Waypoint |
| Skill stage | Level |
| Group of levels | Zone |
| Daily practice | Flight simulator (session) |
| Level test | Level check |
| Zone test | Asteroid field |
| Remedial work | Repair mission |
| Review of old skills | Maintenance check / refresher mission |
| Streak currency | Fuel |
| Cosmetic currency | Flight hours |

Rank names and zone or location names are defined in `.kiro/steering/curriculum.md` and may change. They are data, not code constants.

Journey (default concept): Earth launch, Moon, Mars, belt approach, main asteroid belt, arrival at Jupiter. Theme names are flavour only and must be easy to rename.

---

## 11. Privacy, safety and compliance

- Children's data is sensitive. Collect only what is needed to run the learning programme (account email for the parent, learner first name or nickname, progress and event data).
- Do not collect or display a child's full name, location or photo.
- No advertising and no third-party trackers on learner-facing pages.
- No learner-to-learner communication and no user-generated content visible to other users.
- Parents can export and delete their learner's data.
- The product targets an Australian audience first; design with the Australian Privacy Act and the Australian Privacy Principles in mind, and treat any other jurisdiction's requirements as needing explicit review before launch there. This file is not legal advice.

---

## 12. Accessibility and inclusion

Requirements, not nice-to-haves:
- **Reduced-motion option** and no flashing content.
- **Adjustable game speed** for learners who need more time, with the adjusted pace recorded so results remain interpretable.
- **Colour-blind-safe design**: never use red and green alone to signal right and wrong.
- Keyboard-operable and tap-operable throughout; large, forgiving touch targets.
- Readable fonts, with a dyslexia-friendly font option and text-to-speech where practical.
- Plain, age-appropriate language.

---

## 13. Parent and teacher view

- Show: time practised, streak, current level and rank, recent accuracy and speed trends, and where the learner is currently stuck.
- Keep it simple. Avoid overwhelming detail; offer drill-down on request.
- Surface concrete, actionable summaries (for example "struggling with the 7 and 8 times tables") derived from error patterns.
- Parents can change accessibility settings and re-run placement.
- Parents cannot grant ranks or pips or skip mastery gates.

---

## 14. MVP scope

The first slice proves the core loop before anything else.

**In scope**
- Levels 1 to 4 (first zone) as defined in `.kiro/steering/curriculum.md`
- Seeded question generators for those levels
- Daily session with timing, accuracy, self-correction and event logging
- Mastery engine implementing Section 4 (pass rules, level check, no-loss progression)
- Asteroid field for zone 1 (answer-asteroids mode) with server-side validation
- Basic ranks and pips, minimal journey map
- Simple parent progress page

**Out of scope for MVP (build later, in roughly this order)**
1. Placement assessment
2. Retention and review scheduling
3. Remaining zones and game modes (spot-the-error, typed answers, splitting asteroids)
4. Repair missions
5. Cosmetics, badges and fuel refinements
6. Printable worksheets with answer keys
7. Teacher and class features

---

## 15. Engineering principles that follow from these rules

- **Curriculum is data.** Levels, waypoints, thresholds, target times, rank names and zone names live in curriculum data (see `.kiro/steering/curriculum.md`), not in application logic.
- **One mastery engine.** Daily drills, level checks, placement, repair missions and asteroid fields all feed the same attempt log and mastery logic. Delivery mode differs; the rules do not.
- **Determinism.** Question generation is seeded and reproducible. Tests can replay any session.
- **Server authority.** Scoring and mastery decisions happen on the server from the event log.
- **Separation of concerns.** Gamification state is isolated from mastery state and can never alter promotion.
- **Themeable.** Terminology and visuals are a skin, so renaming or re-theming does not touch the engine.
- **Testing.** Generators, pass rules and promotion logic need unit tests covering boundary cases (accuracy just under or over threshold, fast but sloppy, accurate but slow, consecutive-session counting).

---

## 16. Open questions (decide and record here as they are settled)

- Target age range and the lowest level a new young learner should reach on day one
- Exact daily-practice minimum and session length defaults
- Monetisation model (individual subscription, school licence, free)
- Whether teacher and class features enter the first release
- Final rank and zone names
