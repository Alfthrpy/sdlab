---
id: P1-002
title: "Decision: content language and target audience"
milestone: M0
type: decision
owner: human
review: none
status: done
priority: high
depends_on: []
estimate: 1
outputs:
  - docs/decisions/0004-audience-and-goals.md
---

## Context

ADR 0003 used interim defaults (Indonesian, junior–mid + students, dual goal of interview and production). Agents can already work with these defaults, but the curriculum (M2) should be locked only after the final decision.

## Tasks

1. Read ADR 0003.
2. Decide: content language (Indonesian only / Indonesian + English), main target audience, main goals (interview / production / both).
3. Write the decision briefly (a PR comment or a chat message to the agent is fine; the agent writes ADR 0004).

## Done criteria

- [x] Language decision recorded
- [x] Audience & goals decision recorded
- [x] ADR 0003 status updated

## Notes

Owner decision 2026-11-12: audience is students and junior engineers; three equal goals: understand production-scale systems, learn new things, and interview prep (interview was added by the owner after the first decision). Language was not stated explicitly, so the Indonesian default is kept and marked unconfirmed in ADR 0004.
Aligning documents with the three goals and the junior audience was split off into P1-065.
