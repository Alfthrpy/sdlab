---
id: P1-062
title: "Kalibrasi tingkat kesulitan soal"
milestone: M5
type: review
owner: agent
review: agent
status: todo
priority: low
depends_on: [P1-040, P1-041, P1-042]
estimate: 1
outputs:
  - content/concepts/
---

## Konteks

Distribusi kesulitan harus seimbang dan soal tidak bocor.

## Tugas

1. Hitung distribusi difficulty per konsep dan unit.
2. Jalankan heuristik anti-bocor; perbaiki soal yang tertandai.

## Kriteria selesai

- [ ] Distribusi kesulitan tercatat
- [ ] Tidak ada peringatan anti-bocor tersisa
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
