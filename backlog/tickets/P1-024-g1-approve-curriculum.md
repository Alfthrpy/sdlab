---
id: P1-024
title: "G1 — Approve curriculum"
milestone: M2
type: review
owner: human
review: human
status: done
priority: high
depends_on: [P1-021, P1-022, P1-023, P1-002]
estimate: 1
outputs:
  - curriculum/
---

## Context

Gate G1. The agent prepares a summary: concept list per unit, graph, case studies, and design decisions the owner should look at.

## Tasks

1. Read the summary in the Notes section and `curriculum/graph.md`.
2. Approve or request changes (add/remove/merge concepts).

## Done criteria

- [x] Decision recorded
- [x] Curriculum is marked version `curriculum-v1` (Git tag)

## Notes

**Decision (owner, 2026-11-16, in chat): G1 approved.** The owner checked the curriculum and said it is safe.

Summary prepared for the gate:
- 50 concepts: Unit 0: 8, Unit 1: 6, Unit 2: 9, Unit 3: 8, Unit 4: 5, Unit 5: 6, Unit 6: 8. 84 prerequisite edges, one root (`request-lifecycle`), no cycles, longest chain 8 (`curriculum/graph.md`).
- Every concept has 2 or more approved sources (min 2, average 4.6), a trigger for Units 1-6, and 1-4 Indonesian objectives.
- 12 case studies and 12 incidents (`curriculum/case-studies.yaml`); every unit is practiced by at least 3 items. Incident mix leans on deploy/config mechanisms; known gaps are in the file header.
- Git tag `curriculum-v1` marks the approved state (commit feeade6, `main` after PR #40).

Carried over (not blocking G1): the `capacity-headroom` trigger quotes 70-80% with no source; `request-lifecycle`, `distributed-transactions` (2PC coordinator), DNS TTL are thin on sources (see P1-079 Notes and `references/coverage.md`); B11 (`tail-at-scale-cacm13` full read) is the owner's.
