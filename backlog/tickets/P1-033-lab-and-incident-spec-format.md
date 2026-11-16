---
id: P1-033
title: "Lab and incident spec format"
milestone: M3
type: infra
owner: agent
review: agent
status: done
priority: medium
depends_on: [P1-024]
estimate: 1
outputs:
  - docs/conventions/content-schema.md
  - templates/concept/lab.yaml
  - templates/incident.md
---

## Context

Lab specs are written in Phase 1 and read by the simulator in Phase 2. The format must be fairly neutral toward the simulator implementation.

## Tasks

1. Define the `lab.yaml` schema: goal, initial architecture (components + connections), load/traffic, failure scenarios, metric targets, structural rules, hints.
2. Define the incident template (see content-schema §5).
3. Add basic validation.

## Done criteria

- [x] Lab & incident schema documented
- [x] Templates available
- [x] `python scripts/validate.py` passes

## Notes

- Format follows the STUD Simulator Master Plan (Claude Docs): lab spec fields (section 6.1), validation rules C01-C14 and anti-leak A1-A5. `content-schema.md` sections 5-7 hold the final lab and incident format; templates are `templates/concept/lab.yaml` and `templates/incident.md`.
- Validator (`scripts/validate.py`, `check_labs`): enforces everything that needs no simulator catalog, and reports invalid YAML, wrong types and unknown fields as errors (a catch-all turns any other surprise into an error line, never a traceback). Tests: 156 pass (`tests/test_labs.py` has 52 of them).
- Review (general-purpose agent, independent): fixed the crashes on wrong-typed fields, unknown fields now rejected, non-numeric edit values rejected, anti-leak now reads Indonesian numbers and units, incident `sim_spec` must be a diagnose-mode `.lab.yaml` under `content/incidents/` and its scenarios must match. Deliberate differences from the plan and what is not specified or checked yet are written in section 5 ("Deliberate differences", "Not yet specified", "Not checked yet").
- To feed back into the master plan (stud-sim): `brute_force: true` on wrong answers; `feedback_pass`/`feedback_fail` on structural rules; the plan's example omits both. The catalog-dependent rules (C01-C04, C10, C11) wait for `contracts/sim/` to be vendored.
- Pilot lab: `content/concepts/caching-basics/lab.yaml` was a draft with invented fields and invalid YAML; it now uses the plan's example lab. Cost: it practises objectives 2 and 3 only; the earlier draft's write path, invalidation order and staleness metrics (objective 1) need a second lab. Also, TTL has no cost in this lab (a longer TTL is never penalised), so it cannot teach the staleness trade-off yet. The lab shares two numbers with the lesson (20 ms read time, 20 as a capacity value) and the 30 s initial TTL with a quiz question; these are initial or lesson values, not reference values, but the content-reviewer should look at rule A5.
- Out-of-scope fixes: the stale templates `lesson.md`, `misconceptions.md`, `questions.yaml` now match the P1-030 schema (draft status, `Kenapa keliru`, `objective`).
- Stacked on the P1-032 branch (PR #44) because the pilot lab had to be converted; merge #44 first.
