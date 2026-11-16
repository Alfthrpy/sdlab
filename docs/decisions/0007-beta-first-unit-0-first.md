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
4. **Next goal: a working lab and quiz.** Build the application and simulator far enough that a quiz and a lab for Unit 0 run end to end for the owner. This starts Phase 2 (simulation) and Phase 3 (application) work in this repo; the plans for those phases are written next.
5. **Public decisions wait.** The name, content license and public technical reviewer (P1-003) stay at the ADR 0003 interim defaults and do not block anything until the content is shown outside.

## Consequences

- Changing content after the app exists is more expensive than before it exists (formats, lab specs). The owner accepts that cost.
- P1-035 (revise templates from pilot results) now depends on P1-032 instead of P1-034. The pilot's obstacle list in the P1-032 Notes is its input. P1-033 (lab and incident spec) matters more: the lab spec must fit what the simulator will actually do.
- `AGENTS.md` ("no application code yet") and `docs/ROADMAP.md` are revised once the stack decision is made.
- The Phase 2 and Phase 3 plan documents are still to be written (they were due when Phase 1 reached M3).
- Quality gates for public release stay: G2 before any public beta, G3 before content v1.
