# Session 2026-11-12 — agent docs translation (no ticket)

- **Done by:** agent (Claude)
- **Ticket:** none — requested directly by the owner as an out-of-ticket change (an exception to golden rule 1)
- **Final status:** done (PR pending owner merge)

## What was done

- Translated everything an agent reads into English: AGENTS.md, docs, ADRs, conventions, templates, READMEs, subagent and command definitions, PR template, all 39 tickets, session logs, registry comments/notes, script messages and docstrings.
- Left Indonesian only where it is learner-facing content: examples in `writing-style.md`, the attribution text in `citation-guide.md`, and the `Bisa ...` / `diadaptasi` validator checks. The ticket section headings are now `Context / Tasks / Done criteria / Notes`; the validator and `new_ticket.py` were updated.
- Renamed Indonesian-named files to English: `docs/PLAN-FASE-1.md` → `PLAN-PHASE-1.md`, the four ADR files, and all ticket slugs (ids unchanged).

## Decisions made

- New ADR 0005 records the language policy. P1-003 now outputs ADR 0006 instead of 0005.
- Existing text was translated faithfully, including the stale "junior–mid" wording in some files, so P1-065 can still do the audience alignment.

## Not finished / for the next session

- Next ready tickets are unchanged: P1-010, P1-065, P1-004.

## New tickets created

- None.
