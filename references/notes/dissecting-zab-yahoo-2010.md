---
source: dissecting-zab-yahoo-2010
read_by: agent
date: 2026-11-16
sections_read: ["1 Introduction", "3 system model (skimmed)", "4.1 Terminology", "4.2 Zab description (phases 1-3, message table)", "4.3 Some insight (examples)"]
---

# Notes: Dissecting Zab (Yahoo! Labs Technical Report YL-2010-0007)

> Notes are in English and in your own words. Read via pdftotext. Sections 5-7 (proofs, lemmas, common wrong claims) were not read beyond their headings. This is NOT the DSN 2011 paper (that paper could not be opened); it is the earlier technical report on the same protocol by the same authors, with a more formal presentation and different message names (CEPOCH, NEWEPOCH, ACK-E, NEWLEADER, ACK-LD, COMMIT-LD).

## Key points

- (1) Zab is used by ZooKeeper to broadcast the state changes produced by one primary. Changes depend on the state before them, so every replica must deliver a prefix of the primary's sequence, in order. The authors call the problem primary-order atomic broadcast and note that it differs from classic atomic broadcast in its causality properties.
- (1) Four highlights: the protocol runs in epochs with at most one broadcasting process per epoch; a process that finishes phase 1 promises to reject proposals from older epochs; every participant's history must start with the epoch's initial history; a new leader must finish recovery before broadcasting.
- (4.2, phase 1 Discovery) Followers tell the prospective leader their last promised epoch; once a quorum has, the leader proposes a new epoch larger than any it saw; followers that accept send back their current epoch and history; the leader picks the history of the follower with the highest (epoch, last transaction id) as the initial history.
- (4.2, phase 2 Synchronization) The leader sends the initial history as a NEWLEADER proposal; followers adopt it and acknowledge; with a quorum of acks the leader sends a commit and followers deliver the initial history. The epoch is then "established".
- (4.2, phase 3 Broadcast) The leader proposes transactions in increasing id order; a quorum of acks leads to COMMIT; a follower delivers a transaction only after earlier ones are delivered. A late-joining follower that sends CEPOCH during broadcast is brought up to date with a NEWEPOCH plus NEWLEADER carrying the history so far.
- (4.3) The examples show why a leader must adopt the history of the follower that is furthest ahead among a quorum, and why a quorum's promise to ignore older epochs prevents a stale leader from committing anything.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Three phases: discovery, synchronization, broadcast; phases 1+2 form recovery | Sec. 4.1-4.2 | Matches the phase names used in the DSN paper per the search summary; not checked in the paper itself |
| Message names listed in Table 1 | Sec. 4.2 | Names differ from the implemented ZooKeeper protocol on the Apache wiki (`zookeeper-wiki-zab1-0`) |

## Relevant to concepts

- `consensus`: how a leader-based protocol recovers history after a leader change; epochs as fencing against old leaders.
- `locks-leases-fencing`: epoch numbers and zxids play the role of fencing tokens.

## Warnings

- Formal, notation-heavy; teach the three phases and the epoch idea only.
- The report prints no date; the report number suggests 2010 (inference).
- Implementation differs from this description in places (Apache wiki page and the Medeiros report discuss this); the Medeiros report was only skimmed through its outline and is not registered.
