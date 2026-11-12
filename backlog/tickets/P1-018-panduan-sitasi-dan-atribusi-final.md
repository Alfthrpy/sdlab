---
id: P1-018
title: "Panduan sitasi dan atribusi final"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-010]
estimate: 1
outputs:
  - docs/conventions/citation-guide.md
  - scripts/validate.py
---

## Konteks

Panduan v0 sudah ada. Finalkan dan pastikan validator menegakkannya di konten.

## Tugas

1. Uji panduan pada satu lesson contoh (boleh dummy).
2. Tambahkan pengecekan validator: penanda `[^id]` ada di `sources` dan registry; konten `published` tidak boleh mengutip `candidate`; atribusi wajib bila memakai sumber `adapt-with-attribution`.
3. Perjelas aturan kutipan langsung dengan contoh.

## Kriteria selesai

- [ ] Panduan final
- [ ] Validator menegakkan aturan sitasi
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
