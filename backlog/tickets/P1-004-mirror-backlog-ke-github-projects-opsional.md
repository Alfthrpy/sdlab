---
id: P1-004
title: "Mirror backlog ke GitHub Projects (opsional)"
milestone: M0
type: infra
owner: agent
review: human
status: todo
priority: low
depends_on: [P1-001]
estimate: 1
outputs:
  - .github/workflows/sync-issues.yml
  - scripts/sync_issues.py
---

## Konteks

Ticket hidup di file (ADR 0001). Kalau owner ingin tampilan kanban dan notifikasi, buat sinkronisasi satu arah file → GitHub Issues/Projects.

## Tugas

1. Konfirmasi ke owner apakah ini dibutuhkan; kalau tidak, tutup ticket sebagai won't-do.
2. Buat script sinkron satu arah (file sebagai sumber kebenaran) memakai GITHUB_TOKEN di Actions.
3. Label: milestone, owner, type, status.

## Kriteria selesai

- [ ] Owner sudah memutuskan perlu/tidak
- [ ] Kalau perlu: Issues sinkron saat push ke main, tanpa duplikat
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
