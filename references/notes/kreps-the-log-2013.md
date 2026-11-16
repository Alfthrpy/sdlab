---
source: kreps-the-log-2013
read_by: agent
date: 2026-11-16
sections_read: ["headings only, via a fetch-tool summary"]
---

# Notes: The Log (Kreps, 2013)

> These notes come from a fetch-tool SUMMARY of the page (headings and the Log Compaction and retention points), not a full read. Read the essay itself before writing a lesson from it.

## Key points

- (Part One) Logs are an old idea in databases and distributed systems; tables and event streams are two views of the same data (changelog duality).
- (Part Two) Using one log as the hub for data flow between systems replaces many point-to-point pipelines.
- (Part Three, Log Compaction) For event data Kafka keeps a window by time or size; for keyed state it can keep only the newest record per key, which preserves current state but not full history.
- (Part Four) A log can keep a fixed window plus snapshots, or the full history with garbage collection. (UNCONFIRMED: only the Part Three compaction and retention text was re-read; check against the full essay before use.)

## Relevant to concepts

- `event-log-streaming`: why a log differs from a queue; retention and compaction as choices.

## Warnings

- 2013 essay about LinkedIn; product details are dated. Opinionated, not a spec.
