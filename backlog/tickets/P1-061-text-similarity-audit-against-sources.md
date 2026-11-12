---
id: P1-061
title: "Text-similarity audit against sources"
milestone: M5
type: review
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-040, P1-041, P1-042, P1-043, P1-044, P1-045, P1-048]
estimate: 2
outputs:
  - docs/audit-similarity.md
---

## Context

Make sure the 'rewrite, don't copy' principle is met.

## Tasks

1. For a sample of lessons (≥ 30%), compare with the cited section of the source.
2. Flag and rewrite paragraphs that are too similar.

## Done criteria

- [ ] Audit report
- [ ] All findings followed up
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
