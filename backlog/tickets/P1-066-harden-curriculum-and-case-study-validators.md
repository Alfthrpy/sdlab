---
id: P1-066
title: "Harden curriculum and case-study validators against malformed YAML"
milestone: M1
type: infra
owner: agent
review: agent
status: todo
priority: low
depends_on: []
estimate: 1
outputs: []
---

## Context

Found by the P1-010 review: `check_curriculum` and the case-studies loop in `scripts/validate.py` call `.get` on entries without checking they are mappings, so malformed YAML crashes with a traceback instead of a clear error. The registry check was already hardened in P1-010.

## Tasks

1. Check root and entry types in `check_curriculum` and the case-studies loop; emit `err(...)` and skip bad entries.
2. Check list-typed fields (`objectives`, `prerequisites`, `sources`, `concepts`) are lists of strings before cross-checking.
3. Add fixture tests in `tests/` like `tests/test_registry.py`.

## Done criteria

- [ ] Malformed curriculum YAML gives clear errors, no traceback
- [ ] Fixture tests cover the new checks
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
