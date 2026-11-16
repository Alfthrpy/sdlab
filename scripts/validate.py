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
            "CC-BY-NC-SA-4.0", "CC-BY-3.0", "CC-BY-SA-2.5", "MIT", "Apache-2.0", "ISC", "PostgreSQL", "public-domain", "unknown"]
USAGES = ["rewrite-only", "adapt-with-attribution", "map-only"]
ACCESS = ["free", "partial", "paywalled"]
SRC_STATUS = ["candidate", "approved", "rejected", "deprecated"]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
FULL_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DOI = re.compile(r"^10\.\d{4,9}/\S+$")
SEED_MARK = re.compile(r"\bSEED\b")
OPEN_LICENSES = {"CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-3.0", "CC-BY-SA-2.5", "MIT", "Apache-2.0", "ISC", "PostgreSQL", "public-domain"}
REQUIRED_FIELDS = ["id", "title", "url", "accessed", "type", "tier", "license", "usage", "access", "status"]
OPTIONAL_FIELDS = ["authors", "publisher", "doi", "published", "edition", "units", "topics", "notes",
                   "free_companion", "superseded_by", "version", "archive_url", "attribution", "lang", "verified_on"]
LANGS = ["en", "id"]
KNOWN_FIELDS = set(REQUIRED_FIELDS + OPTIONAL_FIELDS)
# Tier implied by type, as a consistency hint (warning only). See research-protocol.md "Tiers".
TYPE_TIER_HINT = {"postmortem": {4}, "paper": {3}}


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _str_list(w: str, s: dict, field: str) -> list:
    """Return field as a list of non-empty strings; report an error and return [] if malformed."""
    v = s.get(field)
    if v is None:
        return []
    if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
        err(w, f"{field} must be a list of non-empty strings, got {v!r}")
        return []
    if len(set(v)) != len(v):
        err(w, f"{field} has duplicate entries: {v!r}")
    return v


def _valid_date(v: str) -> bool:
    try:
        parts = [int(x) for x in v.split("-")]
        date(parts[0], parts[1] if len(parts) > 1 else 1, parts[2] if len(parts) > 2 else 1)
        return True
    except (ValueError, IndexError):
        return False


def _enum(w: str, s: dict, field: str, allowed: list):
    if s.get(field) not in allowed:
        err(w, f"{field}={s.get(field)!r} is not valid; use one of {allowed}")


def check_registry() -> dict[str, dict]:
    data = load_yaml(REGISTRY)
    where = rel(REGISTRY)
    if data is None:
        err(where, "file not found")
        return {}
    if not isinstance(data, dict) or not isinstance(data.get("sources") or [], list):
        err(where, "top level must be a mapping with a 'sources' list")
        return {}
    sources = data.get("sources") or []
    out: dict[str, dict] = {}
    for i, s in enumerate(sources):
        if not isinstance(s, dict):
            err(f"{where} [#{i}]", f"each source must be a mapping, got {type(s).__name__}")
            continue
        sid = s.get("id")
        w = f"{where} [{sid or i}]"
        if not isinstance(sid, str) or not KEBAB.match(sid):
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

        for f in ("title", "publisher", "url", "edition", "notes", "doi", "published", "accessed",
                  "version", "archive_url", "attribution", "verified_on"):
            if s.get(f) is not None and not isinstance(s[f], (str, int)) or isinstance(s.get(f), bool):
                hint = " (quote it in YAML, e.g. \"2026-11-12\" or \"1.2\")" if isinstance(s.get(f), (date, float)) else ""
                err(w, f"{f} must be a string, got {s.get(f)!r}{hint}")
        if s.get("url") and not str(s["url"]).startswith(("https://", "http://")):
            err(w, f"url={s['url']!r} must start with http:// or https://")
        _enum(w, s, "type", REG_TYPES)
        if not _is_int(s.get("tier")) or s.get("tier") not in range(1, 7):
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
        if acc and not (FULL_DATE.match(acc) and _valid_date(acc)):
            err(w, f"accessed={acc!r} must be a valid full date YYYY-MM-DD")
        elif acc and acc > date.today().isoformat():
            err(w, f"accessed={acc!r} is in the future")
        pub = str(s.get("published") or "")
        if pub and not (DATE.match(pub) and _valid_date(pub)):
            err(w, f"published={pub!r} must be a valid YYYY, YYYY-MM, or YYYY-MM-DD")
        if s.get("doi") and not DOI.match(str(s["doi"])):
            err(w, f"doi={s['doi']!r} must be a bare DOI like 10.1145/3713082.3730380 (no https://doi.org/ prefix)")

        if s.get("archive_url") and not str(s["archive_url"]).startswith(("https://", "http://")):
            err(w, f"archive_url={s['archive_url']!r} must start with http:// or https://")
        if s.get("lang") is not None:
            _enum(w, s, "lang", LANGS)
        ver = str(s.get("verified_on") or "")
        if ver and not (FULL_DATE.match(ver) and _valid_date(ver)):
            err(w, f"verified_on={ver!r} must be a valid full date YYYY-MM-DD")
        elif ver and ver > date.today().isoformat():
            err(w, f"verified_on={ver!r} is in the future")
        _str_list(w, s, "authors")
        _str_list(w, s, "free_companion")
        units = s.get("units")
        if units is not None:
            if not isinstance(units, list) or not all(_is_int(u) and 0 <= u <= 6 for u in units):
                err(w, f"units={units!r} must be a list of integers 0–6 (0 = single-server starting unit)")
            elif len(set(units)) != len(units):
                err(w, f"units has duplicate entries: {units!r}")
        for tp in _str_list(w, s, "topics"):
            if not KEBAB.match(tp):
                err(w, f"topic {tp!r} must be kebab-case")
        if s.get("type") == "paper" and not s.get("doi"):
            warn(w, "paper without a doi (add one if it exists)")
        if s.get("type") == "book" and not s.get("edition") and s.get("status") == "approved":
            warn(w, "approved book without an edition")

        notes = str(s.get("notes") or "")
        if s.get("status") == "approved":
            if s.get("license") == "unknown":
                err(w, "an approved source must not have license 'unknown'; verify it on the source page")
            if SEED_MARK.search(notes):
                err(w, "an approved source is still marked SEED (not yet verified); resolve and remove the SEED note")
            if not s.get("authors") and "NO-AUTHOR:" not in notes:
                err(w, "approved source has no authors; add them, or put 'NO-AUTHOR: <reason>' in notes")
            if not s.get("published") and "NO-DATE:" not in notes:
                err(w, "approved source has no published date; add it, or put 'NO-DATE: <reason>' in notes")
            if not str(s.get("verified_on") or "").strip():
                err(w, "approved source needs verified_on: YYYY-MM-DD (the day source-verifier or a human "
                       "reopened the page and checked the metadata)")
            if s.get("usage") == "adapt-with-attribution" and not str(s.get("attribution") or "").strip():
                err(w, "approved adapt-with-attribution source needs attribution: the ready-made credit line "
                       "(see citation-guide.md)")
            if not s.get("units"):
                err(w, "approved source must list the curriculum units it serves (units: [..])")
            if not s.get("topics"):
                err(w, "approved source must list the topics it covers (topics: [..])")
            if s.get("access") == "paywalled" and not s.get("free_companion"):
                err(w, "approved paywalled source needs free_companion: [registry ids of free sources "
                       "covering the same topics] (research-protocol.md, acceptance criteria)")
        if s.get("status") in ("rejected", "deprecated") and not notes:
            warn(w, f"status '{s.get('status')}' should be explained in notes")
        if s.get("status") == "deprecated" and not s.get("superseded_by") and not notes:
            warn(w, "deprecated source should name its replacement in superseded_by (or explain in notes)")

    for sid, s in out.items():
        w = f"{where} [{sid}]"
        fc = s.get("free_companion")
        for c in fc if isinstance(fc, list) and all(isinstance(x, str) for x in fc) else []:
            if c == sid:
                err(w, "free_companion must not reference itself")
            elif c not in out:
                err(w, f"free_companion references unknown source id: {c}")
            elif out[c].get("access") != "free":
                err(w, f"free_companion {c} must have access 'free', got {out[c].get('access')!r}")
        sup = s.get("superseded_by")
        if sup:
            if not isinstance(sup, str):
                err(w, f"superseded_by must be a single registry id, got {sup!r}")
                continue
            if s.get("status") != "deprecated":
                err(w, "superseded_by is only valid on sources with status 'deprecated'")
            if sup == sid:
                err(w, "superseded_by must not reference itself")
            elif sup not in out:
                err(w, f"superseded_by references unknown source id: {sup}")
    return out


