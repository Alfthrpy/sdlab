---
id: P1-046
title: "Paket insiden (8 skenario)"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-033, P1-042]
estimate: 4
outputs:
  - content/incidents/
---

## Konteks

Skenario Design & Fix dari postmortem publik. Dua kandidat pertama sudah di registry: AWS DynamoDB DNS (Okt 2025) dan Cloudflare (18 Nov 2025).

## Tugas

1. Pilih 8 dari kandidat di `curriculum/case-studies.yaml`.
2. Per insiden: ringkasan dengan kata sendiri, kronologi, mekanisme, skenario untuk pemain, pembahasan, konsep terkait.
3. Pecah jadi sub-ticket per insiden kalau perlu.

## Kriteria selesai

- [ ] 8 insiden lolos validator dan content-reviewer
- [ ] Setiap fakta kronologi bersumber dari postmortem resmi
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
