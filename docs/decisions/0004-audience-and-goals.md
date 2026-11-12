# ADR 0004 — Target audience and learning goals

- **Status:** accepted
- **Date:** 2026-11-12
- **Ticket:** P1-002 (decision by the owner)

## Decision

| Item | Decision |
| --- | --- |
| Target audience | **Students and junior engineers.** Replaces "junior–mid + final-year students" from ADR 0003. |
| Main goals | **Three equal goals:** (1) understand production-scale systems, (2) learn new things, (3) system design interview prep. |
| Content language | **Indonesian**, technical terms stay in English (see `writing-style.md`). The owner has not stated a language choice explicitly, so this is still the ADR 0003 default and can change at any time. Agent-facing text is English (see [ADR 0005](0005-agent-facing-language.md)). |

## Consequences for content

1. **Assume low prior knowledge.** Readers know basic programming, HTTP, and basic SQL, but have never operated a distributed system. Terms are explained on first use, and Unit 1 assumes no background beyond that. The list of prerequisite knowledge is written in the curriculum.
2. **"Why" matters more than "what".** Every concept explains the problem it solves, what breaks without it, and the price paid. This serves all three goals: production understanding, learning new things, and being able to explain trade-offs in an interview.
3. **Real-system examples** (incidents, postmortems, papers, engineering articles) are the backbone of the material. This serves goals 1 and 2, and gives concrete stories for goal 3.
4. **The interview goal is served through format, not content.** Content stays based on primary sources. Case studies and a delivery framework (requirements, estimation, design, deep dive, trade-offs) are kept as one practice format. Tier 6 sources stay `map-only` (ADR 0002) and are used to check topic coverage and common questions.
5. **Case studies have two purposes:** practice designing systems in general, and practice explaining a design within a time limit. Rubrics and time frames must cover both (follow-up ticket below).
6. **Difficulty** of questions and labs is calibrated for juniors. A level-3 question means "challenging for a junior", not equivalent to a senior question.

## Follow-ups

- **P1-065** aligns documents and tickets with the three goals and the junior audience: `docs/PLAN-PHASE-1.md`, `docs/ROADMAP.md`, `docs/conventions/writing-style.md`, `curriculum/README.md`, tickets P1-022 and P1-047, and the subagent descriptions.
- ADR 0003 status updated for the language and audience rows. The name, reviewer, and license rows still wait on P1-003.
