---
id: P1-021
title: "Prerequisite graph and DAG validation"
milestone: M2
type: curriculum
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-020]
estimate: 1
outputs:
  - curriculum/concepts.yaml
  - curriculum/graph.md
---

## Context

Prerequisites determine unlock order in the app (skill tree).

## Tasks

1. Fill `prerequisites` as minimally as possible.
2. Make sure the validator detects cycles and unknown ids.
3. Generate a Mermaid diagram of the graph into `curriculum/graph.md` (a script is fine).

## Done criteria

- [x] Graph has no cycles
- [x] No orphan concept that cannot be reached
- [x] `python scripts/validate.py` passes

## Notes

2026-11-13: Filled `prerequisites` for all 50 concepts: one root (`request-lifecycle`), 84 edges after review, no cycles. The P1-020 ordering hints are all satisfied. `scripts/graph.py` generates `curriculum/graph.md` (Mermaid plus a depth-ordered study list); `validate.py` fails if it is stale. New validator rules: prerequisite in a later unit (error), prerequisites not a list or with duplicates (error), no prerequisites in units 1-6 (warning, error at review/published), redundant transitive edge (warning). 45 tests pass.

`content-reviewer` passed with minor fixes. Applied: 16 added or changed edges where a lesson uses another concept's vocabulary (for example `locks-leases-fencing` -> `idempotency`, `transactions-acid`; `timeouts` -> `percentiles-tail-latency`; `event-log-streaming` -> `partitioning-sharding`), test-file `__main__` placement, graph.py/validator consistency, list and duplicate checks, more tests. Decision: triggers are not prerequisites (see `curriculum/README.md`), so `replication` and `partitioning-sharding` do not require `capacity-headroom` or `caching-basics`. Not rendered in a Mermaid viewer. For P1-023/P1-024: the owner may want to confirm that `event-log-streaming` should require `partitioning-sharding`.
