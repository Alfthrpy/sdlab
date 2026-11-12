---
id: P1-021
title: "Graf prasyarat dan validasi DAG"
milestone: M2
type: curriculum
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-020]
estimate: 1
outputs:
  - curriculum/concepts.yaml
  - curriculum/graph.md
---

## Konteks

Prasyarat menentukan urutan buka di aplikasi (skill tree).

## Tugas

1. Isi `prerequisites` seminimal mungkin.
2. Pastikan validator mendeteksi siklus dan id tak dikenal.
3. Generate diagram Mermaid graf ke `curriculum/graph.md` (boleh lewat script).

## Kriteria selesai

- [ ] Graf tanpa siklus
- [ ] Tidak ada konsep yatim yang tidak bisa dicapai
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
