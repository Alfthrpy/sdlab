---
id: P1-010
title: "Finalize source criteria and registry schema"
milestone: M1
type: research
owner: agent
review: agent
status: in-progress
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

- [ ] Final schema documented
- [ ] Validator checks all schema rules
- [ ] Seed entries pass validation
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