# --------------------------------------------------------------------------- curriculum
def prereq_list(c: dict) -> list[str]:
    """The concept's prerequisites if well-formed (a list of strings), else [] (the type error is reported separately)."""
    raw = c.get("prerequisites")
    return list(raw) if isinstance(raw, list) and all(isinstance(p, str) for p in raw) else []


def check_prerequisite_graph(where: str, concepts: dict, has_cycle: bool) -> None:
    """P1-021: prerequisites point backward in unit order, stay minimal, and every concept is reachable from Unit 0."""
    for cid, c in concepts.items():
        w = f"{where} [{cid}]"
        raw = c.get("prerequisites")
        if raw is not None and not (isinstance(raw, list) and all(isinstance(p, str) for p in raw)):
            err(w, f"prerequisites must be a list of concept ids, got {raw!r}")
            continue
        if raw and len(set(raw)) != len(raw):
            err(w, "duplicate entries in prerequisites")
        prereqs = [p for p in (raw or []) if p in concepts]
        for p in prereqs:
            pu, cu = concepts[p].get("unit"), c.get("unit")
            if isinstance(pu, int) and isinstance(cu, int) and pu > cu:
                err(w, f"prerequisite {p} is in a later unit ({pu}) than the concept ({cu})")
        # growth ladder: units 1–6 must hang off the earlier stages, so a concept with no prerequisites is a root,
        # and only Unit 0 may have roots (otherwise the concept cannot be reached from the single-server baseline)
        if not prereqs and c.get("unit") not in (0, None):
            msg = "no prerequisites: a concept in units 1–6 must build on an earlier concept (unreachable from Unit 0)"
            if c.get("status") in ("review", "published"):
                err(w, msg)
            else:
                warn(w, msg)
    if has_cycle:
        return
    graph = {k: [p for p in prereq_list(v) if p in concepts] for k, v in concepts.items()}
    memo: dict[str, set[str]] = {}

    def ancestors(n: str) -> set[str]:
        if n not in memo:
            memo[n] = set()
            for p in graph[n]:
                memo[n] |= {p} | ancestors(p)
        return memo[n]

    for cid, prereqs in graph.items():
        for p in prereqs:
            via = [q for q in prereqs if q != p and p in ancestors(q)]
            if via:
                warn(f"{where} [{cid}]", f"redundant prerequisite {p}: already implied through {via[0]}")


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
        if not _is_int(c.get("unit")) or c.get("unit") not in range(0, 7):
            err(w, f"unit={c.get('unit')!r} must be an integer 0–6 (0 = single-server starting unit)")
        if not c.get("title"):
            err(w, "title is required")
        objs = c.get("objectives") or []
        if not 1 <= len(objs) <= 4:
            err(w, "objectives must have 1–4 items")
        for o in objs:
            # objectives are learner-facing, hence Indonesian (ADR 0005)
            if not str(o).startswith("Bisa "):
                warn(w, f"learning objective should start with 'Bisa ...' (Indonesian, learner-facing): {o!r}")
        # growth ladder (ADR 0004 Amendment 1): beyond Unit 0, say when the concept becomes necessary
        trig = c.get("trigger")
        if trig is not None and (not isinstance(trig, str) or not trig.strip()):
            err(w, f"trigger must be a non-empty string, got {trig!r}")
        elif not trig and c.get("unit") != 0:
            if c.get("status") in ("review", "published"):
                err(w, "a review/published concept in units 1–6 needs a trigger (the symptom or number that "
                       "says it is time to use it)")
            else:
                warn(w, "concept has no trigger yet (the symptom or number that says it is time to use it)")
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
        for p in prereq_list(c):
            if p not in concepts:
                err(f"{where} [{cid}]", f"unknown prerequisite: {p}")
    cyc = find_cycle({k: prereq_list(v) for k, v in concepts.items()})
    if cyc:
        err(where, "prerequisite cycle: " + " -> ".join(cyc))
    check_prerequisite_graph(where, concepts, bool(cyc))

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
# a quoted span followed by a source marker (optional punctuation between), e.g. "..."[^id] or “...”.[^id]
QUOTE = re.compile(r'(?:"([^"\n]+)"|“([^”\n]+)”)[.,;:]?\s*\[\^([a-z0-9-]+)\]')
QUOTE_MAX_WORDS = 14  # citation-guide: a short sentence, fewer than 15 words
QUOTE_MIN_WORDS = 4   # shorter spans are terms ("split brain"), not quotes
Q_TYPES = ["mcq", "multi", "order", "match", "estimate"]
LESSON_STATUSES = ["draft", "review", "published"]
LESSON_WORDS = (300, 600)       # target range (writing-style.md): error for review/published, warning for draft
QUESTIONS_RANGE = (6, 10)       # questions per concept
MISCONCEPTIONS_RANGE = (3, 6)   # misconceptions per concept
MISC_HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
MISC_LABELS = ("**Keyakinan keliru:**", "**Kenapa keliru:**")
OPTION_COUNTS = {"mcq": (3, 5), "multi": (4, 6), "order": (3, 6)}
# Anti-leak and style heuristics (writing-style.md). All of them only warn: they flag patterns, not proof.
ANTILEAK_MIN_MCQ = 4            # heuristics over a concept's mcq questions need at least this many
POSITION_MIN_MCQ = 5            # the position check is noisy with fewer questions (random keys repeat often)
ANTILEAK_SHARE = 0.4            # correct option strictly longest in more than this share
POSITION_SHARE = 0.5            # one answer position holds more than this share
ECHO_SHARE = 0.5                # correct option shares the most prompt words in more than this share
ABSOLUTE_MIN = 3                # questions where only wrong options use an absolute word
NONE_OF_ABOVE = re.compile(r"\b(semua|seluruh)\s+(jawaban|pilihan)(\s+di\s+atas)?\b|\btidak\s+ada\s+(jawaban\s+)?yang\s+(benar|tepat)\b"
                           r"|\b(all|none)\s+of\s+the\s+above\b", re.I)
LETTER_COMBO = re.compile(r"^\s*[A-D]\s+dan\s+[A-D]\s+(benar|keduanya)\b")   # "A dan B benar" (case-sensitive letters)
ABSOLUTES = re.compile(r"\b(selalu|tidak\s+pernah|pasti|mustahil|selamanya|satu-satunya|always|never)\b", re.I)
ECHO_STOPWORDS = {"dengan", "karena", "adalah", "dalam", "untuk", "tidak", "apakah", "berikut", "tentang", "paling",
                  "yang", "dapat", "mana", "akan", "saat", "ketika", "setelah", "sebelum", "supaya", "sebuah", "manakah"}
FILLER = ["sangat penting", "di era modern", "mari kita selami", "kesimpulannya", "dalam dunia yang semakin",
          "tidak dapat dipungkiri", "perlu diingat bahwa"]
