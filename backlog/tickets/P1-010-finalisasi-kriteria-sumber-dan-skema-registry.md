---
id: P1-010
title: "Finalisasi kriteria sumber dan skema registry"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-001]
estimate: 1
outputs:
  - docs/conventions/research-protocol.md
  - docs/conventions/content-schema.md
  - scripts/validate.py
---

## Konteks

Kriteria dan skema v0 sudah ada. Sebelum riset massal, pastikan skema menangkap semua yang dibutuhkan audit dan aplikasi nanti.

## Tugas

1. Review research-protocol.md dan skema registry; uji dengan 5 entri seed yang beragam (buku, paper, postmortem, repo, Tier 6).
2. Tambahkan field yang kurang (mis. `free_companion` untuk sumber berbayar) dan aturan validator yang sesuai.
3. Pastikan validator memberi pesan error yang jelas.

## Kriteria selesai

- [ ] Skema final terdokumentasi
- [ ] Validator mengecek semua aturan skema
- [ ] Entri seed lolos validasi
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
