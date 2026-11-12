---
id: P1-012
title: "Research candidate sources — Unit 3"
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

Fill the Reference Registry for Unit 3: Data (data models, indexes, replication, partitioning, transactions & isolation). Use the `researcher` subagent; review by `source-verifier`.

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

Result: 21 new candidates (unit 3) plus unit 3 added to `use-the-index-luke`; 6 reading notes. `source-verifier`: pass with fixable findings, all applied (Karger id renamed without the unverified year, Dynamo reading scope corrected, Notion wording, Cassandra version caveat, PG license wording).

Gaps and weak spots:
- **Tier 1:** `ddia-2e` is still a seed entry; the O'Reilly page returned 403, so no chapter list or notes.
- **Multi-leader replication:** only the thin CouchDB intro.
- **Failover:** only the PostgreSQL HA intro and standby page (26.3/26.4 not read; guessed failover URL returned 404). Look for an operator postmortem or Builders' Library article.
- **Serializability and isolation theory:** no paper read in full; Berenson and Bigtable are abstract-page only.
- **LSM vs. B-tree:** only the original LSM paper; no modern write-amplification source.
- **Sharding in production:** Notion is the only case; Instagram, GitHub, Vitess not fetched.
- **Graph / wide-column internals:** vendor concepts pages only. MySQL InnoDB MVCC/isolation not covered. No Tier 4 incidents.
- **Weak metadata:** Karger and O'Neil have no verified date or DOI (ACM/dblp 403); Cassandra docs URL is a prerelease `/latest/` path; Dynamo vector clocks, hinted handoff, Merkle trees not yet read.
- Vendor docs (MongoDB, DynamoDB) favour their own designs; teach critically.

Trigger hints found (for lessons): PostgreSQL partitioning is worth it when the table exceeds server memory; MongoDB sharding comes after the vertical-scaling ceiling; MySQL replicas for read scale-out, backups, analytics; Notion sharded after vacuum stalls and transaction-ID wraparound risk; async replication can serve stale reads and lose data on failover.
