---
description: Tutup sesi ticket — validasi, review, log, board, PR
argument-hint: "P1-0xx"
---

Ticket: $ARGUMENTS

1. `python scripts/validate.py` harus lolos. Perbaiki kalau gagal.
2. Centang Kriteria selesai di file ticket yang benar-benar terpenuhi. Jangan centang yang belum.
3. Review:
   - `review: agent` → panggil subagent reviewer yang sesuai (`source-verifier` untuk riset, `content-reviewer` untuk konten/kurikulum). Beri daftar file yang berubah dan kriteria selesai. Perbaiki temuan serius, lalu ulangi sampai lolos.
   - `review: human` → siapkan ringkasan keputusan di bagian Catatan ticket supaya owner bisa memutuskan dalam < 15 menit.
4. Tulis log `sessions/<YYYY-MM-DD>-<ID>.md` dari `templates/session-log.md`.
5. Set status: `done` (review agent lolos), `review` (menunggu human), atau tetap `in-progress` (belum selesai). Jalankan `python scripts/board.py`.
6. Commit, push, buka PR `[<ID>] <judul>` dengan ringkasan, output, checklist, dan hasil review.
7. Kalau `review: agent`, CI hijau, dan reviewer menyatakan lolos → merge PR.
8. Laporkan ke owner dalam 3–5 baris.
