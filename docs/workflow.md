# Workflow: ticket, sesi, review

Semua pekerjaan berjalan lewat **ticket**. Satu sesi kerja (agent atau manusia) mengambil satu ticket, menyelesaikannya sampai kriteria selesai terpenuhi, lalu menyerahkannya untuk review. Tidak ada pekerjaan di luar ticket. Kalau ada pekerjaan baru yang ditemukan, buat ticket baru.

## 1. Ticket

Satu file Markdown di `backlog/tickets/`, nama file `<ID>-<slug>.md`, dengan frontmatter YAML:

```yaml
id: P1-011               # P1 = Fase 1, nomor unik
title: Riset kandidat sumber — Unit 1 & 2
milestone: M1            # lihat docs/PLAN-FASE-1.md
type: research           # research | curriculum | content | review | decision | infra
owner: agent             # siapa yang MENGERJAKAN: agent | human
review: agent            # siapa yang MEREVIEW: agent | human | none
status: todo             # todo | in-progress | review | done | blocked
priority: high           # high | medium | low
depends_on: [P1-010]     # ticket yang harus done dulu
estimate: 1              # perkiraan jumlah sesi
outputs:                 # file yang dibuat/diubah ticket ini
  - references/registry.yaml
```

Badan ticket berisi: **Konteks**, **Tugas**, **Kriteria selesai** (checklist), dan **Catatan** (diisi saat dikerjakan).

### Siapa mengerjakan apa

Proyek ini **agent-heavy**. Aturan penentuan owner dan review:

| Jenis pekerjaan | owner | review |
| --- | --- | --- |
| Riset sumber, ringkasan, pemetaan, draft kurikulum, draft konten, skema, script | agent | agent |
| Keputusan produk (bahasa, target, nama, prioritas) | human | none |
| Gerbang milestone (approve registry, kurikulum, pilot) | agent menyiapkan, human memutuskan | human |
| Uji ke pengguna nyata | human | none |
| Akses eksternal (buat repo, akun, undang reviewer) | human | none |
| Konten yang menyangkut klaim berisiko (angka performa, perilaku produk spesifik) | agent | agent + sampel human di ticket QA |

`review: agent` berarti ticket diverifikasi oleh **subagent reviewer yang tidak ikut mengerjakan** (`.claude/agents/content-reviewer.md` atau `source-verifier.md`). Setelah lolos dan CI hijau, agent boleh merge PR-nya sendiri.

`review: human` berarti PR menunggu approval owner repo. Agent tidak boleh merge.

### Status

```
todo → in-progress → review → done
          ↓
       blocked  (tulis alasannya di Catatan + ticket penghalang di depends_on)
```

Ticket hanya boleh diambil kalau semua `depends_on` sudah `done`.

## 2. Alur satu sesi

1. **Orientasi.** Baca `AGENTS.md`, `backlog/BOARD.md`, dan log sesi terakhir di `sessions/`.
2. **Pilih ticket.** Kalau owner tidak menunjuk, ambil ticket `todo` dengan `owner: agent`, semua dependensi `done`, prioritas tertinggi, nomor terkecil.
3. **Klaim.** Buat branch `t/<ID>-<slug>`, ubah status ke `in-progress`, commit.
4. **Kerjakan** sesuai Tugas. Kalau ticket terlalu besar untuk satu sesi, pecah jadi sub-ticket (`P1-040a`, `P1-040b`) dan kerjakan yang pertama.
5. **Validasi.** `python scripts/validate.py` harus lolos. Centang Kriteria selesai yang terpenuhi.
6. **Review.** `review: agent` → panggil subagent reviewer, perbaiki temuannya. `review: human` → set status `review`.
7. **Catat.** Tulis log sesi di `sessions/YYYY-MM-DD-<ID>.md` (template di `templates/session-log.md`). Isi bagian Catatan di ticket.
8. **Serahkan.** Jalankan `python scripts/board.py`, commit, push, buka PR berjudul `[<ID>] <judul>`. Kalau `review: agent` dan CI hijau, merge dan set `done`.

Satu sesi = satu ticket (atau satu sub-ticket). Kalau sesi berhenti di tengah, status tetap `in-progress` dan log sesi menjelaskan sampai mana.

## 3. Branch, commit, PR

- Branch: `t/P1-011-riset-fondasi`
- Commit: `[P1-011] tambah 12 kandidat sumber unit fondasi`
- PR: judul `[P1-011] <judul ticket>`, isi = ringkasan, daftar output, checklist kriteria selesai, hasil review agent.
- `main` hanya berubah lewat PR.

## 4. Peran manusia (owner)

Kamu cukup melakukan empat hal:

1. Mengerjakan ticket `owner: human` (keputusan, gerbang, uji pengguna).
2. Mereview PR `review: human`.
3. Sesekali spot-check PR `review: agent` yang sudah di-merge (ada ticket QA khusus untuk ini).
4. Memulai sesi agent: "kerjakan ticket berikutnya" atau "kerjakan P1-0xx".

## 5. Kenapa ticket di file, bukan GitHub Issues

Lihat [ADR 0001](decisions/0001-ticket-di-repo.md). Ringkasnya: agent di cloud selalu bisa membaca file tanpa token API, riwayat ticket ikut di Git, dan perubahan ticket direview dalam PR yang sama dengan hasil kerjanya. Mirror ke GitHub Issues/Projects bisa ditambahkan nanti (ticket P1-004).
