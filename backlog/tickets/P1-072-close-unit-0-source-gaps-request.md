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

- [x] Every task above is done or recorded as a gap with a proposed action
- [x] `python scripts/validate.py` passes

## Notes

Per gap (all entries are `candidate`, `verified_on` empty, opened 2026-11-16):

- A1: GAP, propose **accept** (write from `mdn-http-overview` plus own diagram). Opened and rejected: alex/what-happens-when (CC0 per README, but not beginner and no database stage); MDN "How the web works" (no TLS, no database); dev.to articles by Shefali and Onuiteshi, a Rails post by Margheim, and an anonymous study guide (david-marin-0xff.github.io) - no license, weak authority, and at most a one-line database mention. DigitalOcean tutorials returned only navigation, not body text.
- A2: `google-sre-book-data-integrity-ch26` (Tier 1, CC BY-NC-ND 4.0, with notes). Fits; Google-scale parts are to be skipped.
- A11: partial, `capistrano-docs-rollbacks` (Tier 2, no license stated, with notes). Covers release dirs, symlink switch, rollback, and the migration caveat. Propose **accept** for the rest (systemd restart, expand/contract migrations) from `systemd-service-man`, `fowler-bluegreen-deployment`, and the migration entries.
- A12: `owasp-logging-cheat-sheet` (Tier 2, CC BY-SA 4.0, with notes). Security-leaning; acceptable for what/levels/structure/correlation id. Fallback SRE monitoring ch. 6 stays for the operations angle.
- A13: `aws-startups-scaling-part1-primer` and `aws-startups-scaling-part2-10k-users` (Tier 2, AWS blog, 2015, all rights reserved). Single-server start, then triggers for each step. Vendor-specific and dated; use for the ladder logic. No reading notes written. Rejected: scaledojo.dev (commercial, no license), Alex Pareto post (403).

Verification (source-verifier, all 5 reopened): pass; metadata and licenses match the pages. Open doubts: the footer of `aws-startups-scaling-part1-primer` was not visible (`all-rights-reserved` is the protocol fallback; check it in a browser before approval); the two AWS entries have no reading notes. SRE chapter `published` is the 2017 copyright year. Entries stay `candidate`; the owner approves them later.
