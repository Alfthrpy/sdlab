# ADR 0004 — Target audience and learning goals

- **Status:** accepted
- **Date:** 2026-11-12
- **Ticket:** P1-002 (decision by the owner); amended 2026-11-12 (see Amendment 1)

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

## Amendment 1 — solo developers, beginners, and the growth ladder

- **Date:** 2026-11-12
- **Decided by:** the owner, in chat, outside the ticket flow. Follow-up work is ticket P1-068.

### Decision

| Item | Amendment |
| --- | --- |
| Target audience | Extended: **students, junior engineers, and solo developers or beginners starting backend work.** The row above stays valid; this adds to it. |
| Framing | The course is taught as a **growth ladder**: start from a single-server backend (one app, one database), and introduce each distributed-systems concept as what you reach for when the previous stage stops being enough. Distributed systems remain the core of Units 3–6, but they are no longer presented as the starting point. |
| Scope | The course stays **backend system design**. It is not a pure distributed-systems course, and still excludes frontend, mobile, ML system design, and low-level/OOP design. |

### Consequences

1. **A new starting unit** covers the single-server backend: one database, indexes, connection pooling, backups, deploys, and basic monitoring. Its exact scope, name, and numbering are decided in P1-068.
2. **Each concept in Units 1–6 names its trigger** (Unit 0 is the baseline and may omit it; a missing trigger is a warning until the concept reaches `review`, then an error): the symptom or number that says "it is time to use this" (and, through the existing trade-off section, when not to). Triggers also feed questions and labs.
3. **Honest anti-over-engineering.** Lessons say plainly when the simpler stage is enough. This serves goals 1 and 2 and keeps the interview goal intact.
4. **Reader prerequisites stay as in `curriculum/README.md`.** The new unit must not assume more than those prerequisites.
5. **Costs accepted:** scope and duration grow beyond the ±22 weeks in `docs/PLAN-PHASE-1.md` (P1-068 re-estimates), and sources for "start small" material are scarcer at Tier 1–3, so research must look for them deliberately.
6. **Research waits for P1-068.** P1-011 through P1-015 now depend on it, so the new unit is covered by sources from the start.
