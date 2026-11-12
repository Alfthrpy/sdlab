# ADR 0005 — Working language for agents is English

- **Status:** accepted
- **Date:** 2026-11-12
- **Ticket:** none (requested directly by the owner, outside the ticket flow)

## Context

The repo was first written in Indonesian throughout, including agent instructions, tickets, and conventions. The owner wants everything an agent reads to be in English, while the learner-facing product stays Indonesian (see [ADR 0004](0004-audience-and-goals.md)).

## Decision

| Kind of text | Language |
| --- | --- |
| Agent instructions, docs, ADRs, conventions, templates, subagent and command definitions | English |
| Tickets, session logs, board, PR and commit text | English |
| Reference notes (`references/notes/`), registry `notes`, script output and error messages | English |
| File, folder, id, and schema-field names, code | English |
| Lessons, questions and explanations, misconceptions, incident and case-study texts | **Indonesian** |
| Learner-facing curriculum text (concept `title`, `objectives` beginning with "Bisa ...") | **Indonesian** |

Technical terms in Indonesian content stay in English (see `docs/conventions/writing-style.md`).

## Consequences

- Agents read and write English by default; they switch to Indonesian only when producing learner-facing content.
- Some validator checks look at Indonesian content on purpose: objectives must start with "Bisa " and the CC BY attribution check looks for "diadaptasi". These stay Indonesian because they inspect content, not agent text.
- Existing ticket files were renamed to English slugs; ids are unchanged.
- This ADR also covers where the previously planned ADR for name/license/reviewer goes: P1-003 now produces ADR 0006.
