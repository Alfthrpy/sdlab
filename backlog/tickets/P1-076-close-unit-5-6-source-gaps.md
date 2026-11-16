---
id: P1-076
title: "Close Unit 5-6 source gaps: vector clocks, Zab, TrueTime, SLO alerting, tracing"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: medium
depends_on: []
estimate: 1
outputs: []
---

## Context

Gap items B9 and B12 in `references/coverage.md`. B11 (reading `tail-at-scale-cacm13` in full) is blocked for agents and stays with the owner. B12: drop adaptive concurrency from v1.

## Tasks

1. B9: find sources for vector clocks, Zab, and TrueTime detail; read the Jepsen model pages used by Unit 5.
2. B12: find beginner SLO-based alerting, SRE book tracing/release-engineering chapters; read `dapper-2010` in full.
3. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [x] Every task above is done or recorded as a gap with a proposed action
- [x] `python scripts/validate.py` passes

## Notes

Added 10 registry entries (198 -> 208), all `candidate`, `verified_on` empty:
- B9 vector clocks: `mattern-virtual-time-global-states-1989` (Tier 3), `riak-docs-causal-context` (Tier 2, CC BY 4.0 per summary). Gap: Fidge 1988 not opened (author host did not resolve, UCI copy certificate error). Proposed: owner or verifier finds a reachable Fidge copy.
- B9 Zab: `dissecting-zab-yahoo-2010` (Tier 3, YL-2010-0007), `zookeeper-wiki-zab1-0` (Tier 2, wiki, weaker standing). Gap: the DSN 2011 Zab paper could not be opened, so it is not registered. Proposed: verifier tries IEEE/author copies.
- B9 TrueTime: read spanner-osdi12 PDF sections 3, 4, 5.1, 5.3, 7, 8; notes in `references/notes/spanner-osdi12.md`. Appendix A, 2, 5.2, 5.4 not read in depth. The registry entry still says the PDF was not opened; the verifier should update it.
- B9 Jepsen: `jepsen-causal`, `jepsen-serializable`, `jepsen-sequential` (`jepsen-linearizable` already existed). All read through WebFetch summaries.
- B9 incident: no new one. `github-oct21-2018-postmortem` already covers a partition/failover inconsistency. Gap: no official coordination-service (ZooKeeper/etcd) split-brain postmortem found; proposed: accept for v1.
- B12: `sre-workbook-alerting-on-slos-ch5`, `sre-book-release-engineering-ch8`, `sre-book-practical-alerting-ch10` (SRE book has no tracing chapter, checked its table of contents). `dapper-2010` read in full; notes in `references/notes/dapper-2010.md` (the PDF says technical report, April 2010; the registry entry lacks that detail).
- B11 not done (owner only). Adaptive concurrency not researched (dropped).

Verification (source-verifier): all 10 new entries reopened; pass with fixes. SRE Workbook burn-rate numbers (14.4x/1h+5min/2%, 6x/6h+30min/5%, 1x/3d+6h/10%) confirmed. Fixes: `dapper-2010` sampling claim corrected in its notes (below 1/16 is within error; 1/16 still adds 2.12%; full tracing adds 16.3%) and `published` set to 2010-04; outdated `spanner-osdi12` notes updated (PDF opened; sections 3, 4.1-4.2, 5.1, 5.3, 7, 8 read; 2, 5.2, 5.4, 6, Appendix A not read in depth). Entries stay `candidate`, `verified_on` empty.

Owner decisions: `zookeeper-wiki-zab1-0` is a user-editable Confluence wiki recorded at Tier 2 as an explicit exception to research-protocol.md (marked TIER EXCEPTION in its notes); `mattern-virtual-time-global-states-1989` is hosted on a university course page (no author or publisher copy found; an MIT copy exists as an alternative); Riak docs are for the old Riak KV 2.2.3.

Gaps left (proposed actions): Fidge 1988 vector clocks (author host and UCI copy unreachable; Mattern plus Riak cover it meanwhile); Zab DSN 2011 paper (IEEE/UMN/scispace copies failed; Yahoo technical report and the Zab1.0 wiki registered instead); split-brain/coordination incident (accept for v1; `github-oct21-2018-postmortem` is related); SRE book has no tracing chapter (Dapper and the OpenTelemetry primer cover it); Dissecting Zab proof sections 5-7 not read. B11 (read `tail-at-scale-cacm13` in full) stays with the owner; adaptive concurrency was dropped from v1.
