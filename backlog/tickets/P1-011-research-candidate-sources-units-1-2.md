---
id: P1-011
title: "Research candidate sources — Units 1 & 2"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-010, P1-068]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Context

Unit 0 (single-server backend) is researched in P1-069. Fill the Reference Registry for Unit 1: Foundations (latency/throughput, estimation, Little's law, percentiles, SLI/SLO); Unit 2: Building blocks (load balancer, reverse proxy, cache, CDN, REST/gRPC API, idempotency). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [x] ≥ 20 candidates for this unit, all opened in the session
- [x] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [x] Reading notes for the 3–5 main sources
- [x] `source-verifier` says pass
- [x] `python scripts/validate.py` passes

## Notes

Result: 35 new candidates (units 1/2) and 6 reading notes; `nginx-reverse-proxy-admin-guide` now also lists unit 2. `source-verifier`: pass on the second pass (first pass failed on a stale IETF draft revision and missing gaps; fixed).

Gaps and weak spots (for later tickets):
- **Back-of-envelope estimation:** only one weak Tier 3 source (Jeff Dean slides, undated, license unknown, course-site copy) plus two Tier 6 map-only pointers. Teach the method, not the old numbers.
- **Reverse proxy:** only vendor docs (nginx); no conceptual explainer. HAProxy docs fetch failed.
- **CDN, REST, gRPC:** no Tier 1 source; only vendor/official docs, MDN, RFCs, and open-licensed API guides (Microsoft guidelines, Google AIP; contents only partly read).
- **"Is this stage still enough?":** covered only indirectly (SRE overload chapter, SLO sources, AWS load shedding).
- **Latency vs. throughput:** no standalone source; DDIA (paywalled) is the likely one, not opened.
- **403s:** `tail-at-scale-cacm13` has no DOI (ACM blocked); the Little 2011 publisher page (INFORMS) could not be opened, text read from a UMass mirror with unverified posting rights.
- **Abstract-only reads:** tail-at-scale, nishtala-memcache-nsdi13, maglev-nsdi16, tene-how-not-to-measure-latency. Re-read full text before approval.
- IETF idempotency-key draft is an active Internet-Draft (-08); re-check before approval.
- Optional nits left: Dean entry `published: ''` could be `null`; PDF metadata shows a 2009 creation date (file date only).
