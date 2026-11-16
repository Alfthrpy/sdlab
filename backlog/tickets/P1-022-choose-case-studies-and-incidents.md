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

- [x] Every unit is practiced by ≥ 2 items
- [x] Every incident has an official postmortem in the registry
- [x] `python scripts/validate.py` passes

## Notes

- `curriculum/case-studies.yaml`: 12 case studies and 12 incidents. Items per unit: 0: 6, 1: 4, 2: 11, 3: 5, 4: 4, 5: 3, 6: 15. Each case study notes in a comment why it fits both goals; each incident notes its mechanism.
- Review (content-reviewer): pass with minor fixes, applied. Dropped concept mappings the postmortems do not support (e.g. replication-lag-failover for the Cloudflare 2023 incident, observability for CrowdStrike and Atlassian, simple-deploys for OS-update incidents).
- Known gaps (also in the file header): incident mix leans on deploy/config (6 of 12); no registry postmortem for replication/split-brain, true data corruption, or plain traffic-spike overload; Unit 4 incident coverage is only GitHub. Candidate follow-up: a research ticket for Unit 3-5 postmortems.
- `incident-github-2026-08` is a monthly availability summary; M4 should confirm it suffices or swap in another retry-storm postmortem.
- Thin case-study sources (rate limiter, URL shortener key generation, front door DNS/sessions) are marked in comments and covered by P1-078 (open in PR #32).
- Reserves not listed: meta-outage-2021-10-04, fastly-outage-2021-06-08, cloudflare-1111-incident-2025-07-14.
