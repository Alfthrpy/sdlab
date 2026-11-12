---
id: P1-065
title: "Align documents with junior audience and three goals"
milestone: M0
type: curriculum
owner: agent
review: agent
status: done
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

- [x] Audience and goals in all documents are consistent with ADR 0004
- [x] Reader prerequisite knowledge is written in `curriculum/README.md`
- [x] P1-022 and P1-047 mention both case-study goals
- [x] `python scripts/validate.py` passes

## Notes

- Audience and goals now stated in AGENTS.md, ROADMAP.md, PLAN-PHASE-1.md, writing-style.md, and the curriculum-designer, content-writer, and content-reviewer subagents. 'junior–mid' replaced by 'students and junior engineers' (also in P1-034).
- `curriculum/README.md` has a "Reader prerequisite knowledge" section (basic programming, HTTP, basic SQL); Unit 1 assumes nothing else. The curriculum-designer subagent now enforces this.
- `writing-style.md` has the difficulty table (level 3 = challenging for a junior) and a rule that every concept mixes levels.
- P1-022 and P1-047 now state both case-study goals; P1-047 also requires a rubric plus a time frame. `content-schema.md` §5 notes this for case-study files.
- Deliberately unchanged: ADR 0002 (Tier 6 stays `map-only`), ADR 0003/0004, `research-protocol.md` Tier 6 row, and the registry. The interview goal is served by format, not by copying interview-prep content.
