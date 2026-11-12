---
id: P1-046
title: "Incident pack (8 scenarios)"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-033, P1-042]
estimate: 4
outputs:
  - content/incidents/
---

## Context

Design & Fix scenarios from public postmortems. The first two candidates are already in the registry: AWS DynamoDB DNS (Oct 2025) and Cloudflare (18 Nov 2025).

## Tasks

1. Choose 8 from the candidates in `curriculum/case-studies.yaml`.
2. Per incident: summary in your own words, timeline, mechanism, scenario for the player, discussion, related concepts.
3. Split into one sub-ticket per incident if needed.

## Done criteria

- [ ] 8 incidents pass the validator and content-reviewer
- [ ] Every timeline fact is sourced from the official postmortem
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
