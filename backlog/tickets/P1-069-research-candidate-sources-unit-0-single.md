---
id: P1-069
title: "Research candidate sources — Unit 0 (single-server backend)"
milestone: M1
type: research
owner: agent
review: agent
status: review
priority: high
depends_on: [P1-010, P1-068]
estimate: 1
outputs: []
---

## Context

Fill the Reference Registry for Unit 0: Single-server backend (the request lifecycle on one machine, one app plus one database, indexes and query basics, connection pooling, backups and recovery basics, simple deploys, basic monitoring, and the limits of one machine). Added by ADR 0004 Amendment 1. Sources for 'start small' material are scarcer at Tier 1–3, so look for them deliberately: official database and web-server documentation, operations and reliability chapters, and engineering articles about scaling from one server. Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the sub-topic list from the Unit 0 row in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml` with `units: [0]` (or including 0).
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [x] ≥ 12 candidates for this unit, all opened in the session
- [x] Every sub-topic has ≥ 1 Tier 1–3 source or official documentation, or is recorded as a gap
- [x] Reading notes for the 3–5 main sources
- [x] `source-verifier` says pass
- [x] `python scripts/validate.py` passes

## Notes

- Added 22 Unit 0 candidates (1 later swapped), all opened in the session; every sub-topic has at least one official-documentation or Tier 1–2 source. Reading notes: pg-docs-backup-restore, pg-docs-using-explain, pg-docs-kernel-resources, pg-docs-indexes-intro, aws-builders-implementing-health-checks.
- First `source-verifier` pass: FAIL (fixable). Fixed after reopening each page: SQLite license -> public-domain; use-the-index-luke tier 1 -> 2; third-party Stack Overflow summary removed and replaced by the author's own blog post (`craver-stack-overflow-architecture-2016`); wrong section numbers in two notes; unsupported claims in the AWS health-check note; 12-factor license set to `unknown` (site says all rights reserved, repo says MIT); MySQL/MDN/PostgreSQL license notes.
- No Tier 3–6 sources: not expected for Unit 0 (official docs and practitioner articles). Tier 1 is only the SRE book chapter.
- **Gaps:** backup schedules, off-machine storage, restore drills (only the mechanics are covered); a deploy procedure for one box (rolling a version, migrations, rollback); a dedicated logging source (only 12-factor's factor list); a source that follows one request end to end (DNS, TCP, web server, app, database); a primary engineering article on scaling from one server; a Tier 1 book chapter written for beginners; the nginx.org beginner's guide could not be opened.
- **Doubts for P1-016:** the Stack Overflow 2016 post was only partly read and is not single-server; the MySQL manual is all-rights-reserved and 8.4 is not the page's "current" series (9.x is); `verified_on` is empty on every entry on purpose.
- Follow-up: P1-070 (license values and a tier for official docs).
