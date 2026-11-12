---
id: P1-010
title: "Finalize source criteria and registry schema"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-001]
estimate: 1
outputs:
  - docs/conventions/research-protocol.md
  - docs/conventions/content-schema.md
  - scripts/validate.py
---

## Context

The v0 criteria and schema exist. Before mass research, make sure the schema captures everything the audit and the app will need later.

## Tasks

1. Review research-protocol.md and the registry schema; test with 5 varied seed entries (book, paper, postmortem, repo, Tier 6).
2. Add missing fields (e.g. `free_companion` for paywalled sources) and matching validator rules.
3. Make sure the validator gives clear error messages.

## Done criteria

- [x] Final schema documented
- [x] Validator checks all schema rules
- [x] Seed entries pass validation
- [x] `python scripts/validate.py` passes

## Notes

- Added registry fields `free_companion` (ids of free sources, required for approved paywalled sources) and `superseded_by` (for deprecated sources). Added unknown-field detection with "did you mean" hints, calendar-date and DOI format checks, type-tier consistency warnings, and stricter rules for `approved` entries (known license, no SEED marker, authors/published or an explicit `NO-AUTHOR:` / `NO-DATE:` note, units and topics present).
- The 11 seed entries are all `candidate`, so the approved-only rules were exercised with fixtures instead: `tests/test_registry.py` covers a book, paper, postmortem, repo, and Tier 6 entry as approved plus broken variants (10 tests, run in CI).
- Review: `content-reviewer` (closest available reviewer for a schema ticket) gave "pass with minor fixes". Fixed: crashes on malformed input, type checks, date validation, enum mismatch between docs and validator, `superseded_by` self-reference, weak "notes explains" escape hatch, `\bSEED\b` matching, DOI regex, and the missing fixtures.
- Not done here, as new tickets: P1-066 (same crash class in the curriculum validators), P1-067 (optional fields `version`, `archive_url`, `attribution`, `lang`, `verified_on`; best decided before P1-011).
