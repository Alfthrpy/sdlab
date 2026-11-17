---
source: atlassian-pir-april-2022
read_by: agent
date: 2026-11-17
sections_read: ["Letter from our co-founders", "Executive summary", "Overview of Atlassian's cloud architecture (incl. Disaster Recovery program)", "What happened, timeline, and recovery (What happened, How we coordinated, Workstreams 1-3)", "Minimal data loss following the restoration of deleted sites", "Incident communications (skimmed for facts)", "Learning 1, Learning 2 (Atlassian Data Management paragraph), Learning 3, Learning 4", "Closing remarks"]
---

# Notes: Post-Incident Review on the Atlassian April 2022 outage

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location.
> Read the whole page on 2026-11-17 via `curl` on the raw HTML; every figure below was checked there. Published April 29, 2022, in "How We Build"; the author Sri Viswanath (the registry author) is named under "About This Article" at the end of the page; footer "Copyright 2026 Atlassian". The figures (timeline diagram, Figure 6) are images and were not read; only the surrounding text was.

## Key points

- (Executive summary, "What happened?") The cause was operational, not an attack. A legacy standalone app (Insight - Asset Management) had to be removed from customer sites. The team asking for the removal gave the team running the script site IDs instead of app IDs. The deletion API accepted either kind of ID and gave no warning about which kind was being deleted, so whole sites were deleted.
- (What happened) Peer review of the script looked at which endpoint was called and how, not at whether the IDs were site or app IDs. A staging test did not help because those IDs did not exist in staging. An earlier production run on 30 sites worked correctly because those IDs had been collected before the mix-up. The second production run (883 sites) used the wrong IDs.
- (What happened) The deletion ran sequentially through the list and finished in about 23 minutes, with no alarm. Atlassian's own monitoring did not notice because the deletions went through a normal workflow; the first signal was a customer support ticket.
- (Disaster Recovery program) The page defines RTO (how fast data is back and returned to the customer) and RPO (how much recent data is lost relative to the last backup). It states that in this incident the RTO was missed and the RPO was met.
- (Disaster Recovery program) Two separate preparations are described: resiliency against infrastructure failures (replication across availability zones, failover tests) and restorability from backups for data corruption, ransomware, software defects and operational errors (immutable backups, restore testing, point-in-time restore of any single data store). The incident hit the second category at a scale that had not been exercised.
- (Multi-site, multi-product automated restorability) Before the incident Atlassian could restore a single data store or a single site. It could not pick a large set of sites and restore all of their linked products to an earlier point in one operation, and there was no automatable runbook for that scale.
- (Workstream 1 and 2) Because each data store holds data of many customers, the deleted data could not simply be rolled back wholesale; pieces had to be extracted from backups and restored per site while other customers kept using the same stores (Learning 2, Atlassian Data Management paragraph).
- (Workstream 2, Restoration 1) First approach: create a new site for each deleted one and rebuild everything around it; about 70 steps; identifiers changed, which forced data remapping and coordination with third-party app vendors.
- (Workstream 3, Restoration 2) Second approach, proposed on April 9: re-create the records of the old site with the old identifiers, which removed more than half of the steps; over 30 steps, mostly parallel, with automated validation. Switching approaches in mid-incident added coordination overhead.
- (Minimal data loss...) Backups are a mix of full and incremental backups that allow restoring to any chosen point in time inside a 30-day retention window. For most customers a restore point five minutes before the deletion was used, and non-primary stores were restored to the same point (or by replaying events) to keep stores consistent with each other. For 57 customers restored early, manual retrieval of snapshots without a consistent policy put some Confluence and Insight databases at a point earlier than that; this was found in a post-restoration audit.
- (Incident communications; Learning 4) The script also deleted customer contact data and site URLs, so customers could not file tickets the normal way and Atlassian lacked reliable contacts; the review lists backing up key contact data outside the product instance as an action.
- (Executive summary, prevention list; Learning 1) Corrective actions: universal soft delete (deletion only after a prior deactivation, staged rollout, rollback plan tested before production), automate large-scale restoration and run regular DR exercises that restore all products for many sites, a large-scale incident management process, and a communications playbook.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Deletion started 2022-04-05 07:38 UTC, finished 08:01 UTC | What happened | About 23 minutes; sequential deletion |
| 883 sites deleted, 775 customers affected (early estimate was about 400 customers, about 700 non-Atlassian sites) | Executive summary; What happened | The estimate changed during the incident; use final figures |
| Products unavailable: Jira family, Confluence, Atlassian Access, Opsgenie, Statuspage | What happened | |
| First customer ticket 07:46 UTC; major incident process started 08:17 UTC; link between ticket and script confirmed 08:53 UTC; highest severity assigned 12:38 UTC | How we coordinated | Detection came from a customer, not from monitoring |
| Outage up to 14 days for some customers; first restorations April 8; all restored by April 18 | Executive summary; What happened | Timeline Figure 6 is an image, not read |
| Restoration 1 took about 48 hours per batch; restored about 53% of affected users across 112 sites (April 5-14) | Workstream 2 | 112 + 771 = 883 sites |
| Restoration 2 took about 12 hours per site; restored about 47% of affected users across 771 sites (April 14-17) | Workstream 3 | Per-site duration, versus per-batch for Restoration 1; the page words them differently, so do not compare the two numbers directly |
| Restoration 1 would have needed about three weeks for everyone | Workstream 3 | Reason for switching approach |
| About 70 steps (Restoration 1) vs over 30 steps (Restoration 2) | Workstreams 2 and 3 | |
| Backup retention 30 days; restore point five minutes before deletion for most customers | Minimal data loss...; Learning 2 | |
| RPO "of one hour" met; data loss capped at 5 minutes before deletion; 57 customers had some databases restored to an earlier point | Minimal data loss...; Learning 2 | The stated RPO (1 hour) is much larger than the actual loss (5 minutes); the RTO value is NOT given on the page |
| "No customer lost more than five minutes of data"; over 99.6% of customers/users unaffected | Executive summary | Statement by Atlassian; later note on the 57 customers qualifies it |
| Automated availability-zone failover typically 60-120 seconds | Learning 2 (Atlassian Data Management paragraph) | Contrast: replica/failover covers infrastructure loss, not operator deletion |
| Incident management team met every three hours; code freeze from April 8 03:30 UTC | How we coordinated | Operational color, less relevant to Unit 0 |

