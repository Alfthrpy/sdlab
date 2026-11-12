---
description: Klaim ticket dan siapkan branch. Argumen: ID ticket (opsional, default = ticket berikutnya)
argument-hint: "[P1-0xx]"
---

Ticket: $ARGUMENTS (kalau kosong, pakai hasil `python scripts/board.py --next`).

1. Baca `AGENTS.md`, file ticket di `backlog/tickets/`, dan log sesi terakhir di `sessions/`.
2. Pastikan `owner: agent`, status `todo` atau `in-progress`, dan semua `depends_on` sudah `done`. Kalau tidak, berhenti dan jelaskan.
3. `git checkout main && git pull` (kalau ada remote), lalu `git checkout -b t/<ID>-<slug>` (atau checkout branch yang sudah ada).
4. Set `status: in-progress`, jalankan `python scripts/board.py`, commit `[<ID>] mulai`.
5. Tulis rencana singkat (3–6 langkah) berdasarkan bagian Tugas dan Kriteria selesai, lalu mulai kerjakan.
