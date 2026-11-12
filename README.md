# SD Lab (nama kerja)

Platform gratis untuk belajar **backend system design** secara interaktif: lesson singkat, kuis, lab simulasi, dan insiden nyata. Semua materi disuling dari referensi yang terverifikasi.

Repo ini berisi **Fase 1: pengumpulan & produksi materi**. Simulator dan aplikasi menyusul di fase berikutnya, di repo yang sama atau terpisah.

## Mulai dari mana

| Kamu adalah | Baca |
| --- | --- |
| Agent (Claude atau lainnya) | [`AGENTS.md`](AGENTS.md), lalu [`backlog/BOARD.md`](backlog/BOARD.md) |
| Manusia (owner/reviewer) | [`docs/PLAN-FASE-1.md`](docs/PLAN-FASE-1.md), lalu [`docs/workflow.md`](docs/workflow.md) |

## Peta repo

```
AGENTS.md               aturan kerja agent (wajib dibaca tiap sesi)
docs/
  ROADMAP.md            3 fase besar proyek
  PLAN-FASE-1.md        rencana detail fase materi (milestone, gerbang)
  workflow.md           sistem ticket, alur sesi, branch, PR, review
  decisions/            ADR: keputusan yang sudah diambil
  conventions/          panduan sitasi, gaya tulisan, skema konten
backlog/
  BOARD.md              papan status (generate: python scripts/board.py)
  tickets/              satu file = satu ticket
references/
  registry.yaml         Registry Referensi (satu-satunya sumber yang boleh dikutip)
  notes/                catatan baca per sumber
curriculum/             peta kurikulum (konsep, prasyarat, studi kasus)
content/                lesson, soal, spesifikasi lab, insiden, studi kasus
templates/              template ticket, konsep, soal, catatan sumber, log sesi
sessions/               log tiap sesi kerja
scripts/                validate.py, board.py, new_ticket.py
.claude/                subagent & slash command untuk Claude Code
```

## Perintah

```bash
pip install pyyaml
python scripts/validate.py      # cek ticket, registry, kurikulum, konten
python scripts/board.py         # regenerate backlog/BOARD.md
python scripts/new_ticket.py "Judul ticket" --milestone M4 --type content
```

## Lisensi

- Kode (folder `scripts/`, `.github/`): MIT.
- Konten (`content/`, `curriculum/`, `docs/`): CC BY 4.0, kecuali dinyatakan lain di file.
- Materi pihak ketiga hanya ditautkan dan ditulis ulang, tidak disalin. Lihat [`docs/conventions/citation-guide.md`](docs/conventions/citation-guide.md).