LESSON_OPENERS = re.compile(r"^\s*(pada|dalam|di|untuk)\s+(lesson|materi|artikel|bab|bagian)\s+ini\b|^\s*(kali ini|mari)\s+kita\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2705\u274C\u26A1\u2B50\u23F0\u231B\uFE0F]")
ABBREVIATIONS = re.compile(r"\b(mis|dst|dll|dsb|dkk|vs|yaitu|e\.g|i\.e|no|hlm|spt|tsb)\.", re.I)
EXPLANATION_MAX_SENTENCES = 3
# Learner-facing text must not narrate provenance; the [^id] markers carry it (citation-guide.md).
PROVENANCE = re.compile(
    r"\b(menurut|berdasarkan)\s+(sumber|penulis|dokumentasi|azure|aws|mdn|rfc)\b"
    r"|\bbukan\s+(fakta|klaim|data)?\s*(dari\s+)?sumber\b|\bdari\s+sumber\s+(ini|itu|di\s+atas)\b"
    r"|\bpenalaran\s+(sendiri|penulis)\b|\bhitungan\s+sendiri\b|\basumsi\s+(buatan\s+)?sendiri\b"
    r"|\b(azure|aws|mdn|rfc)\s+(menyebut|menyatakan|mengatakan|menyuruh|menulis)\b"
    r"|\bsumbernya\b|\bsumber-sumber\b|\bcatatan:\s*ini\b", re.I)


def check_misconceptions(d, cid: str, registry: dict, stage: str) -> set[str] | None:
    """misconceptions.md: frontmatter `concept`, then one `## <kebab-id>` section per misconception with the
    labels **Keyakinan keliru:** and **Kenapa keliru:**. Returns the ids (None when the file is absent)."""
    mfile = d / "misconceptions.md"
    if not mfile.exists():
        if stage in ("review", "published"):
            err(rel(d), "concept in review/published needs misconceptions.md")
        return None
    w = rel(mfile)
    fm, body = split_frontmatter(mfile.read_text(encoding="utf-8"))
    if fm is None:
        err(w, "frontmatter missing")
    elif not isinstance(fm, dict):
        err(w, "frontmatter must be a mapping")
    elif fm.get("concept") != cid:
        err(w, f"frontmatter concept `{fm.get('concept')}` does not match the folder `{cid}`")
    body = re.sub(r"```.*?```", "", body, flags=re.S)  # labels and headings inside code fences do not count
    check_provenance(w, "misconceptions", body)
    heads = list(MISC_HEADING.finditer(body))
    ids: set[str] = set()
    for i, m in enumerate(heads):
        mid = m.group(1)
        section = body[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(body)]
        if not KEBAB.match(mid):
            err(w, f"misconception id must be kebab-case: {mid}")
        if mid in ids:
            err(w, f"duplicate misconception id: {mid}")
        ids.add(mid)
        for label in MISC_LABELS:
            if label not in section:
                err(w, f"{mid}: missing the label {label}")
        for ref in set(FOOTNOTE.findall(section)):
            if ref not in registry:
                err(w, f"{mid}: marker [^{ref}] is not in the registry")
    lo, hi = MISCONCEPTIONS_RANGE
    if not lo <= len(ids) <= hi:
        (err if stage in ("review", "published") and len(ids) < lo else warn)(
            w, f"{len(ids)} misconceptions (target {lo}-{hi})")
    return ids


def check_question_answer(w: str, qid: str, q: dict):
    """Answer format per type (content-schema.md section 4)."""
    t, a = q.get("type"), q.get("answer")
    if not isinstance(t, str):
        return  # the type error is reported by the caller
    if t in OPTION_COUNTS:
        opts = q.get("options")
        lo, hi = OPTION_COUNTS[t]
        if not isinstance(opts, list) or not lo <= len(opts) <= hi:
            err(w, f"{qid}: {t} needs {lo}-{hi} options")
            return
        if len(set(map(str, opts))) != len(opts):
            err(w, f"{qid}: options must be distinct")
        valid = lambda i: isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(opts)  # noqa: E731
        if t == "mcq":
            if not valid(a):
                err(w, f"{qid}: mcq answer must be a valid option index")
        elif t == "multi":
            if not (isinstance(a, list) and 2 <= len(a) < len(opts) and all(valid(i) for i in a)
                    and len(set(a)) == len(a)):
                err(w, f"{qid}: multi answer must be a list of 2 or more distinct option indexes, not all options")
        elif not (isinstance(a, list) and all(valid(i) for i in a) and sorted(a) == list(range(len(opts)))):
            err(w, f"{qid}: order answer must list every option index exactly once (the correct sequence)")
    elif t == "match":
        pairs = q.get("pairs")
        if not (isinstance(pairs, list) and len(pairs) >= 3
                and all(isinstance(p, list) and len(p) == 2 and all(isinstance(x, str) and x for x in p) for p in pairs)):
            err(w, f"{qid}: match needs `pairs`: a list of 3 or more [left, right] string pairs")
        elif len({p[1] for p in pairs}) != len(pairs) or len({p[0] for p in pairs}) != len(pairs):
            err(w, f"{qid}: match pairs must have distinct left and right items")
    elif t == "estimate":
        num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)  # noqa: E731
        if not (isinstance(a, dict) and num(a.get("min")) and num(a.get("max")) and a["min"] < a["max"]):
            err(w, f"{qid}: estimate answer must be {{min, max}} numbers with min < max")
        if not isinstance(q.get("unit"), str) or not q.get("unit"):
            err(w, f"{qid}: estimate needs a `unit` (string)")


def check_questions(qfile, d, cid: str, concept: dict | None, registry: dict, published: bool, stage: str,
                    misc_ids: set[str] | None) -> None:
    w = rel(qfile)
    data = load_yaml(qfile) or {}
    if not isinstance(data, dict) or not isinstance(data.get("questions") or [], list):
        err(w, "questions.yaml must be a mapping with a `questions` list")
        return
    qs = data.get("questions") or []
    objectives = (concept or {}).get("objectives") or []
    if not isinstance(objectives, list):
        objectives = []
    covered: set[int] = set()
    seen: set = set()
    for q in qs:
        if not isinstance(q, dict):
            err(w, f"every question must be a mapping, got: {q!r}")
            continue
        qid = q.get("id")
        if not isinstance(qid, str) or not qid or qid in seen:
            err(w, f"question id empty/duplicate/not a string: {qid!r}")
            qid = str(qid)
        seen.add(qid)
        if qid and not re.fullmatch(re.escape(cid) + r"-q\d{2,}", str(qid)):
            err(w, f"{qid}: id must look like `{cid}-qNN`")
        if not isinstance(q.get("type"), str) or q.get("type") not in Q_TYPES:
            err(w, f"{qid}: type must be one of {Q_TYPES}")
        d = q.get("difficulty")
        if not isinstance(d, int) or isinstance(d, bool) or d not in (1, 2, 3):
            err(w, f"{qid}: difficulty must be 1, 2 or 3")
        if not q.get("prompt") or not q.get("explanation"):
            err(w, f"{qid}: prompt and explanation are required")
        obj = q.get("objective")
        if obj is None:
            (err if stage in ("review", "published") else warn)(
                w, f"{qid}: `objective` (1-based index into the concept's objectives) is missing")
        elif not isinstance(obj, int) or isinstance(obj, bool) or obj < 1 or (objectives and obj > len(objectives)):
            err(w, f"{qid}: objective must be an index from 1 to {len(objectives) or 'N'}")
        else:
            covered.add(obj)
        tm = q.get("targets_misconception")
        if tm is not None and not isinstance(tm, str):
            err(w, f"{qid}: targets_misconception must be a misconception id (string)")
            tm = None
        if tm and misc_ids is not None and tm not in misc_ids:
            err(w, f"{qid}: targets_misconception `{tm}` is not in misconceptions.md")
        elif tm and misc_ids is None:
            err(w, f"{qid}: targets_misconception needs a misconceptions.md")
        qsrc = q.get("sources") or []
        if not isinstance(qsrc, list) or not all(isinstance(x, str) for x in qsrc):
            err(w, f"{qid}: `sources` must be a list of registry ids")
            qsrc = []
        for s in qsrc:
            if s not in registry:
                err(w, f"{qid}: source not in registry: {s}")
            elif published and registry[s].get("status") != "approved":
                err(w, f"{qid}: published content cites a source that is not approved: {s}")
            elif registry[s].get("usage") == "map-only":
                err(w, f"{qid}: a map-only (Tier 6) source must not be a content source: {s}")
        check_question_answer(w, qid, q)
        for field in ("prompt", "explanation"):
            check_provenance(w, f"{qid} {field}", q.get(field))
        for o in q.get("options") if isinstance(q.get("options"), list) else []:
            check_provenance(w, f"{qid} option", o)
    lo, hi = QUESTIONS_RANGE
    if qs and not lo <= len(qs) <= hi:
        (err if stage in ("review", "published") and len(qs) < lo else warn)(
            w, f"{len(qs)} questions (target {lo}-{hi})")
    if objectives and qs:
        missing = [i for i in range(1, len(objectives) + 1) if i not in covered]
        if missing:
            (err if stage in ("review", "published") else warn)(
                w, f"learning objective(s) {missing} are not covered by any question")
    check_anti_leak(w, [q for q in qs if isinstance(q, dict)])


