---
id: P1-068
title: "Define the growth-ladder framing and the single-server starting unit"
milestone: M1
type: curriculum
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-010]
estimate: 1
outputs:
  - curriculum/README.md
  - docs/PLAN-PHASE-1.md
  - docs/ROADMAP.md
  - docs/conventions/content-schema.md
  - scripts/validate.py
---

## Context

ADR 0004 Amendment 1 extends the audience to solo developers and beginners and reframes the course as a growth ladder: start from a single-server backend and add each distributed-systems concept when the previous stage stops being enough. The unit table in `curriculum/README.md` and the research tickets (P1-011 to P1-015) assume the old framing, so the new starting unit and the framing must be defined before research runs.

## Tasks

1. Define the new starting unit (single-server backend): name, core concepts (e.g. one database, indexes, connection pooling, backups, deploys, basic monitoring), and what it must not assume beyond the reader prerequisites in `curriculum/README.md`.
2. Decide the numbering. The validator and docs currently accept units 1–6 (`scripts/validate.py`, `content-schema.md`, `templates/source-entry.yaml`, `PLAN-PHASE-1.md` M4 order). Pick the least disruptive option (e.g. add a Unit 0, or renumber) and apply it consistently, including the validator range and its fixture tests.
3. Add the growth-ladder framing to `curriculum/README.md` and decide how each concept records its "trigger" (the symptom or number that says it is time to use it). If it needs a schema field (e.g. `trigger` in `concepts.yaml`), add it to `content-schema.md` §2 and the validator.
4. Re-estimate scope and duration in `docs/PLAN-PHASE-1.md` (concept count, M4 order, ±22 weeks), and mention the audience extension in `AGENTS.md`, `docs/ROADMAP.md`, and the curriculum-designer subagent.
5. Update the research tickets (P1-011 to P1-015) so the new unit and "start small" sources are covered; if needed, split or re-scope them.

## Done criteria

- [x] New unit defined (name, concepts, assumptions) in `curriculum/README.md`
- [x] Unit numbering applied consistently in docs, validator, and tests
- [x] Trigger convention documented (and validated if it is a schema field)
- [x] `docs/PLAN-PHASE-1.md` has the re-estimated scope
- [x] Audience extension appears in AGENTS.md, ROADMAP.md, and the curriculum-designer subagent
- [x] Research tickets reflect the new unit
- [x] `python scripts/validate.py` passes

## Notes

- **Numbering:** the new starting unit is **Unit 0** (single-server backend), so existing unit numbers 1–6, ticket ids P1-040–P1-045, and registry seeds are untouched. Validator ranges are now 0–6 for `units` (registry) and `unit` (concepts); `tier` stays 1–6.
- **Unit 0 scope:** request lifecycle, one app + one database, indexes and query basics, connection pooling, backups and recovery basics, simple deploys, basic monitoring, and the limits of one machine. **Unit 1** (Foundations) now also covers how to measure whether a stage is still enough.
- **Trigger:** new `trigger` field on concepts (Indonesian string). Units 1–6: warning until status `review`, then an error; Unit 0: optional. Documented in `content-schema.md` §2 and `curriculum/README.md`; tested in `tests/test_curriculum.py`.
- **Re-estimate:** ~40 → ~46 concepts, 300 → ~340 questions, 15 → 16 lab specs, 22 → 24 weeks (M4 weeks 8–24). Rough figures; revisit at G1.
- **Tickets:** new P1-069 (research Unit 0) and P1-048 (epic Unit 0). P1-016 now depends on P1-069; P1-060/061/062 depend on P1-048; P1-020 targets 40–50 concepts incl. triggers. P1-011–P1-015 already depended on P1-068.
- The lesson-level writing style (first-principles framing) is intentionally NOT decided here, at the owner's request; only the trigger requirement was added to writing-style.md. The owner will say when to add it to P1-031.
- P1-066 (hardening the curriculum validators) is still open; the new trigger and unit checks sit inside `check_curriculum`, so that ticket should keep their tests.
- Review: `content-reviewer` said pass with minor fixes; fixed the misplaced first-principles note, M2/M3 week ranges, the ticket-count cell, the Unit 0 trigger exemption in the ADR, and added validator tests.
