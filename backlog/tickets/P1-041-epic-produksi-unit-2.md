---
id: P1-041
title: "EPIC Produksi Unit 2"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-035]
estimate: 6
outputs:
  - content/concepts/
---

## Konteks

Produksi konten Unit 2: Building blocks (load balancer, reverse proxy, cache, CDN, API REST/gRPC, idempotency). Ini epic: pecah dulu sebelum dikerjakan.

## Tugas

1. Sesi pertama: buat satu sub-ticket per konsep unit ini (`python scripts/new_ticket.py ... --depends P1-041`), id `P1-041a`, `P1-041b`, dst. Set epic `in-progress`.
2. Setiap sub-ticket: content-writer → content-reviewer → perbaikan → PR.
3. Setelah semua sub-ticket done: tandai 2 konsep acak untuk spot-check human di P1-063.

## Kriteria selesai

- [ ] Semua konsep unit ini berstatus `review` atau `published` di concepts.yaml
- [ ] Semua sub-ticket done
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
