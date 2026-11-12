---
id: P1-060
title: "Audit sitasi dan tautan mati"
milestone: M5
type: review
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-040, P1-041, P1-042, P1-043, P1-044, P1-045]
estimate: 1
outputs:
  - references/registry.yaml
  - docs/audit-sitasi.md
---

## Konteks

Sebelum freeze, pastikan semua rujukan valid.

## Tugas

1. Cek setiap URL di registry masih hidup; perbaiki/ganti.
2. Cek semua konten published hanya mengutip sumber approved.

## Kriteria selesai

- [ ] Laporan audit di `docs/audit-sitasi.md`
- [ ] Tidak ada tautan mati yang belum ditangani
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