## Relevant to concepts

- `backup-recovery` objective 1 (backup vs replica/mirror, by kind of damage): supported. The Disaster Recovery section separates resiliency (replication across AZs, 60-120 s failover) from restorability (immutable, point-in-time backups for operational errors and corruption). The incident is a user/operator error that a synchronous replica would not have undone; the page does not literally say "a replica would have copied the deletion", so the lesson must phrase that as inference from the described architecture.
- `backup-recovery` objective 2 (choose backup frequency from RPO and RTO): partly supported. It gives plain definitions of RPO and RTO, a real RPO (one hour policy; actual loss five minutes), and a real failure of RTO (days to weeks for 883 sites). It shows the cost of an RTO that was never rehearsed at scale. It does not teach how to turn a target RPO/RTO into a schedule (no backup interval, no restore-time arithmetic, the RTO figure is not stated). A calculation exercise needs another source or the author's own reasoning (and then marked as such).
- `backup-recovery` objective 3 (a backup never restored is not safe): supported, with a nuance. Atlassian tested backups and could restore single stores or sites, yet could not restore many sites at once and the restore took up to 14 days. Lesson: "restores work" has to be tested at the scale and in the shape of the likely disaster, and the full restore procedure (not only the data copy) must be rehearsed. The 57-customer inconsistency (manual snapshot retrieval, no consistent policy) is a second restore-quality example. Do not claim that Atlassian's backups were corrupt or missing; the page says the data was recovered.
- `backup-recovery` (scale caveat): this is a multi-tenant, multi-product platform with hundreds of engineers on the incident. A single-server beginner has none of this complexity; use it for the concepts (RPO/RTO, rehearsal, soft delete, dangerous operations) rather than for the mechanics.
- Registry units are [3, 6], so the source is also meant for later units; for Unit 0 only the backup/recovery facts above are relevant.

## Warnings

- Tier 4 (company postmortem): the account is written by the party responsible, from its own point of view; claims such as "no unauthorized access" and "99.6% unaffected" are its statements. The letter at the top is public-relations text and was only skimmed for facts.
- Figures differ in scope: "883 sites / 775 customers" (deleted), "about 400 customers" (early estimate), "53% of users / 112 sites" and "47% of users / 771 sites" are shares of affected users, not customers. Restoration 1 time is per batch, Restoration 2 time is per site.
- The RPO "met" claim is about the stated one-hour policy; the review also admits 57 customers were restored to an earlier point than the 5-minute target. Read both statements together.
- The RTO target is never given numerically, so "RTO missed" cannot be quantified from this page alone.
- Dated April 2022; older than the 2023-2026 target (registry note). Atlassian's later update posts were not opened.
- All-rights-reserved (see registry): rewrite only, at most one short quote per lesson.
