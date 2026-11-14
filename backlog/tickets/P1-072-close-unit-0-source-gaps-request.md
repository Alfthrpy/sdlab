---
id: P1-072
title: "Close Unit 0 source gaps: request lifecycle, backups, deploy, logging, scaling"
milestone: M1
type: research
owner: agent
review: agent
status: done
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

- [x] Every task above is done or recorded as a gap with a proposed action (A2 and A12 closed; A1, A11, A13 partly or not closed, with accept proposals below)
- [x] `python scripts/validate.py` passes

## Notes

Six new `candidate` entries in `references/registry.yaml`, all opened on 2026-11-14 and reopened by `source-verifier` (no entry rejected; fixes applied).

| Gap | Result | Entry |
| --- | --- | --- |
| A1 request end to end | **Partly closed.** Client side (URL, DNS, TCP, TLS, HTTP, web server) is covered; no source follows the request into the database. Proposal: **accept**, write the server-to-database half from `mdn-http-overview`, `nginx-reverse-proxy-admin-guide`, `pg-docs-connections` and an own diagram. | `aws-blog-what-happens-type-url` (T2, author Jenna Pederson, body vs byline conflict noted), `what-happens-when-repo` (T5, CC0 recorded as public-domain; community-edited, cross-check before use) |
| A2 backups | **Closed.** Off-site copies, restore drills, replication is not a backup. Written for Google scale, so use the principles only. | `sre-book-data-integrity-ch26` (T1, CC BY-NC-ND 4.0) |
| A11 one-box deploy | **Partly closed.** Schema changes (expand, migrate, contract) only; no rollback or one-server procedure. Proposal: **accept**, use `fowler-bluegreen-deployment`, `systemd-service-man`, `twelve-factor-app`. | `fowler-parallel-change` (T2) |
| A12 logging | **Closed, with limits.** Vendor-neutral baseline (what to log, attributes, data to exclude); security-focused, Java-specific in one section. Proposal: **accept** with `google-sre-book-monitoring-ch6` and `twelve-factor-app` for the operational side. | `owasp-logging-cheat-sheet` (T5, CC BY-SA 4.0; adapted text must stay CC BY-SA) |
| A13 scaling from one server | **Not closed.** The only readable candidate is an interview-prep newsletter article (stages 1-2 free, rest paywalled), so it is Tier 6 `map-only` and not citable. Proposal: **accept**, teach it from `craver-stack-overflow-architecture-2016`, `gregg-use-method`, `sqlite-appropriate-uses`, plus the course's own growth-ladder framing. | `algomaster-scaling-0-to-10m-users` (T6, map-only) |

- Verifier fixes applied: AlgoMaster tier 2 -> 6 / map-only; OWASP tier 2 -> 5 with a rationale and corrected notes (it has a severity scale and runtime level changes; Java-specific advice exists); AWS author set to Jenna Pederson; PHP and community-edited caveats on `what-happens-when-repo`; canary/blue-green mention on `fowler-parallel-change`.
- Not done: no entry is `approved` yet (candidates need P1-016-style verification and, for the CC BY-SA and CC0 entries, an attribution check). `curriculum/concepts.yaml` and `references/coverage.md` were not changed; the owner should confirm the accept proposals at G0/G1, and a follow-up can map `sre-book-data-integrity-ch26` to `backup-recovery` and `owasp-logging-cheat-sheet` to `basic-monitoring` once approved.
- No ticket created: the A1, A11 and A13 gaps are proposed as accept (PLAN scope note: Unit 0 may rely on official docs).