def mcq_items(qs: list[dict]) -> list[tuple[dict, list[str], int]]:
    """(question, options as text, correct index) for well-formed mcq questions with 3+ options."""
    out = []
    for q in qs:
        opts, a = q.get("options"), q.get("answer")
        if q.get("type") == "mcq" and isinstance(opts, list) and len(opts) >= 3 and isinstance(a, int) \
                and not isinstance(a, bool) and 0 <= a < len(opts):
            out.append((q, [str(o) for o in opts], a))
    return out


def check_anti_leak(w: str, qs: list[dict]) -> None:
    """Warnings for patterns that let a learner guess the answer without understanding (writing-style.md)."""
    items = mcq_items(qs)
    n = len(items)
    if n >= ANTILEAK_MIN_MCQ:
        longest = sum(1 for _, o, a in items if len(o[a]) == max(map(len, o)) and [len(x) for x in o].count(len(o[a])) == 1)
        if longest / n > ANTILEAK_SHARE:
            warn(w, f"anti-leak: the correct option is the longest in {longest}/{n} mcq questions")
        top = max(set(a for _, _, a in items), key=[a for _, _, a in items].count)
        at_top = sum(1 for _, _, a in items if a == top)
        if n >= POSITION_MIN_MCQ and at_top / n > POSITION_SHARE:
            warn(w, f"anti-leak: the correct answer is option {top + 1} in {at_top}/{n} mcq questions; vary the position")
        echo = 0
        for q, o, a in items:
            words = set(re.findall(r"\w{5,}", str(q.get("prompt", "")).lower())) - ECHO_STOPWORDS
            scores = [len(words & (set(re.findall(r"\w{5,}", x.lower())) - ECHO_STOPWORDS)) for x in o]
            if scores[a] > 0 and scores[a] == max(scores) and scores.count(scores[a]) == 1:
                echo += 1
        if echo / n > ECHO_SHARE:
            warn(w, f"anti-leak: the correct option repeats the most words from the prompt in {echo}/{n} mcq questions")
        absolute = sum(1 for _, o, a in items
                       if not ABSOLUTES.search(o[a]) and any(ABSOLUTES.search(x) for i, x in enumerate(o) if i != a))
        if absolute >= ABSOLUTE_MIN and absolute / n > 0.3:
            warn(w, f"anti-leak: absolute words (selalu, tidak pernah, semua, ...) appear only in wrong options in {absolute}/{n} mcq questions")
    for q in qs:
        opts = q.get("options")
        for o in opts if isinstance(opts, list) else []:
            if NONE_OF_ABOVE.search(str(o)) or LETTER_COMBO.search(str(o)):
                warn(w, f"{q.get('id')}: avoid 'semua jawaban benar' / 'tidak ada yang benar' style options: {str(o)[:40]!r}")
                break
    long_expl = [q.get("id") for q in qs if isinstance(q.get("explanation"), str)
                 and count_sentences(q["explanation"]) > EXPLANATION_MAX_SENTENCES]
    if long_expl:
        warn(w, f"explanations longer than {EXPLANATION_MAX_SENTENCES} sentences: {', '.join(map(str, long_expl[:5]))}")
    rated = [q.get("difficulty") for q in qs
             if isinstance(q.get("difficulty"), int) and not isinstance(q.get("difficulty"), bool)
             and q.get("difficulty") in (1, 2, 3)]
    if len(rated) >= ANTILEAK_MIN_MCQ and len(set(rated)) == 1:
        warn(w, f"all {len(rated)} questions have difficulty {rated[0]}; use a mix of levels")


def check_provenance(w: str, where: str, text) -> None:
    """Warn when learner-facing text says where a statement comes from instead of leaving it to the markers."""
    if isinstance(text, str):
        m = PROVENANCE.search(text)
        if m:
            warn(w, f"{where}: do not narrate provenance ({m.group(0)!r}); the [^id] markers carry it")


def count_sentences(text: str) -> int:
    """Sentence count for the explanation-length warning: abbreviations (mis., dst., dll.) do not end a sentence,
    and a last sentence without a final period still counts."""
    t = ABBREVIATIONS.sub(lambda m: m.group(0)[:-1], text.strip())
    n = len(re.findall(r"[.!?](?:\s|$)", t))
    return n + (1 if t and t[-1] not in ".!?" else 0)


