---
id: P1-074
title: "Close Unit 3 source gaps: replication, isolation, sharding and LSM depth"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: []
estimate: 2
outputs: []
---

## Context

Gap items A7, A8, B5 in `references/coverage.md`. `ddia-2e` is paywalled, so Unit 3 concepts lean on few free sources.

## Tasks

1. A7: find an operator source on failover and replication lag, and a free multi-leader source.
2. A8: find one free explainer on isolation levels and anomalies; re-read `berenson-critique-ansi-isolation-1995` in full.
3. B5: find a production sharding case beyond Notion and a modern write-amplification (LSM vs B-tree) source.
4. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
