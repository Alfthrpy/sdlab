---
id: P1-067
title: "Add optional registry fields: version, archive_url, attribution, lang, verified_on"
milestone: M1
type: infra
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-010]
estimate: 1
outputs: []
---

## Context

Found by the P1-010 review. The schema is declared final, but some fields are cheap to add now and expensive to backfill after P1-011–P1-015 add ~100 entries: `version` (commit hash or docs version; `edition` is documented for books only), `archive_url` (Wayback link against link rot), `attribution` (ready-made credit line for `adapt-with-attribution` sources), `lang` (`en` or `id`), `verified_on` (date the `source-verifier` checked it). Decide which are worth having, then add them before M1 research runs in full.

## Tasks

1. Decide which fields to add (some may be dropped).
2. Add them to the validator (`KNOWN_FIELDS`), `docs/conventions/content-schema.md` §1, `templates/source-entry.yaml`, and `tests/test_registry.py`.
3. Say in `research-protocol.md` when each field must be filled.

## Done criteria

- [ ] Chosen fields documented, validated, and tested
- [ ] `python scripts/validate.py` passes

## Notes

Ideally done before P1-011.