def check_lesson_style(w: str, body: str) -> None:
    """Warnings for filler, machine-sounding openers and emoji (writing-style.md, Lessons)."""
    text = re.sub(r"```.*?```", "", body, flags=re.S)
    text = re.sub(r"`[^`\n]*`|\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", "", text)  # inline code and quoted phrases are mentions
    opening = re.sub(r"^(?:\s*#.*\n|\s*>\s*\n|\s*---\s*\n|\s*\n)*", "", text)   # skip headings and blank lines
    if LESSON_OPENERS.match(opening):
        warn(w, "style: the first sentence should be the core point, not 'Pada lesson ini kita akan ...'")
    low = text.lower()
    hits = [f for f in FILLER if re.search(r"\b" + re.escape(f) + r"\b", low)]
    if hits:
        warn(w, f"style: filler phrases: {', '.join(hits)}")
    check_provenance(w, "lesson", text)
    if EMOJI.search(text):
        warn(w, "style: no emoji in lessons")


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
        stage = "draft"
        if lesson.exists():
            fm, body = split_frontmatter(lesson.read_text(encoding="utf-8"))
            w = rel(lesson)
            if fm is None:
                err(w, "frontmatter missing")
            elif not isinstance(fm, dict):
                err(w, "frontmatter must be a mapping")
            else:
                published = fm.get("status") == "published"
                for field in ("concept", "title", "sources", "status"):
                    if not fm.get(field):
                        err(w, f"frontmatter field `{field}` is required")
                if fm.get("concept") and fm.get("concept") != cid:
                    err(w, f"frontmatter concept `{fm.get('concept')}` does not match the folder `{cid}`")
                if fm.get("status") and fm.get("status") not in LESSON_STATUSES:
                    err(w, f"status must be one of {LESSON_STATUSES}")
                else:
                    stage = fm.get("status") or "draft"
                if published and not fm.get("reviewed_by"):
                    err(w, "published lesson needs `reviewed_by` in the frontmatter")
                raw_srcs = fm.get("sources") or []
                if not isinstance(raw_srcs, list) or not all(
                        isinstance(x, str) or (isinstance(x, dict) and isinstance(x.get("id"), str)) for x in raw_srcs):
                    err(w, "`sources` must be a list of registry ids or {id, loc} mappings")
                    raw_srcs = []
                srcs = [x if isinstance(x, dict) else {"id": x} for x in raw_srcs]
                src_ids = [x.get("id") for x in srcs]
                for s in src_ids:
                    if s not in registry:
                        err(w, f"source not in registry: {s}")
                    elif published and registry[s].get("status") != "approved":
                        err(w, f"published content cites a source that is not approved: {s}")
                    elif registry[s].get("usage") == "map-only":
                        err(w, f"a map-only (Tier 6) source must not be a content source: {s}")
                for s in srcs:
                    r = registry.get(s.get("id"))
                    if r and r.get("type") in ("book", "paper") and not s.get("loc"):
                        err(w, f"source {s['id']} is a {r['type']}: `loc` (chapter/section/page) is required")
                for s in src_ids:
                    r = registry.get(s)
                    if r and r.get("usage") == "adapt-with-attribution":
                        if "diadaptasi" not in body.lower():
                            err(w, f"{s} is adapt-with-attribution: the attribution line ('diadaptasi ...') is missing")
                        elif r.get("title", "") not in body:
                            warn(w, f"attribution for {s} should name the source title")
                for ref in set(FOOTNOTE.findall(body)):
                    if ref not in registry:
                        err(w, f"marker [^{ref}] is not in the registry")
                    elif ref not in src_ids:
                        err(w, f"marker [^{ref}] is not in frontmatter sources")
                quotes: dict[str, int] = {}
                for m in QUOTE.finditer(re.sub(r"```.*?```", "", body, flags=re.S)):
                    text, ref = m.group(1) or m.group(2), m.group(3)
                    if len(text.split()) < QUOTE_MIN_WORDS:
                        continue
                    quotes[ref] = quotes.get(ref, 0) + 1
                    if len(text.split()) > QUOTE_MAX_WORDS:
                        err(w, f"direct quote from {ref} is {len(text.split())} words (max {QUOTE_MAX_WORDS})")
                for ref, n in quotes.items():
                    if n > 1:
                        err(w, f"{n} direct quotes from {ref} (max 1 per source per lesson)")
                check_lesson_style(w, body)
                counted = re.sub(r"```.*?```", "", body, flags=re.S)
                counted = re.sub(r"\[\^[a-z0-9-]+\]|https?://\S+", "", counted)
                words = len(re.findall(r"\w+", counted))
                lo, hi = LESSON_WORDS
                if words and not lo <= words <= hi:
                    (err if stage in ("review", "published") else warn)(
                        w, f"lesson length is {words} words (must be {lo}–{hi} before review)"
                        if stage != "draft" else f"lesson length is {words} words (target {lo}–{hi})")
        misc_ids = check_misconceptions(d, cid, registry, stage)
        qfile = d / "questions.yaml"
        if qfile.exists():
            check_questions(qfile, d, cid, concepts.get(cid), registry, published, stage, misc_ids)
        if published and not qfile.exists():
            err(rel(d), "published concept without questions.yaml")


# --------------------------------------------------------------------------- labs and incidents (P1-033)
# Lab spec and incident format: docs/conventions/content-schema.md sections 5 and 6. The simulator catalog
# (contracts/sim/catalog.json, vendored from stud-sim) does not exist yet, so catalog rules (C02-C04, C10, C11
# of the STUD Simulator Master Plan) are skipped until it does; everything else is checked from the spec alone.
LAB_MODES = ["tune", "diagnose", "build"]
LAB_PREDICATES = ["has-node", "has-edge", "node-between", "param-unchanged", "param-range", "count-le",
                  "policy-present", "no-spof"]
LAB_AGGREGATES = ["mean", "max", "p99"]
LAB_OPS = ["<=", ">=", "<", ">"]
LAB_DURATION = (10, 20)         # minutes, warn outside
LAB_REQUIRED = ["id", "concept", "contract_version", "mode", "difficulty", "duration_min", "illustrative", "title",
                "goal", "topology", "traffic", "targets", "hints", "reference_solution", "wrong_answers", "debrief",
                "sources"]
LAB_KEYS = set(LAB_REQUIRED) | {"secondary_concepts", "illustrative_note", "scenarios", "allowed_edits", "palette",
                                "structural_rules", "brute_force_ok"}
LAB_NODE_KEYS = {"id", "type", "params"}
LAB_TARGET_KEYS = {"id", "metric", "node", "window", "aggregate", "op", "value", "feedback_pass", "feedback_fail"}
LAB_RULE_KEYS = {"id", "predicate", "args", "feedback_pass", "feedback_fail"}
LAB_EDIT_KEYS = {"node", "param", "min", "max"}
LAB_WRONG_KEYS = {"edits", "reason", "brute_force"}
INCIDENT_KEYS = {"id", "title", "date", "sources", "concepts", "modelability", "sim_spec", "sim_scenarios"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
MODELABILITY = ["modeled", "illustrative", "text-only"]
INCIDENT_SECTIONS = ["Ringkasan", "Kronologi", "Mekanisme kegagalan", "Skenario untuk pemain", "Pembahasan"]
CATALOG = ROOT / "contracts" / "sim" / "catalog.json"


def is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def read_yaml(path, w: str):
    """YAML file as data; a syntax error is a validation error, not a crash. Returns (data, ok)."""
    try:
        return load_yaml(path), True
    except Exception as e:  # noqa: BLE001 (yaml.YAMLError and decoding errors)
        err(w, f"invalid YAML: {str(e).splitlines()[0] if str(e) else type(e).__name__}")
        return None, False


def lab_files() -> list:
    out = []
    for pat in ("concepts/*/lab.yaml", "concepts/*/*.lab.yaml", "incidents/*.lab.yaml"):
        out.extend(sorted(CONTENT.glob(pat)))
    return out


def edit_ok(edit, allowed: dict, w: str, where: str) -> None:
    """One {node, param, value} edit must be an allowed edit with a numeric value inside its range."""
    if not isinstance(edit, dict) or not {"node", "param", "value"} <= set(edit):
        err(w, f"{where}: an edit must be {{node, param, value}}")
        return
    node, param, value = edit["node"], edit["param"], edit["value"]
    if not isinstance(node, str) or not isinstance(param, str):
        err(w, f"{where}: edit node and param must be strings")
        return
    if not is_num(value):
        err(w, f"{where}: edit value of {node}.{param} must be a number")
        return
    rng = allowed.get((node, param))
    if rng is None:
        err(w, f"{where}: edit {node}.{param} is not in allowed_edits")
    elif not rng[0] <= value <= rng[1]:
        err(w, f"{where}: {node}.{param}={value} is outside its allowed range {rng[0]}..{rng[1]}")


def unknown_keys(w: str, where: str, mapping, allowed: set) -> None:
    if isinstance(mapping, dict):
        extra = sorted(str(k) for k in mapping if k not in allowed)
        if extra:
            err(w, f"{where}: unknown field(s) {', '.join(extra)} (allowed: {', '.join(sorted(allowed))})")


def numbers_in(text: str) -> set:
    """Numbers written in text, read with Indonesian conventions (1.000 is a thousand, 0,5 is a half)."""
    out = set()
    for tok in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)*", text):
        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", tok):
            out.add(float(tok.replace(".", "")))
        else:
            try:
                out.add(float(tok.replace(",", ".")))
            except ValueError:
                pass
    return out


