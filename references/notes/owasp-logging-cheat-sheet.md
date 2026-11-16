---
source: owasp-logging-cheat-sheet
read_by: agent
date: 2026-11-16
sections_read: ["What to log", "What not to log", "Log levels/severity", "Structure and format", "Interaction identifier", "Storage and protection"]
---

# Notes: OWASP Logging Cheat Sheet

> Notes are in English and in your own words. Section names are paraphrased from the fetch summary; re-read headings before citing.

## Key points

- (what to log) Mainly security-relevant events that also help operations: failed validation, auth failures, session oddities, application errors, admin actions, sensitive-data access, exports and uploads.
- (what not to log) Passwords, session ids, tokens, keys, connection strings, card and bank data, sensitive personal data; mask or hash when needed.
- (levels) Use one documented severity scheme (named levels from fatal to trace, or syslog-style numbers); do not make logging impossible to enable where it is required.
- (structure) Record when, where, who, what for every event; prefer structured formats such as JSON over free text, which is open to CR/LF log injection; cap sizes of user-supplied values.
- (correlation) An interaction identifier ties together all events from one request or action.
- (storage) Keep logs apart from the web root, restrict access, keep clocks synced, guard against log flooding filling the disk, and keep only for the retention period.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| No numbers used | | |

## Relevant to concepts

- Unit 0 logging basics (what to log, levels, structure, request id).

## Warnings

- Security angle: it says little about debugging-oriented logging style or volume/cost.
- Author and last-updated date not on the page (as fetched).
