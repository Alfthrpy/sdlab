---
id: P1-080
title: "Find a data-corruption incident postmortem"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: low
depends_on: []
estimate: 1
outputs: []
---

## Context

Found in P1-022. The ticket asks for incident mechanisms including data corruption, but none of the 15 `postmortem` entries in the registry is about corruption (`atlassian-pir-april-2022` is destructive deletion with a slow restore). `curriculum/case-studies.yaml` records this as a known gap.

## Tasks

1. Search for an official postmortem about silent or visible data corruption (bad write path, replication or storage bug, bad migration) from a vendor or operator, preferably 2020 or later and readable by junior engineers.
2. Register the best 1-2 as `candidate` with `verified_on`; note anything not found as a gap with a proposed action (accept the gap, or use Atlassian only).
3. Do not edit `curriculum/case-studies.yaml`; a follow-up adds the incident once the source is approved.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
