---
source: google-sre-book-data-integrity-ch26
read_by: agent
date: 2026-11-16
sections_read: ["Backups Versus Archives", "Delivering a Recovery System, Rather Than a Backup System", "Second Layer: Backups and Their Related Recovery Methods", "Overarching Layer: Replication", "1T Versus 1E: Not Just a Bigger Backup", "Knowing That Data Recovery Will Work", "Gmail (February 2011)", "Google Music (March 2012)", "Conclusion"]  # headings as shown on the page; verifier-corrected 2026-11-16
---

# Notes: SRE book ch. 26, Data Integrity

> Notes are in English and in your own words. Section names are as shown on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (backups vs. archives) A backup can be loaded back into a running application; an archive is for audit or compliance and may be slow to retrieve. Pick backup frequency from how fast you must recover and how much recent data you can lose.
- (delivering a recovery system) Judge yourself by restores, not by backups taken. Set a data-availability target per failure mode and show you can meet it.
- (second layer: backups) Use layers: fast snapshots close to the data for most software bugs, a few days of on-site copies against storage failure, and less frequent but longer-kept offline or off-site copies against site loss.
- (replication) Replication is not a backup: bad deletes and corruption copy to every replica.
- (knowing recovery works) Recovery paths break silently. Run automated end-to-end restore tests, alert when they stop, and check that backups are complete and restores finish in a sensible time. Off-site vaults may not be available on demand.
- (case studies) Gmail 2011 restored from offline tape and earlier drills made the time estimate accurate; Music 2012 restore took about a week because tapes had to be recalled, and some data had never been backed up.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Gmail 2011 restore from offline backups; Music 2012 restore from off-site tape took about a week | case study sections | Google scale; use only as illustration |

## Relevant to concepts

- Unit 0 backups and recovery basics: schedule, off-machine copies, restore drills.

## Warnings

- Written for Google scale; skip the exabyte sections for Unit 0.
- The page gives no publication date, only the 2017 copyright year.
