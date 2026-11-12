---
id: P1-031
title: "Panduan gaya dan aturan anti-bocor soal"
milestone: M3
type: content
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-024]
estimate: 1
outputs:
  - docs/conventions/writing-style.md
---

## Konteks

Keluhan nyata di aplikasi sejenis: judul soal membocorkan jawaban dan konten terasa buatan AI.

## Tugas

1. Finalkan panduan gaya dengan contoh baik/buruk untuk lesson dan soal.
2. Tambahkan heuristik anti-bocor yang bisa dicek otomatis (mis. opsi benar paling panjang di > 40% soal sebuah konsep) ke validator sebagai peringatan.

## Kriteria selesai

- [ ] Panduan final dengan ≥ 5 contoh baik/buruk
- [ ] Heuristik anti-bocor ada di validator
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
