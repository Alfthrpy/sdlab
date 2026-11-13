---
id: P1-077
title: "Pin moving registry URLs (Cassandra, ZooKeeper, Redis, IETF draft)"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: low
depends_on: []
estimate: 1
outputs: []
---

## Context

Gap item C4 in `references/coverage.md`: Cassandra `/latest/`, ZooKeeper `/current/`, Redis `/latest/` change over time, and the IETF idempotency-key draft is an active Internet-Draft.

## Tasks

1. For each entry, set `version` and/or `archive_url` so the cited page is reproducible.
2. Record the current draft revision for the IETF idempotency-key entry.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
