---
id: P1-075
title: "Close Unit 4 source gaps: log streaming, backpressure, ordering, consumer lag"
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

Gap items A9, A10, B7, B8 in `references/coverage.md`. `reactive-manifesto` must not be counted as backpressure coverage.

## Tasks

1. A9: find a working URL for Kreps "The Log" and check whether the Kafka design docs cover retention and compaction.
2. A10: find one source on bounded queues and flow control between services.
3. B7: find a free primary source on ordering guarantees (per partition vs total).
4. B8: find a queue-age or consumer-lag monitoring source.
5. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
