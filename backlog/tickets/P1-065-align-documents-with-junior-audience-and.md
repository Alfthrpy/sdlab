---
id: P1-065
title: "Align documents with junior audience and three goals"
milestone: M0
type: curriculum
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-002]
estimate: 1
outputs:
  - docs/PLAN-PHASE-1.md
  - docs/ROADMAP.md
  - docs/conventions/writing-style.md
  - curriculum/README.md
---

## Context

ADR 0004 sets the audience to students and junior engineers with three equal goals: understand production-scale systems, learn new things, and interview prep. Documents written before this decision assume junior–mid, and some describe the goal as only interview prep or only production understanding. They need aligning before research (M1) and curriculum (M2) run in full. Note: all these documents were translated to English on 2026-11-12 (ADR 0005); this ticket works on the English text.

## Tasks

1. Check and adjust mentions of audience and goals in: `docs/PLAN-PHASE-1.md`, `docs/ROADMAP.md`, `docs/conventions/*.md`, `curriculum/README.md`, `.claude/agents/*.md`, `AGENTS.md`. Replace the 'junior–mid' assumption with 'students and junior engineers'.
2. Add a 'Reader prerequisite knowledge' section in `curriculum/README.md` (basic programming, HTTP, basic SQL) and a rule that Unit 1 assumes nothing else.
3. In tickets P1-022 and P1-047, make sure case studies serve two goals: practice designing systems, and practice explaining a design under time limits. The rubric and time frame cover both.
4. In `writing-style.md`, write the question difficulty rule: level 3 means challenging for a junior.
5. Do not change ADR 0002 (Tier 6 stays `map-only`). Note in the Notes section what was deliberately left unchanged.

## Done criteria

- [ ] Audience and goals in all documents are consistent with ADR 0004
- [ ] Reader prerequisite knowledge is written in `curriculum/README.md`
- [ ] P1-022 and P1-047 mention both case-study goals
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
