# Workflow: tickets, sessions, review

All work goes through **tickets**. One work session (agent or human) takes one ticket, finishes it until its done-criteria are met, then hands it over for review. No work happens outside a ticket. If you discover new work, create a new ticket.

## 1. Tickets

One Markdown file in `backlog/tickets/`, named `<ID>-<slug>.md`, with YAML frontmatter:

```yaml
id: P1-011               # P1 = Phase 1, unique number
title: Research candidate sources — Units 1 & 2
milestone: M1            # see docs/PLAN-PHASE-1.md
type: research           # research | curriculum | content | review | decision | infra
owner: agent             # who DOES the work: agent | human
review: agent            # who REVIEWS it: agent | human | none
status: todo             # todo | in-progress | review | done | blocked
priority: high           # high | medium | low
depends_on: [P1-010]     # tickets that must be done first
estimate: 1              # estimated number of sessions
outputs:                 # files this ticket creates/changes
  - references/registry.yaml
```

The ticket body has: **Context**, **Tasks**, **Done criteria** (checklist), and **Notes** (filled in during the work).

### Who does what

This project is **agent-heavy**. Rules for assigning owner and review:

| Kind of work | owner | review |
| --- | --- | --- |
| Source research, summaries, mapping, curriculum drafts, content drafts, schemas, scripts | agent | agent |
| Product decisions (language, audience, name, priorities) | human | none |
| Milestone gates (approve registry, curriculum, pilot) | agent prepares, human decides | human |
| Testing with real users | human | none |
| External access (create repo, accounts, invite reviewers) | human | none |
| Content with risky claims (performance numbers, specific product behavior) | agent | agent + human sample in the QA ticket |

`review: agent` means the ticket is verified by a **reviewer subagent that did not do the work** (`.claude/agents/content-reviewer.md` or `source-verifier.md`). After it passes and CI is green, the agent may merge its own PR.

`review: human` means the PR waits for the repo owner's approval. The agent must not merge.

### Status

```
todo → in-progress → review → done
          ↓
       blocked  (write the reason in Notes + the blocking ticket in depends_on)
```

A ticket may only be taken when all its `depends_on` are `done`.

## 2. Flow of one session

1. **Orient.** Read `AGENTS.md`, `backlog/BOARD.md`, and the latest session log in `sessions/`.
2. **Pick a ticket.** If the owner does not name one, take the `todo` ticket with `owner: agent`, all dependencies `done`, highest priority, lowest number.
3. **Claim.** Create branch `t/<ID>-<slug>`, set status to `in-progress`, commit.
4. **Work** per the Tasks. If the ticket is too big for one session, split it into sub-tickets (`P1-040a`, `P1-040b`) and do the first.
5. **Validate.** `python scripts/validate.py` must pass. Tick the Done criteria that are met.
6. **Review.** `review: agent` → call a reviewer subagent, fix its findings. `review: human` → set status to `review`.
7. **Record.** Write the session log at `sessions/YYYY-MM-DD-<ID>.md` (template: `templates/session-log.md`). Fill in the Notes section of the ticket.
8. **Hand off.** Run `python scripts/board.py`, commit, push, open a PR titled `[<ID>] <title>`. If `review: agent` and CI is green, merge and set `done`.

One session = one ticket (or one sub-ticket). If a session stops midway, the status stays `in-progress` and the session log explains how far it got.

## 3. Branch, commit, PR

- Branch: `t/P1-011-foundation-research`
- Commit: `[P1-011] add 12 candidate sources for foundations unit`
- PR: title `[P1-011] <ticket title>`, body = summary, list of outputs, done-criteria checklist, agent review result.
- `main` changes only through PRs.

## 4. The human (owner) role

You only need to do four things:

1. Do `owner: human` tickets (decisions, gates, user tests).
2. Review `review: human` PRs.
3. Occasionally spot-check merged `review: agent` PRs (there is a dedicated QA ticket for this).
4. Start agent sessions: "do the next ticket" or "do P1-0xx".

## 5. Why tickets are files, not GitHub Issues

See [ADR 0001](decisions/0001-tickets-in-repo.md). In short: cloud agents can always read files without an API token, ticket history lives in Git, and ticket changes are reviewed in the same PR as the work. A mirror to GitHub Issues/Projects can be added later (ticket P1-004).
