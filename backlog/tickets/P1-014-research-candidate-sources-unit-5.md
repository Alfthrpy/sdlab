---
id: P1-014
title: "Research candidate sources — Unit 5"
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

Fill the Reference Registry for Unit 5: Consistency & coordination (CAP/PACELC, consistency models, consensus, locks & leases, time & clocks). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [x] ≥ 15 candidates for this unit, all opened in the session
- [x] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [x] Reading notes for the 3–5 main sources
- [x] `source-verifier` says pass
- [x] `python scripts/validate.py` passes

## Notes

Result: 25 new candidates (unit 5; one removed and one added during fixes, net 25), `dynamo-sosp07` extended to unit 5, 5 reading notes. `source-verifier`: pass conditional on fixes; fixes applied by a second `researcher` run (SRE ch. 23 authors, `raft-github-io` retiered to 2, blog summary of FLP replaced by the original paper, Chubby/ZooKeeper dates from USENIX program pages, Brewer DOI from Crossref).

Not independently re-verified after the fixes: the new `flp-impossibility-1985` entry (Princeton course scan, first page and abstract only) and the Brewer DOI (Crossref record; IEEE Xplore page unreadable). The verifier also did not reopen the etcd (2) and ZooKeeper (2) docs pages or the Jepsen landing page.

Gaps and weak spots:
- **FLP:** the original is registered but no reading note; proof not read.
- **Vector clocks:** no dedicated source (only Dynamo headings and the HLC paper's discussion).
- **Zab:** only the ZooKeeper paper, Zab sections not read closely; Viewstamped Replication unreachable.
- **TrueTime detail:** `spanner-osdi12` is abstract-page only; the Google Cloud TrueTime page had no usable metadata.
- **Jepsen:** sequential, causal and session-guarantee model pages not opened; the landing page lists no models.
- **Gilbert-Lynch CAP proof:** scanned bitmap, skipped. Ongaro dissertation: fetch timed out.
- **Postmortems:** no Tier 4 split-brain or coordination incident was looked for.
- **ddia-2e:** still unverified; free companions cover the topics.
- **Weak metadata:** `kulkarni-hybrid-logical-clocks` has no verified year or venue (non-peer-reviewed report, Tier 3 borderline); several papers lack DOIs; Brewer URL is the InfoQ republication; CC BY 3.0 pages (Raft site, Kleppmann) stay `license: unknown` because the schema enum lacks it; `zookeeper-docs-*` and `redis-docs-distributed-locks` use moving `/current/` or `/latest/` URLs (pin before approval); CockroachDB post is a vendor claim.
- Kleppmann blog posts are Tier 2 by judgment call; Redlock author's rebuttal not opened.

Trigger hints found: a DB row lock suffices while all writers share one database; move to a consensus-backed service (etcd, ZooKeeper) when several processes must agree on a fact and a wrong answer corrupts data; a TTL lock is fine when duplicate work is harmless, but correctness needs a fencing token; heartbeats and timeouts alone lead to split-brain; linearizable reads cost a consensus round, so session guarantees are the cheaper middle step; use logical or hybrid clocks when you need ordering, not wall-clock timestamps.
