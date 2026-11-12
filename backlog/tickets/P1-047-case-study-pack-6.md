---
id: P1-047
title: "Case-study pack (6)"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-040, P1-041, P1-043]
estimate: 4
outputs:
  - content/case-studies/
---

## Context

Long case studies in the style of interview questions, with a 5-criterion rubric (problem understanding, requirements analysis, components, architecture, mitigation & trade-offs). They serve two goals (ADR 0004): practice designing a system, and practice explaining a design within a limited time. The rubric and time frame must cover both.

## Tasks

1. Choose 6 from the candidates in case-studies.yaml.
2. Per case study: prompt, discoverable requirements, estimation, one or two reference designs with trade-offs, grading rubric, and a suggested time frame for a time-boxed explanation (e.g. requirements, estimation, design, deep dive, trade-offs, with minutes per phase).
3. Split into one sub-ticket per case study.

## Done criteria

- [ ] Each case study has a rubric for design quality and a time frame for time-boxed explanation
- [ ] 6 case studies pass the validator and content-reviewer
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
