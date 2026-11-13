---
id: P1-076
title: "Close Unit 5-6 source gaps: vector clocks, Zab, TrueTime, SLO alerting, tracing"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: []
estimate: 1
outputs: []
---

## Context

Gap items B9 and B12 in `references/coverage.md`. B11 (reading `tail-at-scale-cacm13` in full) is blocked for agents and stays with the owner. B12: drop adaptive concurrency from v1.

## Tasks

1. B9: find sources for vector clocks, Zab, and TrueTime detail; read the Jepsen model pages used by Unit 5.
2. B12: find beginner SLO-based alerting, SRE book tracing/release-engineering chapters; read `dapper-2010` in full.
3. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
