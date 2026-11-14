---
id: P1-022
title: "Choose case studies and incidents"
milestone: M2
type: curriculum
owner: agent
review: agent
status: done
priority: medium
depends_on: [P1-020]
estimate: 1
outputs:
  - curriculum/case-studies.yaml
---

## Context

Target: ~12 case studies and ~12 incident candidates, to pick 6 and 8 from in M4. Case studies serve two goals (ADR 0004): practice designing a system in general, and practice explaining a design within a limited time (interview prep). Choose topics that work for both.

## Tasks

1. Choose case studies that cover all units (check coverage via Tier 6).
2. Choose incidents from postmortems in the registry: varied mechanisms (retry storm, config push, DNS, overload, data corruption, dependency).
3. Map each item to the concepts it practices.
4. For each case study, note why it suits both goals (open-ended design practice and a time-boxed explanation).

## Done criteria

- [x] Every unit is practiced by ≥ 2 items (smallest: Unit 5 with 3)
- [x] Every incident has an official postmortem in the registry
- [x] `python scripts/validate.py` passes

## Notes

- `curriculum/case-studies.yaml`: 12 case studies and 13 incidents (13 of the 15 registry postmortems; Fastly 2021 and Meta 2021 held in reserve). Every item lists the concepts it practices and approved, non-Tier-6 sources. Incidents cite only the postmortem.
- "Why it suits both goals" is recorded as YAML comments (`design` / `timebox`), not schema fields; the validator does not check them. Extending the schema is left to the M4 content tickets (P1-033 / P1-047) if wanted.
- Tier 6 was read for coverage only (Hello Interview intro page problem list; ByteByteGo page lists only course titles). Three case studies are only partial matches (key-value store, read-heavy catalog, SLO monitoring plan).
- Reviewer (`content-reviewer`) fixes applied: corrected titles (1.1.1.1 "berminggu-minggu", Atlassian "hingga 14 hari"), scoped the GitHub item to the 2026-08-06 incident only, trimmed or replaced weak incident concepts (Bot Management, Datadog, Slack, Cloudflare 2023, Heroku), added missing sources to seven case studies, and dropped two concepts that the item did not practice.
- Known gaps: no data-corruption incident (new ticket P1-080); Units 4 and 5 have no incident (only case studies; the GitHub item adds one Unit 4 concept); `rate-limiter` and `payments-checkout` depend on thin sources (P1-078).
- Not applied: adding `data-models` and `index-structures` to `cs-key-value-store` (would bloat it); concepts that no item practices (`request-lifecycle`, `latency-throughput`, `data-models`, `index-structures`) stay that way; lessons cover them.
- Pick guidelines for M4 are in the header of `case-studies.yaml`.
