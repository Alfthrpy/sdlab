---
id: P1-022
title: "Pilih studi kasus dan insiden"
milestone: M2
type: curriculum
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-020]
estimate: 1
outputs:
  - curriculum/case-studies.yaml
---

## Konteks

Target: ±12 studi kasus (soal interview umum) dan ±12 kandidat insiden, untuk dipilih 6 dan 8 di M4.

## Tugas

1. Pilih studi kasus yang mencakup semua unit (cek cakupan via Tier 6).
2. Pilih insiden dari postmortem di registry: beragam mekanisme (retry storm, config push, DNS, overload, data corruption, dependency).
3. Petakan setiap item ke konsep yang dilatihnya.

## Kriteria selesai

- [ ] Setiap unit dilatih ≥ 2 item
- [ ] Setiap insiden punya postmortem resmi di registry
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
