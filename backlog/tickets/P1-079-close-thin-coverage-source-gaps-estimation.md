---
id: P1-079
title: "Close thin-coverage source gaps: estimation, ACID, hot keys, sessions, headroom"
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

Found in the P1-023 review. These concepts are mapped, but their sources are thin, abstract-only, or do not cover every objective, and no existing gap ticket (P1-072 to P1-078) covers them:

- `back-of-envelope-estimation`: only `dean-software-engineering-advice-slides` (image-only PDF, license unknown) and a partial `brooker-telling-stories-littles-law`; nothing teaches QPS, storage, or bandwidth estimation (coverage.md B1).
- `transactions-acid`: `pg-docs-mvcc-intro` is a short intro and `pg-docs-transaction-iso` covers isolation only; nothing on atomicity or durability (WAL).
- `cache-stampede-hot-keys`: no read source for the hot-key objective; `nishtala-memcache-nsdi13` was read at abstract level only.
- `stateless-services-sessions`: no source compares signed-cookie, shared-store, and sticky sessions; `twelve-factor-app` has only the factor list read.
- `capacity-headroom`: no source on computing headroom from load-test data.
- `app-plus-database`: `craver-stack-overflow-architecture-2016` is not single-server and is flagged "read fully before approval"; no source for sizing users and RPS.
- Abstract-only sources with no ticket: `nishtala-memcache-nsdi13`, `tene-how-not-to-measure-latency`, `flp-impossibility-1985`.

## Tasks

1. For each concept above, find one or two free sources that cover the missing objective, or record a gap with a proposed action (accept, merge, drop).
2. Read the three abstract-only sources in full and update their registry notes.
3. Register new sources as `candidate` with `verified_on`. Do not edit `curriculum/concepts.yaml`; a follow-up updates the mapping once sources are approved.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
