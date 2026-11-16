---
source: capistrano-docs-rollbacks
read_by: agent
date: 2026-11-16
sections_read: ["Rollbacks", "Structure (sibling page)"]
---

# Notes: Capistrano docs, Rollbacks (and Structure)

> Notes are in English and in your own words. Tool-specific; use the pattern, not the commands.

## Key points

- (Structure) One timestamped directory per release, a shared directory for files that survive releases, and a `current` symlink moved only after a deploy succeeds, so a failed deploy leaves the old version running.
- (Rollbacks) If failure happens before the symlink moves, nothing to do; after it moves, rollback re-points `current` to the previous release and archives and removes the failed one. A specific release can be named.
- (Rollbacks) The docs themselves suggest that reverting the bad code and redeploying often makes more sense than a rollback, and that each app must test its rollback.
- (Rollbacks) Rolling back code does not reverse database migrations; plan and test schema changes yourself.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Rollback picks the second most recent release by default | Rollbacks, reverting step | Capistrano 3 behavior |

## Relevant to concepts

- Unit 0 simple deploys: release directories, atomic switch, rollback, migration caveat.

## Warnings

- No license stated; no date or version on the pages. Does not cover systemd restart, health check after deploy, or expand/contract migrations.