def check_lab(path, registry: dict, concepts: dict) -> None:
    w = rel(path)
    spec, ok = read_yaml(path, w)
    if not ok:
        return
    if not isinstance(spec, dict):
        err(w, "a lab spec must be a mapping")
        return
    for f in LAB_REQUIRED:
        if spec.get(f) in (None, "", []):
            err(w, f"required field `{f}` is missing or empty")
    unknown_keys(w, "lab", spec, LAB_KEYS)
    lid = spec.get("id")
    if isinstance(lid, str) and not KEBAB.match(lid):
        err(w, "id must be kebab-case")
    cid = spec.get("concept")
    c = concepts.get(cid) if isinstance(cid, str) else None
    if cid and c is None and concepts:
        err(w, f"concept `{cid}` is not in curriculum/concepts.yaml")
    elif c is not None and "lab" not in (c.get("formats") or []):
        warn(w, f"concept `{cid}` does not list `lab` in its formats")
    if path.parent.parent.name == "concepts" and cid and path.parent.name != cid:
        err(w, f"lab in folder `{path.parent.name}` names concept `{cid}`")
    sec = spec.get("secondary_concepts") or []
    if not isinstance(sec, list) or not all(isinstance(x, str) for x in sec):
        err(w, "secondary_concepts must be a list of concept ids")
    else:
        for x in sec:
            if concepts and x not in concepts:
                err(w, f"secondary concept `{x}` is not in curriculum/concepts.yaml")
    cv = spec.get("contract_version")
    if cv is not None and not (isinstance(cv, str) and SEMVER.match(cv)):
        err(w, "contract_version must be a semver string like \"0.1.0\"")
    mode = spec.get("mode")
    if mode is not None and mode not in LAB_MODES:
        err(w, f"mode must be one of {LAB_MODES}")
    d = spec.get("difficulty")
    if d is not None and (not isinstance(d, int) or isinstance(d, bool) or d not in (1, 2, 3)):
        err(w, "difficulty must be 1, 2 or 3")
    dm = spec.get("duration_min")
    if dm is not None:
        if not is_num(dm) or dm <= 0:
            err(w, "duration_min must be a positive number")
        elif not LAB_DURATION[0] <= dm <= LAB_DURATION[1]:
            warn(w, f"duration_min {dm} is outside the {LAB_DURATION[0]}-{LAB_DURATION[1]} minute target")
    ill = spec.get("illustrative")
    if ill is not None and not isinstance(ill, bool):
        err(w, "illustrative must be true or false")
    if ill is True and not (isinstance(spec.get("illustrative_note"), str) and spec["illustrative_note"].strip()):
        err(w, "illustrative: true needs a non-empty Indonesian `illustrative_note`")
    if ill is False and spec.get("illustrative_note"):
        warn(w, "illustrative_note is set but illustrative is false")
    for f in ("title", "goal", "debrief"):
        if f in spec and not (isinstance(spec[f], str) and spec[f].strip()):
            err(w, f"`{f}` must be a non-empty string")
    if isinstance(spec.get("debrief"), str) and spec["debrief"].strip() in ("...", "TODO"):
        warn(w, "debrief is still a placeholder")

    # topology
    nodes: dict = {}
    topo = spec.get("topology")
    if topo is not None:
        if not isinstance(topo, dict) or not isinstance(topo.get("nodes"), list) or not topo.get("nodes"):
            err(w, "topology needs a `nodes` list")
        else:
            for n in topo["nodes"]:
                if not isinstance(n, dict) or not isinstance(n.get("id"), str) or not isinstance(n.get("type"), str):
                    err(w, "every node needs a string `id` and `type`")
                    continue
                unknown_keys(w, f"node {n['id']}", n, LAB_NODE_KEYS)
                if not KEBAB.match(n["id"]):
                    err(w, f"node id must be kebab-case: {n['id']}")
                if n["id"] in nodes:
                    err(w, f"duplicate node id: {n['id']}")
                params = n.get("params") or {}
                if not isinstance(params, dict):
                    err(w, f"node {n['id']}: params must be a mapping")
                    params = {}
                nodes[n["id"]] = params
            edges = topo.get("edges") or []
            if not isinstance(edges, list):
                err(w, "topology.edges must be a list")
                edges = []
            for e in edges:
                pair = e if isinstance(e, list) else ([e.get("from"), e.get("to")] if isinstance(e, dict) else None)
                if not (isinstance(pair, list) and len(pair) == 2 and all(isinstance(x, str) for x in pair)):
                    err(w, "every edge must be [from, to] or {from, to, policies}")
                    continue
                for x in pair:
                    if x not in nodes:
                        err(w, f"edge refers to an unknown node: {x}")
    # traffic
    tr = spec.get("traffic")
    if tr is not None:
        sched = tr.get("schedule") if isinstance(tr, dict) else None
        if not isinstance(sched, list) or not sched or not all(
                isinstance(x, dict) and is_num(x.get("at_s")) and is_num(x.get("rate")) and x["rate"] >= 0 for x in sched):
            err(w, "traffic needs a `schedule` list of {at_s, rate} with numbers")
        elif [x["at_s"] for x in sched] != sorted(x["at_s"] for x in sched):
            err(w, "traffic schedule must be sorted by at_s")
        rs = tr.get("read_share") if isinstance(tr, dict) else None
        if rs is not None and not (is_num(rs) and 0 <= rs <= 1):
            err(w, "traffic.read_share must be a number from 0 to 1")
    # scenarios
    scen = spec.get("scenarios") or []
    if not isinstance(scen, list) or not all(isinstance(x, dict) and isinstance(x.get("id"), str) and is_num(x.get("at_s")) for x in scen):
        err(w, "scenarios must be a list of {id, at_s, ...}")
        scen = []
    if mode == "diagnose" and not scen:
        err(w, "diagnose mode needs at least one hidden scenario in `scenarios`")
    if mode in ("tune", "build") and scen:
        err(w, f"`scenarios` belong to diagnose mode, not {mode}")
    if mode == "build" and spec.get("allowed_edits"):
        err(w, "build mode uses `palette`, not `allowed_edits`")
    if mode in ("tune", "diagnose") and spec.get("palette"):
        err(w, f"{mode} mode uses `allowed_edits`, not `palette`")
    # edits / palette
    allowed: dict = {}
    if mode in ("tune", "diagnose"):
        ae = spec.get("allowed_edits")
        if not isinstance(ae, list) or not ae:
            err(w, f"{mode} mode needs `allowed_edits`")
        else:
            for a in ae:
                unknown_keys(w, "allowed_edits entry", a, LAB_EDIT_KEYS)
                if not (isinstance(a, dict) and isinstance(a.get("node"), str) and isinstance(a.get("param"), str)
                        and is_num(a.get("min")) and is_num(a.get("max")) and a["min"] <= a["max"]):
                    err(w, "every allowed edit needs node, param and numeric min <= max")
                    continue
                if a["node"] not in nodes:
                    err(w, f"allowed_edits refers to an unknown node: {a['node']}")
                    continue
                init = nodes[a["node"]].get(a["param"])
                if a["param"] not in nodes[a["node"]]:
                    err(w, f"allowed_edits: node {a['node']} has no initial param `{a['param']}`")
                elif is_num(init) and not a["min"] <= init <= a["max"]:
                    warn(w, f"initial {a['node']}.{a['param']}={init} is outside its allowed range {a['min']}..{a['max']}")
                if (a["node"], a["param"]) in allowed:
                    err(w, f"allowed_edits lists {a['node']}.{a['param']} twice")
                allowed[(a["node"], a["param"])] = (a["min"], a["max"])
    elif mode == "build":
        pal = spec.get("palette")
        if not isinstance(pal, list) or not pal or not all(isinstance(x, dict) and isinstance(x.get("type"), str) for x in pal):
            err(w, "build mode needs a `palette` list of {type, max}")
    # grading rules
    rule_ids: set = set()

    def rule_common(r, kind):
        rid = r.get("id")
        if not isinstance(rid, str) or not KEBAB.match(rid):
            err(w, f"{kind}: id must be kebab-case")
        elif rid in rule_ids:
            err(w, f"duplicate grading rule id: {rid}")
        else:
            rule_ids.add(rid)
        for f in ("feedback_pass", "feedback_fail"):
            if not (isinstance(r.get(f), str) and r[f].strip()):
                err(w, f"{kind} {rid}: `{f}` (Indonesian feedback) is required")

    metrics = []
    targets = spec.get("targets")
    if isinstance(targets, list):
        for t in targets:
            if not isinstance(t, dict):
                err(w, "every target must be a mapping")
                continue
            rule_common(t, "target")
            unknown_keys(w, f"target {t.get('id')}", t, LAB_TARGET_KEYS)
            if not isinstance(t.get("metric"), str):
                err(w, f"target {t.get('id')}: `metric` is required")
            else:
                metrics.append(t["metric"])
            win = t.get("window")
            if not (isinstance(win, dict) and is_num(win.get("from_s")) and is_num(win.get("to_s"))
                    and win["from_s"] < win["to_s"]):
                err(w, f"target {t.get('id')}: window needs numbers from_s < to_s")
            if t.get("aggregate") not in LAB_AGGREGATES:
                err(w, f"target {t.get('id')}: aggregate must be one of {LAB_AGGREGATES}")
            if t.get("op") not in LAB_OPS:
                err(w, f"target {t.get('id')}: op must be one of {LAB_OPS}")
            if not is_num(t.get("value")):
                err(w, f"target {t.get('id')}: value must be a number")
            if t.get("node") is not None and (not isinstance(t["node"], str) or (nodes and t["node"] not in nodes)):
                err(w, f"target {t.get('id')}: unknown node {t['node']}")
        if any("latency" in m for m in metrics) and not any(m in ("error_rate", "goodput_rps") for m in metrics):
            err(w, "a latency target must be paired with an error_rate or goodput_rps target (C12)")
    srules = spec.get("structural_rules") or []
    if not isinstance(srules, list):
        err(w, "structural_rules must be a list")
        srules = []
    for r in srules:
        if not isinstance(r, dict):
            err(w, "every structural rule must be a mapping")
            continue
        rule_common(r, "structural rule")
        unknown_keys(w, f"structural rule {r.get('id')}", r, LAB_RULE_KEYS)
        if r.get("predicate") not in LAB_PREDICATES:
            err(w, f"structural rule {r.get('id')}: predicate must be one of {LAB_PREDICATES}")
        args = r.get("args")
        if not isinstance(args, dict):
            err(w, f"structural rule {r.get('id')}: args must be a mapping")
        elif args.get("node") is not None and (not isinstance(args["node"], str) or (nodes and args["node"] not in nodes)):
            err(w, f"structural rule {r.get('id')}: unknown node {args['node']}")
    # hints
    hints = spec.get("hints")
    if hints is not None and not isinstance(hints, list):
        err(w, "hints must be a list")
        hints = None
    if isinstance(hints, list):
        tiers = []
        for h in hints:
            if not (isinstance(h, dict) and h.get("tier") in (1, 2, 3) and not isinstance(h.get("tier"), bool)
                    and isinstance(h.get("text"), str) and h["text"].strip()):
                err(w, "every hint needs tier 1, 2 or 3 and a text")
            else:
                unknown_keys(w, "hint", h, {"tier", "text"})
                tiers.append(h["tier"])
        if tiers and set(tiers) != {1, 2, 3}:
            err(w, "hints must cover tiers 1, 2 and 3")
        if len(tiers) != len(set(tiers)):
            warn(w, "more than one hint for the same tier")
    # reference solution and wrong answers (C09, C13, A3)
    ref = spec.get("reference_solution")
    if ref is not None and not isinstance(ref, list):
        err(w, "reference_solution must be a list of {node, param, value} edits")
        ref = None
    ref_final: dict = {}
    if isinstance(ref, list) and ref:
        for e in ref:
            if mode != "build":
                edit_ok(e, allowed, w, "reference_solution")
            if isinstance(e, dict) and isinstance(e.get("node"), str) and isinstance(e.get("param"), str):
                ref_final[(e["node"], e["param"])] = e.get("value")
    wa = spec.get("wrong_answers")
    if wa is not None and not isinstance(wa, list):
        err(w, "wrong_answers must be a list")
        wa = None
    brute = False
    if isinstance(wa, list) and wa:
        for i, x in enumerate(wa):
            if not (isinstance(x, dict) and isinstance(x.get("edits"), list) and x["edits"]
                    and isinstance(x.get("reason"), str) and x["reason"].strip()):
                err(w, f"wrong_answers[{i}] needs `edits` and a `reason`")
                continue
            unknown_keys(w, f"wrong_answers[{i}]", x, LAB_WRONG_KEYS)
            same = {(e.get("node"), e.get("param"), e.get("value")) for e in x["edits"] if isinstance(e, dict)}
            if isinstance(ref, list) and same and same == {(e.get("node"), e.get("param"), e.get("value"))
                                                           for e in ref if isinstance(e, dict)}:
                err(w, f"wrong_answers[{i}] is identical to the reference solution")
            if mode != "build":
                for e in x["edits"]:
                    edit_ok(e, allowed, w, f"wrong_answers[{i}]")
            if x.get("brute_force") is True:
                brute = True
    if isinstance(wa, list) and wa and not brute and not (isinstance(spec.get("brute_force_ok"), str) and spec["brute_force_ok"].strip()):
        err(w, "list a wrong answer with `brute_force: true` (all numeric edits at their extreme) or give `brute_force_ok` with a reason (A3)")
    # structural rules the reference must meet (the two predicates that need no simulator)
    for r in srules:
        if not isinstance(r, dict) or not isinstance(r.get("args"), dict) or not isinstance(ref, list):
            continue
        a = r["args"]
        if not isinstance(a.get("node"), str) or not isinstance(a.get("param"), str):
            continue
        key = (a["node"], a["param"])
        if r.get("predicate") == "param-unchanged" and key in ref_final:
            err(w, f"the reference solution changes {key[0]}.{key[1]}, which rule {r.get('id')} keeps unchanged")
        if r.get("predicate") == "param-range" and key in nodes_flat(nodes):
            val = ref_final.get(key, nodes[key[0]].get(key[1]))
            if is_num(val) and ((is_num(a.get("min")) and val < a["min"]) or (is_num(a.get("max")) and val > a["max"])):
                err(w, f"the reference solution breaks rule {r.get('id')}: {key[0]}.{key[1]}={val}")
    # anti-leak (A1, A2, C08): goal and tier 1-2 hints must not give away the reference values or its components
    if isinstance(ref, list):
        values = {float(e["value"]) for e in ref if isinstance(e, dict) and is_num(e.get("value")) and e["value"] != 0}
        words = {str(e["value"]) for e in ref if isinstance(e, dict) and isinstance(e.get("value"), str) and len(e["value"]) >= 4}
        node_ids = {e["node"] for e in ref if isinstance(e, dict) and isinstance(e.get("node"), str)}
        texts = [("goal", spec.get("goal"))] + [(f"hint tier {h['tier']}", h.get("text")) for h in hints or []
                                                if isinstance(h, dict) and h.get("tier") in (1, 2)]
        for label, text in texts:
            if not isinstance(text, str):
                continue
            for v in sorted(values & numbers_in(text)):
                err(w, f"anti-leak: {label} contains the reference value {v:g}")
            for word in words:
                if re.search(r"\b" + re.escape(word) + r"\b", text, re.I):
                    err(w, f"anti-leak: {label} contains the reference value `{word}`")
            for nid in node_ids:
                if re.search(r"\b" + re.escape(nid) + r"\b", text, re.I):
                    warn(w, f"anti-leak: {label} names the component `{nid}` that the reference solution edits")
    # sources
    srcs = spec.get("sources")
    if isinstance(srcs, list):
        for sid in srcs:
            if not isinstance(sid, str) or sid not in registry:
                err(w, f"source not in registry: {sid}")
            elif registry[sid].get("usage") == "map-only":
                err(w, f"a map-only (Tier 6) source must not be a content source: {sid}")
    elif srcs is not None:
        err(w, "sources must be a list of registry ids")


