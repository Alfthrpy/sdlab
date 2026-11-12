---
id: P1-033
title: "Format spesifikasi lab dan insiden"
milestone: M3
type: infra
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-024]
estimate: 1
outputs:
  - docs/conventions/content-schema.md
  - templates/concept/lab.yaml
  - templates/incident.md
---

## Konteks

Spesifikasi lab ditulis di Fase 1 dan dibaca simulator di Fase 2. Formatnya harus cukup netral terhadap implementasi simulator.

## Tugas

1. Definisikan skema `lab.yaml`: tujuan, arsitektur awal (komponen + koneksi), beban/trafik, skenario kegagalan, target metrik, aturan struktur, petunjuk.
2. Definisikan template insiden (lihat content-schema §5).
3. Tambahkan validasi dasar.

## Kriteria selesai

- [ ] Skema lab & insiden terdokumentasi
- [ ] Template tersedia
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
