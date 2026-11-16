---
id: P1-032
title: "Pilot the 'caching' concept in all formats"
milestone: M3
type: content
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-030, P1-031]
estimate: 2
outputs:
  - content/concepts/caching-basics/
---

## Context

A pilot to test templates and the production flow before mass production. The concept id follows `curriculum/concepts.yaml`.

## Tasks

1. Do it with the `content-writer` subagent: misconceptions, lesson, 8–10 questions, lab.yaml (draft spec).
2. Review with `content-reviewer`, fix.
3. Record time and production obstacles in the Notes (input for M4 estimates).

## Done criteria

- [x] All concept files are complete and pass the validator
- [x] `content-reviewer` passes (second pass: pass with minor fixes, all fixed; no third review)
- [x] Time & production obstacles recorded
- [x] `python scripts/validate.py` passes

## Notes

Output: `content/concepts/caching-basics/` (`lesson.md` 575 words by the validator's method, `questions.yaml` 10 questions, `misconceptions.md` 6, `lab.yaml` draft). Validator 0 errors, no warnings for these files; 100 tests pass.

**Production flow actually used:** content-writer (draft) -> content-reviewer (pass 1: many findings, "closer to fail on the question set") -> content-writer (fixes) -> content-reviewer (pass 2: pass with minor fixes) -> content-writer (fixes) -> my own check. Five subagent runs for one concept.

**Time.** Wall clock from claim to final check: about 16 minutes (13:53 to 14:09, 2026-11-16). Subagent run times: writer 2 min 40 s, reviewer 1 2 min 10 s, fix 1 4 min 30 s, reviewer 2 2 min 6 s, fix 2 2 min 50 s, i.e. about 14 minutes of agent time. The writer's own report estimated "45-50 min of effort"; that figure is not measured time and should not be used for M4 estimates. Rough M4 planning figure: about 15-20 minutes of agent time per concept for a full lesson + questions + misconceptions pass with two review rounds, plus owner review time that this pilot did not measure. Units 1-6 have 50 concepts, so about 12-17 hours of agent time (before parallelism), mostly bounded by review rounds, not writing.

**Obstacles and lessons for M4 (input to P1-035):**
1. Review pass 1 found a claim inverted from the source (the lesson said caches lack read-through/write-through; Azure says many have them). Instruct writers to re-read the exact sentence before rewording. A reviewer who reopens sources is essential; the validator cannot see it.
2. Own reasoning vs source claims: sentences that are the author's inference ("database-first narrows the race") sat next to an Azure marker, so a reader could take them as the source's claim. The first fix labelled them in the text ("penalaran penulis", "bukan dari sumber", "hitungan sendiri"). **The owner rejected that style** (2026-11-16): provenance narration in learner text reads like a disclaimer. Rule now (citation-guide.md "Do not narrate where a statement comes from"): the `[^id]` marker is the only provenance signal, the author's own reasoning and arithmetic are plain sentences without a marker, worked examples open with "Misalkan ...", and the validator warns on the narrating phrases. The reviewer, not the text, checks that unmarked claims are the author's own.
3. Questions leaked in ways the validator cannot see: the correct option the only one explained or the only one not starting with a common word (odd-one-out), prompt keywords echoing the answer, and estimate ranges that accepted the common wrong result (7.6 inside 7.5-8.5). Writers should check each estimate by computing the wrong-method result, and each mcq for odd-one-out shape.
4. Questions that test untaught material (HTTP directives not in the lesson; `no-store`) and questions that do not fit the tagged objective. The `objective` field exposed this only because reviewers checked it; consider a validator warning when a question's `sources` is empty yet it has an `objective` (arithmetic questions need an explicit "hitungan sendiri").
5. Source material did not support everything the objectives promise: write-back (see P1-081) and hit-ratio arithmetic (needed own labelled computation, accepted as an explicit own-computation policy). Check "objective wording vs sources" at the curriculum stage for every concept before writing (cheap) so gaps surface early.
6. The lesson length limit is tight: the first draft was 554 words, after fixes 575; adding explanations pushes against 600. The writer cannot preview the count (it used a throwaway script). Suggest `python scripts/validate.py --stats` or a small helper (candidate for P1-035).
7. No reading notes existed for 3 of the 4 sources, so the writer fetched pages itself (the biggest time cost). Researchers should write reading notes for any source mapped to a concept in Units with epics (P1-040..045).
8. Schema friction: `match` has no per-option misconception link; `order` answer is a list of indexes in sequence order (easy to invert); the lab format is not final (P1-033), so the lab is a draft with invented fields.
9. Lab draft fields invented (scenario, initial_state, parameters, simulator_must_model, metrics, goal, failure_injection, hints, grading, debrief). P1-033 should decide: simulation seed and time scale, an event timeline for failure injection, whether the score comes from metrics or explicit checks, and a shared latency model between lesson formulas and the simulator. The lab's own calibration note (a 5000-key LRU over 50000 Zipf keys tops out near an ideal hit ratio of about 80%, while the goal needs about 82%) is arithmetic by the author, verified by the reviewer, not simulator-tested.
10. WebFetch returns summaries, and the RFC page was truncated, so exact quotes cannot be verified; the lesson uses no direct quotes.

**Follow-up after owner feedback:** the pilot content was rewritten to drop the provenance labels; validator warning and guide/agent rules added (104 tests pass).

**Not met / open:** objective 1 is only partly met (write-back): see P1-081. The owner has not yet read the pilot content; G2 (P1-034, test with 5 target users) is the human check. The owner's decisions P1-003 (content license) should come before the pilot is shown outside.
