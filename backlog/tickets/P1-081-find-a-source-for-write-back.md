---
id: P1-081
title: "Find a source for write-back/write-behind caching (caching-basics objective 1)"
milestone: M3
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: []
estimate: 1
outputs:
  - references/registry.yaml
---

## Context

Found in the P1-032 pilot. Objective 1 of `caching-basics` says "kapan cache-aside lebih cocok daripada write-through atau write-back". The four approved sources only mention write-behind in one Azure sentence and say nothing about its trade-offs (risk of losing writes not yet flushed, ordering, batching). The pilot lesson introduces write-behind in one cited sentence and says its trade-offs come later, so objective 1 is only partly met.

## Tasks

1. Find a free, authoritative source on write-back / write-behind caching and its trade-offs (candidates: a vendor docs page, the Azure write-behind or caching guidance, a database/caching engineering article, an operator write-up). Open it before recording; follow `docs/conventions/research-protocol.md`.
2. Register it as `candidate`; the owner approves it later.
3. If nothing suitable exists, propose to the owner to amend objective 1 (drop "write-back") through the curriculum-edit path instead of leaving the gap silent.

## Done criteria

- [ ] One candidate source for write-back, or a documented gap with a proposed action
- [ ] After approval, `caching-basics` is updated (lesson, a question, the lab) and the source added to its `sources`
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
