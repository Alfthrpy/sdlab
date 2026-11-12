---
id: P1-068
title: "Define the growth-ladder framing and the single-server starting unit"
milestone: M1
type: curriculum
owner: agent
review: agent
status: todo
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

- [ ] New unit defined (name, concepts, assumptions) in `curriculum/README.md`
- [ ] Unit numbering applied consistently in docs, validator, and tests
- [ ] Trigger convention documented (and validated if it is a schema field)
- [ ] `docs/PLAN-PHASE-1.md` has the re-estimated scope
- [ ] Audience extension appears in AGENTS.md, ROADMAP.md, and the curriculum-designer subagent
- [ ] Research tickets reflect the new unit
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
