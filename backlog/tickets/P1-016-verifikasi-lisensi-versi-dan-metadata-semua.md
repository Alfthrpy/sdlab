---
id: P1-016
title: "Verifikasi lisensi, versi, dan metadata semua kandidat"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-011, P1-012, P1-013, P1-014, P1-015]
estimate: 2
outputs:
  - references/registry.yaml
---

## Konteks

Termasuk 11 entri SEED dari riset awal yang sebagian metadatanya berasal dari hasil pencarian.

## Tugas

1. Buka ulang setiap entri (prioritas: SEED dan Tier 1–3).
2. Lengkapi `authors`, `published`, `edition`, URL kanonik, dan `license` dari halaman sumber.
3. Cek edisi/versi terbaru; tandai yang usang `deprecated`.
4. Untuk sumber `paywalled`, catat sumber pendamping gratis.

## Kriteria selesai

- [ ] Tidak ada entri dengan `published` atau `authors` kosong kecuali memang tidak tersedia (dijelaskan di notes)
- [ ] Tidak ada `license: unknown` tanpa penjelasan
- [ ] Semua catatan 'SEED' dihapus atau diselesaikan
- [ ] `source-verifier` lolos
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
