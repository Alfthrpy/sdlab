---
id: P1-022
title: "Choose case studies and incidents"
milestone: M2
type: curriculum
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-020]
estimate: 1
outputs:
  - curriculum/case-studies.yaml
---

## Context

Target: ~12 case studies (common interview-style questions) and ~12 incident candidates, to pick 6 and 8 from in M4.

## Tasks

1. Choose case studies that cover all units (check coverage via Tier 6).
2. Choose incidents from postmortems in the registry: varied mechanisms (retry storm, config push, DNS, overload, data corruption, dependency).
3. Map each item to the concepts it practices.

## Done criteria

- [ ] Every unit is practiced by ≥ 2 items
- [ ] Every incident has an official postmortem in the registry
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
