---
id: P1-033
title: "Lab and incident spec format"
milestone: M3
type: infra
owner: agent
review: agent
status: todo
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

- [ ] Lab & incident schema documented
- [ ] Templates available
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
