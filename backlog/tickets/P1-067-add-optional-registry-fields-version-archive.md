---
id: P1-067
title: "Add optional registry fields: version, archive_url, attribution, lang, verified_on"
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

Found by the P1-010 review. The schema is declared final, but some fields are cheap to add now and expensive to backfill after P1-011–P1-015 add ~100 entries: `version` (commit hash or docs version; `edition` is documented for books only), `archive_url` (Wayback link against link rot), `attribution` (ready-made credit line for `adapt-with-attribution` sources), `lang` (`en` or `id`), `verified_on` (date the `source-verifier` checked it). Decide which are worth having, then add them before M1 research runs in full.

## Tasks

1. Decide which fields to add (some may be dropped).
2. Add them to the validator (`KNOWN_FIELDS`), `docs/conventions/content-schema.md` §1, `templates/source-entry.yaml`, and `tests/test_registry.py`.
3. Say in `research-protocol.md` when each field must be filled.

## Done criteria

- [x] Chosen fields documented, validated, and tested
- [x] `python scripts/validate.py` passes

## Notes

Decisions: all five fields added. `version` (free string) and `archive_url` (http/https) and `lang` (en|id, absent means en) are optional. `verified_on` (valid non-future date) is required for approved entries; `attribution` is required for approved `adapt-with-attribution` entries. Fields are set at verification time (P1-016), so P1-016 and P1-019 and research-protocol.md were updated to say so.
Review: `content-reviewer` gave "pass with minor fixes"; fixed the P1-016/P1-019 process gap, whitespace-only values, an unquoted-date hint, wording, and test gaps. Left as is: `verified_on` is not compared with `accessed`, and `date.today()` is local time (CI runs in UTC).