def nodes_flat(nodes: dict) -> set:
    return {(n, p) for n, params in nodes.items() for p in params}


def check_incident(path, registry: dict, concepts: dict, case_items: dict, specs_by_path: dict) -> None:
    """content/incidents/<id>.md: frontmatter plus five Indonesian sections (content-schema.md section 6)."""
    w = rel(path)
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    if fm is None:
        err(w, "frontmatter missing")
        return
    if not isinstance(fm, dict):
        err(w, "frontmatter must be a mapping")
        return
    unknown_keys(w, "incident", fm, INCIDENT_KEYS)
    iid = fm.get("id")
    if not isinstance(iid, str):
        err(w, "id must be a string")
        iid = None
    elif iid != path.stem:
        err(w, f"id `{iid}` must equal the file name `{path.stem}`")
    for f in ("title", "date", "sources", "concepts", "modelability"):
        if fm.get(f) in (None, "", []):
            err(w, f"frontmatter field `{f}` is required")
    d = fm.get("date")
    if d is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d)):
        err(w, "date must be YYYY-MM-DD")
    srcs = fm.get("sources")
    if isinstance(srcs, list):
        if not all(isinstance(x, str) for x in srcs) or any(x not in registry for x in srcs):
            err(w, "every source must be a registry id")
        elif not any(registry[x].get("type") == "postmortem" for x in srcs):
            err(w, "an incident needs a source of type postmortem")
    elif srcs is not None:
        err(w, "sources must be a list of registry ids")
    cons = fm.get("concepts")
    if isinstance(cons, list):
        for x in cons:
            if not isinstance(x, str) or (concepts and x not in concepts):
                err(w, f"unknown concept: {x}")
    elif cons is not None:
        err(w, "concepts must be a list")
    m = fm.get("modelability")
    if m is not None and m not in MODELABILITY:
        err(w, f"modelability must be one of {MODELABILITY}")
    if m in ("modeled", "illustrative"):
        sp = fm.get("sim_spec")
        scen_ids = fm.get("sim_scenarios")
        if not isinstance(scen_ids, list) or not scen_ids or not all(isinstance(x, str) for x in scen_ids):
            err(w, "sim_scenarios (a list of catalog scenario ids) is required unless text-only")
            scen_ids = []
        if not isinstance(sp, str) or not sp:
            err(w, "sim_spec (path to the diagnose-mode lab spec) is required unless text-only")
        else:
            target = (ROOT / sp).resolve()
            try:
                inside = target.is_relative_to((CONTENT / "incidents").resolve())
            except ValueError:
                inside = False
            if not inside or not sp.endswith("lab.yaml"):
                err(w, "sim_spec must be a path to a `.lab.yaml` file under content/incidents/")
            elif not target.is_file():
                err(w, f"sim_spec does not exist: {sp}")
            else:
                spec = specs_by_path.get(target)
                if isinstance(spec, dict):
                    if spec.get("mode") != "diagnose":
                        err(w, "the sim_spec lab must be in diagnose mode")
                    have = {x.get("id") for x in spec.get("scenarios") or [] if isinstance(x, dict)}
                    for x in scen_ids:
                        if x not in have:
                            err(w, f"sim_scenarios `{x}` is not a scenario of the sim_spec lab")
    elif m == "text-only" and (fm.get("sim_spec") or fm.get("sim_scenarios")):
        warn(w, "a text-only incident should not set sim_spec or sim_scenarios")
    if iid is None:
        pass
    elif iid in case_items and case_items[iid].get("kind") != "incident":
        err(w, "curriculum/case-studies.yaml lists this id with another kind")
    elif case_items and iid not in case_items:
        warn(w, "this incident is not listed in curriculum/case-studies.yaml")
    heads = [h.strip() for h in re.findall(r"^##[ \t]+(.+?)[ \t]*$", re.sub(r"```.*?```", "", body, flags=re.S), re.M)]
    for sec in INCIDENT_SECTIONS:
        if sec not in heads:
            err(w, f"missing section `## {sec}`")
    present = [h for h in heads if h in INCIDENT_SECTIONS]
    if present != [x for x in INCIDENT_SECTIONS if x in present]:
        err(w, "sections are out of order; expected " + ", ".join(INCIDENT_SECTIONS))
    for ref in set(FOOTNOTE.findall(body)):
        if ref not in registry:
            err(w, f"marker [^{ref}] is not in the registry")
        elif isinstance(srcs, list) and ref not in srcs:
            err(w, f"marker [^{ref}] is not in frontmatter sources")


