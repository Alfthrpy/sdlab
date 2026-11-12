---
id: P1-001
title: "Setup repo, workflow ticket, dan file pendukung agent"
milestone: M0
type: infra
owner: agent
review: none
status: done
priority: high
depends_on: []
estimate: 1
outputs:
  - AGENTS.md
  - docs/
  - backlog/
  - templates/
  - scripts/
  - .claude/
  - .github/
---

## Konteks

Fondasi kerja Fase 1: struktur repo, sistem ticket, aturan agent, template, dan validasi otomatis.

## Tugas

1. Buat struktur repo dan dokumen workflow.
2. Tulis AGENTS.md, subagent, dan slash command.
3. Tulis plan Fase 1 dan backlog awal.
4. Buat script validate/board/new_ticket dan CI.
5. Seed registry dari riset awal.

## Kriteria selesai

- [x] Struktur repo sesuai README
- [x] Backlog awal lengkap dengan owner/review/dependensi
- [x] CI menjalankan validate.py
- [x] `python scripts/validate.py` lolos

## Catatan

Dibuat di sesi perencanaan 2026-11-12 atas permintaan owner. Perubahan struktur berikutnya dibuat sebagai ticket baru.
