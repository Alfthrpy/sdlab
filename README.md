# SD Lab (working name)

A free platform for learning **backend system design** interactively: short lessons, quizzes, simulation labs, and real incidents. All material is distilled from verified references. Learner-facing content is in Indonesian; everything agents read is in English (see [ADR 0005](docs/decisions/0005-agent-facing-language.md)).

This repo holds **Phase 1: collecting & producing materials**. The simulator and application follow in later phases, in this repo or a separate one.

## Where to start

| You are | Read |
| --- | --- |
| An agent (Claude or other) | [`AGENTS.md`](AGENTS.md), then [`backlog/BOARD.md`](backlog/BOARD.md) |
| A human (owner/reviewer) | [`docs/PLAN-PHASE-1.md`](docs/PLAN-PHASE-1.md), then [`docs/workflow.md`](docs/workflow.md) |

## Repo map

```
AGENTS.md               agent working rules (read every session)
docs/
  ROADMAP.md            the 3 major project phases
  PLAN-PHASE-1.md       detailed plan for the materials phase (milestones, gates)
  workflow.md           ticket system, session flow, branch, PR, review
  decisions/            ADRs: decisions already made
  conventions/          citation guide, writing style, content schema
backlog/
  BOARD.md              status board (generate: python scripts/board.py)
  tickets/              one file = one ticket
references/
  registry.yaml         Reference Registry (the only sources that may be cited)
  notes/                reading notes per source
curriculum/             curriculum map (concepts, prerequisites, case studies)
content/                lessons, questions, lab specs, incidents, case studies
templates/              templates for tickets, concepts, questions, source notes, session logs
sessions/               log of each work session
scripts/                validate.py, board.py, new_ticket.py
.claude/                subagents & slash commands for Claude Code
```

## Commands

```bash
pip install pyyaml
python scripts/validate.py      # check tickets, registry, curriculum, content
python scripts/board.py         # regenerate backlog/BOARD.md
python scripts/new_ticket.py "Ticket title" --milestone M4 --type content
```

## License

- Code (`scripts/`, `.github/`): MIT.
- Content (`content/`, `curriculum/`, `docs/`): CC BY 4.0, unless stated otherwise in a file.
- Third-party material is only linked and rewritten, never copied. See [`docs/conventions/citation-guide.md`](docs/conventions/citation-guide.md).
