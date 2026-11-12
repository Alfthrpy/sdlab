# Phase 1 Plan — Materials

**Goal:** produce v1 materials ready for the application: about 46 concepts (7 units), 340 questions, 16 lab specs, 8 incidents, and 6 case studies. Every claim is sourced from the verified Reference Registry.

**Audience and goals:** students and junior engineers, with three equal goals: understand production-scale systems, learn new things, and prepare for system design interviews ([ADR 0004](decisions/0004-audience-and-goals.md)). Content assumes low prior knowledge (basic programming, HTTP, basic SQL) and explains the "why" before the "what". Case studies serve both interview goals: practice designing a system, and practice explaining a design within a time limit.

**How we work:** agent-heavy. Agents do research, mapping, and drafting. Other agents review without having done the work. The repo owner (human) only decides at milestone gates, runs user tests, and spot-checks quality. Flow details are in [workflow.md](workflow.md).

**Scope note:** the extra lab spec is for Unit 0 (for example a "limits of one machine" lab). Unit 0 may pass gate G0 through official documentation where Tier 1–3 sources are scarce.

**Estimated duration:** 24 weeks for the full volume (22 before the Unit 0 addition in ADR 0004 Amendment 1). M1–M3 (about 6–7 weeks) is the critical path. M4 can be sped up by adding parallel agent sessions per unit.

## Milestones and gates

| Milestone | Contents | Weeks | Exit gate (decided by a human) |
| --- | --- | --- | --- |
| **M0** Foundation | Repo, workflow, base decisions | 1 | Language, audience, and reviewer decisions recorded in ADRs |
| **M1** Reference Registry | Criteria, candidate research per unit, license & version verification, gap map | 1–2 | **G0:** every unit has ≥1 Tier 1–2 source and ≥1 Tier 3–4 |
| **M2** Curriculum | ~46 concepts + learning objectives and triggers, prerequisite graph, case studies & incidents, source mapping | 3–6 | **G1:** valid DAG, each concept has an objective + ≥2 sources |
| **M3** Pedagogy & pilot | Content schema + validator, style guide, "caching" pilot in all formats, test with 5 people | 6–7 | **G2:** pilot tested, templates revised |
| **M4** Production | 7 content units (Units 0–6), incident pack, case-study pack | 8–24 | Per unit: passes agent review + human sample |
| **M5** QA & freeze | Citation audit, plagiarism audit, question calibration, content v1 release | 23–24 | **G3:** content v1 frozen (tag `content-v1.0`) |

## M4 production order

Units are done by differentiating value and dependencies:

0. **Unit 0 Single-server backend.** The bottom rung of the growth ladder; Unit 1 builds on it.
1. **Unit 1 Foundations.** All later units need it.
2. **Unit 2 Building blocks.** Basis for the first lab.
3. **Unit 6 Production reliability.** Main differentiator (retry storm, metastable, real incidents), and closest to the simulator.
4. **Unit 3 Data.**
5. **Unit 4 Async & streams.**
6. **Unit 5 Consistency & coordination.**

The incident and case-study packs run in parallel once the units they need are done.

The epic tickets per unit (`P1-040` onward) are split by the agent into one sub-ticket per concept when the unit starts, using `scripts/new_ticket.py`.

## Division of work

| | Agent | Human |
| --- | --- | --- |
| Initial ticket count | 31 + 3 added for Unit 0 (P1-048, P1-068, P1-069) | 7 |
| Kind | Research, mapping, curriculum, schemas, drafting, cross-review, automated QA | Base decisions, 3 gates, pilot test, QA spot-check |
| Estimated human time | — | 2–4 hours per gate, ~1 hour/week spot-check |

## Final outputs of Phase 1

```
references/registry.yaml          ~150 sources, status approved, license & version recorded
references/notes/*.md             reading notes per main source
curriculum/concepts.yaml          ~46 concepts, learning objectives, triggers, prerequisites, sources
curriculum/case-studies.yaml      20–25 selected case studies & incidents
content/concepts/<id>/            lesson.md, questions.yaml, lab.yaml (optional), misconceptions.md
content/incidents/<id>.md         8 incident scenarios from public postmortems
content/case-studies/<id>.md      6 case studies with rubrics
```

The format of each file is defined in [conventions/content-schema.md](conventions/content-schema.md) and checked by `scripts/validate.py`.

## Phase 1 risks

| Risk | Mitigation |
| --- | --- |
| Agent invents sources or URLs | "Open first, then record" rule in AGENTS.md, mandatory `accessed` field, `source-verifier` reviewer reopens every new URL |
| Content too close to sources | Rewriting guide, similarity check in M5 QA, ban on copying diagrams |
| Content feels "AI-made" | Style guide (concrete examples, sourced numbers, no filler), human pilot test at G2 |
| Slow production | Parallel agent sessions per unit after G2 |
| Gates stalled waiting for a human | Agent prepares a ready-to-approve decision summary in each gate ticket |

## Ticket list

Current status is always in [../backlog/BOARD.md](../backlog/BOARD.md). Initial list:

**M0 Foundation**
- P1-001 Set up repo & workflow — agent (done)
- P1-002 Decision: content language & target audience — **human**
- P1-003 Decision: working name & technical reviewer — **human**
- P1-004 Mirror backlog to GitHub Projects (optional) — agent

**M1 Reference Registry** (P1-068 first: defines the growth ladder and Unit 0)
- P1-010 Finalize registry criteria & schema — agent
- P1-011 to P1-015 Candidate research for Units 1–6 (5 tickets) — agent
- P1-069 Candidate research for Unit 0 (single-server backend) — agent
- P1-016 Verify license & version of all candidates — agent
- P1-017 Source → topic map & gap list — agent
- P1-018 Final citation & attribution guide — agent
- P1-019 **G0** Approve Registry v1 — **human**

**M2 Curriculum**
- P1-020 Concept list v0 with learning objectives — agent
- P1-021 Prerequisite graph & DAG validation — agent
- P1-022 Choose case studies & incidents — agent
- P1-023 Concept → source mapping — agent
- P1-024 **G1** Approve curriculum — **human**

**M3 Pedagogy & pilot**
- P1-030 Content schema & validator — agent
- P1-031 Style guide & anti-leak rules for questions — agent
- P1-032 "Caching" concept pilot in all formats — agent
- P1-033 Lab & incident spec format — agent
- P1-034 **G2** Pilot test with 5 target users — **human**
- P1-035 Revise templates from pilot results — agent

**M4 Production** (epics, split per concept when started)
- P1-048 Unit 0 Single-server backend
- P1-040 Unit 1 Foundations
- P1-041 Unit 2 Building blocks
- P1-042 Unit 6 Production reliability
- P1-043 Unit 3 Data
- P1-044 Unit 4 Async & streams
- P1-045 Unit 5 Consistency & coordination
- P1-046 Incident pack (8)
- P1-047 Case-study pack (6)

**M5 QA & freeze**
- P1-060 Citation & dead-link audit — agent
- P1-061 Text-similarity audit against sources — agent
- P1-062 Question difficulty calibration — agent
- P1-063 Content sample spot-check — **human**
- P1-064 **G3** Freeze content v1 — **human**
