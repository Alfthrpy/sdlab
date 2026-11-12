#!/usr/bin/env python3
"""Buat ticket baru dari template.

  python scripts/new_ticket.py "Lesson: dasar caching" --milestone M4 --type content \
      --depends P1-041 [--id P1-041a] [--owner agent] [--review agent] [--priority medium]

Tanpa --id, nomor berikutnya yang kosong dipakai (P1-0xx).
Dengan --depends ke sebuah epic dan tanpa --id, id sub-ticket (P1-041a, b, ...) dibuat otomatis.
"""
from __future__ import annotations

import argparse
import re
import string

from common import MILESTONES, OWNERS, PRIORITIES, REVIEWS, TICKETS_DIR, TYPES, load_tickets


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return "-".join(s.split("-")[:6]) or "ticket"


def next_id(existing: set[str], phase: str, parent: str | None) -> str:
    if parent and re.match(r"^P\d-\d{3}$", parent):
        for ch in string.ascii_lowercase:
            cand = parent + ch
            if cand not in existing:
                return cand
        raise SystemExit("Sub-ticket habis (a–z).")
    nums = [int(m.group(1)) for i in existing if (m := re.match(rf"^{phase}-(\d{{3}})$", i))]
    n = max(nums, default=0) + 1
    while f"{phase}-{n:03d}" in existing:
        n += 1
    return f"{phase}-{n:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title")
    ap.add_argument("--id")
    ap.add_argument("--phase", default="P1")
    ap.add_argument("--milestone", required=True, choices=MILESTONES)
    ap.add_argument("--type", required=True, choices=TYPES)
    ap.add_argument("--owner", default="agent", choices=OWNERS)
    ap.add_argument("--review", default="agent", choices=REVIEWS)
    ap.add_argument("--priority", default="medium", choices=PRIORITIES)
    ap.add_argument("--depends", nargs="*", default=[])
    ap.add_argument("--estimate", type=int, default=1)
    ap.add_argument("--sub", action="store_true", help="paksa id sub-ticket dari dependensi pertama")
    a = ap.parse_args()

    existing = {t.get("id") for t in load_tickets()}
    parent = a.depends[0] if a.depends and (a.sub or a.milestone == "M4") else None
    tid = a.id or next_id(existing, a.phase, parent)
    if tid in existing:
        raise SystemExit(f"{tid} sudah ada.")

    deps = "[" + ", ".join(a.depends) + "]"
    text = f"""---
id: {tid}
title: "{a.title}"
milestone: {a.milestone}
type: {a.type}
owner: {a.owner}
review: {a.review}
status: todo
priority: {a.priority}
depends_on: {deps}
estimate: {a.estimate}
outputs: []
---

## Konteks

(Kenapa ticket ini ada.)

## Tugas

1. ...

## Kriteria selesai

- [ ] ...
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
"""
    path = TICKETS_DIR / f"{tid}-{slugify(a.title)}.md"
    path.write_text(text, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
