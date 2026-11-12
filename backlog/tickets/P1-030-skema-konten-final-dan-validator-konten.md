---
id: P1-030
title: "Skema konten final dan validator konten"
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

## Konteks

Skema konten v0 (lesson, questions, misconceptions) masih draft.

## Tugas

1. Finalkan skema `lesson.md`, `questions.yaml`, `misconceptions.md`.
2. Validator: frontmatter, tipe soal & format jawaban, id soal unik, sumber valid, panjang lesson 300–600 kata, setiap tujuan belajar ter-cover ≥ 1 soal (via field `objective`).

## Kriteria selesai

- [ ] Skema final
- [ ] Validator menegakkan skema konten
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
