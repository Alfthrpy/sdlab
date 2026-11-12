---
id: P1-043
title: "EPIC Produksi Unit 3"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-035]
estimate: 6
outputs:
  - content/concepts/
---

## Konteks

Produksi konten Unit 3: Data (model data, indeks, replikasi, partisi, transaksi & isolasi). Ini epic: pecah dulu sebelum dikerjakan.

## Tugas

1. Sesi pertama: buat satu sub-ticket per konsep unit ini (`python scripts/new_ticket.py ... --depends P1-043`), id `P1-043a`, `P1-043b`, dst. Set epic `in-progress`.
2. Setiap sub-ticket: content-writer → content-reviewer → perbaikan → PR.
3. Setelah semua sub-ticket done: tandai 2 konsep acak untuk spot-check human di P1-063.

## Kriteria selesai

- [ ] Semua konsep unit ini berstatus `review` atau `published` di concepts.yaml
- [ ] Semua sub-ticket done
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
