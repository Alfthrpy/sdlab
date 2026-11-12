---
id: P1-069
title: "Research candidate sources — Unit 0 (single-server backend)"
milestone: M1
type: research
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-010, P1-068]
estimate: 1
outputs: []
---

## Context

Fill the Reference Registry for Unit 0: Single-server backend (the request lifecycle on one machine, one app plus one database, indexes and query basics, connection pooling, backups and recovery basics, simple deploys, basic monitoring, and the limits of one machine). Added by ADR 0004 Amendment 1. Sources for 'start small' material are scarcer at Tier 1–3, so look for them deliberately: official database and web-server documentation, operations and reliability chapters, and engineering articles about scaling from one server. Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the sub-topic list from the Unit 0 row in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml` with `units: [0]` (or including 0).
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [ ] ≥ 12 candidates for this unit, all opened in the session
- [ ] Every sub-topic has ≥ 1 Tier 1–3 source or official documentation, or is recorded as a gap
- [ ] Reading notes for the 3–5 main sources
- [ ] `source-verifier` says pass
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
