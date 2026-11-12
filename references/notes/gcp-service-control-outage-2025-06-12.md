---
source: gcp-service-control-outage-2025-06-12
read_by: agent
date: 2026-11-12
sections_read: ["Summary", "Root cause", "Recovery and mitigation", "Remediation"]
---

# Notes: Google Cloud incident report, 12 June 2025 (Service Control)

> Notes are in English and in your own words. Read through a summarizing fetch of the status-page incident report; confirm wording before writing a timeline.

## Key points

- (Root cause) A new quota-check feature in the Service Control binary (shipped 2025-05-29) had a code path with no error handling and no feature flag. A policy record with blank fields, written on 2025-06-12 at about 10:45 PDT, reached that path and caused a null pointer crash.
- (Why global) The policy data lives in a globally replicated Spanner table, so the bad record reached every region within seconds and each regional deployment crash-looped.
- (Detection and mitigation) Engineers found the cause in about 10 minutes and rolled out a "red-button" kill switch for the faulty path in about 40 minutes. Smaller regions recovered first.
- (Recovery in us-central1) Restarting many tasks at once overloaded the Spanner backend because the restart path lacked randomized exponential backoff. Recovery took until about 2 hours 40 minutes after mitigation, using throttled task creation and rerouting to multi-region databases.
- (Remediation) Fail open when a check fails; propagate globally replicated data gradually; require feature flags (off by default) for risky code in critical binaries; test error handling; audit for randomized exponential backoff; keep status communication independent of the affected infrastructure; freeze changes in the stack.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Incident window 10:51 to 18:18 PDT on 2025-06-12 | status page header | The earlier mini report gave a different end time |
| Full incident report dated 2025-06-13 16:45 PDT | page | |
| Cause found in about 10 min; kill switch in about 40 min | Recovery | |

## Relevant to concepts

- `safe-deploy`: feature flags and gradual propagation of data as well as code.
- `retry-backoff-jitter`: a recovery stampede on the database caused by missing backoff.
- `blast-radius`: global replication turns one bad record into a global outage.
- ladder trigger: shows up when config or data is pushed to all regions at once.

## Warnings

- Window times differ between mini report and dashboard; avoid precise duration claims without stating which.
- Search-engine summaries of this incident disagree about details (for example a "14 day dormant" claim); use only the Google page.
