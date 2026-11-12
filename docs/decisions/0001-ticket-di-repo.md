# ADR 0001 — Ticket disimpan sebagai file di repo

- **Status:** diterima
- **Tanggal:** 2026-11-12

## Konteks

Pengembangan dilakukan bersama agent di cloud dan owner manusia sebagai reviewer. Setiap sesi harus tahu persis tugasnya. Agent di cloud tidak selalu punya token GitHub API yang valid, tapi selalu bisa membaca isi repo.

## Keputusan

Ticket adalah file Markdown dengan frontmatter YAML di `backlog/tickets/`. `backlog/BOARD.md` di-generate oleh `scripts/board.py`. Perubahan status ticket di-commit di PR yang sama dengan hasil kerjanya.

## Konsekuensi

- Agent bisa bekerja tanpa akses API, dan riwayat ticket ikut tercatat di Git.
- Konflik merge mungkin terjadi di `BOARD.md`. Solusinya: regenerate, jangan diedit manual.
- Tidak ada notifikasi atau tampilan kanban bawaan GitHub. Kalau diperlukan, P1-004 menambahkan mirror ke GitHub Projects dengan file tetap sebagai sumber kebenaran.
