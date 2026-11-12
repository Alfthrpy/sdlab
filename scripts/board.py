#!/usr/bin/env python3
"""Generate backlog/BOARD.md from ticket files.

  python scripts/board.py          # tulis BOARD.md
  python scripts/board.py --next   # cetak ticket agent berikutnya yang siap
  python scripts/board.py --check  # gagal kalau BOARD.md belum diperbarui (dipakai CI)
"""
from __future__ import annotations

import sys
from collections import Counter

from common import ROOT, load_tickets, ready_tickets, sort_key

BOARD = ROOT / "backlog" / "BOARD.md"
MS_NAMES = {
    "M0": "Fondasi", "M1": "Registry Referensi", "M2": "Kurikulum",
    "M3": "Pedagogi & pilot", "M4": "Produksi konten", "M5": "QA & freeze",
}
ICON = {"todo": "·", "in-progress": "▶", "review": "◆", "blocked": "✖", "done": "✓"}


def link(t):
    return f"[{t['id']}](tickets/{t['_path'].name})"


def render(tickets: list[dict]) -> str:
    by_id = {t["id"]: t for t in tickets}
    out = ["# Board", "",
           "> File ini di-generate oleh `python scripts/board.py`. Jangan diedit manual.", ""]

    c = Counter(t.get("status") for t in tickets)
    out.append("**Ringkasan:** " + " · ".join(f"{s} {c.get(s, 0)}" for s in
                                              ["todo", "in-progress", "review", "blocked", "done"]))
    out.append("")

    ready = ready_tickets(tickets, "agent")
    out += ["## Siap dikerjakan agent", ""]
    if ready:
        out += ["| Ticket | Judul | Prioritas | Estimasi (sesi) |", "| --- | --- | --- | --- |"]
        out += [f"| {link(t)} | {t['title']} | {t['priority']} | {t.get('estimate', '')} |" for t in ready[:8]]
    else:
        out.append("_Tidak ada._")
    out.append("")

    human = [t for t in tickets if t.get("owner") == "human" and t.get("status") in ("todo", "in-progress")]
    human_review = [t for t in tickets if t.get("status") == "review" and t.get("review") == "human"]
    out += ["## Menunggu owner (manusia)", ""]
    rows = []
    for t in sorted(human, key=sort_key):
        deps_ok = all(by_id.get(d, {}).get("status") == "done" for d in t.get("depends_on") or [])
        rows.append(f"| {link(t)} | {t['title']} | {'siap' if deps_ok else 'menunggu dependensi'} |")
    for t in sorted(human_review, key=sort_key):
        rows.append(f"| {link(t)} | Review: {t['title']} | perlu review |")
    if rows:
        out += ["| Ticket | Tugas | Keadaan |", "| --- | --- | --- |"] + rows
    else:
        out.append("_Tidak ada._")
    out.append("")

    active = [t for t in tickets if t.get("status") in ("in-progress", "blocked")]
    if active:
        out += ["## Sedang berjalan / terhambat", "", "| Ticket | Judul | Status | Owner |", "| --- | --- | --- | --- |"]
        out += [f"| {link(t)} | {t['title']} | {t['status']} | {t['owner']} |" for t in sorted(active, key=sort_key)]
        out.append("")

    out += ["## Semua ticket per milestone", ""]
    for ms, name in MS_NAMES.items():
        ts = sorted([t for t in tickets if t.get("milestone") == ms], key=lambda t: t["id"])
        if not ts:
            continue
        done = sum(1 for t in ts if t.get("status") == "done")
        out += [f"### {ms} — {name} ({done}/{len(ts)} selesai)", "",
                "| | Ticket | Judul | Owner | Review | Bergantung pada |", "| --- | --- | --- | --- | --- | --- |"]
        for t in ts:
            deps = ", ".join(t.get("depends_on") or []) or "—"
            out.append(f"| {ICON.get(t.get('status'), '?')} | {link(t)} | {t['title']} | {t['owner']} | "
                       f"{t['review']} | {deps} |")
        out.append("")
    out.append("Legenda: · todo · ▶ in-progress · ◆ review · ✖ blocked · ✓ done")
    out.append("")
    return "\n".join(out)


def main():
    tickets = [t for t in load_tickets() if t.get("_has_fm") and t.get("id")]
    if "--next" in sys.argv:
        ready = ready_tickets(tickets, "agent")
        if not ready:
            print("Tidak ada ticket agent yang siap. Cek ticket owner: human di BOARD.md.")
            return
        for t in ready[:5]:
            print(f"{t['id']}  [{t['priority']}]  {t['title']}  ({t['_path'].relative_to(ROOT)})")
        return
    text = render(tickets)
    if "--check" in sys.argv:
        current = BOARD.read_text(encoding="utf-8") if BOARD.exists() else ""
        if current != text:
            print("BOARD.md belum diperbarui. Jalankan: python scripts/board.py")
            sys.exit(1)
        return
    BOARD.write_text(text, encoding="utf-8")
    print(f"Ditulis: {BOARD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
