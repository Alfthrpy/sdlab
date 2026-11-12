---
id: P1-060
title: "Citation and dead-link audit"
milestone: M5
type: review
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-040, P1-041, P1-042, P1-043, P1-044, P1-045, P1-048]
estimate: 1
outputs:
  - references/registry.yaml
  - docs/audit-citations.md
---

## Context

Before the freeze, make sure all references are valid.

## Tasks

1. Check that every URL in the registry is still alive; fix/replace.
2. Check that all published content cites only approved sources.

## Done criteria

- [ ] Audit report in `docs/audit-citations.md`
- [ ] No unhandled dead links
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
