---
id: P1-079
title: "Add approved P1-072/P1-078 sources to concepts"
milestone: M2
type: curriculum
owner: agent
review: agent
status: in-progress
priority: medium
depends_on: []
estimate: 1
outputs:
  - curriculum/concepts.yaml
---

## Context

P1-072 and P1-078 registered `candidate` sources for thin concepts. Only `approved` sources may be cited, and the owner approves them. Do this ticket after that approval. It needs the owner to approve (or reject) the candidates first, so do not start it before then.

## Tasks

1. List which P1-072 and P1-078 candidates are now `approved`.
2. Add each to `sources` of the concepts named in the P1-072 and P1-078 ticket Notes (backup-recovery, simple-deploys, basic-monitoring, app-plus-database, single-machine-limits; rate-limiting, dns-networking-basics, distributed-transactions, back-of-envelope-estimation, stateless-services-sessions, transactions-acid, capacity-headroom, observability).
3. Update `references/coverage.md` gap rows to match, and re-run the graph and validator.

## Done criteria

- [ ] Every approved candidate is mapped to its concept(s)
- [ ] Gaps still open (A1, TTL, 2PC, sticky sessions, headroom formula, beginner estimation) are listed in the ticket Notes
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
