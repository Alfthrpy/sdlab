# ADR 0007 — Beta-first: the owner is the only tester, Unit 0 ships first

- **Status:** accepted
- **Date:** 2026-11-16
- **Decided by:** the owner, in chat, after reading the P1-032 pilot lesson (`content/concepts/caching-basics/`).

## Context

The pilot concept (`caching-basics`) passed two independent agent reviews and the owner's own read. The plan said to test it with 5 target users (G2, P1-034) before mass production. The owner prefers to move faster: the product is not ready for other people yet, and the owner can act as the beta tester once lessons, quizzes and labs run in an app.

## Decision

1. **Beta-first.** The owner is the only tester for now. Content is not shown to other people yet.
2. **G2 (P1-034) is deferred, not cancelled.** The 5-user test happens after a usable beta exists. It no longer blocks P1-035 or M4.
3. **Unit 0 first.** Unit 0 (Single-server backend, 8 concepts) is produced and shipped first (P1-048). The other units are produced alongside later, "as we go".
4. **Next goal: a working lab and quiz.** Build the application and simulator far enough that a quiz and a lab for Unit 0 run end to end for the owner. The technical plan is the existing **STUD Simulator Master Plan** (Claude Docs, 2026-11-13); this ADR does not replace it. The product is meant to run for real, so the stack follows that plan and is not a throwaway prototype (see below).
5. **Public decisions wait.** The name, content license and public technical reviewer (P1-003) stay at the ADR 0003 interim defaults and do not block anything until the content is shown outside.

## Stack and plan (from the STUD Simulator Master Plan)

- Decisions already confirmed there: usable on mobile is the only hard constraint (D6); the simulation runs client-side, a server is allowed only if the owner's Render free plan can carry it (D7); grading is rule-based with no LLM (D11); v1 interaction modes are tune, diagnose and fix, and constrained build (D2).
- Architecture: a separate repo, `stud-sim`, with four layers (contract, engine, lab runtime, UI) and a TypeScript discrete-event engine running in a Worker; `sdlab` owns what is taught and vendors the contract, `stud-sim` owns what can be simulated.
- Milestones there: S0 bootstrap and spikes (SG0 go/no-go, build vs adopt), S1 contract v0, S2 caching vertical slice, S3 engine complete, S4 labs per unit (M4 order: Units 0, 1, 2, 6, 3, 4, 5), S5 incidents, QA and release.
- **Changed by this ADR:** the plan's G2 gate (week 9, a running caching lab piloted with 5 users) becomes "a running caching lab that the owner tests alone". The 5-user pilot moves to before any public beta. The plan's M4 order is kept, but Unit 0 production and its one lab (D4) come first for shipping.
- **Open:** where the code lives. The plan says a new repo (`stud-sim`); the owner said "later" (2026-11-16). Nothing is created until the owner decides.

## Consequences

- Changing content after the app exists is more expensive than before it exists (formats, lab specs). The owner accepts that cost.
- P1-035 (revise templates from pilot results) now depends on P1-032 instead of P1-034. The pilot's obstacle list in the P1-032 Notes is its input. P1-033 (lab and incident spec) matters more: the lab spec must fit what the simulator will actually do.
- `AGENTS.md` ("no application code yet") stays true for this repo until the owner decides where the application code lives; the simulator work happens in `stud-sim` per the master plan.
- Phase 2 and Phase 3 do not need new plan documents now: the master plan covers the simulator. The learner-facing application (lessons, quiz, progress) is covered only in outline there and needs its own plan before building.
- Quality gates for public release stay: G2 before any public beta, G3 before content v1.
