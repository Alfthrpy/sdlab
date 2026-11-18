---
id: P1-086
title: "Reader layering: core lesson + Lebih dalam section, term budget, cold-read gate"
milestone: M4
type: infra
owner: agent
review: human
status: review
priority: high
depends_on: []
estimate: 1
outputs: []
---

## Context

P1-048b (`app-plus-database`) passed accuracy review but the owner found the lesson hard to follow even for them. Analysis: (1) two unrelated ideas in one lesson; (2) caveats added for every reviewer finding piled up as chains inside the core, raising sentence length from 12.5 to 17 words per sentence; (3) no story spine, sourced numbers interrupted the worked example; (4) about 10 new terms in about 590 words; (5) no review gate asked "can a newcomer follow this in one read?". Unit 0 must work for beginners, practitioners and seniors. Owner decisions (2026-11-18): keep one concept with two light stages, and add a core + "Lebih dalam" layer.

## Tasks

1. Validator: `## Lebih dalam` section (cap 250 words, excluded from the core count); readability warnings (more than 6 italic terms, average sentence over 16 words); fixture tests.
2. Conventions: writing-style.md (two reading layers, story spine, term budget, sentence shape, cold-read gate), content-schema.md, lesson template.
3. Agents: new `cold-reader`; content-writer writes the two layers; content-reviewer gets a readability check; AGENTS.md table and workflow.md step 6.
4. Add the cold-read gate to the Tasks of the Unit 0 content tickets (048b–h).
5. Rewrite `app-plus-database` under P1-048b with the new rules (separate PR).

## Done criteria

- [x] Validator checks and fixture tests added; `python -m unittest discover tests` passes
- [x] Conventions, template, agents, workflow and AGENTS.md updated
- [x] Cold-read gate added to the Unit 0 content tickets
- [x] `python scripts/validate.py` passes
- [ ] Owner approves the convention (review: human)

## Notes

Thresholds are starting points, not measured: 6 italic terms and 16 words per sentence are set from the two Unit 0 lessons written so far (`request-lifecycle` 9 terms, 12.5 words/sentence; `app-plus-database` 8 terms, 17 words/sentence). The new check already warns on `request-lifecycle` and `caching-basics` (term count), so those two should be re-read with the `cold-reader` before Unit 0 ships. Task 5 (rewrite of `app-plus-database`) is done under P1-048b, not here. Decision for the owner: the term and sentence limits and the 250-word cap on `## Lebih dalam`.
