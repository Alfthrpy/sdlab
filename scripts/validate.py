#!/usr/bin/env python3
"""Validate tickets, reference registry, curriculum, and content.

Exit code 1 on any error. Warnings are printed but do not fail.
"""
from __future__ import annotations

import re
import sys
from datetime import date

from common import (CASES, CONCEPTS, CONTENT, MILESTONES, OWNERS, PRIORITIES, REGISTRY, REVIEWS, ROOT,
                    STATUSES, TICKET_ID, TYPES, load_tickets, load_yaml, split_frontmatter)

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str):
    errors.append(f"ERROR  {where}: {msg}")


def warn(where: str, msg: str):
    warnings.append(f"WARN   {where}: {msg}")


def rel(p):
    return str(p.relative_to(ROOT))


# --------------------------------------------------------------------------- tickets
def check_tickets():
    tickets = load_tickets()
    ids: dict[str, str] = {}
    for t in tickets:
        where = rel(t["_path"])
        if not t["_has_fm"]:
            err(where, "YAML frontmatter not found")
            continue
        tid = t.get("id")
        if not tid or not TICKET_ID.match(str(tid)):
            err(where, f"invalid id: {tid!r} (format P1-000 or P1-000a)")
            continue
        if not t["_path"].name.startswith(f"{tid}-"):
            err(where, f"file name must start with '{tid}-'")
        if tid in ids:
            err(where, f"duplicate id with {ids[tid]}")
        ids[tid] = where
        for field, allowed in [("status", STATUSES), ("owner", OWNERS), ("review", REVIEWS),
                               ("type", TYPES), ("priority", PRIORITIES), ("milestone", MILESTONES)]:
            if t.get(field) not in allowed:
                err(where, f"{field}={t.get(field)!r}, must be one of {allowed}")
        if not t.get("title"):
            err(where, "title is empty")
        if not isinstance(t.get("depends_on", []), list):
            err(where, "depends_on must be a list")
        for section in ("## Context", "## Tasks", "## Done criteria"):
            if section not in t["_body"]:
                err(where, f"section '{section}' is missing")
        if t.get("status") == "done" and re.search(r"^- \[ \]", t["_body"], re.M):
            warn(where, "status is done but some criteria are still unticked")
        if t.get("status") == "blocked" and "(Filled in during the work.)" in t["_body"]:
            err(where, "status is blocked with no explanation in Notes")

    status = {t.get("id"): t.get("status") for t in tickets}
    for t in tickets:
        where = rel(t["_path"])
        for d in t.get("depends_on") or []:
            if d not in status:
                err(where, f"depends_on names an unknown ticket: {d}")
            elif t.get("status") in ("in-progress", "review", "done") and status[d] != "done":
                warn(where, f"status is {t.get('status')} but dependency {d} is still {status[d]}")

    # dependency cycles
    graph = {t.get("id"): list(t.get("depends_on") or []) for t in tickets}
    cyc = find_cycle(graph)
    if cyc:
        err("backlog", "ticket dependency cycle: " + " -> ".join(cyc))
    return tickets


def find_cycle(graph: dict[str, list[str]]):
    WHITE, GREY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    stack: list[str] = []

    def dfs(n):
        color[n] = GREY
        stack.append(n)
        for m in graph.get(n, []):
            if m not in color:
                continue
            if color[m] == GREY:
                return stack[stack.index(m):] + [m]
            if color[m] == WHITE:
                r = dfs(m)
                if r:
                    return r
        stack.pop()
        color[n] = BLACK
        return None

    for n in graph:
        if color[n] == WHITE:
            r = dfs(n)
            if r:
                return r
    return None


# --------------------------------------------------------------------------- registry
REG_TYPES = ["book", "paper", "article", "postmortem", "docs", "repo", "course", "talk"]
LICENSES = ["all-rights-reserved", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-ND-4.0", "CC-BY-NC-4.0",
            "CC-BY-NC-SA-4.0", "MIT", "Apache-2.0", "public-domain", "unknown"]
USAGES = ["rewrite-only", "adapt-with-attribution", "map-only"]
ACCESS = ["free", "partial", "paywalled"]
SRC_STATUS = ["candidate", "approved", "rejected", "deprecated"]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
OPEN_LICENSES = {"CC-BY-4.0", "CC-BY-SA-4.0", "MIT", "Apache-2.0", "public-domain"}


