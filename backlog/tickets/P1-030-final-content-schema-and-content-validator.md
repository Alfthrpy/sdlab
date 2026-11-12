---
id: P1-030
title: "Final content schema and content validator"
milestone: M3
type: infra
owner: agent
review: agent
status: todo
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

- [ ] Final schema
- [ ] Validator enforces the content schema
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
