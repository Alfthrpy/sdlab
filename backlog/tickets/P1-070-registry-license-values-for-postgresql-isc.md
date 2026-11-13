---
id: P1-070
title: "Registry: license values for PostgreSQL/ISC/CC-BY-SA-2.5 and a tier for official docs"
milestone: M1
type: infra
owner: agent
review: agent
status: done
priority: medium
depends_on: [P1-010]
estimate: 1
outputs: []
---

## Context

Found in P1-069. Several clearly open sources cannot be recorded accurately: the `license` enum has no value for the PostgreSQL License (PostgreSQL docs), ISC (PgBouncer software), or CC-BY-SA 2.5-or-later (MDN text), so they are stored as `unknown` with the real license in `notes`. Official documentation also has no tier in the tier table in `research-protocol.md`; P1-069 (and the Jepsen seed) put it in Tier 2 by convention. Both need fixing before P1-016 verifies licenses, otherwise `unknown` blocks approval of these sources.

## Tasks

1. Decide which license values to add (for example `PostgreSQL`, `ISC`, `CC-BY-SA-2.5`) and whether `usage: adapt-with-attribution` is allowed for them (extend `OPEN_LICENSES` only for genuinely permissive ones).
2. Update `LICENSES`/`OPEN_LICENSES` in `scripts/validate.py`, `docs/conventions/content-schema.md` §1, `templates/source-entry.yaml`, and `tests/test_registry.py`.
3. Add official documentation to the tier table in `docs/conventions/research-protocol.md` (state the Tier it belongs to and when a docs page is Tier 2 vs something else).
4. Update the registry entries that currently say `unknown` for these reasons (only where the notes already record the verified license).

## Done criteria

- [x] New license values documented, validated, and tested
- [x] Tier table covers official documentation
- [x] Registry entries updated where the verified license is now expressible
- [x] `python scripts/validate.py` passes

## Notes

Entries affected so far: pg-docs-* (PostgreSQL License), pgbouncer-features (ISC for the software), mdn-http-overview (CC-BY-SA 2.5+), hikaricp-about-pool-sizing (Apache-2.0 repo, wiki unspecified).

Done 2026-11-12: added `PostgreSQL`, `ISC`, `CC-BY-SA-2.5`, `CC-BY-3.0` (all in `OPEN_LICENSES`; CC-BY-3.0 added because Debezium/Raft/Kleppmann entries hit the same gap). Official docs = Tier 2 (rules in research-protocol.md). Switched 13 pg-docs-*, 3 MDN, 4 CC-BY-3.0 entries. Left `unknown`: pgbouncer-features (ISC covers software only), hikaricp-about-pool-sizing, debezium-docs-outbox-event-router (no license on page). ADR 0002 rule 5 updated to match the validator. Reviewed by source-verifier; its findings were fixed.

2026-11-13: Status was left at in-progress after PR #14 merged; all done criteria were already met, so only the status is changed here. `license: unknown` now appears in no registry entry.
