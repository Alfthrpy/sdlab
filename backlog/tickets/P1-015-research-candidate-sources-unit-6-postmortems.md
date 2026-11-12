---
id: P1-015
title: "Research candidate sources — Unit 6 + postmortems"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-010, P1-068]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Context

Fill the Reference Registry for Unit 6: Production reliability (timeout, retry/backoff/jitter, circuit breaker, load shedding, cascading & metastable failure, observability, safe deploys). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Collect ≥ 12 official postmortems (varied companies and failure mechanisms; prioritize 2023–2026) as material for the incident pack.
4. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
5. Write reading notes for the 3–5 most important sources.
6. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [ ] ≥ 15 candidates + ≥ 12 postmortems for this unit, all opened in the session
- [ ] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [ ] Reading notes for the 3–5 main sources
- [ ] `source-verifier` says pass
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
