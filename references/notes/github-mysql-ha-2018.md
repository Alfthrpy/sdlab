---
source: github-mysql-ha-2018
read_by: agent
date: 2026-11-16
sections_read: ["whole article as returned by the fetch tool (model-written summary of the page; section names reconstructed)"]
---

# Notes: MySQL High Availability at GitHub (2018)

> Notes are in English and in your own words. The page was read through a fetch tool that returns a summary, not raw text; re-check numbers against the page at verification.

## Key points

- (Design) Each MySQL cluster has one writable primary and asynchronous replicas. Failover is split into detection plus promotion (orchestrator, running as a raft group across data centers), a small key-value store that publishes who the primary is (Consul), and proxies in front of the primary (HAProxy-based GLB).
- (Design) Applications connect to a stable proxy name, so a failover does not need a DNS or virtual IP change. This removes the old failure mode where two hosts both held the VIP.
- (Failover flow) After promotion, the new primary identity is written to the local key-value store in each data center, a template tool rewrites the proxy config, and the proxy reloads. A short hard-stop timeout cuts connections to the old primary.
- (Outage time) Reported total outage is mostly 10 to 13 seconds, up to 20 or 25 s in rarer cases.
- (Semi-sync) A commit waits for at least one replica to acknowledge; GitHub uses a 500 ms timeout after which the primary falls back to async. The cost is blocked writes when no replica answers, the gain is that failover is usually lossless.
- (Remaining risk) If the whole data center holding the primary is isolated, apps inside it can keep writing to the old primary; the quorum design makes the other data centers decide, but a short split-brain window remains.
- (Replication lag) Mentioned only for heartbeat-based lag measurement and throttling.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 10-13 s typical outage, up to 25 s | Failover section | GitHub's own claim for this design |
| 500 ms semi-sync timeout | Semi-sync section | Per the article |

## Relevant to concepts

- `replication-lag-failover`: failover steps, split-brain risk, why the old primary must be cut off (fencing).
- `replication`: sync vs async trade-off in a production setting.

## Warnings

- 2018 design, MySQL-specific; the page shows an update in 2020. The learner course covers manual failover, so use this for the idea of automation and its limits, not as a build guide.
