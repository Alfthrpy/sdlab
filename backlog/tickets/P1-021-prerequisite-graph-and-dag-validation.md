---
id: P1-021
title: "Prerequisite graph and DAG validation"
milestone: M2
type: curriculum
owner: agent
review: agent
status: in-progress
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

- [ ] Graph has no cycles
- [ ] No orphan concept that cannot be reached
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
