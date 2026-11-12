#!/usr/bin/env python3
"""Validate tickets, reference registry, curriculum, and content.

Exit code 1 on any error. Warnings are printed but do not fail.
"""
from __future__ import annotations

import difflib
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
REQUIRED_FIELDS = ["id", "title", "url", "accessed", "type", "tier", "license", "usage", "access", "status"]
OPTIONAL_FIELDS = ["authors", "publisher", "doi", "published", "edition", "units", "topics", "notes",
                   "free_companion", "superseded_by"]
KNOWN_FIELDS = set(REQUIRED_FIELDS + OPTIONAL_FIELDS)
# Tier implied by type, as a consistency hint (warning only). See research-protocol.md "Tiers".
TYPE_TIER_HINT = {"postmortem": {4}, "paper": {3}}


def _enum(w: str, s: dict, field: str, allowed: list):
    if s.get(field) not in allowed:
        err(w, f"{field}={s.get(field)!r} is not valid; use one of {allowed}")


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
            err(w, f"id={sid!r} must be kebab-case (lowercase letters, digits, hyphens)")
            continue
        if sid in out:
            err(w, "duplicate id; ids must be unique and stable")
        out[sid] = s

        for f in s:
            if f not in KNOWN_FIELDS:
                close = difflib.get_close_matches(f, KNOWN_FIELDS, n=1)
                hint = f" (did you mean '{close[0]}'?)" if close else ""
                err(w, f"unknown field '{f}'{hint}")
        for f in REQUIRED_FIELDS:
            if s.get(f) in (None, ""):
                err(w, f"required field '{f}' is missing or empty")

        if s.get("url") and not str(s["url"]).startswith(("https://", "http://")):
            err(w, f"url={s['url']!r} must start with http:// or https://")
        _enum(w, s, "type", REG_TYPES)
        if not isinstance(s.get("tier"), int) or isinstance(s.get("tier"), bool) or s.get("tier") not in range(1, 7):
            err(w, f"tier={s.get('tier')!r} must be an integer 1–6 (see research-protocol.md)")
        _enum(w, s, "license", LICENSES)
        _enum(w, s, "usage", USAGES)
        _enum(w, s, "access", ACCESS)
        _enum(w, s, "status", SRC_STATUS)

        if s.get("usage") == "adapt-with-attribution" and s.get("license") not in OPEN_LICENSES:
            err(w, f"usage 'adapt-with-attribution' needs an open license {sorted(OPEN_LICENSES)}, "
                   f"got {s.get('license')!r}; use 'rewrite-only' instead")
        if s.get("tier") == 6 and s.get("usage") != "map-only":
            err(w, f"tier 6 sources must have usage 'map-only', got {s.get('usage')!r}")
        if s.get("usage") == "map-only" and s.get("tier") != 6:
            warn(w, "usage 'map-only' is meant for tier 6 sources")
        hint = TYPE_TIER_HINT.get(s.get("type"))
        if hint and s.get("tier") not in hint:
            warn(w, f"type '{s.get('type')}' usually has tier {sorted(hint)}, got {s.get('tier')!r}")
        if s.get("tier") == 5 and s.get("license") not in OPEN_LICENSES:
            warn(w, "tier 5 means open material, but the license is not open")

        acc = str(s.get("accessed") or "")
        if acc and not DATE.match(acc):
            err(w, f"accessed={acc!r} must be YYYY-MM-DD")
        elif acc and len(acc) == 10 and acc > date.today().isoformat():
            err(w, f"accessed={acc!r} is in the future")
        elif acc and len(acc) != 10:
            err(w, f"accessed={acc!r} must be a full date YYYY-MM-DD")
        pub = str(s.get("published") or "")
        if pub and not DATE.match(pub):
            err(w, f"published={pub!r} must be YYYY, YYYY-MM, or YYYY-MM-DD")
        if s.get("doi") and not str(s["doi"]).startswith("10."):
            err(w, f"doi={s['doi']!r} must be a bare DOI starting with '10.' (no https://doi.org/ prefix)")

        for f in ("authors", "units", "topics", "free_companion"):
            if f in s and s[f] is not None and not isinstance(s[f], list):
                err(w, f"{f} must be a list, got {type(s[f]).__name__}")
        units = s.get("units") or []
        if isinstance(units, list) and not all(isinstance(u, int) and 1 <= u <= 6 for u in units):
            err(w, f"units={units!r} must be integers 1–6")
        topics = s.get("topics") or []
        if isinstance(topics, list):
            for tp in topics:
                if not KEBAB.match(str(tp)):
                    err(w, f"topic {tp!r} must be kebab-case")
        if s.get("type") == "paper" and not s.get("doi"):
            warn(w, "paper without a doi (add one if it exists)")
        if s.get("type") == "book" and not s.get("edition") and s.get("status") == "approved":
            warn(w, "approved book without an edition")

        notes = str(s.get("notes") or "")
        if s.get("status") == "approved":
            if s.get("license") == "unknown":
                err(w, "an approved source must not have license 'unknown'; verify it on the source page")
            if "SEED" in notes:
                err(w, "an approved source is still marked SEED (not yet verified); resolve and remove the SEED note")
            if not s.get("authors") and not notes:
                err(w, "approved source has no authors; add them, or explain in notes why none exist")
            if not s.get("published") and not notes:
                err(w, "approved source has no published date; add it, or explain in notes why none exists")
            if not s.get("units"):
                err(w, "approved source must list the curriculum units it serves (units: [..])")
            if not s.get("topics"):
                err(w, "approved source must list the topics it covers (topics: [..])")
            if s.get("access") == "paywalled" and not s.get("free_companion"):
                err(w, "approved paywalled source needs free_companion: [registry ids of free sources "
                       "covering the same topics] (research-protocol.md, acceptance criteria)")
        if s.get("status") in ("rejected", "deprecated") and not notes:
            warn(w, f"status '{s.get('status')}' should be explained in notes")

    for sid, s in out.items():
        w = f"{where} [{sid}]"
        for c in s.get("free_companion") or []:
            if c == sid:
                err(w, "free_companion must not reference itself")
            elif c not in out:
                err(w, f"free_companion references unknown source id: {c}")
            elif out[c].get("access") != "free":
                err(w, f"free_companion {c} must have access 'free', got {out[c].get('access')!r}")
        sup = s.get("superseded_by")
        if sup:
            if s.get("status") != "deprecated":
                err(w, "superseded_by is only valid on sources with status 'deprecated'")
            if sup not in out:
                err(w, f"superseded_by references unknown source id: {sup}")
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