def check_labs(registry: dict, concepts: dict) -> None:
    files = lab_files()
    seen: dict = {}
    specs: list = []
    specs_by_path: dict = {}
    for f in files:
        try:
            check_lab(f, registry, concepts)
        except Exception as e:  # noqa: BLE001  a malformed spec must be an error line, never a traceback
            err(rel(f), f"unexpected structure ({type(e).__name__}: {e}); check the field types against content-schema.md section 5")
        try:
            spec = load_yaml(f)
        except Exception:  # noqa: BLE001 (already reported by check_lab)
            continue
        specs.append(spec)
        specs_by_path[f.resolve()] = spec
        if isinstance(spec, dict) and isinstance(spec.get("id"), str):
            if spec["id"] in seen:
                err(rel(f), f"duplicate lab id `{spec['id']}` (also in {seen[spec['id']]})")
            seen[spec["id"]] = rel(f)
    idir = CONTENT / "incidents"
    case_items = {}
    cs = load_yaml(CASES)
    if isinstance(cs, dict):
        case_items = {i.get("id"): i for i in cs.get("items") or [] if isinstance(i, dict)}
    if idir.exists():
        for p in sorted(idir.glob("*.md")):
            try:
                check_incident(p, registry, concepts, case_items, specs_by_path)
            except Exception as e:  # noqa: BLE001  a malformed frontmatter must be an error line, never a traceback
                err(rel(p), f"unexpected structure ({type(e).__name__}: {e}); check the frontmatter types against content-schema.md section 6")
    if CATALOG.exists():
        warn(rel(CATALOG), "simulator catalog found, but catalog checks (C02-C04, C10, C11) are not implemented yet")
    if concepts:
        have = {s["concept"] for s in specs if isinstance(s, dict) and isinstance(s.get("concept"), str)}
        sec = {x for s in specs if isinstance(s, dict) and isinstance(s.get("secondary_concepts"), list)
               for x in s["secondary_concepts"] if isinstance(x, str)}
        missing = [cid for cid, c in concepts.items() if "lab" in (c.get("formats") or [])
                   and cid not in have and cid not in sec]
        late = [cid for cid in missing if concepts[cid].get("status") in ("review", "published")]
        if late:
            err("curriculum/concepts.yaml", "concept(s) in review/published list `lab` but have no lab spec: " + ", ".join(late))
        if missing and files:
            warn("curriculum/concepts.yaml", f"{len(missing)} concepts list `lab` but have no lab spec yet (planned)")


def check_graph_fresh() -> None:
    """curriculum/graph.md is generated from concepts.yaml (scripts/graph.py); a stale copy is an error."""
    import graph
    try:
        text = graph.build()
    except SystemExit as e:
        err("curriculum/graph.md", f"cannot generate graph: {e}")
        return
    if not graph.OUT.exists() or graph.OUT.read_text(encoding="utf-8") != text:
        err("curriculum/graph.md", "out of date: run python scripts/graph.py")


def main():
    check_tickets()
    registry = check_registry()
    concepts = check_curriculum(registry)
    if not errors:  # graph.py needs a valid, acyclic prerequisite graph
        check_graph_fresh()
    check_content(registry, concepts)
    check_labs(registry, concepts)
    for line in warnings:
        print(line)
    for line in errors:
        print(line)
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
