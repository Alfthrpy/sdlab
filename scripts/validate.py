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
    for line in warnings:
        print(line)
    for line in errors:
        print(line)
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
