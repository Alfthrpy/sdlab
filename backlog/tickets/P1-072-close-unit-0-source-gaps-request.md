---
id: P1-072
title: "Close Unit 0 source gaps: request lifecycle, backups, deploy, logging, scaling"
milestone: M1
type: research
owner: agent
review: agent
status: in-progress
priority: medium
depends_on: []
estimate: 2
outputs: []
---

## Context

Gap items A1, A2, A11, A12, A13 in `references/coverage.md` (Unit 0 has the thinnest concept sources). Accept fallbacks are allowed per the PLAN scope note.

## Tasks

1. A1: find one free article that follows a request end to end (DNS to database).
2. A2: find one operator-practice source on backup policy, off-machine copies, and restore drills.
3. A11: find a source for a one-box deploy procedure (rolling a version, migrations, rollback).
4. A12: find vendor-neutral logging guidance.
5. A13: find one practitioner article on scaling from one server.
6. Add each source to the registry as `candidate` with `verified_on`, only from pages opened in this session. If nothing suitable exists, write the gap down and propose `accept`.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
