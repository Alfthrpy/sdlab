# ADR 0002 — Rules for using third-party sources

- **Status:** accepted
- **Date:** 2026-11-12

## Context

The materials are distilled from books, papers, engineering articles, and postmortems, most of which are under copyright. Some have open licenses with different terms. For example, System Design Primer is CC BY 4.0 (may be adapted with attribution), while the Google SRE Book is CC BY-NC-ND 4.0 (derivatives not allowed).

## Decision

1. **Only sources in `references/registry.yaml`** with status `approved` may be cited in published content. `candidate` sources may be used in drafts.
2. **Default for every source: rewrite.** Take concepts and facts, write them in your own words and structure, and link the source.
3. **Direct quotes:** at most one short sentence (< 15 words) per source per lesson, and only when the exact wording matters.
4. **Diagrams are always original.** No diagram is copied or traced from a source.
5. **Adaptation** (taking structure or text and modifying it) is allowed only for sources with `license: CC-BY-*` or public domain, with attribution per `docs/conventions/citation-guide.md`.
6. **Tier 6 sources** (interview-prep courses/books) are used only to map common topics and questions, never as a content source.

## Consequences

Content production is slower than summarizing directly, but the content can be released under CC BY 4.0 and the M5 audit stays simple.

*Note: this is project policy, not legal advice.*
