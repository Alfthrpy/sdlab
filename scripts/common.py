"""Shared helpers for repo scripts."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TICKETS_DIR = ROOT / "backlog" / "tickets"
REGISTRY = ROOT / "references" / "registry.yaml"
CONCEPTS = ROOT / "curriculum" / "concepts.yaml"
CASES = ROOT / "curriculum" / "case-studies.yaml"
CONTENT = ROOT / "content"

TICKET_ID = re.compile(r"^P\d-\d{3}[a-z]?$")
STATUSES = ["todo", "in-progress", "review", "blocked", "done"]
OWNERS = ["agent", "human"]
REVIEWS = ["agent", "human", "none"]
TYPES = ["research", "curriculum", "content", "review", "decision", "infra"]
PRIORITIES = ["high", "medium", "low"]
MILESTONES = ["M0", "M1", "M2", "M3", "M4", "M5"]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def load_tickets() -> list[dict]:
    tickets = []
    for p in sorted(TICKETS_DIR.glob("*.md")):
        fm, body = split_frontmatter(p.read_text(encoding="utf-8"))
        tickets.append({"_path": p, "_body": body, **(fm or {}), "_has_fm": fm is not None})
    return tickets


def load_yaml(path: Path):
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sort_key(t: dict):
    prio = {"high": 0, "medium": 1, "low": 2}.get(t.get("priority"), 3)
    return (prio, str(t.get("id")))


def ready_tickets(tickets: list[dict], owner: str | None = "agent") -> list[dict]:
    status = {t.get("id"): t.get("status") for t in tickets}
    out = []
    for t in tickets:
        if t.get("status") != "todo":
            continue
        if owner and t.get("owner") != owner:
            continue
        if all(status.get(d) == "done" for d in t.get("depends_on") or []):
            out.append(t)
    return sorted(out, key=sort_key)
