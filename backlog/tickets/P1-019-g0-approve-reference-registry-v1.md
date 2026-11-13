---
id: P1-019
title: "G0 — Approve Reference Registry v1"
milestone: M1
type: review
owner: human
review: human
status: todo
priority: high
depends_on: [P1-016, P1-017, P1-018, P1-072, P1-073, P1-074, P1-075, P1-076, P1-077]
estimate: 1
outputs:
  - references/registry.yaml
---

## Context

Gate G0. The agent has prepared the registry, coverage, and gap list. The owner decides whether it is enough to start the curriculum.

## Tasks

1. Read `references/coverage.md` (a ready-to-decide summary is prepared by the agent in the Notes section).
2. Decide: approve, or ask for more research on specific gaps.
3. After approval, the agent changes the status of the chosen sources to `approved`. The validator requires `verified_on` (and `attribution` for adapt-with-attribution sources) on each of them.

## Done criteria

- [ ] Owner decision recorded
- [ ] Every unit has ≥ 1 approved Tier 1–2 source and ≥ 1 approved Tier 3–4

## Notes

(Filled in during the work.)