def check_registry() -> dict[str, dict]:
    data = load_yaml(REGISTRY)
    where = rel(REGISTRY)
    if data is None:
        err(where, "file not found")
        return {}
    sources = data.get("sources") or []
    out: dict[str, dict] = {}
    for i, s in enumerate(sources):
        sid = s.get("id")
        w = f"{where} [{sid or i}]"
        if not sid or not KEBAB.match(str(sid)):
            err(w, "id must be kebab-case")
            continue
        if sid in out:
            err(w, "duplicate id")
        out[sid] = s
        for f in ("title", "url", "accessed"):
            if not s.get(f):
                err(w, f"{f} is required")
        if s.get("url") and not str(s["url"]).startswith(("https://", "http://")):
            err(w, "url must be http(s)")
        if s.get("type") not in REG_TYPES:
            err(w, f"type must be one of {REG_TYPES}")
        if s.get("tier") not in range(1, 7):
            err(w, "tier must be 1–6")
        if s.get("license") not in LICENSES:
            err(w, f"unknown license: {s.get('license')!r}")
        if s.get("usage") not in USAGES:
            err(w, f"usage must be one of {USAGES}")
        if s.get("access") not in ACCESS:
            err(w, f"access must be one of {ACCESS}")
        if s.get("status") not in SRC_STATUS:
            err(w, f"status must be one of {SRC_STATUS}")
        if s.get("usage") == "adapt-with-attribution" and s.get("license") not in OPEN_LICENSES:
            err(w, "adapt-with-attribution is only for open licenses (CC BY/SA, MIT, Apache, public-domain)")
        if s.get("tier") == 6 and s.get("usage") != "map-only":
            err(w, "tier 6 requires usage: map-only")
        acc = str(s.get("accessed") or "")
        if acc and not DATE.match(acc):
            err(w, "accessed must be YYYY-MM-DD")
        elif acc and len(acc) == 10 and acc > date.today().isoformat():
            err(w, "accessed is in the future")
        pub = str(s.get("published") or "")
        if pub and not DATE.match(pub):
            err(w, "published must be YYYY, YYYY-MM, or YYYY-MM-DD")
        units = s.get("units") or []
        if not all(isinstance(u, int) and 1 <= u <= 6 for u in units):
            err(w, "units must be numbers 1–6")
        if s.get("type") == "paper" and not s.get("doi"):
            warn(w, "paper without a doi")
        if s.get("status") == "approved":
            if s.get("license") == "unknown":
                err(w, "an approved source must not have license: unknown")
            if "SEED" in str(s.get("notes") or ""):
                err(w, "an approved source is still marked SEED (not yet verified)")
        if s.get("access") == "paywalled" and s.get("status") == "approved" and not s.get("notes"):
            warn(w, "a paywalled source should note a free companion in notes")
    return out


# --------------------------------------------------------------------------- curriculum
def check_curriculum(registry: dict[str, dict]) -> dict[str, dict]:
    data = load_yaml(CONCEPTS)
    if data is None:
        return {}
    where = rel(CONCEPTS)
    concepts: dict[str, dict] = {}
    for i, c in enumerate(data.get("concepts") or []):
        cid = c.get("id")
        w = f"{where} [{cid or i}]"
        if not cid or not KEBAB.match(str(cid)):
            err(w, "id must be kebab-case")
            continue
        if cid in concepts:
            err(w, "duplicate id")
        concepts[cid] = c
        if c.get("unit") not in range(1, 7):
            err(w, "unit must be 1–6")
        if not c.get("title"):
            err(w, "title is required")
        objs = c.get("objectives") or []
        if not 1 <= len(objs) <= 4:
            err(w, "objectives must have 1–4 items")
        for o in objs:
            # objectives are learner-facing, hence Indonesian (ADR 0005)
            if not str(o).startswith("Bisa "):
                warn(w, f"learning objective should start with 'Bisa ...' (Indonesian, learner-facing): {o!r}")
        srcs = c.get("sources") or []
        for s in srcs:
            if s not in registry:
                err(w, f"source not in registry: {s}")
            elif registry[s].get("status") in ("rejected", "deprecated"):
                err(w, f"source has status {registry[s].get('status')}: {s}")
        if c.get("status") in ("review", "published") and len(srcs) < 2:
            err(w, "a review/published concept needs ≥ 2 sources")
        elif len(srcs) < 2:
            warn(w, "a concept needs ≥ 2 sources before production")
    for cid, c in concepts.items():
        for p in c.get("prerequisites") or []:
            if p not in concepts:
                err(f"{where} [{cid}]", f"unknown prerequisite: {p}")
    cyc = find_cycle({k: list(v.get("prerequisites") or []) for k, v in concepts.items()})
    if cyc:
        err(where, "prerequisite cycle: " + " -> ".join(cyc))

    cases = load_yaml(CASES)
    if cases is not None:
        w0 = rel(CASES)
        seen = set()
        for i, it in enumerate(cases.get("items") or []):
            iid = it.get("id")
            w = f"{w0} [{iid or i}]"
            if not iid or not KEBAB.match(str(iid)):
                err(w, "id must be kebab-case")
                continue
            if iid in seen:
                err(w, "duplicate id")
            seen.add(iid)
            if it.get("kind") not in ("incident", "case-study"):
                err(w, "kind must be incident or case-study")
            for cc in it.get("concepts") or []:
                if cc not in concepts:
                    err(w, f"unknown concept: {cc}")
            for s in it.get("sources") or []:
                if s not in registry:
                    err(w, f"source not in registry: {s}")
            if it.get("kind") == "incident" and not any(
                    registry.get(s, {}).get("type") == "postmortem" for s in it.get("sources") or []):
                err(w, "an incident must have a source of type postmortem")
    return concepts


