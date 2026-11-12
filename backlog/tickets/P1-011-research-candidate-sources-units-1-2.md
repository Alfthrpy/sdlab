---
id: P1-011
title: "Research candidate sources — Units 1 & 2"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-010]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Context

Fill the Reference Registry for Unit 1: Foundations (latency/throughput, estimation, Little's law, percentiles, SLI/SLO); Unit 2: Building blocks (load balancer, reverse proxy, cache, CDN, REST/gRPC API, idempotency). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [ ] ≥ 20 candidates for this unit, all opened in the session
- [ ] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [ ] Reading notes for the 3–5 main sources
- [ ] `source-verifier` says pass
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
