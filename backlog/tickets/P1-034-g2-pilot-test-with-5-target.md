---
id: P1-034
title: "G2 — Pilot test with 5 target users"
milestone: M3
type: review
owner: human
review: none
status: blocked
priority: high
depends_on: [P1-032]
estimate: 1
outputs:
  - docs/pilot-feedback.md
---

## Context

Gate G2. Test whether the content format works for real readers before mass production.

## Tasks

1. Ask 5 people (students and junior engineers) to read the pilot lesson and do the questions. The agent can prepare an easy-to-share HTML/markdown version if asked.
2. Collect: confusing parts, questions that are too easy/hard/ambiguous, 'AI-made' impressions, duration.
3. Write the summary in `docs/pilot-feedback.md` (raw bullets are fine; the agent tidies them).

## Done criteria

- [ ] Feedback from ≥ 5 people recorded

## Notes

**Deferred (ADR 0007, 2026-11-16):** the owner chose beta-first; the owner is the only tester for now and the pilot lesson is not shown to others yet. This gate is not cancelled: run it after a usable beta exists and before any public beta. Nothing depends on it any more (P1-035 now depends on P1-032).