# --------------------------------------------------------------------------- content
FOOTNOTE = re.compile(r"\[\^([a-z0-9-]+)\]")
Q_TYPES = ["mcq", "multi", "order", "match", "estimate"]


def check_content(registry: dict[str, dict], concepts: dict[str, dict]):
    cdir = CONTENT / "concepts"
    if not cdir.exists():
        return
    for d in sorted(p for p in cdir.iterdir() if p.is_dir()):
        cid = d.name
        if concepts and cid not in concepts:
            err(rel(d), "concept folder is not in curriculum/concepts.yaml")
        lesson = d / "lesson.md"
        published = False
        if lesson.exists():
            fm, body = split_frontmatter(lesson.read_text(encoding="utf-8"))
            w = rel(lesson)
            if fm is None:
                err(w, "frontmatter missing")
            else:
                published = fm.get("status") == "published"
                src_ids = [s.get("id") if isinstance(s, dict) else s for s in fm.get("sources") or []]
                for s in src_ids:
                    if s not in registry:
                        err(w, f"source not in registry: {s}")
                    elif published and registry[s].get("status") != "approved":
                        err(w, f"published content cites a source that is not approved: {s}")
                    elif registry[s].get("usage") == "map-only":
                        err(w, f"a map-only (Tier 6) source must not be a content source: {s}")
                for s in src_ids:
                    if s in registry and registry[s].get("usage") == "adapt-with-attribution" \
                            and "diadaptasi" in body.lower() and registry[s].get("title", "") not in body:
                        warn(w, f"attribution for {s} should name the source title")
                for ref in set(FOOTNOTE.findall(body)):
                    if ref not in src_ids:
                        err(w, f"marker [^{ref}] is not in frontmatter sources")
                words = len(re.findall(r"\w+", re.sub(r"```.*?```", "", body, flags=re.S)))
                if words and not 250 <= words <= 700:
                    warn(w, f"lesson length is {words} words (target 300–600)")
        qfile = d / "questions.yaml"
        if qfile.exists():
            w = rel(qfile)
            data = load_yaml(qfile) or {}
            qs = data.get("questions") or []
            seen = set()
            longest_correct = 0
            mcq = 0
            for q in qs:
                qid = q.get("id")
                if not qid or qid in seen:
                    err(w, f"question id empty/duplicate: {qid}")
                seen.add(qid)
                if q.get("type") not in Q_TYPES:
                    err(w, f"{qid}: type must be one of {Q_TYPES}")
                if not q.get("prompt") or not q.get("explanation"):
                    err(w, f"{qid}: prompt and explanation are required")
                for s in q.get("sources") or []:
                    if s not in registry:
                        err(w, f"{qid}: source not in registry: {s}")
                if q.get("type") == "mcq":
                    opts = q.get("options") or []
                    a = q.get("answer")
                    if not isinstance(a, int) or not 0 <= a < len(opts):
                        err(w, f"{qid}: mcq answer must be a valid option index")
                    elif len(opts) >= 3:
                        mcq += 1
                        lens = [len(str(o)) for o in opts]
                        if lens[a] == max(lens) and lens.count(max(lens)) == 1:
                            longest_correct += 1
                if q.get("type") == "estimate":
                    a = q.get("answer") or {}
                    if not isinstance(a, dict) or "min" not in a or "max" not in a:
                        err(w, f"{qid}: estimate answer must be {{min, max}}")
            if mcq >= 4 and longest_correct / mcq > 0.4:
                warn(w, f"anti-leak: the correct option is the longest in {longest_correct}/{mcq} mcq questions")
        if published and not qfile.exists():
            err(rel(d), "published concept without questions.yaml")


def main():
    check_tickets()
    registry = check_registry()
    concepts = check_curriculum(registry)
    check_content(registry, concepts)
    for line in warnings:
        print(line)
    for line in errors:
        print(line)
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
