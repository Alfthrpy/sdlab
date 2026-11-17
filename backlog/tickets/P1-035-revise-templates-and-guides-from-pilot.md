---
id: P1-035
title: "Revise templates and guides from pilot results"
milestone: M3
type: content
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-032]
estimate: 1
outputs:
  - docs/conventions/
  - templates/
  - content/concepts/caching-basics/
---

## Context

Apply the lessons from the pilot before M4.

## Tasks

1. Group pilot feedback into template/guide/validator changes.
2. Apply them, then update the caching pilot.
3. Update per-concept production estimates in PLAN-PHASE-1.

## Done criteria

- [x] Every piece of pilot feedback has a follow-up (applied, or rejected with a reason)
- [x] `python scripts/validate.py` passes

## Notes

Follow-up per item of the P1-032 "Obstacles and lessons" list:

1. Inverted claim from the source: content-writer step 2 (re-read the exact source sentence), content-reviewer check 1 (look for inverted claims), research-protocol (raw page, not summary). Applied.
2. Own reasoning next to a source marker: handled before this ticket (citation-guide "Do not narrate where a statement comes from", `check_provenance` warning). Verified.
3. Leaky questions the validator cannot see: writing-style rules 12 (odd-one-out shape) and 13 (estimate ranges that accept the wrong result), writer step 6, reviewer check 4. Manual checks; applied.
4. Questions on untaught material or without a source: writing-style rule 14, new validator warning for a question with no `sources` unless `own_computation: true` (pilot q07-q09 marked), warning when both are set. Applied.
5. Objective wording vs sources: curriculum-designer principle, content-writer step 2 (objective check, gap becomes a ticket). Applied.
6. Lesson length: `python scripts/validate.py --stats` (word count by the validator's method, plus question and misconception counts); aim for about 500 words. Applied.
7. No reading notes for sources: researcher step 5 and research-protocol now require notes for every source mapped to a concept. Backfill for Unit 0 is a new ticket, P1-035a (20 of 28 sources lack notes), now a dependency of P1-048. Units 1-6 sources are not backfilled; each unit epic should schedule a notes pass when it starts.
8. Schema friction: `order` answer example added (a 3-cycle, so a mix-up between "position of each option" and "option at each position" shows); `match` per-pair misconception links rejected (no pilot question needed them, and they add a second answer structure). Lab format: see 9.
9. Lab format invented fields: handled by P1-033 (content-schema section 5 is final; pilot lab uses it). Verified.
10. WebFetch summaries and truncation: research-protocol, writer step 2 and reviewer check 1 say to confirm exact wording and numbers on the raw page. Applied.

Also done: per-concept production estimate in `docs/PLAN-PHASE-1.md` (about 15-20 minutes of agent time per concept; 50 concepts in total, 42 in Units 1-6), and the `--stats` command in AGENTS.md. Note: the P1-032 notes say "Units 1-6 have 50 concepts"; 50 is the total with Unit 0.

Review: content-reviewer (independent run), conclusion pass with minor fixes. Fixed: the `order` example was its own inverse (now a 3-cycle), the estimate table wrongly put `caching-basics` in Unit 0 (it is Unit 2), notes backfill ticket created, `own_computation` plus `sources` warning, `--stats` test and AGENTS.md entry, the unmeasured "almost linearly" speed-up claim softened. Not done: a validator warning for concepts at `review` whose sources lack notes (left as an idea for P1-035a).

