---
id: P1-018
title: "Finalize citation and attribution guide"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-010]
estimate: 1
outputs:
  - docs/conventions/citation-guide.md
  - scripts/validate.py
---

## Context

The v0 guide exists. Finalize it and make sure the validator enforces it in content.

## Tasks

1. Test the guide on one sample lesson (may be a dummy).
2. Add validator checks: `[^id]` markers exist in `sources` and the registry; `published` content must not cite `candidate`; attribution is required when using an `adapt-with-attribution` source.
3. Clarify the direct-quote rule with examples.

## Done criteria

- [ ] Guide is final
- [ ] Validator enforces the citation rules
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
