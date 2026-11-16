---
id: P1-030
title: "Final content schema and content validator"
milestone: M3
type: infra
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-024]
estimate: 1
outputs:
  - docs/conventions/content-schema.md
  - scripts/validate.py
---

## Context

The v0 content schema (lesson, questions, misconceptions) is still a draft.

## Tasks

1. Finalize the schema for `lesson.md`, `questions.yaml`, `misconceptions.md`.
2. Validator: frontmatter, question types & answer format, unique question ids, valid sources, lesson length 300–600 words, every learning objective covered by ≥ 1 question (via an `objective` field).

## Done criteria

- [x] Final schema
- [x] Validator enforces the content schema
- [x] `python scripts/validate.py` passes

## Notes

- Schema final in `docs/conventions/content-schema.md` §4: lesson frontmatter (`concept` = folder name, `status` draft|review|published, `reviewed_by` when published), question types with answer formats (mcq, multi, order, match with `pairs`, estimate with `unit`), `difficulty` 1-3, new `objective` field (1-based index into the concept's objectives), `misconceptions.md` format (`## <kebab-id>` with two labels).
- Validator (`scripts/validate.py`): stage-dependent strictness. `draft` gaps warn; from `review` on, lesson length outside 300-600 words, fewer than 6 questions, an uncovered learning objective, a question without `objective`, a missing `misconceptions.md` and fewer than 3 misconceptions are errors. Word count method documented (fences, `[^id]` markers and URLs excluded).
- Tests: 75 pass (`tests/test_content.py` grew from 45 to 75 incl. malformed-structure, boundary and answer-format cases).
- Review (general-purpose agent, independent): main finding was tracebacks on malformed YAML (non-mapping questions, unhashable ids/types/sources, list frontmatter). All fixed and covered by regression tests; a fuzz harness found 0 crashes afterwards. Also fixed: `difficulty: true/2.0` accepted, non-kebab misconception headings ignored, code-fenced labels counting, doc/code mismatches.
- Not covered: `lab.yaml`, incident and case-study content formats (P1-033); question wording and anti-leak rules beyond the existing option-length warning (P1-031). Existing curriculum validators still crash on some malformed YAML (P1-066).
- Writer instruction `.claude/agents/content-writer.md` updated to use `objective` and the new formats.
